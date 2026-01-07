from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Client, NiveauEtude, Sexe, Region, SituationFamiliale
from pydantic import BaseModel
from datetime import date

app = FastAPI()

@app.get('/clients/', tags=["clients"])
async def list_clients(db: Session = Depends(get_db), page: int = Query(1, ge=1, description="Numéro de page"), page_size: int = Query(50, ge=1, le=200, description="Nombre d'éléments par page")):
    total = db.query(func.count(Client.id)).scalar()
    offset = (page - 1) * page_size

    items = db.query(Client).offset(offset).limit(page_size).all()
    return {
        "page": page,
        "page_size": page_size,
        "total": total,
        "pages": (total + page_size - 1) // page_size,
        "items": items,
    }


class ClientPayload(BaseModel):
    nom: str
    prenom: str
    age: int
    taille: float
    poids: float
    sexe_id: int
    sport_licence: bool
    niveau_etude_id: int
    region_id: int
    fumeur: bool
    nationalite_francaise: bool
    revenu_estime_mois: int
    situation_familiale_id: int | None = None
    historique_credits: float | None = None
    risque_personnel: float
    date_creation_compte: date
    score_credit: float | None = None
    loyer_mensuel: float | None = None
    montant_pret: float


@app.post('/clients/', tags=["clients"])
async def create_client(payload: ClientPayload, db: Session = Depends(get_db)):
    client = Client(**payload.model_dump())

    db.add(client)
    db.commit()
    return client


@app.put('/clients/{client_id}', tags=["clients"])
async def update_client(client_id: int, payload: ClientPayload, db: Session = Depends(get_db)):
    client = db.query(Client).filter_by(id=client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client non trouvé")
    for key, value in payload.model_dump().items():
        setattr(client, key, value)

    db.commit()
    return client

@app.delete('/clients/{client_id}', tags=["clients"])
async def delete_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter_by(id=client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client non trouvé")

    db.delete(client)
    db.commit()
    return {"message": "Client supprimé avec succès"}


@app.get('/sexes/', tags=["sexes"])
async def list_sexes(db: Session = Depends(get_db)):
    return db.query(Sexe).all()


class SexePayload(BaseModel):
    nom: str

@app.post('/sexes/', tags=["sexes"])
async def create_sexe(payload: SexePayload, db: Session = Depends(get_db)):
    sexe = Sexe(**payload.model_dump())

    db.add(sexe)
    db.commit()
    return sexe

@app.put('/sexes/{sexe_id}', tags=["sexes"])
async def update_sexe(sexe_id: int, payload: SexePayload, db: Session = Depends(get_db)):
    sexe = db.query(Sexe).filter_by(id=sexe_id).first()
    if not sexe:
        raise HTTPException(status_code=404, detail="Sexe non trouvé")

    for key, value in payload.model_dump().items():
        setattr(sexe, key, value)

    db.commit()
    return sexe


@app.delete('/sexes/{sexe_id}', tags=["sexes"])
async def delete_sexe(sexe_id: int, db: Session = Depends(get_db)):
    sexe = db.query(Sexe).filter_by(id=sexe_id).first()
    if not sexe:
        raise HTTPException(status_code=404, detail="Sexe non trouvé")
    db.delete(sexe)
    db.commit()
    return {"message": "Sexe supprimé avec succès"}


@app.get('/niveaux-etudes/', tags=["niveaux-etudes"])
async def list_niveaux_etudes(db: Session = Depends(get_db)):
    return db.query(NiveauEtude).all()


class NiveauEtudePayload(BaseModel):
    nom: str

@app.post('/niveaux-etudes/', tags=["niveaux-etudes"])
async def create_niveau_etude(payload: NiveauEtudePayload, db: Session = Depends(get_db)):
    niveau_etude = NiveauEtude(**payload.model_dump())

    db.add(niveau_etude)
    db.commit()
    return niveau_etude

@app.put('/niveaux-etudes/{niveau_etude_id}', tags=["niveaux-etudes"])
async def update_niveau_etude(niveau_etude_id: int, payload: NiveauEtudePayload, db: Session = Depends(get_db)):
    niveau_etude = db.query(NiveauEtude).filter_by(id=niveau_etude_id).first()
    if not niveau_etude:
        raise HTTPException(status_code=404, detail="Niveau d'étude non trouvé")
    for key, value in payload.model_dump().items():
        setattr(niveau_etude, key, value)

    db.commit()
    return niveau_etude


@app.delete('/niveaux-etudes/{niveau_etude_id}', tags=["niveaux-etudes"])
async def delete_niveau_etude(niveau_etude_id: int, db: Session = Depends(get_db)):
    niveau_etude = db.query(NiveauEtude).filter_by(id=niveau_etude_id).first()
    if not niveau_etude:
        raise HTTPException(status_code=404, detail="Niveau d'étude non trouvé")
    db.delete(niveau_etude)
    db.commit()
    return {"message": "Niveau d'étude supprimé avec succès"}


@app.get('/regions/', tags=["regions"])
async def list_regions(db: Session = Depends(get_db)):
    return db.query(Region).all()


class RegionPayload(BaseModel):
    nom: str

@app.post('/regions/', tags=["regions"])
async def create_region(payload: RegionPayload, db: Session = Depends(get_db)):
    region = Region(**payload.model_dump())

    db.add(region)
    db.commit()
    return region

@app.put('/regions/{region_id}', tags=["regions"])
async def update_region(region_id: int, payload: RegionPayload, db: Session = Depends(get_db)):
    region = db.query(Region).filter_by(id=region_id).first()
    if not region:
        raise HTTPException(status_code=404, detail="Région non trouvée")
    for key, value in payload.model_dump().items():
        setattr(region, key, value)

    db.commit()
    return region

@app.delete('/regions/{region_id}', tags=["regions"])
async def delete_region(region_id: int, db: Session = Depends(get_db)):
    region = db.query(Region).filter_by(id=region_id).first()
    if not region:
        raise HTTPException(status_code=404, detail="Région non trouvée")
    db.delete(region)
    db.commit()
    return {"message": "Région supprimée avec succès"}


@app.get('/situations-familiales/', tags=["situations-familiales"])
async def list_situations_familiales(db: Session = Depends(get_db)):
    return db.query(SituationFamiliale).all()


class SituationFamilialePayload(BaseModel):
    nom: str

@app.post('/situations-familiales/', tags=["situations-familiales"])
async def create_situation_familiale(payload: SituationFamilialePayload, db: Session = Depends(get_db)):
    situation_familiale = SituationFamiliale(**payload.model_dump())

    db.add(situation_familiale)
    db.commit()
    return situation_familiale

@app.put('/situations-familiales/{situation_familiale_id}', tags=["situations-familiales"])
async def update_situation_familiale(situation_familiale_id: int, payload: SituationFamilialePayload, db: Session = Depends(get_db)):
    situation_familiale = db.query(SituationFamiliale).filter_by(id=situation_familiale_id).first()
    if not situation_familiale:
        raise HTTPException(status_code=404, detail="Situation familiale non trouvée")
    for key, value in payload.model_dump().items():
        setattr(situation_familiale, key, value)

    db.commit()
    return situation_familiale

@app.delete('/situations-familiales/{situation_familiale_id}', tags=["situations-familiales"])
async def delete_situation_familiale(situation_familiale_id: int, db: Session = Depends(get_db)):
    situation_familiale = db.query(SituationFamiliale).filter_by(id=situation_familiale_id).first()
    if not situation_familiale:
        raise HTTPException(status_code=404, detail="Situation familiale non trouvée")
    db.delete(situation_familiale)
    db.commit()
    return {"message": "Situation familiale supprimée avec succès"}
