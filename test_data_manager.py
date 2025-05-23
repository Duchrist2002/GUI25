from data_manager import init_db, add_user, check_login

def run_tests():
    print(" Initialisation de la base de donnees...")
    init_db()

    # Donnees de test
    username = "tresor"
    email = "tresor@example.com"
    password = "monmotdepasse"

    # ajout d’utilisateur
    print(f"\n Ajout de l'utilisateur : {username}")
    user_added = add_user(username, email, password)
    if user_added:
        print(" Utilisateur ajoute avec succes.")
    else:
        print(" echec de l'ajout (peut-etre deja existant).")

    # Test de connexion avec les bonnes informations
    print(f"\n Verification du login pour : {username}")
    if check_login(username, email, password):
        print(" Connexion reussie.")
    else:
        print(" Connexion echouee.")

    # Test de connexion avec un mauvais mot de passe
    wrong_password = "mauvaismotdepasse"
    print(f"\n Verification du login avec mauvais mot de passe pour : {username}")
    if check_login(username, email, wrong_password):
        print(" Connexion ne devrait pas reussir, mais a reussi.")
    else:
        print(" echec de connexion attendu avec mauvais mot de passe.")

if __name__ == "__main__":
    run_tests()
