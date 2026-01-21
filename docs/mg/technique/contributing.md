# Mandray anjara

Torolalana handray anjara amin'ny tetikasa CNTEMAD LMS.

## Nahoana no mandray anjara?

Ny CNTEMAD LMS dia tetikasa open source mikendry ny hanatsara ny fanabeazana ao Madagasikara. Ny fandraisanao anjara dia manampy:

- **17 000 mpianatra** hiditra amin'ny fanabeazana
- **34 foibe isam-paritra** hiasa tsara kokoa
- Ny **fiovana nomerika** ny fampianarana malagasy

::: tip Ho an'ny mpianatra CNTEMAD
Ny fandraisana anjara amin'ny tetikasa dia azo omena lanja amin'ny lalanao ara-pianarana. Mifandraisa amin'ny foibe-nao hahazoana fampahalalana fanampiny.
:::

## Zavatra ilaina

### Tontolo

- Python 3.10+
- Node.js 18+
- MariaDB 10.6+
- Redis
- Git

### Fitaovana voatolotra

- VS Code miaraka amin'ny extensions Python sy Vue
- Docker (azo atao, ho an'ny tontolo mitokana)

## Fametrahana eo an-toerana

### 1. Mametraka Frappe Bench

```bash
# Mametraka ny dependencies système (Ubuntu/Debian)
sudo apt-get install git python3-dev python3-pip \
    redis-server mariadb-server mariadb-client \
    libmysqlclient-dev

# Mametraka bench
pip3 install frappe-bench

# Mamorona bench vaovao
bench init frappe-bench --frappe-branch version-15
cd frappe-bench
```

### 2. Manadika ny tetikasa

```bash
# Fork ny repo ao amin'ny GitHub, avy eo:
bench get-app https://github.com/ANARANAO/cntemad-lms

# Na mivantana avy amin'ny repo lehibe (famakiana ihany):
bench get-app https://github.com/cntemad-mg/cntemad-lms
```

### 3. Mamorona site fampandrosoana

```bash
bench new-site dev.cntemad.local --mariadb-root-password root
bench --site dev.cntemad.local install-app cntemad_lms
bench --site dev.cntemad.local add-to-hosts
```

### 4. Mandefa ny serveur

```bash
bench start
```

Midira amin'ny `http://dev.cntemad.local:8000`

## Workflow fandraisana anjara

### 1. Mitady issue

Jereo ny [Issues GitHub](https://github.com/cntemad-mg/cntemad-lms/issues):

| Label | Famaritana |
|-------|------------|
| `good-first-issue` | Tsara ho an'ny manomboka |
| `help-wanted` | Mila fanampiana ny ekipa |
| `bug` | Fanitsiana bug |
| `enhancement` | Feature vaovao |
| `documentation` | Fanatsarana doc |

### 2. Mamorona branche

```bash
# Manavao main
git checkout main
git pull origin main

# Mamorona branche feature
git checkout -b feature/ma-nouvelle-feature

# Na ho an'ny bugfix
git checkout -b fix/description-du-bug
```

### 3. Mampandroso

Araho ny conventions code (jereo etsy ambany).

### 4. Mitsapa

```bash
# Tests Python
bench run-tests --app cntemad_lms

# Lint Python
pre-commit run --all-files

# Build frontend
cd apps/cntemad_lms/frontend
npm run build
```

### 5. Commit

Ampiasao ny [Conventional Commits](https://www.conventionalcommits.org/):

```bash
# Format
<type>(<scope>): <description>

# Ohatra
feat(student): add progress tracking widget
fix(payment): handle MVola timeout error
docs(api): update endpoint documentation
```

Types ekena: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

### 6. Mamorona Pull Request

1. Push ny branche-nao
   ```bash
   git push origin feature/ma-nouvelle-feature
   ```

2. Sokafy PR ao amin'ny GitHub

3. Fenoy ny template:
   ```markdown
   ## Famaritana
   [Lazao ny fanovana nataonao]

   ## Karazana fanovana
   - [ ] Bug fix
   - [ ] Feature vaovao
   - [ ] Breaking change
   - [ ] Documentation

   ## Checklist
   - [ ] Ny code-ko dia manaraka ny conventions
   - [ ] Nanampy tests aho
   - [ ] Nanova ny documentation aho
   - [ ] Ny tests dia mandeha eo an-toerana
   ```

4. Andraso ny review

## Conventions code

### Python

```python
# Manaraka PEP 8
# Docstrings ho an'ny fonctions publiques
# Type hints voatolotra

def get_student_progress(student_id: str) -> dict:
    """
    Mahazo ny fandrosoan'ny mpianatra.

    Args:
        student_id: ID ny mpianatra

    Returns:
        dict misy total_ec, validated_ec, progress_percent
    """
    pass
```

### Vue.js

```vue
<script setup>
// Composition API tsara kokoa
// Frappe UI ho an'ny composants UI rehetra
import { Button, Card } from 'frappe-ui'
</script>

<template>
  <!-- Classes Tailwind ho an'ny style -->
  <Card class="p-4">
    <Button variant="solid">Hetsika</Button>
  </Card>
</template>
```

### Frappe UI tsy maintsy

**Ampiasao Frappe UI foana** ho an'ny composants frontend:

```vue
<!-- ✅ Marina -->
<Button variant="solid" @click="save">Tehirizo</Button>

<!-- ❌ Diso -->
<button class="btn btn-primary" @click="save">Tehirizo</button>
```

## Tests

### Tests unitaires Python

```python
# tests/test_student.py
import frappe
import unittest

class TestStudent(unittest.TestCase):
    def setUp(self):
        # Mamorona data fitsapana
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
        # Manadio
        pass
```

### Mandefa ny tests

```bash
# Tests rehetra
bench run-tests --app cntemad_lms

# Module manokana
bench run-tests --app cntemad_lms --module student

# Miaraka amin'ny coverage
bench run-tests --app cntemad_lms --coverage
```

## Mila fanampiana?

- **Discord** : [Miditra amin'ny serveur](https://discord.gg/cntemad)
- **Issues** : [GitHub Issues](https://github.com/cntemad-mg/cntemad-lms/issues)
- **Mailaka** : dev@cntemad.mg

---

Misaotra mandray anjara amin'ny CNTEMAD LMS! 🇲🇬
