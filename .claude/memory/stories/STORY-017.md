# STORY-017: Logique progression EC

## Epic parent
EPIC-003: Apprentissage & Quiz

## Description
En tant que système, je veux tracker la progression d'un étudiant dans un EC.

## Critères d'acceptation spécifiques
- [ ] États EC: not_started → in_progress → completed → validated
- [ ] Tracking par leçon consultée
- [ ] Quiz réussi → EC validated
- [ ] Calcul progression année (% EC validés)
- [ ] API get_student_progress() retourne données complètes

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
- `cntemad_lms/doctype/cntemad_enrollment/cntemad_enrollment.py`
- `cntemad_lms/api/student.py`
- `docs/INDEX.md`

## Commandes de validation
```bash
bench run-tests --app cntemad_lms
bench migrate
```
