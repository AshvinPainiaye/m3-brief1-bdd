import pandas as pd

def clean_data():
    df = pd.read_csv("data.csv")
    
    nb_doublons = df.duplicated().sum()
    if nb_doublons > 0:
        print("Nombre de doublons détectés :", nb_doublons)
        df_cleaned = df.drop_duplicates()
    else:
        df_cleaned = df

    df_cleaned.to_csv("data_cleaned.csv", index=False)
    print("Fichier OK")
