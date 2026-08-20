# Travail avec les fichiers de configuration YAML

## Qu'est-ce que YAML ?

YAML (YAML Ain't Markup Language) est un standard de sérialisation de données humainement compréhensible pour tous les
langages de programmation. Il est couramment utilisé pour les fichiers de configuration et l'échange de données entre
systèmes.

### Caractéristiques clés de YAML

- **Lisible par l'homme** : Syntaxe propre et intuitive facile à comprendre
- **Supporte des structures de données complexes** : Listes, dictionnaires, objets imbriqués
- **Commentaires** : Peut inclure des commentaires pour la documentation
- **Inférence de types** : Détecte automatiquement les types de données
- **Sensible aux espaces** : Utilise l'indentation pour la structure (comme Python)

### YAML vs autres formats

| Caractéristique     | YAML                 | JSON      | TOML     | INI       |
|---------------------|----------------------|-----------|----------|-----------|
| Lisible par l'homme | ✅ Excellent          | ❌ Verbose | ✅ Bon    | ✅ Bon     |
| Commentaires        | ✅ Oui                | ❌ Non     | ✅ Oui    | ✅ Oui     |
| Types de données    | ✅ Riches             | ✅ Bon     | ✅ Riches | ❌ Limités |
| Hiérarchique        | ✅ Excellent          | ✅ Oui     | ✅ Oui    | ❌ Limité  |
| Complexité          | ❌ Peut être complexe | ✅ Simple  | ✅ Simple | ✅ Simple  |

## Où YAML est utilisé

YAML est largement utilisé dans divers domaines :

### DevOps et Cloud Computing

- **Docker Compose** - Orchestration de conteneurs
- **Kubernetes** - Configuration de cluster
- **Ansible** - Infrastructure as code
- **Terraform** - Provisionnement d'infrastructure

### Projets Python

- **PyYAML** - Parseur YAML pour Python
- **Sphinx** - Générateur de documentation
- **Travis CI** - Configuration d'intégration continue
- **GitHub Actions** - Définitions de workflows

### Pourquoi YAML pour la configuration ?

1. **Lisible** : Les utilisateurs non techniques peuvent comprendre et modifier les paramètres
2. **Flexible** : Supporte des structures imbriquées complexes
3. **Commentaires** : Documenter pourquoi certains paramètres existent
4. **Inférence de types** : Réduit les erreurs de configuration
5. **Compatible avec le contrôle de version** : Diffs clairs lorsque les paramètres changent

## Installation de la bibliothèque YAML

Python dispose de plusieurs bibliothèques YAML disponibles :

```bash
# PyYAML - Bibliothèque YAML la plus populaire pour Python
pip install pyyaml

# Alternative : ruamel.yaml (supporte la préservation du parcours aller-retour)
pip install ruamel.yaml
```

## Opérations YAML de base

### Syntaxe YAML de base

```yaml
# Ceci est un commentaire en YAML

# Valeurs scalaires
nom: "Mon Application"
version: 1.0.0
debug: true
max_connexions: 100
timeout: 30.5

# Listes (tableaux)
hôtes_autorisés:
  - localhost
  - 127.0.0.1
  - example.com

ports: [ 8000, 8001, 8002 ]

# Dictionnaires (mappings)
base_de_données:
  hôte: localhost
  port: 5432
  nom: myapp
  utilisateur: admin

# Structures imbriquées
serveur:
  hôte: 0.0.0.0
  port: 8000
  workers: 4
  base_de_données:
    taille_pool: 10
    timeout: 30
```

### Lecture des fichiers YAML

```python
import yaml


def lire_config(fichier):
    """Lire le fichier de configuration YAML"""
    try:
        with open(fichier, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)

        return config if config else {}

    except FileNotFoundError:
        print(f"Fichier de configuration {fichier} introuvable")
        return {}
    except yaml.YAMLError as e:
        print(f"Erreur lors de l'analyse du fichier YAML: {e}")
        return {}


# Utilisation
config = lire_config('config.yaml')
print(f"Nom de l'application: {config.get('nom', 'Inconnu')}")
print(f"Hôte de la base de données: {config.get('base_de_données', {}).get('hôte', 'localhost')}")
```

### Écriture des fichiers YAML

```python
import yaml


def écrire_config(fichier, données_config):
    """Écrire la configuration dans un fichier YAML"""
    try:
        with open(fichier, 'w', encoding='utf-8') as file:
            yaml.dump(données_config, file, sort_keys=False)
        print(f"Configuration sauvegardée dans {fichier}")
        return True

    except Exception as e:
        print(f"Erreur lors de l'écriture de la configuration: {e}")
        return False


# Données de configuration d'exemple
config = {
    'nom': 'Mon Application',
    'version': 1.0,
    'debug': True,
    'base_de_données': {
        'hôte': 'localhost',
        'port': 5432,
        'nom': 'myapp'
    },
    'hôtes_autorisés': ['localhost', '127.0.0.1']
}

# Écrire la configuration
écrire_config('output.yaml', config)
```

## Exemple complet de configuration d'application

### Fichier de configuration d'exemple (`app_config.yaml`)

```yaml
# Fichier de Configuration de l'Application
# Généré automatiquement - modifier avec précaution

application:
  nom: "Serveur WebAPI"
  version: "2.1.0"
  description: "Un serveur web API haute performance"
  debug: false
  environnement: "production"

serveur:
  hôte: "0.0.0.0"
  port: 8000
  workers: 4
  timeout: 30
  taille_max_request: "10MB"
  méthodes_autorisées:
    - GET
    - POST
    - PUT
    - DELETE

base_de_données:
  moteur: "postgresql"
  hôte: "db.example.com"
  port: 5432
  nom: "webapp_prod"
  utilisateur: "webapp_user"
  # Note: Le mot de passe doit être dans les variables d'environnement, pas dans les fichiers de configuration
  max_connexions: 20
  timeout: 30.0
  ssl_requis: true

  pool:
    taille_min: 5
    taille_max: 20
    timeout_acquisition: 10.0
    temps_recyclage: 3600

cache:
  activé: true
  backend: "redis"
  hôte: "cache.example.com"
  port: 6379
  base_de_données: 0
  préfixe_clé: "webapp:"
  timeout_par_defaut: 300

logs:
  niveau: "INFO"
  format: "{temps} | {niveau} | {nom} | {message}"
  fichier_activé: true
  chemin_fichier: "/var/log/webapp/app.log"
  rotation_fichier: "quotidienne"
  rétention_fichier: 30

  console:
    activée: true
    colorée: true

email:
  activé: true
  hôte_smtp: "smtp.example.com"
  port_smtp: 587
  utiliser_tls: true
  adresse_expéditeur: "noreply@example.com"
  emails_admin:
    - "admin@example.com"
    - "ops@example.com"

sécurité:
  clé_secrète_env: "APP_SECRET_KEY"  # Nom de la variable d'environnement
  durée_jwt_heures: 24
  tours_bcrypt: 12
  limite_taux_minute: 60
  origines_cors:
    - "https://app.example.com"
    - "https://admin.example.com"

fonctionnalités:
  inscription_utilisateur: true
  vérification_email: true
  authentification_2_facteurs: false
  tableau_de_bord_admin: true
  analytics_api: true

intégrations:
  - nom: "paiement_gateway"
    activé: true
    url_base: "https://api.payments.com"
    timeout: 15
    tentatives_reessai: 3

  - nom: "service_email"
    activé: true
    url_base: "https://api.emailprovider.com"
    timeout: 10
    tentatives_reessai: 2

surveillance:
  activée: true
  port_métriques: 9090
  chemin_vérification_santé: "/health"
  chemin_métriques: "/metrics"

  alertes:
    seuil_cpu: 80.0
    seuil_mémoire: 85.0
    seuil_disque: 90.0
    seuil_temps_reponse: 1000  # millisecondes
```

### Classe de gestionnaire de configuration

```python
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
import os


class GestionnaireConfigurationYAML:
    """Gère la configuration de l'application en utilisant des fichiers YAML"""

    def __init__(self, fichier_config: str = "config.yaml"):
        self.fichier_config = Path(fichier_config)
        self.config = {}
        self._charger_config()

    def _charger_config(self):
        """Charger la configuration depuis le fichier YAML"""
        try:
            if self.fichier_config.exists():
                with open(self.fichier_config, 'r', encoding='utf-8') as file:
                    self.config = yaml.safe_load(file)
                print(f"Configuration chargée depuis {self.fichier_config}")
            else:
                print(f"Fichier de configuration {self.fichier_config} introuvable, utilisation des valeurs par défaut")
                self._créer_config_par_défaut()

        except yaml.YAMLError as e:
            print(f"Erreur lors de l'analyse de la configuration YAML: {e}")
            print("Utilisation de la configuration par défaut")
            self._créer_config_par_défaut()

    def _créer_config_par_défaut(self):
        """Créer une configuration par défaut"""
        self.config = {
            'application': {
                'nom': 'Mon Application',
                'version': 1.0,
                'debug': True,
                'environnement': 'développement'
            },
            'serveur': {
                'hôte': 'localhost',
                'port': 8000,
                'workers': 1
            },
            'base_de_données': {
                'hôte': 'localhost',
                'port': 5432,
                'nom': 'myapp_dev',
                'max_connexions': 10
            },
            'logs': {
                'niveau': 'DEBUG',
                'console': {'activée': True}
            }
        }

    def obtenir(self, chemin_clé: str, valeur_par_défaut: Any = None) -> Any:
        """
        Obtenir la valeur de configuration en utilisant la notation pointée
        Exemple : obtenir('base_de_données.hôte') ou obtenir('serveur.port')
        """
        clés = chemin_clé.split('.')
        valeur = self.config

        try:
            for clé in clés:
                valeur = valeur[clé]
            return valeur
        except (KeyError, TypeError):
            return valeur_par_défaut

    def définir(self, chemin_clé: str, valeur: Any):
        """
        Définir la valeur de configuration en utilisant la notation pointée
        Exemple : définir('base_de_données.hôte', 'nouvel-hôte')
        """
        clés = chemin_clé.split('.')
        section_config = self.config

        # Naviguer jusqu'à la section parente
        for clé in clés[:-1]:
            if clé not in section_config:
                section_config[clé] = {}
            section_config = section_config[clé]

        # Définir la valeur finale
        section_config[clés[-1]] = valeur

    def sauvegarder(self, fichier: Optional[str] = None):
        """Sauvegarder la configuration actuelle dans un fichier YAML"""
        fichier_cible = Path(fichier) if fichier else self.fichier_config

        try:
            with open(fichier_cible, 'w', encoding='utf-8') as file:
                yaml.dump(self.config, file, sort_keys=False)
            print(f"Configuration sauvegardée dans {fichier_cible}")
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde de la configuration: {e}")
            return False

    def valider(self) -> bool:
        """Valider la configuration pour les champs requis"""
        sections_requises = ['application', 'serveur', 'base_de_données']
        erreurs = []

        for section in sections_requises:
            if section not in self.config:
                erreurs.append(f"Section requise manquante: {section}")

        # Valider les champs spécifiques requis
        champs_requis = {
            'application.nom': str,
            'application.version': (str, int, float),
            'serveur.hôte': str,
            'serveur.port': int,
            'base_de_données.hôte': str,
            'base_de_données.port': int
        }

        for chemin_champ, types_attendus in champs_requis.items():
            valeur = self.obtenir(chemin_champ)
            if valeur is None:
                erreurs.append(f"Champ requis manquant: {chemin_champ}")
            elif not isinstance(valeur, types_attendus):
                noms_types = ', '.join(t.__name__ for t in types_attendus)
                erreurs.append(f"Le champ {chemin_champ} doit être de type {noms_types}")

        if erreurs:
            print("Erreurs de validation de la configuration:")
            for erreur in erreurs:
                print(f"  - {erreur}")
            return False

        print("Validation de la configuration réussie")
        return True

    def obtenir_url_base_de_données(self) -> str:
        """Générer l'URL de la base de données à partir de la configuration"""
        config_bdd = self.config.get('base_de_données', {})
        utilisateur = config_bdd.get('utilisateur', '')
        mot_de_passe = os.getenv('DB_PASSWORD', '')  # Obtenir depuis l'environnement
        hôte = config_bdd.get('hôte', 'localhost')
        port = config_bdd.get('port', 5432)
        nom = config_bdd.get('nom', 'myapp')

        if utilisateur and mot_de_passe:
            return f"postgresql://{utilisateur}:{mot_de_passe}@{hôte}:{port}/{nom}"
        else:
            return f"postgresql://{hôte}:{port}/{nom}"

    def est_développement(self) -> bool:
        """Vérifier si l'exécution se fait en environnement de développement"""
        return self.obtenir('application.environnement', 'développement') == 'développement'

    def est_debug_activé(self) -> bool:
        """Vérifier si le mode debug est activé"""
        return self.obtenir('application.debug', False)

    def obtenir_adresse_serveur(self) -> tuple:
        """Obtenir l'hôte et le port du serveur sous forme de tuple"""
        hôte = self.obtenir('serveur.hôte', 'localhost')
        port = self.obtenir('serveur.port', 8000)
        return (hôte, port)

    def afficher_résumé(self):
        """Afficher un résumé de la configuration"""
        print(f"\n=== Résumé de la Configuration ===")
        print(f"Application: {self.obtenir('application.nom')} v{self.obtenir('application.version')}")
        print(f"Environnement: {self.obtenir('application.environnement')}")
        print(f"Debug: {self.obtenir('application.debug')}")
        print(f"Serveur: {self.obtenir('serveur.hôte')}:{self.obtenir('serveur.port')}")
        print(f"Base de données: {self.obtenir('base_de_données.hôte')}:{self.obtenir('base_de_données.port')}")
        print(f"Niveau de log: {self.obtenir('logs.niveau')}")

        if self.obtenir('fonctionnalités'):
            fonctionnalités_activées = [k for k, v in self.obtenir('fonctionnalités', {}).items() if v]
            print(f"Fonctionnalités: {', '.join(fonctionnalités_activées)}")

        print("=" * 30)


# Exemple d'utilisation et de test
def main():
    """Exemple d'utilisation du GestionnaireConfigurationYAML"""

    # Initialiser le gestionnaire de configuration
    config = GestionnaireConfigurationYAML('app_config.yaml')

    # Valider la configuration
    if not config.valider():
        print("Validation de la configuration échouée!")
        return

    # Afficher le résumé de la configuration
    config.afficher_résumé()

    # Accéder aux valeurs de configuration
    print(f"\nAccès à la configuration:")
    print(f"Nom de l'application: {config.obtenir('application.nom')}")
    print(f"Port du serveur: {config.obtenir('serveur.port')}")
    print(f"Hôte de la base de données: {config.obtenir('base_de_données.hôte')}")
    print(f"Debug activé: {config.est_debug_activé()}")
    print(f"Mode développement: {config.est_développement()}")

    # Obtenir l'URL de la base de données
    print(f"URL de la base de données: {config.obtenir_url_base_de_données()}")

    # Accéder à la configuration imbriquée
    niveau_logs = config.obtenir('logs.niveau', 'INFO')
    console_activée = config.obtenir('logs.console.activée', True)
    print(f"Logs: {niveau_logs}, Console: {console_activée}")

    # Accéder aux configurations de liste
    méthodes_autorisées = config.obtenir('serveur.méthodes_autorisées', [])
    print(f"Méthodes HTTP autorisées: {méthodes_autorisées}")

    # Accéder à la liste de dictionnaires
    intégrations = config.obtenir('intégrations', [])
    intégrations_activées = [i['nom'] for i in intégrations if i.get('activé')]
    print(f"Intégrations activées: {intégrations_activées}")

    # Démonstration de la modification de configuration
    print(f"\nModification de la configuration:")
    config.définir('application.debug', False)
    config.définir('serveur.port', 9000)
    print(f"Debug maintenant: {config.obtenir('application.debug')}")
    print(f"Port maintenant: {config.obtenir('serveur.port')}")

    # Sauvegarder la configuration modifiée
    config.sauvegarder('modified_config.yaml')


if __name__ == "__main__":
    main()
```

## Bonnes pratiques pour la configuration YAML

### 1. Structure et organisation

- Regrouper les paramètres liés dans des dictionnaires imbriqués
- Utiliser des noms de clés clairs et descriptifs
- Garder l'imbrication à un niveau raisonnable (2-3 niveaux max)
- Utiliser des conventions de nommage cohérentes (snake_case recommandé)

### 2. Considérations de sécurité

```yaml
# Bon : Référencer les variables d'environnement pour les secrets
base_de_données:
  mot_de_passe_env: "DB_PASSWORD"  # Nom de la variable d'environnement

# Mauvais : Ne jamais stocker les secrets dans les fichiers de configuration
# mot_de_passe: "super_secret_password"  # NE PAS FAIRE ÇA

sécurité:
  clé_secrète_env: "APP_SECRET_KEY"
  jwt_secrétaire_env: "JWT_SECRET"
```

### 3. Documentation et commentaires

```yaml
# Configuration de l'Application
# Dernière mise à jour : 2024-01-15
# Environnement : Production

serveur:
  # Nombre maximum de processus workers
  # Recommandé : 2 * nombre de cœurs CPU
  workers: 4

  # Timeout des requêtes en secondes
  # Augmenter pour les endpoints lents
  timeout: 30
```

### 4. Validation et gestion des erreurs

Toujours valider votre configuration :

```python
def valider_types_config(config):
    """Valider les types de données de la configuration"""
    vérifications_type = [
        ('serveur.port', int, lambda x: 1 <= x <= 65535),
        ('serveur.workers', int, lambda x: x > 0),
        ('base_de_données.max_connexions', int, lambda x: x > 0),
        ('application.debug', bool, None),
    ]

    for chemin, type_attendu, validateur in vérifications_type:
        valeur = config.get(chemin)
        if valeur is not None:
            if not isinstance(valeur, type_attendu):
                raise ValueError(f"{chemin} doit être {type_attendu.__name__}")
            if validateur and not validateur(valeur):
                raise ValueError(f"{chemin} a échoué la validation")
```

## Points clés à retenir

1. **YAML est pour la configuration** : Parfait pour les paramètres d'application, pas pour le stockage de données
   général
2. **Lisible par l'homme** : Conçu pour être modifié par des humains
3. **Inférence de types** : Détecte automatiquement les types de données
4. **Les commentaires comptent** : Documenter vos choix de configuration
5. **Séparation des environnements** : Utiliser différents fichiers pour différents environnements
6. **Sécurité d'abord** : Ne jamais stocker les secrets dans les fichiers de configuration
7. **Validation** : Toujours valider la configuration après chargement
8. **Valeurs par défaut** : Fournir des valeurs par défaut sensées pour les paramètres optionnels

## Erreurs courantes à éviter

- Stocker les mots de passe ou clés API dans les fichiers YAML
- Créer des structures imbriquées trop complexes
- Ne pas valider la configuration des données
- Mélanger la configuration avec les données d'exécution
- Ne pas utiliser les configurations spécifiques à l'environnement
- Oublier de gérer les fichiers de configuration manquants
- Ne pas documenter les options de configuration

YAML offre un excellent support pour la configuration complexe des applications, rendant facile pour les développeurs et
les opérateurs de comprendre et modifier les paramètres d'application tout en maintenant la lisibilité.