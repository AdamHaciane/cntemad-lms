# STORY-027: Page "Mes Cours"

## Epic parent
EPIC-005: Enseignant & Création Contenu

## Description
En tant qu'enseignant, je veux voir la liste de mes cours et EC.

## Critères d'acceptation spécifiques
- [ ] Liste cours avec nb EC, nb étudiants
- [ ] Filtres: année, statut (brouillon/publié)
- [ ] Actions: éditer, voir stats, créer EC
- [ ] Bouton créer nouveau cours
- [ ] Vue cards ou liste

## Critères standard (OBLIGATOIRES)

### Fonctionnel
- [ ] Comportement attendu implémenté
- [ ] Cas limites gérés (aucun cours)
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
- `frontend/src/pages/teacher/MyCourses.vue`
- `frontend/src/router.js`
- `cntemad_lms/api/course.py`
- `docs/INDEX.md`

## Commandes de validation
```bash
bench run-tests --app cntemad_lms --module api.course
npm run build --prefix frontend
```
