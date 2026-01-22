# STORY-032: Export rapports nationaux

## Epic parent
EPIC-006: Admin National

## Description
En tant qu'admin national, je veux générer des rapports PDF complets.

## Critères d'acceptation spécifiques
- [ ] Rapport par période (mois, trimestre, année)
- [ ] Sections: résumé, détail par centre, graphiques
- [ ] Format PDF téléchargeable
- [ ] Logo CNTEMAD inclus
- [ ] Date génération

## Critères standard (OBLIGATOIRES)

### Fonctionnel
- [ ] Comportement attendu implémenté
- [ ] Cas limites gérés
- [ ] Happy path fonctionne

### Technique
- [ ] Frappe Print Format ou WeasyPrint
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
- `cntemad_lms/api/reports.py`
- `cntemad_lms/templates/reports/national_report.html`
- `frontend/src/pages/admin/Reports.vue`
- `docs/INDEX.md`

## Commandes de validation
```bash
bench run-tests --app cntemad_lms --module api.reports
npm run build --prefix frontend
```
