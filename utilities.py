import requests
import os
# raw_data_folder = os.getcwd() + "\\raw_data"

# def import_raw_data( season, league ):
#     os.chdir("H:\\Il mio Drive\\serie a\\python\\football-data.com\\raw_data")
    
#     # scarica i raw data e li deposita in cartella (sovrascrivendoli ad ogni aggiornamento)
#     url = f"https://www.football-data.co.uk/mmz4281/{season}/{league}.csv"
#     print(url)
#     response = requests.get(url)
#     # se la chiamata da esito positivo (200) scarica il contenuto del file, altrimenti segnala errore
#     if response.status_code == 200:
#         # print(response.status_code)
#         print(f"Salvo i file in {os.getcwd()}")
#         with open(f"{league}.csv", "wb") as f:
#             f.write(response.content)
#     else:
#         print("Error on the download of " + url)

# # capire come unire tutti i file scaricati in un unico db
# # prima di applicare la funzione team

# def union_csv_files(input_dir, output_dir):
#   """
#   Importa tutti i file .csv di una cartella in un pandas DataFrame e li appende per riga.
#   Salva il DataFrame in formato pickle e .sas7bdat nella cartella di output.

#   Args:
#     input_dir: Il percorso della cartella contenente i file .csv.
#     output_dir: Il percorso della cartella in cui salvare il DataFrame unificato.

#   Returns:
#     Il DataFrame unificato.
#   """

#   # Importa tutti i file .csv in un DataFrame
# df_list = []
# for file in os.listdir(input_dir):
# if file.endswith('.csv'):
#   df_list.append(pd.read_csv(os.path.join(input_dir, file)))

# # Appende i DataFrame per riga
# df_all = pd.concat(df_list, ignore_index=True)

# # Salva il DataFrame unificato in formato pickle
# df_all.to_pickle(os.path.join(output_dir, 'df_all.pkl'))

# # Salva il DataFrame unificato in formato .sas7bdat
# df_all.to_sas7bdat(os.path.join(output_dir, 'df_all.sas7bdat'))

# return df_all

def estrai_ultime_due_cifre(stringa):
    """
  Estrae le ultime due cifre di una stringa.

  Args:
    stringa: la stringa da cui estrarre le ultime due cifre.

  Returns:
    Una stringa con le ultime due cifre della stringa originale.
    """
    anno_1 = stringa.split("-")[0][-2:]
    anno_2 = stringa.split("-")[1][-2:]
    return anno_1 + anno_2

def get_final_links(links_squads, stagione):
    parts = [link.split('/') for link in links_squads]
    final_links = [ parte[1] + '/' + parte[2] + '/' + parte[3] + '/' + f'{stagione}' + '/' + parte[4] for parte in parts ]
    return final_links


# final_links = get_final_links(links_squads, stagione)



