import joblib
import pandas as pd
from os.path import join as join
from sqlalchemy.orm import joinedload
from ml.modules.preprocess import preprocessing, split
from ml.models.models import create_nn_model, train_model, model_predict
from ml.modules.evaluate import evaluate_performance
from ml.modules.print_draw import print_data, draw_loss
from app.db import SessionLocal
from app.models import Client

def load_data():
    with SessionLocal() as db:
        clients = (
            db.query(Client)
            .options(
                joinedload(Client.sexe),
                joinedload(Client.region),
                joinedload(Client.niveau_etude),
                joinedload(Client.situation_familiale),
            )
            .all()
        )

    data = []
    for client in clients:
        data.append({
            "nom": client.nom,
            "prenom": client.prenom,
            
            "age": client.age,
            "taille": client.taille,
            "poids": client.poids,
            "sport_licence": int(bool(client.sport_licence)),
            "fumeur": int(bool(client.fumeur)),
            "nationalite_francaise": int(bool(client.nationalite_francaise)),
            "revenu_estime_mois": client.revenu_estime_mois,
            "historique_credits": client.historique_credits,
            "risque_personnel": client.risque_personnel,
            "score_credit": client.score_credit,
            "loyer_mensuel": client.loyer_mensuel,
            "montant_pret": client.montant_pret,

            "sexe": client.sexe.nom if client.sexe else None,
            "region": client.region.nom if client.region else None,
            "niveau_etude": client.niveau_etude.nom if client.niveau_etude else None,
            "situation_familiale": client.situation_familiale.nom if client.situation_familiale else None,
        })
        
    df = pd.DataFrame(data)
    return df


train = False

model_name = "model_2026_01"
model_filename = f"{model_name}.pkl"

# Chargement des datasets
df_new = load_data()

# Charger le préprocesseur
# preprocessor_loaded = joblib.load(join('models','preprocessor.pkl'))

# preprocesser les data
X, y, _ = preprocessing(df_new)

# split data in train and test dataset
X_train, X_test, y_train, y_test = split(X, y)

if train:
    # create a new model
    model = create_nn_model(X_train.shape[1])
    
    # entraîner le modèle
    model, hist = train_model(model, X_train, y_train, X_val=X_test, y_val=y_test)
    draw_loss(hist)
    
    # sauvegarder le modèle
    joblib.dump(model, join('ml', 'models', model_filename))


# charger le modèle
loaded_model = joblib.load(join('ml', 'models', model_filename))

#%% predire sur les valeurs de train
y_pred = model_predict(loaded_model, X_train)
# mesurer les performances MSE, MAE et R²
perf = evaluate_performance(y_train, y_pred)
print_data(perf)

 #%% predire sur les valeurs de tests
y_pred = model_predict(loaded_model, X_test)
# mesurer les performances MSE, MAE et R²
perf = evaluate_performance(y_test, y_pred)
print_data(perf)
