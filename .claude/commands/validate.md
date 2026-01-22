# Validation qualité complète

Exécute tous les checks de qualité avant PR ou merge.

## Étapes

1. **Lint (pre-commit)**
   ```bash
   pre-commit run --all-files
   ```
   Vérifie: trailing whitespace, YAML/JSON valide, Black, isort, flake8, ESLint

2. **Tests unitaires**
   ```bash
   bench --site lms.local run-tests --app cntemad_lms
   ```
   Critère: tous les tests passent

3. **Build frontend**
   ```bash
   bench build --app cntemad_lms
   ```
   Critère: build sans erreur

4. **Migration dry-run**
   ```bash
   bench --site lms.local migrate --dry-run
   ```
   Critère: pas d'erreur de migration

5. **Vérification Story (si applicable)**
   - Tous les critères d'acceptation cochés?
   - Tests écrits pour la nouvelle fonctionnalité?
   - Documentation mise à jour?

## Résumé des commandes

```bash
# Tout en une fois
pre-commit run --all-files && \
bench --site lms.local run-tests --app cntemad_lms && \
bench build --app cntemad_lms && \
bench --site lms.local migrate --dry-run
```

## Checklist validation

### Code
- [ ] Lint passe (pre-commit)
- [ ] Tests passent
- [ ] Build réussit
- [ ] Migration OK

### Story (si applicable)
- [ ] Critères fonctionnels validés
- [ ] Tests unitaires écrits
- [ ] Test manuel effectué
- [ ] Mobile responsive vérifié

### Documentation
- [ ] INDEX.md mis à jour si nouveau fichier
- [ ] Docstrings ajoutés
- [ ] README mis à jour si feature visible

## En cas d'échec

| Étape | Action |
|-------|--------|
| Lint | Corriger avec `black .` / `isort .` ou manuellement |
| Tests | Lire l'erreur, corriger le code ou le test |
| Build | Vérifier les imports/exports Vue |
| Migration | Vérifier les dépendances entre doctypes |
