# Contribuer

Guide pour contribuer au projet CNTEMAD LMS.

## Pourquoi contribuer ?

Le CNTEMAD LMS est un projet open source qui vise à moderniser l'éducation à Madagascar. Vos contributions aident :

- **17 000 étudiants** à accéder à l'éducation
- **34 centres régionaux** à mieux fonctionner
- La **transformation numérique** de l'enseignement malgache

::: tip Pour les étudiants CNTEMAD
Les contributions au projet peuvent être valorisées dans votre parcours académique. Contactez votre centre pour plus d'informations.
:::

## Prérequis

### Environnement

- Python 3.10+
- Node.js 18+
- MariaDB 10.6+
- Redis
- Git

### Outils recommandés

- VS Code avec extensions Python et Vue
- Docker (optionnel, pour environnement isolé)

## Installation locale

### 1. Installer Frappe Bench

```bash
# Installer les dépendances système (Ubuntu/Debian)
sudo apt-get install git python3-dev python3-pip \
    redis-server mariadb-server mariadb-client \
    libmysqlclient-dev

# Installer bench
pip3 install frappe-bench

# Créer un nouveau bench
bench init frappe-bench --frappe-branch version-15
cd frappe-bench
```

### 2. Cloner le projet

```bash
# Fork le repo sur GitHub, puis :
bench get-app https://github.com/VOTRE-USERNAME/cntemad-lms

# Ou directement depuis le repo principal (lecture seule) :
bench get-app https://github.com/cntemad-mg/cntemad-lms
```

### 3. Créer un site de développement

```bash
bench new-site dev.cntemad.local --mariadb-root-password root
bench --site dev.cntemad.local install-app cntemad_lms
bench --site dev.cntemad.local add-to-hosts
```

### 4. Lancer le serveur

```bash
bench start
```

Accédez à `http://dev.cntemad.local:8000`

## Workflow de contribution

### 1. Trouver une issue

Parcourez les [Issues GitHub](https://github.com/cntemad-mg/cntemad-lms/issues) :

| Label | Description |
|-------|-------------|
| `good-first-issue` | Idéal pour débuter |
| `help-wanted` | L'équipe a besoin d'aide |
| `bug` | Correction de bug |
| `enhancement` | Nouvelle fonctionnalité |
| `documentation` | Amélioration de la doc |

### 2. Créer une branche

```bash
# Mettre à jour main
git checkout main
git pull origin main

# Créer une branche feature
git checkout -b feature/ma-nouvelle-feature

# Ou pour un bugfix
git checkout -b fix/description-du-bug
```

### 3. Développer

Suivez les conventions de code (voir ci-dessous).

### 4. Tester

```bash
# Tests Python
bench run-tests --app cntemad_lms

# Lint Python
pre-commit run --all-files

# Build frontend
cd apps/cntemad_lms/frontend
npm run build
```

### 5. Commiter

Utilisez les [Conventional Commits](https://www.conventionalcommits.org/) :

```bash
# Format
<type>(<scope>): <description>

# Exemples
feat(student): add progress tracking widget
fix(payment): handle MVola timeout error
docs(api): update endpoint documentation
refactor(course): simplify EC validation logic
test(payment): add unit tests for callback
```

Types autorisés : `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

### 6. Créer une Pull Request

1. Push votre branche
   ```bash
   git push origin feature/ma-nouvelle-feature
   ```

2. Ouvrez une PR sur GitHub

3. Remplissez le template :
   ```markdown
   ## Description
   [Décrivez vos changements]

   ## Type de changement
   - [ ] Bug fix
   - [ ] Nouvelle fonctionnalité
   - [ ] Breaking change
   - [ ] Documentation

   ## Checklist
   - [ ] Mon code suit les conventions du projet
   - [ ] J'ai ajouté des tests
   - [ ] J'ai mis à jour la documentation
   - [ ] Les tests passent localement
   ```

4. Attendez la review

## Conventions de code

### Python

```python
# Suivre PEP 8
# Docstrings pour fonctions publiques
# Type hints recommandés

def get_student_progress(student_id: str) -> dict:
    """
    Récupère la progression d'un étudiant.

    Args:
        student_id: ID de l'étudiant

    Returns:
        dict avec total_ec, validated_ec, progress_percent
    """
    # Implementation
    pass
```

### Vue.js

```vue
<script setup>
// Composition API préféré
// Frappe UI pour tous les composants UI
import { Button, Card } from 'frappe-ui'
</script>

<template>
  <!-- Classes Tailwind pour le style -->
  <Card class="p-4">
    <Button variant="solid">Action</Button>
  </Card>
</template>
```

### Frappe UI obligatoire

**Toujours utiliser Frappe UI** pour les composants frontend :

```vue
<!-- ✅ Correct -->
<Button variant="solid" @click="save">Sauvegarder</Button>

<!-- ❌ Incorrect -->
<button class="btn btn-primary" @click="save">Sauvegarder</button>
```

Composants disponibles : Button, Input, Select, Card, Dialog, Table, Badge, Avatar, etc.

## Structure du projet

```
cntemad_lms/
├── cntemad_lms/
│   ├── doctype/           # Modèles de données
│   │   └── cntemad_*/     # Un dossier par doctype
│   ├── api/               # Endpoints REST
│   │   ├── student.py
│   │   ├── course.py
│   │   └── payment.py
│   ├── overrides/         # Extensions Frappe LMS
│   └── hooks.py           # Configuration app
├── frontend/              # Vue 3 + Frappe UI
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── composables/
│   └── vite.config.js
└── tests/                 # Tests
```

## Tests

### Tests unitaires Python

```python
# tests/test_student.py
import frappe
import unittest

class TestStudent(unittest.TestCase):
    def setUp(self):
        # Créer données de test
        pass

    def test_student_creation(self):
        student = frappe.get_doc({
            "doctype": "CNTEMAD Student",
            "student_name": "Test Student",
            "email": "test@example.com"
        })
        student.insert()
        self.assertEqual(student.status, "active")

    def tearDown(self):
        # Nettoyer
        pass
```

### Exécuter les tests

```bash
# Tous les tests
bench run-tests --app cntemad_lms

# Un module spécifique
bench run-tests --app cntemad_lms --module student

# Avec couverture
bench run-tests --app cntemad_lms --coverage
```

## Documentation

### Ajouter de la documentation

1. Éditez les fichiers dans `docs/`
2. Suivez le format VitePress
3. Testez localement :
   ```bash
   cd docs
   npm run docs:dev
   ```

### Documenter une API

Ajoutez dans `docs/fr/technique/api.md` :

```markdown
### Nouvel endpoint

\`\`\`bash
GET /api/method/cntemad_lms.api.module.function
\`\`\`

Paramètres :
| Param | Type | Description |
|-------|------|-------------|
| `param1` | string | Description |

Réponse :
\`\`\`json
{
  "message": { ... }
}
\`\`\`
```

## Besoin d'aide ?

- **Discord** : [Rejoindre le serveur](https://discord.gg/cntemad)
- **Issues** : [GitHub Issues](https://github.com/cntemad-mg/cntemad-lms/issues)
- **Email** : dev@cntemad.mg

---

Merci de contribuer au CNTEMAD LMS ! 🇲🇬
