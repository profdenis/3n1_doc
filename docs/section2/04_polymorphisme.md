# **Polymorphisme : Comparaison Java vs Python**

*Et introduction au "Duck Typing"*

---

## **1. Polymorphisme en Java (Approche Statique)**

En Java, le polymorphisme repose sur :

- **Héritage** (`extends`).
- **Redéfinition de méthodes** (`@Override`).
- **Types explicites** (vérifiés à la compilation).

### **Exemple Java**

```java
class Personne {
    public String saluer() { return "Bonjour!"; }
}

class Etudiant extends Personne {
    @Override
    public String saluer() { return "Salut, je suis étudiant!"; }
}

// Utilisation
Personne p = new Etudiant();
System.out.println(p.saluer());  // "Salut, je suis étudiant!"
```

**Caractéristiques :**

- Le type est vérifié à la **compilation**.
- Nécessite une hiérarchie de classes explicite.

---

## **2. Polymorphisme en Python (Approche Dynamique)**

En Python :

- Pas besoin d'héritage pour le polymorphisme.
- Les méthodes sont redéfinies naturellement.
- Le type est vérifié à l'**exécution** (`duck typing`).

### **Exemple Python**

```python
class Personne:
    def saluer(self):
        return "Bonjour!"


class Etudiant(Personne):  # Héritage optionnel
    def saluer(self):
        return "Salut, je suis étudiant!"


# Utilisation
p = Etudiant()
print(p.saluer())  # "Salut, je suis étudiant!"
```

**Caractéristiques :**

- Fonctionne même **sans héritage** (voir `duck typing`).
- Plus flexible, mais moins strict.

---

## **3. Comparaison Clé**

| Java                            | Python                        |
|---------------------------------|-------------------------------|
| Héritage obligatoire            | Héritage optionnel            |
| Types vérifiés à la compilation | Types vérifiés à l'exécution  |
| `@Override` requis              | Pas de mot-clé pour redéfinir |

---

## **4. Duck Typing : "Si ça marche comme un canard, c'est un canard"**

Version longue : "Si ça ressemble à un canard, si ça nage comme un canard et si ça cancane comme un canard, c'est un 
canard."

En Python, le polymorphisme ne nécessite pas d'héritage :

- Une méthode est appelée si l'objet a cette méthode.
- Le type n'a pas d'importance.

### **Exemple sans Héritage**

```python
class Oiseau:
    def voler(self):
        return "Je vole!"


class Avion:
    def voler(self):  # Même méthode, mais pas de relation d'héritage
        return "L'avion décolle!"


def faire_voler(obj):
    print(obj.voler())  # Polymorphisme sans héritage !


faire_voler(Oiseau())  # "Je vole!"
faire_voler(Avion())  # "L'avion décolle!"
```

**Avantages :**

- **Flexibilité** : Pas besoin de créer une hiérarchie de classes.
- **Code plus simple** pour des cas simples.

---

## **5. Quand Utiliser l'Héritage vs Duck Typing ?**

| Héritage                                               | Duck Typing                                |
|--------------------------------------------------------|--------------------------------------------|
| Relations "est-un" (ex: `Etudiant` est une `Personne`) | Comportements similaires sans lien logique |
| Code plus structuré                                    | Code plus flexible                         |

---

### **Conclusion**

- Java utilise un **polymorphisme statique** (héritage).
- Python permet les deux :
    - Polymorphisme classique (avec héritage).
    - **Duck typing** (plus flexible, sans héritage).

!!! note "📌 **Astuce**"
    En Python, préférez le duck typing pour des interfaces simples, et l'héritage pour des hiérarchies logiques !