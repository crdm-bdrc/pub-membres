# Pub-membres
Outil pour extraire d'ORCID les publications de chercheurs

## Installation

```bash
git clone https://github.com/crdm-bdrc/pub-membres
cd pub-membres
poetry install
```

Créer un fichier orcids.txt, et y insérer ligne par ligne les orcids des chercheurs dont on veut extraire les publications.

Voir main.py pour un exemple d'utilisation. On peut changer les valeurs de YEARS pour extraire les publications d'une autre période.

Pour exécuter le script:

```bash
poetry run python main.py
```
