from backend.loader import load_reisen
from backend.filters import get_filtered_cruises

if __name__ == "__main__":
    filters = {
        "meerart": "Ostsee",
        "naechte": 7,
        "staedte": ["Stockholm", "Tallinn"],
        "schiffstyp": "A"
    }

    reisen = get_filtered_cruises(filters)
    for r in reisen:
        print(r)
