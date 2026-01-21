# Décisions Architecture

> Chaque décision importante documentée ici.

## 2025-01: Choix licence
**Contexte**: Besoin licence open source compatible Frappe
**Décision**: GPLv3
**Raison**: Compatibilité avec Frappe Framework (MIT) et LMS
**Conséquence**: Contributions doivent rester open source

## 2025-01: Architecture LMS
**Contexte**: Choix entre Frappe Education et LMS custom
**Décision**: Frappe LMS + extensions custom (pas Frappe Education)
**Raison**: Modèle EC/validation progressive spécifique à CNTEMAD
**Conséquence**: Admin construit sur mesure dans cntemad_lms

## 2025-01: Paiements mobile
**Contexte**: Besoin paiement mobile Madagascar
**Décision**: MVola + Orange Money + Airtel Money
**Raison**: Couverture maximale du territoire malgache
**Conséquence**: 3 intégrations API à maintenir

## 2025-01: Stratégie responsive
**Contexte**: Majorité étudiants sur mobile (3G/4G)
**Décision**: Mobile-first design
**Raison**: Optimiser pour le cas d'usage principal
**Conséquence**: Desktop = amélioration progressive

## 2025-01: Multi-langues
**Contexte**: Public diversifié Madagascar
**Décision**: Français (défaut) + Malgache + Anglais
**Raison**: Accessibilité maximale
**Conséquence**: Système i18n Frappe à configurer
