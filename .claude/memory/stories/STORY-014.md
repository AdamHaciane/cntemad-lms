# STORY-014: Page détail EC

## Epic parent
EPIC-003: Apprentissage & Quiz

## Description
En tant qu'étudiant, je veux voir le détail d'un EC avec son contenu et quiz.

## Critères d'acceptation spécifiques
- [ ] Infos EC: titre, description, cours parent
- [ ] Liste des leçons avec progression
- [ ] Accès au contenu si EC payé
- [ ] Bouton quiz si contenu complété
- [ ] Message "Payer pour accéder" si non payé

## Critères standard (OBLIGATOIRES)

### Fonctionnel
- [ ] Comportement attendu implémenté
- [ ] Cas limites gérés (EC non payé, pas de contenu)
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
- `frontend/src/pages/ECDetail.vue`
- `frontend/src/router.js`
- `cntemad_lms/api/ec.py`
- `docs/INDEX.md`

## Commandes de validation
```bash
bench run-tests --app cntemad_lms --module api.ec
npm run build --prefix frontend
```
