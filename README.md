# Progetto di Web Scraping dei Dati del Campionato di Calcio

Questo progetto esegue il web scraping dei dati relativi al campionato di calcio Serie A, raccogliendo informazioni dettagliate sulle partite, i tiri, il possesso palla e i passaggi delle squadre. I dati vengono estratti dal sito FBref.

## Descrizione del Progetto

Il progetto utilizza Python e le librerie `requests`, `BeautifulSoup` e `pandas` per raccogliere, elaborare e salvare i dati in un formato strutturato. Lo script esegue le seguenti operazioni principali:
1. Estrae i link delle squadre dal sito FBref.
2. Scarica e elabora i dati delle partite, dei tiri, del possesso palla e dei passaggi per ogni squadra.
3. Combina i dati in un unico DataFrame e li salva in un file `.pkl` per un'analisi successiva.

## Requisiti

Assicurati di avere installato le seguenti librerie Python:

- `requests`
- `beautifulsoup4`
- `pandas`
- `numpy`
- `html5lib`
- `pickle`




## Descrizione delle Funzioni Principali
rename_cols(topic_kpi, word: str)
Questa funzione aggiunge un prefisso alle colonne specificate, a meno che il nome della colonna non sia 'date' o 'opponent'.

get_final_links(links_squads, stagione)
Questa funzione, definita nel file utilities.py, estrae i link finali per ogni squadra.

Processo di Raccolta dei Dati
Lo script segue questi passaggi per raccogliere i dati:

Scarica la pagina principale del campionato: Estrae i link delle squadre.
Scarica e processa i dati delle partite: Utilizza pandas.read_html per estrarre la tabella "Scores & Fixtures".
Scarica e processa i dati dei tiri: Utilizza pandas.read_html per estrarre la tabella "Shooting".
Scarica e processa i dati del possesso palla: Utilizza pandas.read_html per estrarre la tabella "Possession".
Scarica e processa i dati dei passaggi: Utilizza pandas.read_html per estrarre la tabella "Passing".
Unisce i dati: Combina i dati delle partite, dei tiri, del possesso palla e dei passaggi in un unico DataFrame.
Salva i dati: Salva il DataFrame finale in un file .pkl.
Salvataggio dei Dati
I dati finali vengono salvati in un file .pkl nella directory output_data con il nome all_matches_{season_suffix}.pkl, dove season_suffix è l'ultimo numero della stagione (ad esempio, 23 per la stagione 2023-2024).


