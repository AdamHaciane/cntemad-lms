# STORY-038: Page "Mes mentorés"

## Epic parent
EPIC-008: Mentor

## Description
En tant que mentor, je veux voir la liste de mes étudiants assignés.

## Critères d'acceptation spécifiques
- [ ] Liste mentorés avec: nom, année, progression, dernière activité
- [ ] Indicateur alerte si inactif >7j
- [ ] Filtres: année, statut activité
- [ ] Action: voir détail, envoyer message
- [ ] Vue cards ou liste

## Critères standard (OBLIGATOIRES)

### Fonctionnel
- [ ] Comportement attendu implémenté
- [ ] Cas limites gérés (aucun mentoré)
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
- `frontend/src/pages/mentor/MyMentees.vue`
- `frontend/src/router.js`
- `cntemad_lms/api/mentor.py`
- `docs/INDEX.md`

## Commandes de validation
```bash
bench run-tests --app cntemad_lms --module api.mentor
npm run build --prefix frontend
```
