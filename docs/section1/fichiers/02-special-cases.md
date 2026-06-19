# Gestion des problèmes de fichiers sous Windows : encodage et fins de ligne

## Le problème

Les systèmes Windows peuvent causer deux principaux problèmes lors du travail avec des fichiers texte :

1. **Problèmes d'encodage** : Windows utilise souvent CP-1252 ou d'autres encodages au lieu de UTF-8
2. **Différences dans les fins de ligne** : Windows utilise `\r\n` (CRLF) tandis que Unix/Linux/Mac utilisent `\n` (LF)

## Solution 1 : Forcer l'encodage UTF-8

### Lecture avec UTF-8

```python
# Forcer l'encodage UTF-8 lors de la lecture
with open('example.txt', 'r', encoding='utf-8') as file:
    content = file.read()
    print(content)
```

### Écriture avec UTF-8

```python
# Forcer l'encodage UTF-8 lors de l'écriture
with open('output.txt', 'w', encoding='utf-8') as file:
    file.write('Bonjour, monde! 🌍\n')
    file.write('Caractères spéciaux: café, naïve, résumé\n')
```

### Gestion des erreurs d'encodage

```python
# Gérer les fichiers avec encodages inconnus ou mélangés
def read_file_safely(filename):
    encodings = ['utf-8', 'cp-1252', 'iso-8859-1', 'utf-16']

    for encoding in encodings:
        try:
            with open(filename, 'r', encoding=encoding) as file:
                content = file.read()
                print(f"Lecture réussie avec l'encodage {encoding}")
                return content
        except UnicodeDecodeError:
            print(f"Échec de la lecture avec l'encodage {encoding}")
            continue

    # Si tous les encodages échouent, essayer avec gestion d'erreur
    try:
        with open(filename, 'r', encoding='utf-8', errors='replace') as file:
            content = file.read()
            print("Lecture avec UTF-8, remplacement des caractères problématiques")
            return content
    except Exception as e:
        print(f"Impossible de lire le fichier: {e}")
        return None


# Utilisation
content = read_file_safely('problematic_file.txt')
```

## Solution 2 : Gestion des fins de ligne

### Méthode 1 : Utilisation du paramètre `newline`

```python
# Lecture : Préserver les fins de ligne originales
with open('example.txt', 'r', encoding='utf-8', newline='') as file:
    content = file.read()
    # Maintenant vous pouvez voir les fins de ligne réelles dans le contenu

# Écriture : Contrôler explicitement les fins de ligne
with open('output.txt', 'w', encoding='utf-8', newline='') as file:
    file.write('Ligne 1\n')  # Fin de ligne style Unix
    file.write('Ligne 2\r\n')  # Fin de ligne style Windows
    file.write('Ligne 3\n')  # Fin de ligne style Unix
```

### Méthode 2 : Conversion des fins de ligne

```python
def convert_line_endings(input_file, output_file, target_ending='\n'):
    """
    Convertir les fins de ligne dans un fichier
    target_ending: '\n' pour Unix, '\r\n' pour Windows, '\r' pour ancien Mac
    """
    with open(input_file, 'r', encoding='utf-8', newline='') as infile:
        content = infile.read()

    # Normaliser toutes les fins de ligne à \n d'abord
    content = content.replace('\r\n', '\n').replace('\r', '\n')

    # Convertir vers la fin de ligne cible
    if target_ending != '\n':
        content = content.replace('\n', target_ending)

    with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        outfile.write(content)


# Exemples d'utilisation
convert_line_endings('windows_file.txt', 'unix_file.txt', '\n')  # Vers Unix
convert_line_endings('unix_file.txt', 'windows_file.txt', '\r\n')  # Vers Windows
```

### Méthode 3 : Lecture des lignes sans lignes vides supplémentaires

```python
def read_lines_clean(filename):
    """Lire les lignes et supprimer les lignes vides causées par des problèmes de fin de ligne"""
    with open(filename, 'r', encoding='utf-8') as file:
        lines = []
        for line in file:
            cleaned_line = line.strip()
            if cleaned_line:  # Ajouter uniquement les lignes non vides
                lines.append(cleaned_line)
    return lines


# Utilisation
clean_lines = read_lines_clean('messy_file.txt')
for line in clean_lines:
    print(line)
```

## Exemple complet : Traitement robuste de fichiers

```python
def process_text_file(input_filename, output_filename):
    """
    Traiter un fichier texte de manière robuste avec une gestion appropriée de l'encodage et des fins de ligne
    """
    try:
        # Lire avec encodage UTF-8, en préservant les fins de ligne
        with open(input_filename, 'r', encoding='utf-8', newline='') as infile:
            content = infile.read()

        # Normaliser les fins de ligne au style Unix
        content = content.replace('\r\n', '\n').replace('\r', '\n')

        # Traiter le contenu (exemple : convertir en majuscules)
        processed_content = content.upper()

        # Écrire avec encodage UTF-8 et fins de ligne Unix
        with open(output_filename, 'w', encoding='utf-8', newline='') as outfile:
            outfile.write(processed_content)

        print(f"Traitement réussi {input_filename} -> {output_filename}")

    except UnicodeDecodeError as e:
        print(f"Erreur d'encodage: {e}")
        print("Essayez d'utiliser un autre encodage ou une gestion d'erreur")

    except FileNotFoundError:
        print(f"Fichier {input_filename} introuvable")

    except Exception as e:
        print(f"Une erreur est survenue: {e}")


# Utilisation
process_text_file('input.txt', 'output.txt')
```

## Détection de l'encodage du fichier

```python
def detect_file_info(filename):
    """Détecter et afficher les informations d'encodage et de fin de ligne du fichier"""
    try:
        # Essayer de lire avec UTF-8 d'abord
        with open(filename, 'rb') as file:
            raw_data = file.read()

        # Vérifier la BOM (Byte Order Mark)
        if raw_data.startswith(b'\xef\xbb\xbf'):
            print("Le fichier a une BOM UTF-8")
            encoding = 'utf-8-sig'
        else:
            encoding = 'utf-8'

        # Essayer de décoder
        try:
            text = raw_data.decode(encoding)
            print(f"Le fichier peut être lu comme {encoding}")
        except UnicodeDecodeError:
            print("Le fichier n'est pas encodé en UTF-8")
            # Essayer d'autres encodages courants
            for enc in ['cp-1252', 'iso-8859-1']:
                try:
                    text = raw_data.decode(enc)
                    print(f"Le fichier semble être encodé en {enc}")
                    break
                except UnicodeDecodeError:
                    continue

        # Vérifier les fins de ligne
        if b'\r\n' in raw_data:
            print("Le fichier utilise des fins de ligne Windows (CRLF)")
        elif b'\n' in raw_data:
            print("Le fichier utilise des fins de ligne Unix (LF)")
        elif b'\r' in raw_data:
            print("Le fichier utilise des fins de ligne ancien Mac (CR)")
        else:
            print("Aucune fin de ligne détectée (fichier à une seule ligne ?)")

    except FileNotFoundError:
        print(f"Fichier {filename} introuvable")


# Utilisation
detect_file_info('mystery_file.txt')
```

## Résumé des bonnes pratiques

1. **Spécifiez toujours l'encodage** : Utilisez `encoding='utf-8'` pour une comportement cohérent entre les plateformes
2. **Utilisez `newline=''` lorsque vous avez besoin de contrôle** : Cela préserve les fins de ligne originales ou vous
   permet de les définir explicitement
3. **Gérez les erreurs d'encodage avec grâce** : Utilisez des blocs try-except ou le paramètre `errors`
4. **Testez sur différentes plateformes** : Ce qui fonctionne sous Windows peut se comporter différemment sous Linux/Mac
5. **Utilisez `strip()` pour nettoyer les lignes** : Supprime les espaces problématiques et les caractères de fin de
   ligne

## Paramètres courants de gestion des erreurs

```python
# Différentes façons de gérer les erreurs d'encodage
with open('file.txt', 'r', encoding='utf-8', errors='strict') as f:  # Par défaut : lever une exception
    pass

with open('file.txt', 'r', encoding='utf-8', errors='ignore') as f:  # Ignorer les caractères incorrects
    pass

with open('file.txt', 'r', encoding='utf-8', errors='replace') as f:  # Remplacer par �
    pass

with open('file.txt', 'r', encoding='utf-8', errors='backslashreplace') as f:  # Montrer comme \uXXXX
    pass
```

Ces techniques vous aideront à gérer les problèmes d'encodage et de fin de ligne les plus courants rencontrés sur les
systèmes Windows.