from backend.loader import load_reisen

def get_filtered_cruises(filters):
    reisen = load_reisen()
    ergebnisse = []

    for r in reisen:
        if filters["meerart"] and r["meerart"] != filters["meerart"]:
            continue
        if filters["naechte"] and r["naechte"] != filters["naechte"]:
            continue
        if filters["staedte"]:
            if not all(stadt in r["staedte"] for stadt in filters["staedte"]):
                continue
        if filters["schiffstyp"] and r["schiffstyp"] != filters["schiffstyp"]:
            continue
        ergebnisse.append(r)

    return ergebnisse
