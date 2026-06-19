# Lecture et écriture de fichiers JSON

## Aperçu

JSON (JavaScript Object Notation) est un format d'échange de données léger et lisible par l'homme. Le module intégré
`json` de Python facilite le travail avec les données JSON, permettant des conversions fluides entre chaînes JSON et
objets Python.

## Pourquoi utiliser JSON ?

JSON est idéal pour :

- Les API web et l'échange de données
- Les fichiers de configuration
- Le stockage de données structurées
- Le partage de données multiplateformes
- Le stockage de données lisibles par l'homme

## Correspondance entre les types JSON et Python

### Mappage JSON vers Python

| Type JSON      | Type Python      |
|----------------|------------------|
| `null`         | `None`           |
| `true`/`false` | `True`/`False`   |
| `number`       | `int` ou `float` |
| `string`       | `str`            |
| `array`        | `list`           |
| `object`       | `dict`           |

## Opérations JSON de base

### Lecture de fichiers JSON

```python
import json

# Lire un JSON depuis un fichier
with open('data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
    print(data)
    print(type(data))  # Généralement dict ou list
```

### Écriture de fichiers JSON

```python
import json

# Données d'exemple
data = {
    "name": "Alice",
    "age": 30,
    "city": "New York",
    "hobbies": ["reading", "cycling", "cooking"]
}

# Écrire un JSON dans un fichier
with open('output.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=4, ensure_ascii=False)
```

### Travail avec des chaînes JSON

```python
import json

# Convertir un objet Python en chaîne JSON
data = {"name": "Bob", "age": 25}
json_string = json.dumps(data, indent=2)
print(json_string)

# Convertir une chaîne JSON en objet Python
parsed_data = json.loads(json_string)
print(parsed_data)
print(type(parsed_data))  # <class 'dict'>
```

## Travail avec les types Python standard

### Exemple 1 : Dictionnaire simple

```python
import json

# Créer et sauvegarder une configuration simple
config = {
    "database": {
        "host": "localhost",
        "port": 5432,
        "name": "myapp",
        "ssl": True
    },
    "api": {
        "timeout": 30,
        "retries": 3,
        "endpoints": [
            "/api/users",
            "/api/products",
            "/api/orders"
        ]
    },
    "features": {
        "logging": True,
        "debug": False,
        "cache_size": 1000
    }
}

# Sauvegarder la configuration
with open('config.json', 'w', encoding='utf-8') as file:
    json.dump(config, file, indent=4)

# Charger et utiliser la configuration
with open('config.json', 'r', encoding='utf-8') as file:
    loaded_config = json.load(file)

    db_host = loaded_config['database']['host']
    api_timeout = loaded_config['api']['timeout']
    print(f"Hôte de base de données: {db_host}")
    print(f"Timeout API: {api_timeout} secondes")
```

### Exemple 2 : Liste de dictionnaires

```python
import json

# Enregistrements d'étudiants
students = [
    {
        "id": 1,
        "name": "Alice Johnson",
        "email": "alice@email.com",
        "grades": {
            "math": 95,
            "science": 87,
            "english": 92
        },
        "active": True
    },
    {
        "id": 2,
        "name": "Bob Smith",
        "email": "bob@email.com",
        "grades": {
            "math": 78,
            "science": 91,
            "english": 85
        },
        "active": True
    },
    {
        "id": 3,
        "name": "Charlie Brown",
        "email": "charlie@email.com",
        "grades": {
            "math": 82,
            "science": 79,
            "english": 88
        },
        "active": False
    }
]

# Sauvegarder les données des étudiants
with open('students.json', 'w', encoding='utf-8') as file:
    json.dump(students, file, indent=4)

# Charger et traiter les données des étudiants
with open('students.json', 'r', encoding='utf-8') as file:
    loaded_students = json.load(file)

    # Trouver les étudiants actifs avec une note en math > 80
    high_math_students = [
        student for student in loaded_students
        if student['active'] and student['grades']['math'] > 80
    ]

    print("Étudiants performants en mathématiques:")
    for student in high_math_students:
        print(f"- {student['name']}: {student['grades']['math']}")
```

## Travail avec des classes personnalisées

### Approche de base : Conversion manuelle

```python
import json


class Person:
    def __init__(self, name, age, email, hobbies=None):
        self.name = name
        self.age = age
        self.email = email
        self.hobbies = hobbies or []

    def to_dict(self):
        """Convertir l'objet Person en dictionnaire"""
        return {
            'name': self.name,
            'age': self.age,
            'email': self.email,
            'hobbies': self.hobbies
        }

    @classmethod
    def from_dict(cls, data):
        """Créer un objet Person depuis un dictionnaire"""
        return cls(
            name=data['name'],
            age=data['age'],
            email=data['email'],
            hobbies=data.get('hobbies', [])
        )

    def __repr__(self):
        return f"Person(name='{self.name}', age={self.age}, email='{self.email}')"


# Créer des objets Person
people = [
    Person("Alice", 30, "alice@email.com", ["reading", "hiking"]),
    Person("Bob", 25, "bob@email.com", ["gaming", "cooking"]),
    Person("Charlie", 35, "charlie@email.com", ["photography"])
]

# Convertir en dictionnaires et sauvegarder
people_data = [person.to_dict() for person in people]

with open('people.json', 'w', encoding='utf-8') as file:
    json.dump(people_data, file, indent=4)

# Charger et convertir en objets Person
with open('people.json', 'r', encoding='utf-8') as file:
    loaded_data = json.load(file)

    loaded_people = [Person.from_dict(data) for data in loaded_data]

    print("Personnes chargées:")
    for person in loaded_people:
        print(person)
```

### Approche avancée : Encodage/Decodage JSON personnalisé

```python
import json
from datetime import datetime, date


class Person:
    def __init__(self, name, age, email, birth_date=None, hobbies=None):
        self.name = name
        self.age = age
        self.email = email
        self.birth_date = birth_date
        self.hobbies = hobbies or []

    def __repr__(self):
        return f"Person(name='{self.name}', age={self.age})"


class PersonEncoder(json.JSONEncoder):
    """Encodage JSON personnalisé pour les objets Person"""

    def default(self, obj):
        if isinstance(obj, Person):
            return {
                '__type__': 'Person',
                'name': obj.name,
                'age': obj.age,
                'email': obj.email,
                'birth_date': obj.birth_date.isoformat() if obj.birth_date else None,
                'hobbies': obj.hobbies
            }
        elif isinstance(obj, (datetime, date)):
            return obj.isoformat()

        # Laisser la classe de base gérer les autres types
        return super().default(obj)


def person_decoder(dct):
    """Décodage JSON personnalisé pour les objets Person"""
    if '__type__' in dct and dct['__type__'] == 'Person':
        birth_date = None
        if dct['birth_date']:
            birth_date = datetime.fromisoformat(dct['birth_date']).date()

        return Person(
            name=dct['name'],
            age=dct['age'],
            email=dct['email'],
            birth_date=birth_date,
            hobbies=dct['hobbies']
        )
    return dct


# Créer des objets Person avec dates
people = [
    Person("Alice", 30, "alice@email.com", date(1993, 5, 15), ["reading", "hiking"]),
    Person("Bob", 25, "bob@email.com", date(1998, 8, 22), ["gaming", "cooking"]),
    Person("Charlie", 35, "charlie@email.com", date(1988, 12, 3), ["photography"])
]

# Sauvegarder avec l'encodage personnalisé
with open('people_advanced.json', 'w', encoding='utf-8') as file:
    json.dump(people, file, cls=PersonEncoder, indent=4)

# Charger avec le décodage personnalisé
with open('people_advanced.json', 'r', encoding='utf-8') as file:
    loaded_people = json.load(file, object_hook=person_decoder)

    print("Personnes chargées avec décodage personnalisé:")
    for person in loaded_people:
        print(f"{person} - Né le: {person.birth_date}")
```

## Exemple complexe : Système de gestion de bibliothèque

```python
import json
from datetime import datetime, date
from typing import List, Optional


class Book:
    def __init__(self, isbn, title, author, publication_year, genre=None):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.publication_year = publication_year
        self.genre = genre or "Unknown"

    def to_dict(self):
        return {
            'isbn': self.isbn,
            'title': self.title,
            'author': self.author,
            'publication_year': self.publication_year,
            'genre': self.genre
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            isbn=data['isbn'],
            title=data['title'],
            author=data['author'],
            publication_year=data['publication_year'],
            genre=data.get('genre', 'Unknown')
        )

    def __repr__(self):
        return f"Book('{self.title}' by {self.author})"


class Member:
    def __init__(self, member_id, name, email, join_date=None):
        self.member_id = member_id
        self.name = name
        self.email = email
        self.join_date = join_date or date.today()
        self.borrowed_books = []

    def borrow_book(self, book, due_date):
        loan = {
            'book': book,
            'borrowed_date': date.today(),
            'due_date': due_date
        }
        self.borrowed_books.append(loan)

    def to_dict(self):
        return {
            'member_id': self.member_id,
            'name': self.name,
            'email': self.email,
            'join_date': self.join_date.isoformat(),
            'borrowed_books': [
                {
                    'book': loan['book'].to_dict(),
                    'borrowed_date': loan['borrowed_date'].isoformat(),
                    'due_date': loan['due_date'].isoformat()
                }
                for loan in self.borrowed_books
            ]
        }

    @classmethod
    def from_dict(cls, data):
        member = cls(
            member_id=data['member_id'],
            name=data['name'],
            email=data['email'],
            join_date=datetime.fromisoformat(data['join_date']).date()
        )

        # Reconstruire les livres empruntés
        for loan_data in data['borrowed_books']:
            book = Book.from_dict(loan_data['book'])
            borrowed_date = datetime.fromisoformat(loan_data['borrowed_date']).date()
            due_date = datetime.fromisoformat(loan_data['due_date']).date()

            loan = {
                'book': book,
                'borrowed_date': borrowed_date,
                'due_date': due_date
            }
            member.borrowed_books.append(loan)

        return member

    def __repr__(self):
        return f"Member(ID: {self.member_id}, Name: '{self.name}')"


class Library:
    def __init__(self, name):
        self.name = name
        self.books = []
        self.members = []

    def add_book(self, book):
        self.books.append(book)

    def add_member(self, member):
        self.members.append(member)

    def to_dict(self):
        return {
            'name': self.name,
            'books': [book.to_dict() for book in self.books],
            'members': [member.to_dict() for member in self.members]
        }

    @classmethod
    def from_dict(cls, data):
        library = cls(data['name'])

        # Reconstruire les livres
        library.books = [Book.from_dict(book_data) for book_data in data['books']]

        # Reconstruire les membres
        library.members = [Member.from_dict(member_data) for member_data in data['members']]

        return library

    def save_to_json(self, filename):
        """Sauvegarder les données de la bibliothèque dans un fichier JSON"""
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(self.to_dict(), file, indent=4, ensure_ascii=False)

    @classmethod
    def load_from_json(cls, filename):
        """Charger les données de la bibliothèque depuis un fichier JSON"""
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return cls.from_dict(data)

    def get_overdue_books(self):
        """Trouver tous les livres en retard"""
        today = date.today()
        overdue = []

        for member in self.members:
            for loan in member.borrowed_books:
                if loan['due_date'] < today:
                    overdue.append({
                        'member': member,
                        'book': loan['book'],
                        'due_date': loan['due_date'],
                        'days_overdue': (today - loan['due_date']).days
                    })

        return overdue


# Exemple d'utilisation
def create_sample_library():
    """Créer une bibliothèque d'exemple avec des livres et des membres"""
    library = Library("City Central Library")

    # Ajouter des livres
    books = [
        Book("978-0-547-92822-7", "The Hobbit", "J.R.R. Tolkien", 1937, "Fantasy"),
        Book("978-0-06-112008-4", "To Kill a Mockingbird", "Harper Lee", 1960, "Classic"),
        Book("978-0-7432-7356-5", "The Da Vinci Code", "Dan Brown", 2003, "Thriller"),
        Book("978-0-14-303943-3", "1984", "George Orwell", 1949, "Dystopian")
    ]

    for book in books:
        library.add_book(book)

    # Ajouter des membres
    member1 = Member(1, "Alice Johnson", "alice@email.com", date(2023, 1, 15))
    member2 = Member(2, "Bob Smith", "bob@email.com", date(2023, 3, 22))

    # Simuler l'emprunt de livres
    from datetime import timedelta
    member1.borrow_book(books[0], date.today() + timedelta(days=14))  # The Hobbit
    member1.borrow_book(books[1], date.today() - timedelta(days=5))  # Livre en retard
    member2.borrow_book(books[2], date.today() + timedelta(days=7))  # The Da Vinci Code

    library.add_member(member1)
    library.add_member(member2)

    return library


# Créer et sauvegarder la bibliothèque
library = create_sample_library()
library.save_to_json('library.json')
print(f"Bibliothèque '{library.name}' sauvegardée avec {len(library.books)} livres et {len(library.members)} membres")

# Charger la bibliothèque depuis JSON
loaded_library = Library.load_from_json('library.json')
print(f"Bibliothèque '{loaded_library.name}' chargée")

# Vérifier les livres en retard
overdue = loaded_library.get_overdue_books()
if overdue:
    print("\nLivres en retard:")
    for item in overdue:
        print(f"- {item['member'].name} a '{item['book'].title}' en retard de {item['days_overdue']} jours")
else:
    print("\nAucun livre en retard!")

# Afficher tous les membres et leurs livres
print(f"\nMembres de la bibliothèque:")
for member in loaded_library.members:
    print(f"- {member.name} (rejoint le {member.join_date})")
    if member.borrowed_books:
        for loan in member.borrowed_books:
            status = "EN RETARD" if loan['due_date'] < date.today() else "OK"
            print(f"  * '{loan['book'].title}' à rendre le {loan['due_date']} [{status}]")
    else:
        print("  * Aucun livre emprunté")
```

## Gestion des erreurs et bonnes pratiques

### Lecture JSON robuste

```python
import json


def safe_load_json(filename, default=None):
    """Charger un JSON de manière sécurisée avec une gestion d'erreur complète"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)

    except FileNotFoundError:
        print(f"Fichier {filename} introuvable")
        return default

    except PermissionError:
        print(f"Permission refusée pour accéder à {filename}")
        return default

    except json.JSONDecodeError as e:
        print(f"JSON invalide dans {filename}: {e}")
        return default

    except UnicodeDecodeError as e:
        print(f"Erreur d'encodage lors de la lecture de {filename}: {e}")
        return default

    except Exception as e:
        print(f"Erreur inattendue lors de la lecture de {filename}: {e}")
        return default


# Utilisation
data = safe_load_json('config.json', default={})
if data:
    print("Configuration chargée avec succès")
else:
    print("Utilisation de la configuration par défaut")
```

### Validation de la structure JSON

```python
import json


def validate_person_data(data):
    """Valider que les données contiennent les champs requis pour Person"""
    required_fields = ['name', 'age', 'email']

    if not isinstance(data, dict):
        raise ValueError("Les données de Person doivent être un dictionnaire")

    for field in required_fields:
        if field not in data:
            raise ValueError(f"Champ requis manquant: {field}")

    if not isinstance(data['name'], str) or not data['name'].strip():
        raise ValueError("Le nom doit être une chaîne non vide")

    if not isinstance(data['age'], int) or data['age'] < 0:
        raise ValueError("L'âge doit être un entier non négatif")

    if not isinstance(data['email'], str) or '@' not in data['email']:
        raise ValueError("L'email doit être une adresse email valide")

    return True


def load_people_safely(filename):
    """Charger les données des personnes avec validation"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError("Une liste de personnes était attendue")

        people = []
        for i, person_data in enumerate(data):
            try:
                validate_person_data(person_data)
                people.append(Person.from_dict(person_data))
            except ValueError as e:
                print(f"Données de personne invalides à l'index {i}: {e}")
                continue

        return people

    except Exception as e:
        print(f"Erreur lors du chargement des personnes: {e}")
        return []


# Utilisation
people = load_people_safely('people.json')
print(f"{len(people)} personnes chargées avec succès")
```

## Techniques JSON avancées

### Affichage formaté de JSON

```python
import json


def pretty_print_json(data):
    """Afficher un JSON de manière formatée avec une mise en forme personnalisée"""
    print(json.dumps(data, indent=4, sort_keys=True, ensure_ascii=False))


# Options de mise en forme personnalisées
data = {"name": "José", "age": 30, "hobbies": ["música", "fútbol"]}

# Différentes options de mise en forme
print("Compact:")
print(json.dumps(data, separators=(',', ':')))

print("\nFormaté avec clés triées:")
print(json.dumps(data, indent=2, sort_keys=True))

print("\nAvec caractères Unicode:")
print(json.dumps(data, indent=2, ensure_ascii=False))
```

### Travail avec de grands fichiers JSON

```python
import json


def process_large_json_file(filename, process_item_func):
    """Traiter les grands fichiers JSON élément par élément (en supposant qu'il s'agit d'une liste)"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)

            if isinstance(data, list):
                for i, item in enumerate(data):
                    try:
                        process_item_func(item, i)
                    except Exception as e:
                        print(f"Erreur lors du traitement de l'élément {i}: {e}")
            else:
                process_item_func(data, 0)

    except Exception as e:
        print(f"Erreur lors du traitement du fichier: {e}")


def process_person(person_data, index):
    """Fonction de traitement d'exemple"""
    print(f"Traitement de la personne {index + 1}: {person_data.get('name', 'Inconnu')}")


# Utilisation
process_large_json_file('large_people.json', process_person)
```

## Points clés à retenir

1. **Spécifiez toujours l'encodage** lors de l'ouverture des fichiers (utilisez UTF-8)
2. **Gérez les erreurs JSON avec grâce** à l'aide de blocs try-except
3. **Validez la structure des données** avant le traitement
4. **Utilisez `ensure_ascii=False`** pour préserver les caractères Unicode
5. **Considérez l'utilisation de la mémoire** avec les grands fichiers JSON
6. **Créez des méthodes de conversion** (`to_dict`, `from_dict`) pour les classes personnalisées
7. **Utilisez des encodages/décodages personnalisés** pour les objets complexes
8. **Gérez explicitement les dates et objets datetime** (JSON n'a pas de types de date natifs)

## Erreurs courantes à éviter

- Ne pas gérer les exceptions `JSONDecodeError`
- Oublier que JSON ne supporte pas directement les ensembles, tuples ou objets datetime Python
- Ne pas valider la structure JSON avant le traitement
- Utiliser `eval()` au lieu de `json.loads()` (risque de sécurité)
- Ne pas spécifier l'encodage lors de la lecture des fichiers
- Supposer la structure du fichier JSON sans validation
- Ne pas gérer correctement les valeurs None/null
- Oublier d'utiliser `ensure_ascii=False` pour les caractères internationaux

Ce guide fournit une base complète pour travailler avec JSON en Python, des structures de données simples aux classes
personnalisées complexes avec une gestion et validation des erreurs appropriées.