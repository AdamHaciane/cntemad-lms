# STORY-033: Composant GradeInput

## Epic parent
EPIC-007: Évaluateur

## Description
En tant qu'évaluateur, je veux saisir une note avec un composant dédié.

## Critères d'acceptation spécifiques
- [ ] Saisie numérique avec validation (0-20)
- [ ] Boutons +/- pour ajuster
- [ ] Affichage mention automatique
- [ ] Props: value, min, max, step
- [ ] Événement @change

## Critères standard (OBLIGATOIRES)

### Fonctionnel
- [ ] Comportement attendu implémenté
- [ ] Cas limites gérés (hors limites)
- [ ] Happy path fonctionne

### Technique
- [ ] Frappe UI utilisé (Input)
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
- `frontend/src/components/custom/GradeInput.vue`
- `docs/INDEX.md`

## Commandes de validation
```bash
npm run build --prefix frontend
pre-commit run --all-files
```
