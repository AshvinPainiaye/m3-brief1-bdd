import pandas as pd
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import Client, NiveauEtude, Sexe, Region, SituationFamiliale

CSV_PATH = "data_cleaned.csv"

def get_or_create(db: Session, model, nom: str):
    nom = str(nom).strip()
    obj = db.query(model).filter(model.nom == nom).first()
    if obj:
        return obj
    obj = model(nom=nom)
    db.add(obj)
    db.flush()
    return obj


def main():
    df = pd.read_csv(CSV_PATH)

    with SessionLocal() as db:
        client_add = 0

        for _, r in df.iterrows():
            sexe = get_or_create(db, Sexe, r.get("sexe"))
            region = get_or_create(db, Region, r.get("region"))
            niveau_etude = get_or_create(db, NiveauEtude, r.get("niveau_etude"))

            situation_familiale_value = r.get("situation_familiale")
            situation_familiale = None
            if not pd.isna(situation_familiale_value) and str(situation_familiale_value).strip() != "":
                situation_familiale = get_or_create(db, SituationFamiliale, situation_familiale_value)

            client = Client(
                nom=str(r.get("nom")).strip(),
                prenom=str(r.get("prenom")).strip(),
                age=int(r.get("age")) if not pd.isna(r.get("age")) else None,
                taille=float(r.get("taille")) if not pd.isna(r.get("taille")) else None,
                poids=float(r.get("poids")) if not pd.isna(r.get("poids")) else None,

                sexe_id=sexe.id,
                sport_licence=bool(r.get("sport_licence", False)),

                niveau_etude_id=niveau_etude.id,
                region_id=region.id,

                fumeur=bool(r.get("fumeur", False)),
                nationalite_francaise=bool(r.get("nationalite_francaise", False)),
                revenu_estime_mois=int(r.get("revenu_estime_mois")) if not pd.isna(r.get("revenu_estime_mois")) else None,

                situation_familiale_id=situation_familiale.id if situation_familiale else None,

                historique_credits=float(r.get("historique_credits")) if not pd.isna(r.get("historique_credits")) else None,
                risque_personnel=float(r.get("risque_personnel")) if not pd.isna(r.get("risque_personnel")) else None,
                date_creation_compte=r.get("date_creation_compte"),
                score_credit=float(r.get("score_credit")) if not pd.isna(r.get("score_credit")) else None,
                loyer_mensuel=float(r.get("loyer_mensuel")) if not pd.isna(r.get("loyer_mensuel")) else None,
                montant_pret=float(r.get("montant_pret")) if not pd.isna(r.get("montant_pret")) else None,
            )

            db.add(client)
            client_add += 1

        db.commit()

    print(f"Import OK (Ajoutées : {client_add})")


if __name__ == "__main__":
    main()