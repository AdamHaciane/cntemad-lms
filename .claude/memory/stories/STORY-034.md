# STORY-034: Composant FeedbackEditor

## Epic parent
EPIC-007: Évaluateur

## Description
En tant qu'évaluateur, je veux rédiger un feedback structuré pour l'étudiant.

## Critères d'acceptation spécifiques
- [ ] Éditeur texte simple avec formatage basique
- [ ] Templates de feedback prédéfinis
- [ ] Compteur de caractères
- [ ] Props: value, maxLength, templates
- [ ] Événement @change

## Critères standard (OBLIGATOIRES)

### Fonctionnel
- [ ] Comportement attendu implémenté
- [ ] Cas limites gérés (texte trop long)
- [ ] Happy path fonctionne

### Technique
- [ ] Frappe UI utilisé (Textarea)
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
- `frontend/src/components/custom/FeedbackEditor.vue`
- `docs/INDEX.md`

## Commandes de validation
```bash
npm run build --prefix frontend
pre-commit run --all-files
```
