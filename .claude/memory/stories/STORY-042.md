# STORY-042: Composant StudentCard

## Epic parent
EPIC-009: Parent/Tuteur

## Description
En tant que parent, je veux voir une carte résumé de mon enfant.

## Critères d'acceptation spécifiques
- [ ] Photo profil + nom complet
- [ ] Année en cours (L1, L2, etc.)
- [ ] Progression globale (%)
- [ ] Dernière activité
- [ ] Badge alerte si inactif
- [ ] Props: student, showAlert

## Critères standard (OBLIGATOIRES)

### Fonctionnel
- [ ] Comportement attendu implémenté
- [ ] Cas limites gérés (pas de photo)
- [ ] Happy path fonctionne

### Technique
- [ ] Frappe UI utilisé (Card, Avatar, Badge)
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
- `frontend/src/components/custom/StudentCard.vue`
- `docs/INDEX.md`

## Commandes de validation
```bash
npm run build --prefix frontend
pre-commit run --all-files
```
