from data_manager import init_db, add_user, check_login

def run_tests():
    print(" Initialisation de la base de données...")
    init_db()

    # Données de test
    username = "tresor"
    email = "tresor@example.com"
    password = "monmotdepasse"

    # ajout d’utilisateur
    print(f"\n Ajout de l'utilisateur : {username}")
    user_added = add_user(username, email, password)
    if user_added:
        print(" Utilisateur ajouté avec succès.")
    else:
        print(" Échec de l'ajout (peut-être déjà existant).")

    # Test de connexion avec les bonnes informations
    print(f"\n Vérification du login pour : {username}")
    if check_login(username, email, password):
        print(" Connexion réussie.")
    else:
        print(" Connexion échouée.")

    # Test de connexion avec un mauvais mot de passe
    wrong_password = "mauvaismotdepasse"
    print(f"\n Vérification du login avec mauvais mot de passe pour : {username}")
    if check_login(username, email, wrong_password):
        print(" Connexion ne devrait pas réussir, mais a réussi.")
    else:
        print(" Échec de connexion attendu avec mauvais mot de passe.")

if __name__ == "__main__":
    run_tests()
