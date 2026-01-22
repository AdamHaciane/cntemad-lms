# STORY-012: Composant LessonViewer

## Epic parent
EPIC-003: Apprentissage & Quiz

## Description
En tant qu'étudiant, je veux visualiser le contenu d'une leçon (texte, PDF, vidéo).

## Critères d'acceptation spécifiques
- [ ] Supporte: Markdown/HTML, PDF embed, YouTube/vidéo
- [ ] Détection automatique du type de contenu
- [ ] Mode plein écran disponible
- [ ] Navigation précédent/suivant
- [ ] Props: content, type, navigation

## Critères standard (OBLIGATOIRES)

### Fonctionnel
- [ ] Comportement attendu implémenté
- [ ] Cas limites gérés (contenu vide, format inconnu)
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
- `frontend/src/components/custom/LessonViewer.vue`
- `frontend/src/components/custom/PDFViewer.vue`
- `frontend/src/components/custom/VideoPlayer.vue`
- `docs/INDEX.md`

## Commandes de validation
```bash
npm run build --prefix frontend
pre-commit run --all-files
```
