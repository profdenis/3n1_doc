# Travail avec les fichiers de configuration TOML

## Qu'est-ce que TOML ?

TOML (Tom's Obvious, Minimal Language) est un format de fichier de configuration conçu pour être facile à lire et à
écrire grâce à sa sémantique évidente. Il a été créé par Tom Preston-Werner, co-fondateur de GitHub, comme une
alternative plus conviviale aux autres formats de configuration.

### Caractéristiques clés de TOML

- **Lisible par l'homme** : Syntaxe propre et intuitive facile à comprendre
- **Non ambigu** : Sémantique claire sans cas particuliers surprenants
- **Minimaliste** : Syntaxe simple sans complexité inutile
- **Conscient des types** : Support natif pour les chaînes, entiers, flottants, booléens, dates, tableaux et tables

### TOML vs autres formats

| Caractéristique     | TOML        | JSON      | YAML      | INI       |
|---------------------|-------------|-----------|-----------|-----------|
| Lisible par l'homme | ✅ Excellent | ❌ Verbose | ✅ Bon     | ✅ Bon     |
| Commentaires        | ✅ Oui       | ❌ Non     | ✅ Oui     | ✅ Oui     |
| Types de données    | ✅ Riches    | ✅ Bon     | ✅ Riches  | ❌ Limités |
| Hiérarchique        | ✅ Oui       | ✅ Oui     | ✅ Oui     | ❌ Limité  |
| Complexité          | ✅ Simple    | ✅ Simple  | ❌ Complex | ✅ Simple  |

## Où TOML est utilisé

TOML est devenu populaire dans l'écosystème Python et au-delà :

### Projets Python

- **Poetry** (`pyproject.toml`) - Gestion des dépendances Python
- **Black** - Configuration du formateur de code
- **pytest** - Configuration du framework de test
- **setuptools** - Configuration de construction de paquets
- **pip** - Configuration de l'installateur de paquets

### Autres langages et outils

- **Rust** (`Cargo.toml`) - Configuration du gestionnaire de paquets
- **Hugo** - Configuration du générateur de site statique
- **Netlify** - Configuration de déploiement
- **Docker Compose** - Alternative au format YAML

### Pourquoi TOML pour la configuration ?

1. **Lisible** : Les utilisateurs non techniques peuvent comprendre et modifier les paramètres
2. **Commentaires** : Documenter pourquoi certains paramètres existent
3. **Sécurité des types** : Réduit les erreurs de configuration
4. **Validation** : Facile à valider la structure et les types
5. **Compatible avec le contrôle de version** : Diffs clairs lorsque les paramètres changent

## Installation de la bibliothèque TOML

Python 3.11+ inclut `tomllib` dans la bibliothèque standard (lecture seule). Pour les versions antérieures ou
l'écriture, installez une bibliothèque tierce :

```bash
# Pour Python 3.11+, tomllib est intégré (lecture seule)
# Pour l'écriture ou les versions antérieures de Python :
pip install toml
# ou
pip install tomli tomli-w  # Alternatives plus rapides
```

## Opérations TOML de base

### Syntaxe TOML de base

```toml
# Ceci est un commentaire en TOML

# Paires clé-valeur de base
title = "Mon Application"
version = "1.0.0"
debug = true
max_connections = 100
timeout = 30.5

# Tableaux
allowed_hosts = ["localhost", "127.0.0.1", "example.com"]
ports = [8000, 8001, 8002]

# Tables (similaires aux dictionnaires/objets)
[database]
host = "localhost"
port = 5432
name = "myapp"
username = "admin"

# Tables imbriquées
[database.pool]
min_size = 5
max_size = 20

# Tableau de tables
[[servers]]
name = "web1"
ip = "192.168.1.10"

[[servers]]
name = "web2"
ip = "192.168.1.11"
```

### Lecture des fichiers TOML

```python
# Pour Python 3.11+
import tomllib


# Pour les versions antérieures de Python ou les bibliothèques tierces
# import toml

def read_config(filename):
    """Lire le fichier de configuration TOML"""
    try:
        # Approche pour Python 3.11+
        with open(filename, 'rb') as file:
            config = tomllib.load(file)

        # Alternative pour les versions antérieures de Python :
        # with open(filename, 'r', encoding='utf-8') as file:
        #     config = toml.load(file)

        return config

    except FileNotFoundError:
        print(f"Fichier de configuration {filename} introuvable")
        return {}
    except tomllib.TOMLDecodeError as e:
        print(f"Erreur lors de l'analyse du fichier TOML: {e}")
        return {}


# Utilisation
config = read_config('config.toml')
print(f"Titre de l'application: {config.get('title', 'Inconnu')}")
print(f"Hôte de la base de données: {config.get('database', {}).get('host', 'localhost')}")
```

### Écriture des fichiers TOML

```python
import toml  # Bibliothèque tierce requise pour l'écriture


def write_config(filename, config_data):
    """Écrire la configuration dans un fichier TOML"""
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            toml.dump(config_data, file)
        print(f"Configuration sauvegardée dans {filename}")
        return True

    except Exception as e:
        print(f"Erreur lors de l'écriture de la configuration: {e}")
        return False


# Données de configuration d'exemple
config = {
    'title': 'Mon Application',
    'version': '1.0.0',
    'debug': True,
    'database': {
        'host': 'localhost',
        'port': 5432,
        'name': 'myapp'
    },
    'allowed_hosts': ['localhost', '127.0.0.1']
}

# Écrire la configuration
write_config('output.toml', config)
```

## Exemple complet de configuration d'application

### Fichier de configuration d'exemple (`app_config.toml`)

```toml
# Fichier de Configuration de l'Application
# Généré automatiquement - modifier avec précaution

[app]
name = "Serveur WebAPI"
version = "2.1.0"
description = "Un serveur web API haute performance"
debug = false
environment = "production"

# Configuration du serveur
[server]
host = "0.0.0.0"
port = 8000
workers = 4
timeout = 30
max_request_size = "10MB"
allowed_methods = ["GET", "POST", "PUT", "DELETE"]

# Configuration de la base de données
[database]
engine = "postgresql"
host = "db.example.com"
port = 5432
name = "webapp_prod"
username = "webapp_user"
# Note: Le mot de passe doit être dans les variables d'environnement, pas dans les fichiers de configuration
max_connections = 20
timeout = 30.0
ssl_required = true

# Paramètres du pool de connexions
[database.pool]
min_size = 5
max_size = 20
acquire_timeout = 10.0
recycle_time = 3600

# Configuration du cache Redis
[cache]
enabled = true
backend = "redis"
host = "cache.example.com"
port = 6379
database = 0
key_prefix = "webapp:"
default_timeout = 300

# Configuration des logs
[logging]
level = "INFO"
format = "{time} | {level} | {name} | {message}"
file_enabled = true
file_path = "/var/log/webapp/app.log"
file_rotation = "daily"
file_retention = 30

# Logs console
[logging.console]
enabled = true
colored = true

# Notifications par email
[email]
enabled = true
smtp_host = "smtp.example.com"
smtp_port = 587
use_tls = true
from_address = "noreply@example.com"
admin_emails = ["admin@example.com", "ops@example.com"]

# Paramètres de sécurité
[security]
secret_key_env = "APP_SECRET_KEY"  # Nom de la variable d'environnement
jwt_expiry_hours = 24
bcrypt_rounds = 12
rate_limit_per_minute = 60
cors_origins = ["https://app.example.com", "https://admin.example.com"]

# Indicators de fonctionnalités
[features]
user_registration = true
email_verification = true
two_factor_auth = false
admin_dashboard = true
api_analytics = true

# Intégrations API externes
[[integrations]]
name = "payment_gateway"
enabled = true
base_url = "https://api.payments.com"
timeout = 15
retry_attempts = 3

[[integrations]]
name = "email_service"
enabled = true
base_url = "https://api.emailprovider.com"
timeout = 10
retry_attempts = 2

# Surveillance et métriques
[monitoring]
enabled = true
metrics_port = 9090
health_check_path = "/health"
metrics_path = "/metrics"

[monitoring.alerts]
cpu_threshold = 80.0
memory_threshold = 85.0
disk_threshold = 90.0
response_time_threshold = 1000  # millisecondes
```

### Classe de gestionnaire de configuration

```python
import tomllib
import toml
from pathlib import Path
from typing import Dict, Any, Optional
import os


class ConfigurationManager:
    """Gère la configuration de l'application en utilisant des fichiers TOML"""

    def __init__(self, config_file: str = "config.toml"):
        self.config_file = Path(config_file)
        self.config = {}
        self._load_config()

    def _load_config(self):
        """Charger la configuration depuis le fichier TOML"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'rb') as file:
                    self.config = tomllib.load(file)
                print(f"Configuration chargée depuis {self.config_file}")
            else:
                print(f"Fichier de configuration {self.config_file} introuvable, utilisation des valeurs par défaut")
                self._create_default_config()

        except tomllib.TOMLDecodeError as e:
            print(f"Erreur lors de l'analyse de la configuration TOML: {e}")
            print("Utilisation de la configuration par défaut")
            self._create_default_config()

    def _create_default_config(self):
        """Créer une configuration par défaut"""
        self.config = {
            'app': {
                'name': 'Mon Application',
                'version': '1.0.0',
                'debug': True,
                'environment': 'development'
            },
            'server': {
                'host': 'localhost',
                'port': 8000,
                'workers': 1
            },
            'database': {
                'host': 'localhost',
                'port': 5432,
                'name': 'myapp_dev',
                'max_connections': 10
            },
            'logging': {
                'level': 'DEBUG',
                'console': {'enabled': True}
            }
        }

    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Obtenir la valeur de configuration en utilisant la notation pointée
        Exemple : get('database.host') ou get('server.port')
        """
        keys = key_path.split('.')
        value = self.config

        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default

    def set(self, key_path: str, value: Any):
        """
        Définir la valeur de configuration en utilisant la notation pointée
        Exemple : set('database.host', 'nouvel-hôte')
        """
        keys = key_path.split('.')
        config_section = self.config

        # Naviguer jusqu'à la section parente
        for key in keys[:-1]:
            if key not in config_section:
                config_section[key] = {}
            config_section = config_section[key]

        # Définir la valeur finale
        config_section[keys[-1]] = value

    def save(self, filename: Optional[str] = None):
        """Sauvegarder la configuration actuelle dans un fichier TOML"""
        target_file = Path(filename) if filename else self.config_file

        try:
            with open(target_file, 'w', encoding='utf-8') as file:
                toml.dump(self.config, file)
            print(f"Configuration sauvegardée dans {target_file}")
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde de la configuration: {e}")
            return False

    def validate(self) -> bool:
        """Valider la configuration pour les champs requis"""
        required_sections = ['app', 'server', 'database']
        errors = []

        for section in required_sections:
            if section not in self.config:
                errors.append(f"Section requise manquante: [{section}]")

        # Valider les champs spécifiques requis
        required_fields = {
            'app.name': str,
            'app.version': str,
            'server.host': str,
            'server.port': int,
            'database.host': str,
            'database.port': int
        }

        for field_path, expected_type in required_fields.items():
            value = self.get(field_path)
            if value is None:
                errors.append(f"Champ requis manquant: {field_path}")
            elif not isinstance(value, expected_type):
                errors.append(f"Le champ {field_path} doit être de type {expected_type.__name__}")

        if errors:
            print("Erreurs de validation de la configuration:")
            for error in errors:
                print(f"  - {error}")
            return False

        print("Validation de la configuration réussie")
        return True

    def get_database_url(self) -> str:
        """Générer l'URL de la base de données à partir de la configuration"""
        db_config = self.config.get('database', {})
        username = db_config.get('username', '')
        password = os.getenv('DB_PASSWORD', '')  # Obtenir depuis l'environnement
        host = db_config.get('host', 'localhost')
        port = db_config.get('port', 5432)
        name = db_config.get('name', 'myapp')

        if username and password:
            return f"postgresql://{username}:{password}@{host}:{port}/{name}"
        else:
            return f"postgresql://{host}:{port}/{name}"

    def is_development(self) -> bool:
        """Vérifier si l'exécution se fait en environnement de développement"""
        return self.get('app.environment', 'development') == 'development'

    def is_debug_enabled(self) -> bool:
        """Vérifier si le mode debug est activé"""
        return self.get('app.debug', False)

    def get_server_address(self) -> tuple:
        """Obtenir l'hôte et le port du serveur sous forme de tuple"""
        host = self.get('server.host', 'localhost')
        port = self.get('server.port', 8000)
        return (host, port)

    def print_summary(self):
        """Afficher un résumé de la configuration"""
        print(f"\n=== Résumé de la Configuration ===")
        print(f"Application: {self.get('app.name')} v{self.get('app.version')}")
        print(f"Environnement: {self.get('app.environment')}")
        print(f"Debug: {self.get('app.debug')}")
        print(f"Serveur: {self.get('server.host')}:{self.get('server.port')}")
        print(f"Base de données: {self.get('database.host')}:{self.get('database.port')}")
        print(f"Niveau de log: {self.get('logging.level')}")

        if self.get('features'):
            enabled_features = [k for k, v in self.get('features', {}).items() if v]
            print(f"Fonctionnalités: {', '.join(enabled_features)}")

        print("=" * 30)


# Exemple d'utilisation et de test
def main():
    """Exemple d'utilisation du ConfigurationManager"""

    # Initialiser le gestionnaire de configuration
    config = ConfigurationManager('app_config.toml')

    # Valider la configuration
    if not config.validate():
        print("Validation de la configuration échouée!")
        return

    # Afficher le résumé de la configuration
    config.print_summary()

    # Accéder aux valeurs de configuration
    print(f"\nAccès à la configuration:")
    print(f"Nom de l'application: {config.get('app.name')}")
    print(f"Port du serveur: {config.get('server.port')}")
    print(f"Hôte de la base de données: {config.get('database.host')}")
    print(f"Debug activé: {config.is_debug_enabled()}")
    print(f"Mode développement: {config.is_development()}")

    # Obtenir l'URL de la base de données
    print(f"URL de la base de données: {config.get_database_url()}")

    # Accéder à la configuration imbriquée
    log_level = config.get('logging.level', 'INFO')
    console_enabled = config.get('logging.console.enabled', True)
    print(f"Logs: {log_level}, Console: {console_enabled}")

    # Accéder aux configurations de tableau
    allowed_methods = config.get('server.allowed_methods', [])
    print(f"Méthodes HTTP autorisées: {allowed_methods}")

    # Accéder au tableau de tables
    integrations = config.get('integrations', [])
    enabled_integrations = [i['name'] for i in integrations if i.get('enabled')]
    print(f"Intégrations activées: {enabled_integrations}")

    # Démonstration de la modification de configuration
    print(f"\nModification de la configuration:")
    config.set('app.debug', False)
    config.set('server.port', 9000)
    print(f"Debug maintenant: {config.get('app.debug')}")
    print(f"Port maintenant: {config.get('server.port')}")

    # Sauvegarder la configuration modifiée
    config.save('modified_config.toml')


if __name__ == "__main__":
    main()
```

### Configuration spécifique à l'environnement

```python
import os
from pathlib import Path


class EnvironmentConfigManager(ConfigurationManager):
    """Gestionnaire de configuration avec des substitutions spécifiques à l'environnement"""

    def __init__(self, base_config: str = "config.toml"):
        self.environment = os.getenv('APP_ENV', 'development')
        self.base_config_file = Path(base_config)

        # Charger la configuration de base en premier
        super().__init__(base_config)

        # Puis charger les substitutions spécifiques à l'environnement
        self._load_environment_config()

    def _load_environment_config(self):
        """Charger les substitutions de configuration spécifiques à l'environnement"""
        env_config_file = self.base_config_file.parent / f"config.{self.environment}.toml"

        if env_config_file.exists():
            try:
                with open(env_config_file, 'rb') as file:
                    env_config = tomllib.load(file)

                # Fusionner la configuration de l'environnement avec la configuration de base
                self._deep_merge(self.config, env_config)
                print(f"Configuration de l'environnement chargée depuis {env_config_file}")

            except tomllib.TOMLDecodeError as e:
                print(f"Erreur lors de l'analyse de la configuration de l'environnement: {e}")

    def _deep_merge(self, base_dict: dict, override_dict: dict):
        """Fusionner profondément deux dictionnaires"""
        for key, value in override_dict.items():
            if key in base_dict and isinstance(base_dict[key], dict) and isinstance(value, dict):
                self._deep_merge(base_dict[key], value)
            else:
                base_dict[key] = value


# Exemple d'utilisation
def create_environment_configs():
    """Créer des fichiers de configuration spécifiques à l'environnement"""

    # Substitutions pour le développement
    dev_config = {
        'app': {
            'debug': True,
            'environment': 'development'
        },
        'server': {
            'host': 'localhost',
            'port': 8000,
            'workers': 1
        },
        'database': {
            'host': 'localhost',
            'name': 'myapp_dev'
        },
        'logging': {
            'level': 'DEBUG'
        }
    }

    # Substitutions pour la production
    prod_config = {
        'app': {
            'debug': False,
            'environment': 'production'
        },
        'server': {
            'host': '0.0.0.0',
            'port': 80,
            'workers': 4
        },
        'database': {
            'host': 'prod-db.example.com',
            'name': 'myapp_prod'
        },
        'logging': {
            'level': 'INFO'
        }
    }

    # Sauvegarder les configurations spécifiques à l'environnement
    with open('config.development.toml', 'w') as f:
        toml.dump(dev_config, f)

    with open('config.production.toml', 'w') as f:
        toml.dump(prod_config, f)

    print("Fichiers de configuration spécifiques à l'environnement créés")


# Exemple d'utilisation
if __name__ == "__main__":
    # Définir l'environnement (normalement fait via la variable d'environnement)
    os.environ['APP_ENV'] = 'development'

    # Créer des configurations d'environnement d'exemple
    create_environment_configs()

    # Utiliser une configuration consciente de l'environnement
    config = EnvironmentConfigManager('app_config.toml')
    config.print_summary()
```

## Bonnes pratiques pour la configuration TOML

### 1. Structure et organisation

- Regrouper les paramètres liés dans des tables
- Utiliser des noms de clés clairs et descriptifs
- Garder l'imbrication à un niveau raisonnable (2-3 niveaux max)
- Utiliser des conventions de nommage cohérentes (snake_case recommandé)

### 2. Considérations de sécurité

```toml
# Bon : Référencer les variables d'environnement pour les secrets
[database]
password_env = "DB_PASSWORD"  # Nom de la variable d'environnement

# Mauvais : Ne jamais stocker les secrets dans les fichiers de configuration
# password = "super_secret_password"  # NE PAS FAIRE ÇA

[security]
secret_key_env = "APP_SECRET_KEY"
jwt_secret_env = "JWT_SECRET"
```

### 3. Documentation et commentaires

```toml
# Configuration de l'Application
# Dernière mise à jour : 2024-01-15
# Environnement : Production

[server]
# Nombre maximum de processus workers
# Recommandé : 2 * nombre de cœurs CPU
workers = 4

# Timeout des requêtes en secondes
# Augmenter pour les endpoints lents
timeout = 30
```

### 4. Validation et gestion des erreurs

Toujours valider votre configuration :

```python
def validate_config_types(config):
    """Valider les types de données de la configuration"""
    type_checks = [
        ('server.port', int, lambda x: 1 <= x <= 65535),
        ('server.workers', int, lambda x: x > 0),
        ('database.max_connections', int, lambda x: x > 0),
        ('app.debug', bool, None),
    ]

    for path, expected_type, validator in type_checks:
        value = config.get(path)
        if value is not None:
            if not isinstance(value, expected_type):
                raise ValueError(f"{path} doit être {expected_type.__name__}")
            if validator and not validator(value):
                raise ValueError(f"{path} a échoué la validation")
```

## Points clés à retenir

1. **TOML est pour la configuration** : Parfait pour les paramètres d'application, pas pour le stockage de données
   général
2. **Lisible par l'homme** : Conçu pour être modifié par des humains
3. **Conscient des types** : Supporte des types de données riches nativement
4. **Les commentaires comptent** : Documenter vos choix de configuration
5. **Séparation des environnements** : Utiliser différents fichiers pour différents environnements
6. **Sécurité d'abord** : Ne jamais stocker les secrets dans les fichiers de configuration
7. **Validation** : Toujours valider la configuration après chargement
8. **Valeurs par défaut** : Fournir des valeurs par défaut sensées pour les paramètres optionnels

## Erreurs courantes à éviter

- Stocker les mots de passe ou clés API dans les fichiers TOML
- Créer des structures imbriquées trop complexes
- Ne pas valider la configuration des données
- Mélanger la configuration avec les données d'exécution
- Ne pas utiliser les configurations spécifiques à l'environnement
- Oublier de gérer les fichiers de configuration manquants
- Ne pas documenter les options de configuration

TOML offre un excellent équilibre entre simplicité et puissance pour la configuration des applications, rendant facile
pour les développeurs et les opérateurs de comprendre et modifier les paramètres d'application.