# STORY-XXX: [Titre]

## Epic parent
EPIC-XXX

## Description
En tant que [rôle], je veux [action] pour [bénéfice]

## Critères d'acceptation spécifiques
- [ ] [Critère 1 propre à cette story]
- [ ] [Critère 2 propre à cette story]
- [ ] [Critère 3 propre à cette story]

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
- `chemin/vers/fichier.py`
- `chemin/vers/composant.vue`

## Commandes de validation
```bash
# Tests
bench run-tests --app cntemad_lms --module [module]

# Build
bench build --app cntemad_lms

# Lint
pre-commit run --all-files

# Migration
bench migrate
```

## Checklist finale Claude
Avant de marquer terminé, Claude DOIT :
1. [ ] Relire TOUS les critères ci-dessus
2. [ ] Exécuter TOUTES les commandes de validation
3. [ ] Vérifier que TOUS les checkboxes sont cochés
4. [ ] Si un seul critère échoue → corriger d'abord
