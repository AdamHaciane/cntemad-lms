# Contribuer à CNTEMAD LMS

Merci de votre intérêt pour contribuer au projet CNTEMAD LMS !

## Prérequis

- Frappe Bench installé
- Python 3.10+
- Node.js 18+
- MariaDB 10.6+
- Redis
- Git

## Setup environnement de développement

### 1. Fork et clone

```bash
# Fork le repo sur GitHub, puis :
git clone https://github.com/VOTRE-USERNAME/cntemad-lms.git
cd cntemad-lms
```

### 2. Installation

```bash
# Dans votre bench
bench get-app /chemin/vers/cntemad-lms

# Créer un site de développement
bench new-site dev.local --install-app cntemad_lms

# Activer le mode développeur
bench --site dev.local set-config developer_mode 1

# Lancer
bench start
```

### 3. Installer les hooks pre-commit

```bash
pip install pre-commit
pre-commit install
```

## Workflow de contribution

### 1. Créer une branche

```bash
git checkout -b feature/ma-feature
# ou
git checkout -b fix/mon-bug
```

### 2. Développer

- Suivre les conventions de code (voir ci-dessous)
- Écrire des tests pour les nouvelles fonctionnalités
- Mettre à jour la documentation si nécessaire

### 3. Tester

```bash
# Lancer les tests
bench run-tests --app cntemad_lms

# Lancer le linter
pre-commit run --all-files

# Build
bench build --app cntemad_lms
```

### 4. Commit

Utiliser les [Conventional Commits](https://www.conventionalcommits.org/) :

```bash
git commit -m "feat: ajouter paiement MVola"
git commit -m "fix: corriger calcul progression"
git commit -m "docs: mettre à jour README"
```

Types de commit :
- `feat`: Nouvelle fonctionnalité
- `fix`: Correction de bug
- `docs`: Documentation
- `style`: Formatage (pas de changement de code)
- `refactor`: Refactoring
- `test`: Ajout/modification de tests
- `chore`: Maintenance

### 5. Push et Pull Request

```bash
git push origin feature/ma-feature
```

Puis ouvrir une Pull Request sur GitHub.

## Standards de code

### Python

- Formater avec Black
- Linter avec Flake8
- Docstrings pour les fonctions publiques
- Type hints recommandés

```python
@frappe.whitelist()
def get_student_progress(student_id: str) -> dict:
    """
    Récupère la progression d'un étudiant.

    Args:
        student_id: ID de l'étudiant

    Returns:
        dict: Données de progression
    """
    pass
```

### JavaScript/Vue

- ESLint + Prettier
- Utiliser Frappe UI pour les composants
- Commentaires JSDoc pour les composants

```vue
<!--
  CourseCard.vue
  Affiche une carte de cours.

  Props:
    - course (Object): Données du cours
-->
```

### Frappe

- Naming: `CNTEMAD {Name}` pour les Doctypes
- API prefix: `cntemad_lms.api.`
- Utiliser l'ORM Frappe (pas de SQL brut)

## Labels des issues

| Label | Description |
|-------|-------------|
| `good-first-issue` | Idéal pour débuter |
| `help-wanted` | Besoin d'aide communauté |
| `bug` | Problème confirmé |
| `enhancement` | Amélioration |
| `documentation` | Documentation |
| `question` | Question |

## Process Pull Request

1. Un reviewer assigné automatiquement
2. CI doit passer (lint + tests)
3. Au moins 1 approbation requise
4. Squash and merge sur main

## Communication

- Ouvrir une issue pour discuter des changements majeurs
- Utiliser GitHub Discussions pour les questions générales
- Être respectueux et constructif

## Licence

En contribuant, vous acceptez que votre code soit sous licence GPLv3.

---

Des questions ? Ouvrez une [discussion](https://github.com/cntemad-mg/cntemad-lms/discussions) !
