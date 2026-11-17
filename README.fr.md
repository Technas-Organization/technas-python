# Technas pour Python

Les paiements et les comptes de vos utilisateurs derrière **un seul client et un seul secret**.
[Read in English](README.md).

```python
from technas import Technas

t = Technas()                                    # lit TECHNAS_SECRET

payment = t.pay.payments.create(
    amount=5000, reference="commande-42",
    customer={"email": "awa@exemple.com", "name": "Awa Mensah"},
    return_url="https://boutique.exemple/merci",
)
print(payment.checkout_url)

user = t.accounts.users.resolve(phone="+22890123456", proof="verified")
check = t.accounts.tokens.verify(jeton_d_acces)
```

## Choisir son paquet

Comme une boîte à outils livrée en plusieurs variantes, Technas se prend à la carte. Le même
code, plusieurs découpes :

| Vous voulez | Installer | Importer |
|---|---|---|
| Tout | `technas` (ce paquet) | `from technas import Technas` |
| Les paiements seuls | [`technas-pay`](https://github.com/Technas-Organization/technas-pay-python) | `from technas_pay import TechnasPay` |
| Les comptes seuls | [`technas-accounts`](https://github.com/Technas-Organization/technas-accounts-python) | `from technas_accounts import TechnasAccounts` |

Le paquet complet dépend des paquets minces, jamais l'inverse : un paquet mince ne tire rien d'un
autre produit. Dans `technas`, un produit n'est importé qu'au moment où vous y touchez
(`t.accounts` seul ne charge jamais le code des paiements).

## Installer

```bash
pip install "technas @ git+https://github.com/Technas-Organization/technas-python@v0.1.0"
```

Python 3.9 ou plus. Votre secret vient de la [console](https://console.technas.fr)
(**Développeurs › Clés**) : `tps_test_…` pour le bac à sable (aucun argent réel, utilisateurs du
bac à sable), `tps_live_…` pour la production. Posez-le dans `TECHNAS_SECRET`.

## Ce qu'il y a dedans

| | |
|---|---|
| `t.pay.payments` | `create`, `get`, `get_by_reference`, `cancel`, `refund`, `list` |
| `t.pay.refunds` / `t.pay.balance` | `get` / `get`, `top_up` |
| `t.pay.webhooks` | `verify`, `handle` (webhooks signés) |
| `t.pay.client` | Tout le client mince `technas-pay`, pour le reste (numéro de reversement, compte carte, règles de devise, routes toutes faites pour l'app…) |
| `t.accounts.users` | `resolve`, `get`, `list`, `set_roles`, `disable`, `enable`, `revoke_sessions` |
| `t.accounts.roles` / `t.accounts.tokens` | `list`, `declare` / `verify` |
| `t.accounts.config()` | Ce que votre app branche pour connecter ses utilisateurs |

Chaque produit garde sa documentation : [paiements](https://github.com/Technas-Organization/technas-pay-python#readme),
[comptes](https://github.com/Technas-Organization/technas-accounts-python/blob/main/README.fr.md). La
référence complète de l'API est dans la console (**Développeurs › Référence**).

## Tests

```bash
pip install -e ".[test]" && pytest
```

Licence MIT.
