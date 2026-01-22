# EPIC-004: Admin Centre Régional

## Contexte
L'admin d'un centre voit les étudiants et paiements de son centre.

## Stories
- [ ] STORY-018: Composant StatsCard (KPIs)
- [ ] STORY-019: Composant FilterBar
- [ ] STORY-020: Composant ExportButton
- [ ] STORY-021: Page Dashboard Centre
- [ ] STORY-022: Page Liste Étudiants (filtrée)
- [ ] STORY-023: Page Paiements Centre

## Critères de succès Epic
- [ ] KPIs: nb étudiants, nb paiements, montant total
- [ ] Filtre par année, statut, période
- [ ] Export CSV fonctionnel

## Écrans concernés

| Écran | Composants | API |
|-------|-----------|-----|
| Dashboard | `CenterKPIs`, `AlertList`, `QuickActions` | `get_center_stats()` |
| Étudiants | `StudentTable`, `FilterBar`, `ExportButton` | `get_center_students()` |
| Paiements | `PaymentTable`, `ValidationActions`, `RefundButton` | `get_center_payments()` |
| Rapports | `ReportGenerator`, `DateRangePicker`, `ChartView` | `generate_report()` |

## Dépendances
- Doctypes: CNTEMAD Center, CNTEMAD Student, CNTEMAD Payment
- Rôle: Center Admin

## Notes techniques
- Filtrage automatique par center_id de l'admin
- Permissions strictes sur le centre uniquement
- Export CSV avec Frappe
