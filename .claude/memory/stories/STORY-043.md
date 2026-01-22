# STORY-043: Page Dashboard Parent

## Epic parent
EPIC-009: Parent/Tuteur

## Description
En tant que parent, je veux voir un dashboard avec tous mes enfants.

## Critères d'acceptation spécifiques
- [ ] Liste enfants avec StudentCard
- [ ] KPIs globaux (total EC validés, paiements)
- [ ] Alertes enfants inactifs
- [ ] Accès rapide paiement
- [ ] Notifications récentes

## Critères standard (OBLIGATOIRES)

### Fonctionnel
- [ ] Comportement attendu implémenté
- [ ] Cas limites gérés (aucun enfant lié)
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
- `frontend/src/pages/parent/ParentDashboard.vue`
- `frontend/src/router.js`
- `cntemad_lms/api/guardian.py`
- `docs/INDEX.md`

## Commandes de validation
```bash
bench run-tests --app cntemad_lms --module api.guardian
npm run build --prefix frontend
```
