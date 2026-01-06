# M3 -Brief 1 - Exposer une base de données relationnelle via une API REST et entrainer un modèle d'IA

## Installation

### Créer un environnement virtuel

``` bash
python -m venv venv
```

Activez l'environnement
``` bash
venv\Scripts\activate
```

### Cloner le repo
``` bash
git clone https://github.com/AshvinPainiaye/m3-brief1-bdd core
cd core
```

### Installer les dépendances
``` bash
pip install -r requirements.txt
```

### Configuration (.env)
Copier le fichier .env.base, le renommer en .env, puis modifier la variable de connexion à la BDD

### Migration de la base de données
``` bash
alembic upgrade head
```

### Démarrer FastAPI
``` bash
fastapi dev api.py
```