# STORY-039: Vue progression détaillée mentoré

## Epic parent
EPIC-008: Mentor

## Description
En tant que mentor, je veux voir la progression détaillée d'un mentoré.

## Critères d'acceptation spécifiques
- [ ] Profil étudiant complet
- [ ] Timeline activités récentes
- [ ] Progression par EC (statut, score quiz)
- [ ] Historique paiements
- [ ] Bouton envoyer message

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
- `frontend/src/pages/mentor/MenteeDetail.vue`
- `frontend/src/router.js`
- `cntemad_lms/api/mentor.py`
- `docs/INDEX.md`

## Commandes de validation
```bash
bench run-tests --app cntemad_lms --module api.mentor
npm run build --prefix frontend
```
