# Commit avec validation qualité

Effectue un commit avec lint, tests et format conventional.

## Étapes

1. **Lint complet**
   ```bash
   pre-commit run --all-files
   ```
   Si échec → corriger avant de continuer

2. **Tests**
   ```bash
   bench --site lms.local run-tests --app cntemad_lms
   ```
   Si échec → corriger avant de continuer

3. **Build**
   ```bash
   bench build --app cntemad_lms
   ```
   Si échec → corriger avant de continuer

4. **Commit conventional**
   Format: `type(scope): description`

   **Types autorisés:**
   - `feat` → Nouvelle fonctionnalité
   - `fix` → Correction de bug
   - `docs` → Documentation
   - `style` → Formatage (pas de changement de code)
   - `refactor` → Refactoring
   - `test` → Ajout/modification de tests
   - `chore` → Maintenance (deps, config)
   - `ci` → CI/CD

   **Scopes autorisés:**
   - `doctype` → Doctypes Frappe
   - `api` → Endpoints API
   - `frontend` → Composants Vue
   - `ci` → GitHub Actions
   - `docs` → Documentation
   - `payment` → Paiements mobile money
   - `student` → Fonctionnalités étudiant

   **Règles:**
   - Max 50 caractères pour la description
   - Verbe à l'impératif (Add, Fix, Update)
   - Référencer la story si applicable: `feat(api): add payment endpoint [STORY-010]`

## Exemples

```
feat(doctype): add CNTEMAD EC doctype [STORY-002]
fix(payment): handle MVola timeout error
docs(api): document payment endpoints
refactor(frontend): extract ProgressBar component
test(student): add enrollment tests
chore: update dependencies
```

## Checklist avant commit

- [ ] `pre-commit run --all-files` passe
- [ ] Tests passent
- [ ] Build réussit
- [ ] Message suit le format conventional
- [ ] Story référencée si applicable
