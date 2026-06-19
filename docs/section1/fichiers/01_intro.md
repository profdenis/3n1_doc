# Lecture et écriture de fichiers

## Aperçu

Les opérations sur les fichiers sont essentielles en programmation Python. Ce guide couvre les bases de la lecture et de
l'écriture de fichiers texte à l'aide de la fonction intégrée `open()` de Python.

## La fonction `open()`

La fonction `open()` est le moyen principal de travailler avec des fichiers en Python. Sa syntaxe de base est :

```python
file_object = open(filename, mode)
```

### Modes de fichier courants

- `'r'` - Mode lecture (par défaut)
- `'w'` - Mode écriture (écrase le contenu existant)
- `'a'` - Mode ajout (ajoute à la fin du fichier)
- `'x'` - Création exclusive (échoue si le fichier existe)

## Lecture de fichiers

### Méthode 1 : Lecture de tout le fichier

```python
# Ouvrir et lire tout le fichier
file = open('example.txt', 'r')
content = file.read()
print(content)
file.close()
```

### Méthode 2 : Lecture ligne par ligne

```python
# Lire ligne par ligne
file = open('example.txt', 'r')
for line in file:
    print(line.strip())  # strip() supprime les caractères de nouvelle ligne
file.close()
```

### Méthode 3 : Lecture des lignes dans une liste

```python
# Lire toutes les lignes dans une liste
file = open('example.txt', 'r')
lines = file.readlines()
file.close()

for line in lines:
    print(line.strip())
```

## Écriture de fichiers

### Écriture de nouveau contenu (écrase le contenu existant)

```python
# Écrire dans un fichier (crée un nouveau ou écrase l'existant)
file = open('output.txt', 'w')
file.write('Bonjour, monde!\n')
file.write('Ceci est une nouvelle ligne.')
file.close()
```

### Ajout à des fichiers existants

```python
# Ajouter à un fichier existant
file = open('output.txt', 'a')
file.write('\nCette ligne est ajoutée.')
file.close()
```

### Écriture de plusieurs lignes

```python
# Écrire plusieurs lignes en une fois
lines = ['Première ligne\n', 'Deuxième ligne\n', 'Troisième ligne\n']
file = open('output.txt', 'w')
file.writelines(lines)
file.close()
```

## Bonne pratique : Utilisation des gestionnaires de contexte

L'instruction `with` gère automatiquement la fermeture des fichiers, même en cas d'erreur :

```python
# Lecture avec gestionnaire de contexte
with open('example.txt', 'r') as file:
    content = file.read()
    print(content)
# Le fichier est automatiquement fermé ici

# Écriture avec gestionnaire de contexte
with open('output.txt', 'w') as file:
    file.write('Bonjour, monde!')
# Le fichier est automatiquement fermé ici
```

## Gestion des erreurs

Toujours gérer les erreurs potentielles liées aux fichiers :

```python
try:
    with open('nonexistent.txt', 'r') as file:
        content = file.read()
        print(content)
except FileNotFoundError:
    print("Fichier introuvable!")
except PermissionError:
    print("Permission refusée!")
except Exception as e:
    print(f"Une erreur est survenue: {e}")
```

## Exemples pratiques

### Exemple 1 : Copie simple de fichier

```python
# Copier le contenu d'un fichier à un autre
try:
    with open('source.txt', 'r') as source:
        with open('destination.txt', 'w') as dest:
            dest.write(source.read())
    print("Fichier copié avec succès!")
except FileNotFoundError:
    print("Fichier source introuvable!")
```

### Exemple 2 : Comptage des mots dans un fichier

```python
def count_words(filename):
    try:
        with open(filename, 'r') as file:
            content = file.read()
            words = content.split()
            return len(words)
    except FileNotFoundError:
        return "Fichier introuvable"


word_count = count_words('example.txt')
print(f"Nombre de mots: {word_count}")
```

### Exemple 3 : Création d'un fichier journal simple

```python
import datetime


def write_log(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('log.txt', 'a') as log_file:
        log_file.write(f"{timestamp}: {message}\n")


# Utilisation
write_log("Programme démarré")
write_log("Traitement des données")
write_log("Programme terminé")
```

## Points clés à retenir

1. Toujours fermer les fichiers après les avoir ouverts (ou utiliser les instructions `with`)
2. Utiliser les modes de fichier appropriés pour vos besoins
3. Gérer les exceptions lors du travail avec des fichiers
4. L'instruction `with` est la méthode préférée pour travailler avec des fichiers
5. Utiliser `strip()` pour supprimer les espaces indésirables des lignes
6. Le mode écriture (`'w'`) écrase complètement les fichiers existants
7. Le mode ajout (`'a'`) ajoute du contenu à la fin des fichiers existants

## Erreurs courantes à éviter

- Oublier de fermer les fichiers (cause des fuites de ressources)
- Utiliser le mode écriture alors qu'on voulait ajouter
- Ne pas gérer les exceptions de fichier
- Oublier d'ajouter les caractères de nouvelle ligne (`\n`) lors de l'écriture
- Ne pas vérifier si un fichier existe avant d'essayer de le lire

Cette base vous servira bien lorsque vous progresserez vers des opérations sur fichiers plus avancées et des
bibliothèques externes pour des formats de fichiers spécifiques.