import os
import pandas as pd

def load_reisen(filepath=None):
    """
    Charge les données de croisières depuis un fichier Excel.
    """
    if filepath is None:
        filepath = os.path.join(os.path.dirname(__file__), "..", "schiffreisen.xlsx")

    df = pd.read_excel(filepath, engine="openpyxl", header=3)
    print("Colonnes du fichier Excel:", df.columns.tolist())

    # Nettoyer la colonne 'besuchte Städte' pour avoir des listes
    df["besuchte Städte"] = df["besuchte Städte"].apply(lambda s: s.split(",") if isinstance(s, str) else [])
    return df.to_dict(orient="records")
