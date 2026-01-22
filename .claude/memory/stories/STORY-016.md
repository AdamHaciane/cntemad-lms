# STORY-016: API submit_quiz()

## Epic parent
EPIC-003: Apprentissage & Quiz

## Description
En tant que système, je veux une API pour soumettre les réponses quiz et calculer le score.

## Critères d'acceptation spécifiques
- [ ] Endpoint: POST /api/method/cntemad_lms.api.quiz.submit_quiz
- [ ] Params: ec_id, answers (array)
- [ ] Calcul score automatique
- [ ] Seuil de validation configurable (ex: 70%)
- [ ] Met à jour CNTEMAD Enrollment si réussi
- [ ] Retourne: score, passed, correct_answers

## Critères standard (OBLIGATOIRES)

### Fonctionnel
- [ ] Comportement attendu implémenté
- [ ] Cas limites gérés (quiz déjà passé, triche)
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
- `cntemad_lms/api/quiz.py`
- `cntemad_lms/doctype/cntemad_enrollment/cntemad_enrollment.py`
- `docs/api-reference/quiz.md`

## Commandes de validation
```bash
bench run-tests --app cntemad_lms --module api.quiz
bench migrate
```
