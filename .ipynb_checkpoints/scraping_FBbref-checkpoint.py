import requests
from bs4 import BeautifulSoup
import pandas as pd, numpy as np
import html5lib
import time
import pickle
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.precision", 2)
# pd.set_option("display.freeze_panes", 1)
from datetime import datetime
now = datetime.now()
print(now.strftime('%d/%m/%Y %H:%M:%S'))
import utilities
from utilities import convert_season 
from utilities import get_final_links

# standings_url = "https://fbref.com/en/comps/11/Serie-A-Stats"
# standings_url = f"https://fbref.com/en/comps/{division}"

def rename_cols(topic_kpi , word : str):
    return [word + i if not i.lower() in ('date', 'opponent') else i for i in topic_kpi]

season = [ '2023-2024' ]
division = [ '11/Serie-A-Stats'  ] #  ,'12/La-Liga-Stats' , '9/Premier-League-Stats'
final_links = []

all_matches = pd.DataFrame()
shoot_kpi = ["Date", "Opponent", "Sh", "SoT", "Dist", "FK", "PK", "PKatt"]
# kpi = []
poss_kpi = ['Date' ,"Opponent",  'Touches', 'Def Pen', 'Def 3rd', 'Mid 3rd','Att 3rd', 'Att Pen', 'Live',
            'Att', 'Succ', 'Succ%', 'Tkld', 'Tkld%','Carries', 'TotDist', 'PrgDist', 'PrgC', 
            '1/3', 'CPA', 'Mis', 'Dis','Rec', 'PrgR']
pass_kpi = ['Date' , "Opponent", 'Total_Cmp', 'Total_Att', 'Total_Cmp%', 'Total_TotDist', 'Total_PrgDist', 
                 'Short_Cmp', 'Short_Att', 'Short_Cmp%',
                 'Medium_Cmp', 'Medium_Att', 'Medium_Cmp%', 
                 'Long_Cmp', 'Long_Att', 'Long_Cmp%', 
                 'Ast', 'xAG', 'xA', 'KP', '1/3', 'PPA', 'CrsPA', 'PrgP']

# for year in years:
for stagione in season:
    for campionato in division:

        print((stagione , campionato) , '\n' )
        standings_url = f"https://fbref.com/en/comps/{campionato}"
        print(standings_url , '\n')
        data = requests.get(standings_url )
        soup = BeautifulSoup(data.text , features = "lxml")
        print(data)
        standings_table = soup.select('table.stats_table')[0]
        #dal contenuto isolato su stats_table andiamo ad estrarre i link che contengono i dati di kpi èer singola partita (i dati sono pèresenti a bh)
        links = [ l.get("href") for l in standings_table.find_all('a') ]
        links_squads = [l for l in links if '/squads/' in l]
        # print(links_squads[0:2])
        

        final_links = get_final_links(links_squads, stagione)
        # print(final_links)

        # team_urls = [f"https://fbref.com/{l}" for l in final_links]
        team_urls = [ f"https://fbref.com/en/squads/d609edc0/{season}/Internazionale-Stats" ]

    #     ciclo for sulle squadre
        for i in range(0 , len(team_urls)):
            # print(team_url)
            # print(now.strftime('%Y/%m/%d/ %H:%M'))
            print(team_urls[i])       

            team_name = team_urls[i].split("/")[-1].replace("-Stats", "").replace("-", " ")
            # print(team_urls[i])
            data = requests.get(team_urls[i])
            print("Calling " , team_urls[i] , " result: " , str(data), '\n')

            if str(data) !='<Response [200]>':
                print("Call Problem with : " , team_urls[i] ,  " error: ", str(data))
                continue
    #         print(now.strftime('%Y/%m/%d/ %H:%M') , str(data))
            print("Step 1: matches data for: ", f'{team_name}' ,'\n')
            matches = pd.read_html(data.text, match="Scores & Fixtures")[0] #tabella base delle partite
            matches['season'] =  stagione
            matches['campionato'] = campionato
            matches['team'] =  team_name
            print("Step 1 ended:", f'{team_name}'  ,'\n')
            # print(matches.head())
            # matches.head()
            
            print("Step 2: shoots data for: ", f'{team_name}'  ,'\n')
            soup = BeautifulSoup(data.text ,  features = "lxml")
            links = [l.get("href") for l in soup.find_all('a')]           
            # creiamo i kpi dei topic [shooting , possession , passes] per ogni squadra
            links_shoot = [l for l in links if l and 'all_comps/shooting/' in l]  
            links_shoot
            data_shoot = requests.get(f"https://fbref.com{links_shoot[0]}")

            shooting = pd.read_html(data_shoot.text, match="Shooting")[0]
            shooting.columns = shooting.columns.droplevel()
            shooting = shooting[shoot_kpi]
            shooting.columns = rename_cols(shoot_kpi , 'shoot_')
            print("Step 2 ended:", f'{team_name}'  ,'\n')
            

            print("Step 3: possession data for: ", f'{team_name}'  ,'\n')
            links_poss = [l for l in links if l and 'all_comps/possession/' in l]
            data_poss = requests.get(f"https://fbref.com{links_poss[0]}")

            possession = pd.read_html(data_poss.text, match="Possession")[0]
            possession.columns = possession.columns.droplevel()
            possession = possession[poss_kpi]
            possession.columns = rename_cols(poss_kpi , 'poss_')
            print("Step 3 ended:", f'{team_name}'  ,'\n')

            print("Step 4: passes data for: ", f'{team_name}'  ,'\n')
            links_pass = [l for l in links if l and 'all_comps/passing/' in l]
            data_pass = requests.get(f"https://fbref.com{links_pass[0]}")
            
            # passes ha un problema di duplicazione nomi colonne :
            # rinominare le cols con numeri e poi rinominare selezionanndo quelle d'iteresse definite in pass_kpi
            passes = pd.read_html(data_pass.text, match="Passing")[0]
            passes.columns = passes.columns.droplevel()
            col = [str(i) for i in range(0, len(passes.columns))]
            passes.columns = col
            passes = passes.iloc[: , [0, *range(9, 32)]]
            passes.columns = pass_kpi
            passes.columns = rename_cols(pass_kpi , 'pass_')
            print("Step 4 ended:", f'{team_name}'  ,'\n')

    #     # unisco i topic kpi lasciando solo una colonna 'Date' : .drop(columns='Date')
            all_kpi = pd.merge(shooting, pd.merge(possession , passes, how='inner', on=['Date' , 'Opponent']), how='inner', on=['Date' , 'Opponent'],)
            team_data = matches.merge(all_kpi,on=['Date' , 'Opponent'])
            print("Marged data for: ", f'{team_name}'  ,'\n')

            all_matches = pd.concat([all_matches, team_data], ignore_index=True)
            print("Waiting for 5 seconds...")
            time.sleep(5)
            
            print("End of proccess" ,'\n')

all_matches.columns = [i.lower() for i in all_matches.columns]           
all_matches['round_1'] = all_matches['round'].apply(lambda x: x.split(' ')[1] if 'Matchweek' in x else 0).astype(int)     
all_matches["date"] = pd.to_datetime(all_matches["date"])
all_matches.to_pickle('all_matches_2324.pkl')
# team_urls