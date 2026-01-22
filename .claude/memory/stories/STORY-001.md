# STORY-001: Composant ProgressBar

## Epic parent
EPIC-001: Dashboard Étudiant

## Description
En tant qu'étudiant, je veux voir ma progression sous forme de barre visuelle pour comprendre mon avancement dans l'année.

## Critères d'acceptation spécifiques
- [ ] Barre de progression avec pourcentage
- [ ] Couleurs distinctes: vert (validé), jaune (en cours), gris (non commencé)
- [ ] Animation au chargement
- [ ] Affichage label (ex: "8/12 EC validés")
- [ ] Props: value, max, label, showPercent

## Critères standard (OBLIGATOIRES)

### Fonctionnel
- [ ] Comportement attendu implémenté
- [ ] Cas limites gérés (0%, 100%, valeurs négatives)
- [ ] Happy path fonctionne

### Technique
- [ ] Frappe UI utilisé (base styles)
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
- `frontend/src/components/custom/ProgressBar.vue`
- `docs/INDEX.md`

## Commandes de validation
```bash
# Tests
npm run test --prefix frontend

# Build
npm run build --prefix frontend

# Lint
pre-commit run --all-files
```
