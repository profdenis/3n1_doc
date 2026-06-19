# **Les Types Génériques**

---

## **1. Qu’est-ce qu’un type générique ?**

Un **type générique** permet de définir une classe, une méthode ou une interface qui peut fonctionner avec différents
types de données, sans perdre l’information sur ces types.

### **Avantages :**

- **Sécurité des types** : Le compilateur/interpréteur vérifie les types.
- **Réutilisabilité** : Une seule implémentation pour plusieurs types.
- **Lisibilité** : Le code est plus clair (ex: `List<String>` au lieu de `List`).

---

## **2. Exemple en Java**

### **Classe générique simple : `ArrayList`**

```java
import java.util.ArrayList;

public class Main {
    public static void main(String[] args) {
        ArrayList<String> noms = new ArrayList<>();  // Liste de chaînes
        noms.add("Alice");
        noms.add("Bob");

        String premierNom = noms.get(0);  // Type connu : String
        System.out.println(premierNom);  // Affiche "Alice"
    }
}
```

### **Définition d’une classe générique en Java**

```java
public class Boite<T> {  // T est un paramètre de type
    private T contenu;

    public void mettre(T item) {
        this.contenu = item;
    }

    public T obtenir() {
        return this.contenu;
    }
}

// Utilisation :
Boite<String> boiteDeStrings = new Boite<>();
boiteDeStrings.mettre("Hello");
String message = boiteDeStrings.obtenir();  // Type connu : String
```

---

## **3. Types Génériques en Python**

Python utilise des **annotations de type** (PEP 484) pour les types génériques, mais elles sont **optionnelles** et ne
sont pas vérifiées au runtime (sauf avec des outils comme `mypy`).

### **Exemple : Liste générique (`List`)**

```python
from typing import List

noms: List[str] = ["Alice", "Bob"]  # Liste de chaînes
premier_nom: str = noms[0]  # Type connu : str
print(premier_nom)  # Affiche "Alice"
```

### **Définition d’une classe générique en Python**

```python
from typing import TypeVar, Generic

T = TypeVar('T')  # Paramètre de type (comme <T> en Java)


class Boite(Generic[T]):  # Classe générique
    def __init__(self) -> None:
        self.contenu: T | None = None

    def mettre(self, item: T) -> None:
        self.contenu = item

    def obtenir(self) -> T:
        return self.contenu


# Utilisation :
boite_de_strings: Boite[str] = Boite()
boite_de_strings.mettre("Hello")
message: str = boite_de_strings.obtenir()  # Type connu : str
print(message)  # Affiche "Hello"
```

---

## **4. Types Génériques pour les Fonctions**

### **Exemple en Java**

```java
public <T> T premierElement(List<T> liste) {
    return liste.get(0);
}
```

### **Exemple en Python**

```python
from typing import TypeVar, List

T = TypeVar('T')


def premier_element(liste: List[T]) -> T:
    return liste[0]


# Utilisation :
noms: List[str] = ["Alice", "Bob"]
premier_nom: str = premier_element(noms)  # Type connu : str
print(premier_nom)  # Affiche "Alice"
```

---

## **5. Types Génériques avec `dict` et `set`**

### **Exemple en Python**

```python
from typing import Dict, Set

# Dictionnaire générique (clé: str, valeur: int)
ages: Dict[str, int] = {"Alice": 25, "Bob": 30}

# Ensemble générique (éléments: float)
nombres: Set[float] = {1.5, 2.5, 3.5}
```

---

## **6. Bonnes Pratiques**

- ✅ **Utilise `TypeVar` pour les paramètres de type.**
- ✅ **Annote les fonctions et classes avec des types génériques.**
- ✅ **Vérifie le code avec `mypy`** (pour une vérification statique).

---

## **7. Exercice**

### **Consigne**

1. Créez une classe générique `Pile<T>` en Python qui implémente une pile LIFO.
2. Ajoutez des méthodes `empiler(T)` et `depiler() -> T`.
3. Testez avec des entiers et des chaînes.

??? info "Solution"

        ```python
        from typing import TypeVar, Generic, List
        
        T = TypeVar('T')
        
        
        class Pile(Generic[T]):
            def __init__(self) -> None:
                self._elements: List[T] = []
        
            def empiler(self, item: T) -> None:
                self._elements.append(item)
        
            def depiler(self) -> T:
                return self._elements.pop()
        
        
        # Test :
        pile_de_entiers: Pile[int] = Pile()
        pile_de_entiers.empiler(1)
        pile_de_entiers.empiler(2)
        print(pile_de_entiers.depiler())  # Affiche 2
        
        pile_de_strings: Pile[str] = Pile()
        pile_de_strings.empiler("A")
        pile_de_strings.empiler("B")
        print(pile_de_strings.depiler())  # Affiche "B"
        ```

---

## **8. Ressources Supplémentaires**

- [Documentation Python sur `typing`](https://docs.python.org/3/library/typing.html)
- [Tutoriel sur les types génériques](https://realpython.com/python-type-checking/)

---

### **Résumé Final**

| Concept            | Java                     | Python                         |
|--------------------|--------------------------|--------------------------------|
| Classe générique   | `class Boite<T> { ... }` | `class Boite(Generic[T]): ...` |
| Paramètre de type  | `<T>`                    | `TypeVar('T')`                 |
| Annotation de type | `List<String>`           | `List[str]`                    |

**Points clés :**

- Les types génériques améliorent la sécurité et la réutilisabilité.
- En Python, utilisez `typing` pour les annotations (optionnelles mais recommandées).
- Vérifiez le code avec `mypy` pour une meilleure robustesse.

