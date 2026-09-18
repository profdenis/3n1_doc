# Guide de l'utilisation de `argparse`

Le module `argparse` est l'outil standard de Python pour créer des interfaces en ligne de commande. Il permet de définir
quels arguments votre programme accepte, de spécifier leur type (entier, texte, etc.), et de générer automatiquement
l'aide (`--help`).

## 1. Le Workflow de base

Pour utiliser `argparse`, on suit toujours ces quatre étapes :

1. **Créer** un objet `ArgumentParser`.
2. **Ajouter** des arguments avec `add_argument()`.
3. **Parser** (analyser) les arguments avec `parse_args()`.
4. **Utiliser** les arguments récupérés.

```python
import argparse

# 1. Création du parseur
parser = argparse.ArgumentParser(description="Un programme de test")

# 2. Ajout des arguments
parser.add_argument("nom", help="Votre nom")  # Argument positionnel (obligatoire)
parser.add_argument("-a", "--age", type=int, help="Votre âge")  # Argument optionnel

# 3. Analyse
args = parser.parse_args()

# 4. Utilisation
print(f"Bonjour {args.nom}")
if args.age:
    print(f"Vous avez {args.age} ans.")
```

---

## 2. Les différents types d'arguments

### A. Arguments Positionnels (Obligatoires)

Ils ne commencent pas par un tiret (`-`). L'ordre dans lequel l'utilisateur les tape est crucial.

```python
parser.add_argument("source", help="Fichier source")
parser.add_argument("destination", help="Fichier destination")
# Utilisation : python script.py fichier1.txt fichier2.txt
```

### B. Arguments Optionnels (Flags)

Ils commencent par `-` (raccourci) ou `--` (version longue). Ils sont facultatifs par défaut.

```python
parser.add_argument("-v", "--verbose", help="Mode verbeux")
# Utilisation : python script.py fichier1.txt --verbose
```

### C. Les "Flags" Booléens (`action="store_true"`)

C'est ce que vous utiliserez dans votre TP pour les options `--no-lower`, `--validate`, etc.
Ici, on ne passe pas de valeur. La simple présence de l'argument dans la commande met la variable à `True`. Si
l'argument est absent, elle est `False`.

```python
parser.add_argument("--debug", action="store_true", help="Active le mode debug")
# Utilisation : python script.py --debug  => args.debug est True
# Utilisation : python script.py         => args.debug est False
```

### D. Limiter les choix (`choices`)

Pour forcer l'utilisateur à choisir dans une liste précise.

```python
parser.add_argument("--mode", choices=["fast", "safe", "secure"], default="safe")
# Utilisation : python script.py --mode secure
```

---

## 3. Exemple Complet : "Le Gestionnaire de Tâches"

Cet exemple montre comment organiser un programme qui utilise des types différents et des options booléennes. C'est une
excellente préparation pour votre TP.

```python
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


if __name__ == "__main__":
    main()
```

---

## 4. Aide-mémoire pour les étudiants (Cheat Sheet)

| Commande                             | Effet sur l'objet `args`                   | Usage typique                      |
|:-------------------------------------|:-------------------------------------------|:-----------------------------------|
| `parser.add_argument("nom")`         | `args.nom`                                 | Argument obligatoire (positionnel) |
| `parser.add_argument("--nom")`       | `args.nom`                                 | Option facultative                 |
| `parser.add_argument("-n", "--nom")` | `args.nom`                                 | Option avec raccourci              |
| `type=int`                           | Convertit l'entrée en entier               | Pour les nombres                   |
| `default=valeur`                     | Définit une valeur si l'option est absente | Pour les paramètres configurables  |
| `action="store_true"`                | `True` si présent, `False` sinon           | Pour les interrupteurs (On/Off)    |
| `choices=["a", "b"]`                 | Vérifie que l'entrée est dans la liste     | Pour limiter les options           |

### Conseil pour le TP :

Lorsque vous implémentez votre `main.py`, n'oubliez pas que les arguments de `argparse` sont stockés dans l'objet
`args`. Si vous avez défini `--no-lower`, vous accéderez à la valeur avec `args.no_lower`.