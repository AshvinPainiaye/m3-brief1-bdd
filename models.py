from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float, Date
from sqlalchemy.orm import relationship
from db import Base


class Client(Base):
    __tablename__ = 'clients'
    
    id = Column(Integer, primary_key=True)
    nom = Column(String)
    prenom = Column(String)
    age = Column(Integer)
    taille = Column(Float)
    poids = Column(Float)

    sexe_id = Column(Integer, ForeignKey("sexes.id"))
    sexe = relationship("Sexe", back_populates="clients")

    sport_licence = Column(Boolean, default=False)

    niveau_etude_id = Column(Integer, ForeignKey("niveau_etudes.id"))
    niveau_etude = relationship("NiveauEtude", back_populates="clients")

    region_id = Column(Integer, ForeignKey("regions.id"))
    region = relationship("Region", back_populates="clients")

    fumeur = Column(Boolean, default=False)
    nationalite_francaise = Column(Boolean, default=False)
    revenu_estime_mois = Column(Integer)

    situation_familiale_id = Column(Integer, ForeignKey("situations_familiales.id"), nullable=True)
    situation_familiale = relationship("SituationFamiliale", back_populates="clients")

    region_id = Column(Integer, ForeignKey("regions.id"))
    region = relationship("Region", back_populates="clients")

    historique_credits = Column(Float, nullable=True)
    risque_personnel = Column(Float)
    date_creation_compte = Column(Date)
    score_credit = Column(Float, nullable=True)
    loyer_mensuel = Column(Float, nullable=True)
    montant_pret = Column(Float)


class Sexe(Base):
    __tablename__ = 'sexes'
    
    id = Column(Integer, primary_key=True)
    nom = Column(String, unique=True)
    clients = relationship("Client", back_populates="sexe")


class NiveauEtude(Base):
    __tablename__ = 'niveau_etudes'
    
    id = Column(Integer, primary_key=True)
    nom = Column(String, unique=True)
    clients = relationship("Client", back_populates="niveau_etude")


class Region(Base):
    __tablename__ = 'regions'
    
    id = Column(Integer, primary_key=True)
    nom = Column(String, unique=True)
    clients = relationship("Client", back_populates="region")


class SituationFamiliale(Base):
    __tablename__ = 'situations_familiales'
    
    id = Column(Integer, primary_key=True)
    nom = Column(String, unique=True)
    clients = relationship("Client", back_populates="situation_familiale")
