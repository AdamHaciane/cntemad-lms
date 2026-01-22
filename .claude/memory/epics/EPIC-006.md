# EPIC-006: Admin National

## Contexte
Vue globale des 34 centres et analytics nationales.

## Stories
- [ ] STORY-029: Page Dashboard National (KPIs globaux)
- [ ] STORY-030: Vue carte des 34 centres
- [ ] STORY-031: Comparaison centres
- [ ] STORY-032: Export rapports nationaux

## Critères de succès Epic
- [ ] KPIs agrégés des 34 centres
- [ ] Drill-down par centre
- [ ] Rapport PDF générable

## Écrans concernés

| Écran | Composants | API |
|-------|-----------|-----|
| Dashboard | `NationalKPIs`, `CenterMap`, `AlertsPanel` | `get_national_stats()` |
| Centres | `CenterTable`, `CenterDetail`, `CompareView` | `get_all_centers()` |
| Analytics | `TrendCharts`, `Heatmap`, `ExportAll` | `get_analytics()` |
| Config | `SettingsForm`, `UserManagement`, `SystemHealth` | `update_settings()` |

## Dépendances
- EPIC-004 (Admin Centre)
- Rôle: National Admin

## Notes techniques
- Agrégation données tous centres
- Carte interactive (Leaflet)
- Charts avec Chart.js/ApexCharts
