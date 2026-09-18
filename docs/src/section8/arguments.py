import argparse


def main():
    parser = argparse.ArgumentParser(description="Gestionnaire de tâches CLI")

    # Argument positionnel : l'action à faire
    parser.add_argument("action", choices=["add", "list", "remove"], help="L'action à effectuer")

    # Argument optionnel avec valeur par défaut
    parser.add_argument("--priority", type=int, default=1, help="Niveau de priorité (1-5)")

    # Flag booléen (Store True)
    parser.add_argument("-v", "--verbose", action="store_true", help="Affiche des détails")

    # Argument avec choix limités
    parser.add_argument("--category", choices=["travail", "perso"], default="perso", help="Catégorie de la tâche")

    args = parser.parse_args()

    # Utilisation de la logique selon l'argument positionnel
    if args.action == "add":
        print(f"Ajout d'une tâche...")
        if args.verbose:
            print(f"Détails : Priorité {args.priority}, Catégorie {args.category}")

    elif args.action == "list":
        print("Liste des tâches :")
        if args.verbose:
            print("Mode détaillé activé...")

    elif args.action == "remove":
        print("Suppression en cours...")

    print(args)

if __name__ == "__main__":
    main()