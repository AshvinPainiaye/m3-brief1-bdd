import pandas as pd

def to_bool(x):
    if pd.isna(x):
        return False
    s = str(x).strip().lower()
    return s in {"1", "oui"}


def clean_data():
    df = pd.read_csv("data.csv")
    
    nb_doublons = df.duplicated().sum()
    if nb_doublons > 0:
        print("Nombre de doublons détectés :", nb_doublons)
        df_cleaned = df.drop_duplicates()
    else:
        df_cleaned = df

    for col in ["sport_licence", "smoker", "nationalite_francaise"]:
        if col in df_cleaned.columns:
            df_cleaned[col] = df_cleaned[col].apply(to_bool)

    df_cleaned.to_csv("data_cleaned.csv", index=False)
    print("Fichier OK")
