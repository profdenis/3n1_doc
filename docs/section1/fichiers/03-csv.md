# Lecture et écriture de fichiers CSV

## Aperçu

Les fichiers CSV (Comma-Separated Values) sont l'un des formats les plus courants pour stocker des données tabulaires.
Le module intégré `csv` de Python fournit des outils puissants pour lire et écrire des fichiers CSV tout en gérant
automatiquement de nombreux cas particuliers.

## Pourquoi utiliser le module `csv` ?

Bien que vous puissiez lire des fichiers CSV avec des opérations de base sur les fichiers, le module `csv` gère :

- Les champs cités contenant des virgules
- Les guillemets échappés dans les champs
- Différents délimiteurs (virgules, points-virgules, tabulations)
- Les sauts de ligne dans les champs cités
- Divers dialectes et formats CSV

## Lecture de base des fichiers CSV

### Méthode 1 : Lecture sous forme de listes

```python
import csv

# Lire un fichier CSV ligne par ligne
with open('data.csv', 'r', encoding='utf-8', newline='') as file:
    csv_reader = csv.reader(file)

    # Lire la ligne d'en-tête
    header = next(csv_reader)
    print("En-tête:", header)

    # Lire les lignes de données
    for row in csv_reader:
        print(row)
```

### Méthode 2 : Lecture sous forme de dictionnaires

```python
import csv

# Lire un CSV avec les noms de colonnes comme clés de dictionnaire
with open('data.csv', 'r', encoding='utf-8', newline='') as file:
    csv_reader = csv.DictReader(file)

    for row in csv_reader:
        print(f"Nom: {row['name']}, Âge: {row['age']}, Ville: {row['city']}")
```

## Écriture de base des fichiers CSV

### Méthode 1 : Écriture de listes

```python
import csv

# Écrire des données sous forme de listes
data = [
    ['Nom', 'Âge', 'Ville'],
    ['Alice', '25', 'New York'],
    ['Bob', '30', 'San Francisco'],
    ['Charlie', '35', 'Chicago']
]

with open('output.csv', 'w', encoding='utf-8', newline='') as file:
    csv_writer = csv.writer(file)

    for row in data:
        csv_writer.writerow(row)

    # Ou écrire toutes les lignes en une fois
    # csv_writer.writerows(data)
```

### Méthode 2 : Écriture de dictionnaires

```python
import csv

# Définir des données sous forme de dictionnaires
data = [
    {'name': 'Alice', 'age': 25, 'city': 'New York'},
    {'name': 'Bob', 'age': 30, 'city': 'San Francisco'},
    {'name': 'Charlie', 'age': 35, 'city': 'Chicago'}
]

fieldnames = ['name', 'age', 'city']

with open('output.csv', 'w', encoding='utf-8', newline='') as file:
    csv_writer = csv.DictWriter(file, fieldnames=fieldnames)

    # Écrire l'en-tête
    csv_writer.writeheader()

    # Écrire les lignes de données
    for row in data:
        csv_writer.writerow(row)

    # Ou écrire toutes les lignes en une fois
    # csv_writer.writerows(data)
```

## Gestion des différents formats CSV

### Délimiteurs personnalisés

```python
import csv

# Lecture d'un fichier séparé par des points-virgules
with open('data.csv', 'r', encoding='utf-8', newline='') as file:
    csv_reader = csv.reader(file, delimiter=';')
    for row in csv_reader:
        print(row)

# Écriture avec un délimiteur personnalisé
with open('output.csv', 'w', encoding='utf-8', newline='') as file:
    csv_writer = csv.writer(file, delimiter=';')
    csv_writer.writerow(['Nom', 'Âge', 'Ville'])
    csv_writer.writerow(['Alice', '25', 'New York'])
```

### Valeurs séparées par des tabulations (TSV)

```python
import csv

# Lecture de fichiers TSV
with open('data.tsv', 'r', encoding='utf-8', newline='') as file:
    csv_reader = csv.reader(file, delimiter='\t')
    for row in csv_reader:
        print(row)

# Écriture de fichiers TSV
with open('output.tsv', 'w', encoding='utf-8', newline='') as file:
    csv_writer = csv.writer(file, delimiter='\t')
    csv_writer.writerow(['Nom', 'Âge', 'Ville'])
```

### Gestion des guillemets et caractères spéciaux

```python
import csv

# Données avec virgules et guillemets
data = [
    ['Nom', 'Description', 'Prix'],
    ['Apple iPhone', 'Téléphone "flagship" le plus récent, très cher', '$999'],
    ['Samsung Galaxy', 'Téléphone Android, bon rapport qualité-prix', '$699'],
    ['Google Pixel', 'Expérience Android pure, appareil photo excellent', '$799']
]

# Écrire avec une citation appropriée
with open('products.csv', 'w', encoding='utf-8', newline='') as file:
    csv_writer = csv.writer(file, quoting=csv.QUOTE_ALL)  # Citer tous les champs
    csv_writer.writerows(data)

# Différentes options de citation :
# csv.QUOTE_ALL - Citer tous les champs
# csv.QUOTE_MINIMAL - Citer uniquement lorsque nécessaire (par défaut)
# csv.QUOTE_NONNUMERIC - Citer tous les champs non numériques
# csv.QUOTE_NONE - Ne jamais citer (à utiliser avec prudence)
```

## Exemples pratiques

### Exemple 1 : Gestionnaire de notes d'élèves

```python
import csv


def read_grades(filename):
    """Lire les notes des élèves depuis un fichier CSV"""
    students = []
    try:
        with open(filename, 'r', encoding='utf-8', newline='') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                # Convertir les notes en entiers
                student = {
                    'name': row['name'],
                    'math': int(row['math']),
                    'science': int(row['science']),
                    'english': int(row['english'])
                }
                students.append(student)
    except FileNotFoundError:
        print(f"Fichier {filename} introuvable")
        return []
    except ValueError as e:
        print(f"Erreur de conversion des notes en nombres: {e}")
        return []

    return students


def calculate_averages(students):
    """Calculer la moyenne pour chaque élève"""
    for student in students:
        avg = (student['math'] + student['science'] + student['english']) / 3
        student['average'] = round(avg, 2)
    return students


def write_grades_with_averages(students, filename):
    """Écrire les élèves et leurs moyennes dans un CSV"""
    fieldnames = ['name', 'math', 'science', 'english', 'average']

    with open(filename, 'w', encoding='utf-8', newline='') as file:
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(students)


# Utilisation
students = read_grades('grades.csv')
students_with_avg = calculate_averages(students)
write_grades_with_averages(students_with_avg, 'grades_with_averages.csv')
print(f"Traitement de {len(students)} élèves")
```

### Exemple 2 : Analyse des données de vente

```python
import csv
from datetime import datetime


def read_sales_data(filename):
    """Lire les données de vente et convertir les types de données"""
    sales = []

    with open(filename, 'r', encoding='utf-8', newline='') as file:
        csv_reader = csv.DictReader(file)

        for row in csv_reader:
            sale = {
                'date': datetime.strptime(row['date'], '%Y-%m-%d'),
                'product': row['product'],
                'quantity': int(row['quantity']),
                'price': float(row['price']),
                'salesperson': row['salesperson']
            }
            sale['total'] = sale['quantity'] * sale['price']
            sales.append(sale)

    return sales


def generate_sales_report(sales, output_filename):
    """Générer un rapport de vente"""
    # Calculer les totaux par vendeur
    salesperson_totals = {}

    for sale in sales:
        person = sale['salesperson']
        if person not in salesperson_totals:
            salesperson_totals[person] = {'sales': 0, 'revenue': 0.0}

        salesperson_totals[person]['sales'] += sale['quantity']
        salesperson_totals[person]['revenue'] += sale['total']

    # Écrire le rapport
    with open(output_filename, 'w', encoding='utf-8', newline='') as file:
        fieldnames = ['salesperson', 'total_sales', 'total_revenue', 'avg_per_sale']
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        csv_writer.writeheader()

        for person, data in salesperson_totals.items():
            avg_per_sale = data['revenue'] / data['sales'] if data['sales'] > 0 else 0
            csv_writer.writerow({
                'salesperson': person,
                'total_sales': data['sales'],
                'total_revenue': round(data['revenue'], 2),
                'avg_per_sale': round(avg_per_sale, 2)
            })


# Utilisation
sales_data = read_sales_data('sales.csv')
generate_sales_report(sales_data, 'sales_report.csv')
```

### Exemple 3 : Nettoyage et validation des données

```python
import csv
import re


def validate_email(email):
    """Validation simple de l'email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def clean_phone_number(phone):
    """Nettoyer et formater le numéro de téléphone"""
    # Supprimer tous les caractères non numériques
    digits = re.sub(r'\D', '', phone)

    # Formater comme (XXX) XXX-XXXX si 10 chiffres
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits[0] == '1':
        return f"({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
    else:
        return phone  # Retourner l'original si impossible à formater


def clean_customer_data(input_filename, output_filename, error_filename):
    """Nettoyer les données clients et séparer les erreurs"""
    clean_data = []
    error_data = []

    with open(input_filename, 'r', encoding='utf-8', newline='') as file:
        csv_reader = csv.DictReader(file)

        for row_num, row in enumerate(csv_reader, start=2):  # Commencer à 2 pour l'en-tête
            errors = []

            # Nettoyer et valider les données
            name = row['name'].strip().title()
            email = row['email'].strip().lower()
            phone = clean_phone_number(row['phone'])

            # Valider
            if not name:
                errors.append("Nom manquant")
            if not validate_email(email):
                errors.append("Email invalide")
            if not phone or len(re.sub(r'\D', '', phone)) < 10:
                errors.append("Téléphone invalide")

            # Préparer la ligne nettoyée
            cleaned_row = {
                'name': name,
                'email': email,
                'phone': phone
            }

            if errors:
                cleaned_row['errors'] = '; '.join(errors)
                cleaned_row['row_number'] = row_num
                error_data.append(cleaned_row)
            else:
                clean_data.append(cleaned_row)

    # Écrire les données nettoyées
    if clean_data:
        with open(output_filename, 'w', encoding='utf-8', newline='') as file:
            fieldnames = ['name', 'email', 'phone']
            csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
            csv_writer.writeheader()
            csv_writer.writerows(clean_data)

    # Écrire les données d'erreur
    if error_data:
        with open(error_filename, 'w', encoding='utf-8', newline='') as file:
            fieldnames = ['row_number', 'name', 'email', 'phone', 'errors']
            csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
            csv_writer.writeheader()
            csv_writer.writerows(error_data)

    return len(clean_data), len(error_data)


# Utilisation
clean_count, error_count = clean_customer_data(
    'customers_raw.csv',
    'customers_clean.csv',
    'customers_errors.csv'
)
print(f"{clean_count} enregistrements nettoyés, {error_count} erreurs trouvées")
```

## Fonctionnalités avancées

### Travail avec de grands fichiers CSV

```python
import csv


def process_large_csv(filename, batch_size=1000):
    """Traiter les grands fichiers CSV par lots"""
    with open(filename, 'r', encoding='utf-8', newline='') as file:
        csv_reader = csv.DictReader(file)

        batch = []
        for row in csv_reader:
            batch.append(row)

            if len(batch) >= batch_size:
                # Traiter le lot
                process_batch(batch)
                batch = []

        # Traiter les lignes restantes
        if batch:
            process_batch(batch)


def process_batch(batch):
    """Traiter un lot de lignes"""
    print(f"Traitement d'un lot de {len(batch)} lignes")
    # Votre logique de traitement ici
```

### Dialectes CSV personnalisés

```python
import csv

# Définir un dialecte CSV personnalisé
csv.register_dialect('custom',
                     delimiter='|',
                     quotechar='"',
                     quoting=csv.QUOTE_MINIMAL,
                     lineterminator='\n')

# Utiliser le dialecte personnalisé
with open('data.csv', 'w', encoding='utf-8', newline='') as file:
    csv_writer = csv.writer(file, dialect='custom')
    csv_writer.writerow(['Nom', 'Âge', 'Ville'])
    csv_writer.writerow(['Alice', '25', 'New York'])
```

## Bonnes pratiques de gestion des erreurs

```python
import csv


def robust_csv_reader(filename):
    """Lire un CSV avec une gestion d'erreur complète"""
    try:
        with open(filename, 'r', encoding='utf-8', newline='') as file:
            # Essayer de détecter le dialecte
            sample = file.read(1024)
            file.seek(0)

            try:
                dialect = csv.Sniffer().sniff(sample)
                csv_reader = csv.reader(file, dialect)
            except csv.Error:
                # Revenir au défaut
                csv_reader = csv.reader(file)

            data = []
            for row_num, row in enumerate(csv_reader, start=1):
                try:
                    # Traiter la ligne
                    data.append(row)
                except Exception as e:
                    print(f"Erreur lors du traitement de la ligne {row_num}: {e}")
                    continue

            return data

    except FileNotFoundError:
        print(f"Fichier {filename} introuvable")
        return []
    except PermissionError:
        print(f"Permission refusée pour accéder à {filename}")
        return []
    except UnicodeDecodeError as e:
        print(f"Erreur d'encodage: {e}")
        return []
    except csv.Error as e:
        print(f"Erreur de parsing CSV: {e}")
        return []


# Utilisation
data = robust_csv_reader('data.csv')
```

## Points clés à retenir

1. **Utilisez toujours `newline=''`** lors de l'ouverture des fichiers CSV pour éviter les lignes vides supplémentaires
   sous Windows
2. **Spécifiez l'encodage** (de préférence UTF-8) pour une comportement cohérent entre les plateformes
3. **Utilisez `DictReader` et `DictWriter`** pour un code plus lisible lorsque vous travaillez avec des en-têtes
4. **Gérez les conversions de types de données explicitement** (le module CSV lit tout comme des chaînes)
5. **Validez et nettoyez les données** lors de leur lecture
6. **Utilisez une citation appropriée** lors de l'écriture des fichiers CSV avec des caractères spéciaux
7. **Gérez les erreurs avec grâce** à l'aide de blocs try-except
8. **Considérez l'utilisation de la mémoire** lorsque vous travaillez avec de grands fichiers

## Erreurs courantes à éviter

- Ne pas utiliser le paramètre `newline=''` (cause des lignes vides supplémentaires)
- Oublier que le module CSV lit tout comme des chaînes
- Ne pas gérer correctement les virgules, guillemets ou sauts de ligne dans les données
- Supposer que tous les fichiers CSV utilisent des délimiteurs par virgule
- Ne pas valider les types de données lors de la lecture
- Oublier d'écrire les en-têtes lorsque vous utilisez `DictWriter`
- Ne pas gérer correctement les problèmes d'encodage

Ce guide fournit une base solide pour travailler avec les fichiers CSV en Python, gérant les scénarios et cas
particuliers les plus courants que vous rencontrerez dans des applications réelles.