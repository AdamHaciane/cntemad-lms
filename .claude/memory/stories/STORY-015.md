# STORY-015: Page Quiz

## Epic parent
EPIC-003: Apprentissage & Quiz

## Description
En tant qu'étudiant, je veux une page dédiée pour passer le quiz de validation d'un EC.

## Critères d'acceptation spécifiques
- [ ] Intro avec règles et temps limite
- [ ] QuizPlayer avec toutes les questions
- [ ] Pas de retour arrière une fois commencé
- [ ] Résultat final avec score
- [ ] Bouton "Retour à l'EC" ou "Reprendre"

## Critères standard (OBLIGATOIRES)

### Fonctionnel
- [ ] Comportement attendu implémenté
- [ ] Cas limites gérés (déconnexion pendant quiz)
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
- `frontend/src/pages/Quiz.vue`
- `frontend/src/router.js`
- `docs/INDEX.md`

## Commandes de validation
```bash
npm run build --prefix frontend
pre-commit run --all-files
```
