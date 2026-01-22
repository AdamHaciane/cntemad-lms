# STORY-003: Composable useStudent()

## Epic parent
EPIC-001: Dashboard Étudiant

## Description
En tant que développeur, je veux un composable qui gère les données étudiant pour éviter la duplication de code.

## Critères d'acceptation spécifiques
- [ ] Expose: student (reactive), loading, error
- [ ] Méthode: fetchStudent(), refreshProgress()
- [ ] Cache les données (évite appels répétés)
- [ ] Gère erreurs avec messages clairs
- [ ] Utilise $resources pattern Frappe UI

## Critères standard (OBLIGATOIRES)

### Fonctionnel
- [ ] Comportement attendu implémenté
- [ ] Cas limites gérés (non connecté, erreur réseau)
- [ ] Happy path fonctionne

### Technique
- [ ] Frappe UI utilisé ($resources)
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
- `frontend/src/composables/useStudent.js`
- `cntemad_lms/api/student.py`
- `docs/INDEX.md`

## Commandes de validation
```bash
bench run-tests --app cntemad_lms --module api.student
npm run build --prefix frontend
```
