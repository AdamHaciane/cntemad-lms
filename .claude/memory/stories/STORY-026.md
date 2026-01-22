# STORY-026: Quiz Builder

## Epic parent
EPIC-005: Enseignant & Création Contenu

## Description
En tant qu'enseignant, je veux créer des quiz QCM pour mes EC.

## Critères d'acceptation spécifiques
- [ ] Ajouter/supprimer questions
- [ ] Types: choix unique, choix multiple
- [ ] Définir bonne(s) réponse(s)
- [ ] Points par question
- [ ] Seuil de réussite configurable
- [ ] Preview quiz

## Critères standard (OBLIGATOIRES)

### Fonctionnel
- [ ] Comportement attendu implémenté
- [ ] Cas limites gérés (0 questions)
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
- `frontend/src/components/custom/QuizBuilder.vue`
- `frontend/src/pages/teacher/ECEditor.vue`
- `cntemad_lms/api/quiz.py`
- `docs/INDEX.md`

## Commandes de validation
```bash
bench run-tests --app cntemad_lms --module api.quiz
npm run build --prefix frontend
```
