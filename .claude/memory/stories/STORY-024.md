# STORY-024: Éditeur contenu EC

## Epic parent
EPIC-005: Enseignant & Création Contenu

## Description
En tant qu'enseignant, je veux éditer le contenu d'un EC avec un éditeur visuel.

## Critères d'acceptation spécifiques
- [ ] Éditeur WYSIWYG (TipTap/Frappe UI)
- [ ] Formatage: titres, listes, gras, italique, liens
- [ ] Insertion images depuis upload
- [ ] Preview en temps réel
- [ ] Sauvegarde brouillon automatique

## Critères standard (OBLIGATOIRES)

### Fonctionnel
- [ ] Comportement attendu implémenté
- [ ] Cas limites gérés (contenu très long)
- [ ] Happy path fonctionne

### Technique
- [ ] Frappe UI utilisé (TipTap)
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
- `frontend/src/components/custom/ContentEditor.vue`
- `frontend/src/pages/teacher/ECEditor.vue`
- `docs/INDEX.md`

## Commandes de validation
```bash
npm run build --prefix frontend
pre-commit run --all-files
```
