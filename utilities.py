import requests
import os
import pandas as pd
import re

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



def filter_rows_with_spaces(df, column_name):
    """
    Filtra le righe di un DataFrame dove una colonna specifica contiene spazi vuoti.
    
    :param df: DataFrame Pandas
    :param column_name: Nome della colonna da controllare per spazi vuoti
    :return: Nuovo DataFrame contenente solo le righe con spazi vuoti nella colonna specificata
    """
    if column_name not in df.columns:
        raise ValueError(f"Colonna '{column_name}' non trovata nel DataFrame")
    
    # Filtra le righe dove la colonna specificata contiene spazi vuoti
    filtered_df = df[df[column_name].str.contains(' ', na=False)]
    
    return filtered_df


def clean_value(value):
    # Usa un'espressione regolare per rimuovere ' (n)'
    cleaned_value = re.sub(r' \(\d\)', '', value)
    # Rimuove gli spazi rimanenti
    cleaned_value = cleaned_value.strip()
    return cleaned_value
    