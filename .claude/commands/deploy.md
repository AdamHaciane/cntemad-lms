# Déploiement

Déploie sur staging ou production (Contabo).

## Environnements

| Env | Serveur | Usage |
|-----|---------|-------|
| staging | 62.171.136.243 | Tests avant prod |
| production | 62.171.136.243 | Production live |

## Pré-requis

- Accès SSH configuré
- `/validate` passé
- Branche mergée dans main (pour prod)

## `/deploy staging`

Déploie sur l'environnement de staging.

```bash
# 1. Valider localement
pre-commit run --all-files
bench --site lms.local run-tests --app cntemad_lms

# 2. Pousser sur develop
git push origin develop

# 3. Déployer sur staging
ssh root@62.171.136.243 << 'EOF'
cd /home/frappe/frappe-bench
bench pull --apps cntemad_lms
bench --site lms.local migrate
bench build --app cntemad_lms
bench restart
EOF

# 4. Vérifier
curl -I https://staging.lms.cntemad.mg
```

## `/deploy production`

Déploie sur l'environnement de production.

### Checklist pré-déploiement

- [ ] Tests passent sur staging
- [ ] PR mergée dans main
- [ ] Backup récent disponible
- [ ] Pas de déploiement en cours

### Étapes

```bash
# 1. Créer backup
ssh root@62.171.136.243 << 'EOF'
cd /home/frappe/frappe-bench
bench --site lms.local backup --with-files
EOF

# 2. Déployer
ssh root@62.171.136.243 << 'EOF'
cd /home/frappe/frappe-bench
bench pull --apps cntemad_lms
bench --site lms.local migrate
bench build --app cntemad_lms
bench restart
EOF

# 3. Vérifier
curl -I https://lms.cntemad.mg

# 4. Smoke tests
# - Connexion étudiant
# - Liste des cours
# - Page de paiement
```

## Rollback

En cas de problème après déploiement:

```bash
ssh root@62.171.136.243 << 'EOF'
cd /home/frappe/frappe-bench

# Restaurer le backup
bench --site lms.local restore \
  /path/to/backup.sql.gz \
  --with-private-files /path/to/private-files.tar \
  --with-public-files /path/to/public-files.tar

# Ou revenir au commit précédent
cd apps/cntemad_lms
git checkout HEAD~1
cd ../..
bench migrate
bench build --app cntemad_lms
bench restart
EOF
```

## Monitoring post-déploiement

```bash
# Logs en temps réel
ssh root@62.171.136.243 "tail -f /home/frappe/frappe-bench/logs/frappe.log"

# Status services
ssh root@62.171.136.243 "supervisorctl status"

# Erreurs récentes
ssh root@62.171.136.243 "tail -100 /home/frappe/frappe-bench/logs/web.error.log"
```

## Commandes rapides

```bash
# Status serveur
ssh root@62.171.136.243 "cd /home/frappe/frappe-bench && bench version"

# Restart sans redéployer
ssh root@62.171.136.243 "cd /home/frappe/frappe-bench && bench restart"

# Clear cache
ssh root@62.171.136.243 "cd /home/frappe/frappe-bench && bench --site lms.local clear-cache"
```
