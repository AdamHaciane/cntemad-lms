# STORY-013: Composant QuizPlayer

## Epic parent
EPIC-003: Apprentissage & Quiz

## Description
En tant qu'étudiant, je veux passer un quiz QCM avec feedback immédiat.

## Critères d'acceptation spécifiques
- [ ] Affiche questions une par une
- [ ] Types: choix unique, choix multiple
- [ ] Timer optionnel par question/quiz
- [ ] Feedback immédiat ou à la fin (configurable)
- [ ] Score final avec détail par question
- [ ] Props: questions, timeLimit, showFeedback

## Critères standard (OBLIGATOIRES)

### Fonctionnel
- [ ] Comportement attendu implémenté
- [ ] Cas limites gérés (0 questions, timeout)
- [ ] Happy path fonctionne

### Technique
- [ ] Frappe UI utilisé (Card, Button, Badge)
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
- `frontend/src/components/custom/QuizPlayer.vue`
- `frontend/src/components/custom/QuestionCard.vue`
- `docs/INDEX.md`

## Commandes de validation
```bash
npm run build --prefix frontend
pre-commit run --all-files
```
