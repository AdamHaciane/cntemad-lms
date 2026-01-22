# STORY-004: Page Dashboard étudiant

## Epic parent
EPIC-001: Dashboard Étudiant

## Description
En tant qu'étudiant, je veux voir ma page d'accueil personnalisée avec ma progression et mes EC.

## Critères d'acceptation spécifiques
- [ ] Section progression globale (ProgressBar)
- [ ] Liste EC en cours (ECCard)
- [ ] Historique paiements récents
- [ ] Accès rapide au catalogue
- [ ] Responsive: stack vertical mobile, grille desktop

## Critères standard (OBLIGATOIRES)

### Fonctionnel
- [ ] Comportement attendu implémenté
- [ ] Cas limites gérés (nouvel étudiant sans EC)
- [ ] Happy path fonctionne

### Technique
- [ ] Frappe UI utilisé (Card, Badge, Button)
- [ ] Code propre, pas de debug
- [ ] Pas de credentials en dur

### Tests
- [ ] Tests unitaires écrits
- [ ] `bench run-tests` passe
- [ ] Test manuel OK
- [ ] Mobile responsive vérifié (iPhone SE, iPad)

### Intégration
- [ ] `bench build` passe
- [ ] `bench migrate` passe
- [ ] Pas de régression

### Documentation
- [ ] INDEX.md mis à jour

## Fichiers impactés
- `frontend/src/pages/Dashboard.vue`
- `frontend/src/router.js`
- `docs/INDEX.md`

## Commandes de validation
```bash
npm run build --prefix frontend
pre-commit run --all-files
```
