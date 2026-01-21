# CNTEMAD LMS

> Plateforme d'apprentissage en ligne du Centre National de Télé-Enseignement de Madagascar

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![CI](https://github.com/cntemad-mg/cntemad-lms/workflows/CI/badge.svg)](https://github.com/cntemad-mg/cntemad-lms/actions)
[![Contributors](https://img.shields.io/github/contributors/cntemad-mg/cntemad-lms)](https://github.com/cntemad-mg/cntemad-lms/graphs/contributors)

## À propos

Le **CNTEMAD** est le pionnier de l'enseignement à distance en Afrique depuis 1992.
Avec 34 centres régionaux et 17 000 étudiants annuels, nous devenons la première
université numérique de Madagascar.

Ce projet open source vise à moderniser notre plateforme LMS avec la participation
de notre communauté d'étudiants et développeurs.

## Fonctionnalités

- Gestion des cours, chapitres et leçons
- Système d'Éléments Constitutifs (EC) pour validation progressive
- Évaluations et quiz avec scoring automatique
- Certifications automatiques
- Suivi de progression détaillé
- Paiements locaux (MVola, Orange Money, Airtel Money)
- Multi-langues (Français, Malgache, Anglais)
- Interface responsive mobile-first (Frappe UI)

## Stack technique

- **Backend**: Frappe Framework 15+
- **Frontend**: Vue 3 + Frappe UI + TailwindCSS
- **Database**: MariaDB
- **Cache**: Redis

## Installation

### Prérequis
- Frappe Bench installé ([guide d'installation](https://frappeframework.com/docs/user/en/installation))
- Python 3.10+
- Node.js 18+
- MariaDB 10.6+
- Redis

### Installation rapide

```bash
# Récupérer l'app
bench get-app https://github.com/cntemad-mg/cntemad-lms

# Créer un nouveau site (ou utiliser un existant)
bench new-site lms.local --install-app cntemad_lms

# Ou installer sur un site existant
bench --site votre-site install-app cntemad_lms

# Lancer le serveur de développement
bench start
```

### Configuration

```bash
# Configurer le site
bench --site lms.local set-config developer_mode 1

# Migrer la base de données
bench --site lms.local migrate

# Build les assets
bench build --app cntemad_lms
```

## Développement

```bash
# Lancer les tests
bench run-tests --app cntemad_lms

# Lancer le linter
pre-commit run --all-files

# Build frontend
cd apps/cntemad_lms/frontend && npm run dev
```

## Contribution

Nous accueillons les contributions ! Voir [CONTRIBUTING.md](CONTRIBUTING.md)

Les étudiants CNTEMAD peuvent contribuer et gagner des crédits académiques.

### Premiers pas
1. Fork le repo
2. Créer une branche (`git checkout -b feature/ma-feature`)
3. Commit (`git commit -m "feat: description"`)
4. Push (`git push origin feature/ma-feature`)
5. Ouvrir une Pull Request

## Documentation

- [Guide d'installation](docs/getting-started.md)
- [Architecture](docs/architecture/)
- [API Reference](docs/api-reference/)
- [Guide de contribution](docs/contributing/)

## Équipe

- **Core Team**: CNTEMAD + SAYNA
- **Contributeurs**: [Voir la liste](https://github.com/cntemad-mg/cntemad-lms/graphs/contributors)

## Support

- Issues: [GitHub Issues](https://github.com/cntemad-mg/cntemad-lms/issues)
- Discussions: [GitHub Discussions](https://github.com/cntemad-mg/cntemad-lms/discussions)

## Licence

GPLv3 - Voir [LICENSE](LICENSE)

---

Fait avec passion à Madagascar
