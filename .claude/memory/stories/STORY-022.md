# STORY-022: Page Liste Étudiants Centre

## Epic parent
EPIC-004: Admin Centre Régional

## Description
En tant qu'admin centre, je veux voir et gérer les étudiants de mon centre.

## Critères d'acceptation spécifiques
- [ ] Table avec: nom, email, année, statut, date inscription
- [ ] Filtres: année, statut, recherche
- [ ] Actions: voir détail, suspendre, exporter
- [ ] Pagination
- [ ] Export CSV

## Critères standard (OBLIGATOIRES)

### Fonctionnel
- [ ] Comportement attendu implémenté
- [ ] Cas limites gérés (aucun étudiant)
- [ ] Happy path fonctionne

### Technique
- [ ] Frappe UI utilisé (Table)
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
- `frontend/src/pages/admin/CenterStudents.vue`
- `frontend/src/router.js`
- `cntemad_lms/api/center.py`
- `docs/INDEX.md`

## Commandes de validation
```bash
bench run-tests --app cntemad_lms --module api.center
npm run build --prefix frontend
```
