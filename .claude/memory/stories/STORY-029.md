# STORY-029: Dashboard National

## Epic parent
EPIC-006: Admin National

## Description
En tant qu'admin national, je veux voir les KPIs globaux des 34 centres.

## Critères d'acceptation spécifiques
- [ ] KPIs: total étudiants, total paiements, revenus
- [ ] Comparaison avec période précédente
- [ ] Top 5 centres par inscriptions
- [ ] Alertes système (centres en retard)
- [ ] Graphiques tendances

## Critères standard (OBLIGATOIRES)

### Fonctionnel
- [ ] Comportement attendu implémenté
- [ ] Cas limites gérés
- [ ] Happy path fonctionne

### Technique
- [ ] Frappe UI utilisé
- [ ] Code propre, pas de debug
- [ ] Pas de credentials en dur

### Tests
- [ ] Tests unitaires écrits
- [ ] `bench run-tests` passe
- [ ] Test manuel OK
- [ ] Mobile responsive vérifié

### Intégration
- [ ] `bench build` passe
- [ ] `bench migrate` passe
- [ ] Pas de régression

### Documentation
- [ ] INDEX.md mis à jour

## Fichiers impactés
- `frontend/src/pages/admin/NationalDashboard.vue`
- `frontend/src/router.js`
- `cntemad_lms/api/national.py`
- `docs/INDEX.md`

## Commandes de validation
```bash
bench run-tests --app cntemad_lms --module api.national
npm run build --prefix frontend
```
