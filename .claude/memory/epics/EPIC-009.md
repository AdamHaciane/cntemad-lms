# EPIC-009: Parent/Tuteur

## Contexte
Suivi des enfants étudiants au CNTEMAD.

## Stories
- [ ] STORY-042: Composant StudentCard
- [ ] STORY-043: Page Dashboard Parent
- [ ] STORY-044: Suivi progression enfant
- [ ] STORY-045: Paiement par parent
- [ ] STORY-046: Notifications parent (SMS/email)

## Critères de succès Epic
- [ ] Parent voit progression de tous ses enfants
- [ ] Parent peut payer pour enfant
- [ ] SMS quand enfant valide EC

## Écrans concernés

| Écran | Composants | API |
|-------|-----------|-----|
| Mes enfants | `ChildList`, `QuickStats` | `get_my_children()` |
| Progression enfant | `ProgressCard`, `ECStatusList`, `AlertBadge` | `get_child_progress()` |
| Paiements | `PaymentHistory`, `PaymentButton` | `get_child_payments()` |

## Dépendances
- Doctypes: LMS Guardian, LMS Student Guardian
- EPIC-002 (Paiement)

## Notes techniques
- Réutiliser Frappe LMS guardian system
- Lien parent-enfant via LMS Student Guardian
- Notifications SMS via provider local
