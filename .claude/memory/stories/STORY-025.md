# STORY-025: Upload média

## Epic parent
EPIC-005: Enseignant & Création Contenu

## Description
En tant qu'enseignant, je veux uploader des fichiers PDF et vidéos pour mes EC.

## Critères d'acceptation spécifiques
- [ ] Types supportés: PDF, MP4, WebM, images
- [ ] Limite taille configurable (ex: 100MB)
- [ ] Barre progression upload
- [ ] Preview après upload
- [ ] Gestion erreurs (format, taille)

## Critères standard (OBLIGATOIRES)

### Fonctionnel
- [ ] Comportement attendu implémenté
- [ ] Cas limites gérés (fichier trop gros)
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
- `frontend/src/components/custom/MediaUpload.vue`
- `cntemad_lms/api/upload.py`
- `docs/INDEX.md`

## Commandes de validation
```bash
bench run-tests --app cntemad_lms
npm run build --prefix frontend
```
