# EPIC-002: Paiement Mobile Money

## Contexte
L'étudiant paie un EC via MVola, Orange Money ou Airtel Money.

## Stories
- [ ] STORY-006: Composant ProviderSelector
- [ ] STORY-007: Composant PaymentButton
- [ ] STORY-008: Composable usePayment()
- [ ] STORY-009: API initiate_payment()
- [ ] STORY-010: Webhook callback providers
- [ ] STORY-011: Page Paiement complète

## Critères de succès Epic
- [ ] 3 providers fonctionnels (MVola, Orange, Airtel)
- [ ] Statut temps réel (pending → success/failed)
- [ ] Reçu SMS après paiement

## Écrans concernés

| Écran | Composants | API |
|-------|-----------|-----|
| Paiement | `ProviderSelector`, `PhoneInput`, `PaymentStatus` | `initiate_payment()` |

## Dépendances
- EPIC-001 (Dashboard Étudiant)
- Doctype CNTEMAD Payment

## Notes techniques
- Intégration API MVola, Orange Money, Airtel Money
- Webhooks pour confirmation asynchrone
- Stockage transaction_id uniquement (pas de données sensibles)
