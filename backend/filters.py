from backend.loader import load_reisen
import pandas as pd

def get_filtered_cruises(filters):
    all_cruises = load_reisen()

    def match(cruise):
        if filters.get("meerart") and cruise["Meerart"] != filters["meerart"]:
            return False
        if filters.get("naechte"):
            if pd.isna(cruise["Übernachtungen"]):
                return False
            if abs(int(cruise["Übernachtungen"]) - filters["naechte"]) > 2:
                return False
        if filters.get("staedte"):
            if not any(stadt in cruise["besuchte Städte"] for stadt in filters["staedte"]):
                return False
        if filters.get("schiffstyp") and cruise["Schiffstyp"] != filters["schiffstyp"]:
            return False
        return True

    return [c for c in all_cruises if match(c)]
