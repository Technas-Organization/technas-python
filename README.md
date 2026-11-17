# Technas for Python

Payments and user accounts behind **one client and one secret**. [Lire en français](README.fr.md).

```python
from technas import Technas

t = Technas()                                    # reads TECHNAS_SECRET

payment = t.pay.payments.create(
    amount=5000, reference="order-42",
    customer={"email": "awa@example.com", "name": "Awa Mensah"},
    return_url="https://shop.example/thanks",
)
print(payment.checkout_url)

user = t.accounts.users.resolve(phone="+22890123456", proof="verified")
check = t.accounts.tokens.verify(access_token)
```

## Pick your package

Like a toolkit that ships in several builds, Technas comes in variants. Same code, different cuts:

| You want | Install | Import |
|---|---|---|
| Everything | `technas` (this package) | `from technas import Technas` |
| Payments only | [`technas-pay`](https://github.com/Technas-Organization/technas-pay-python) | `from technas_pay import TechnasPay` |
| User accounts only | [`technas-accounts`](https://github.com/Technas-Organization/technas-accounts-python) | `from technas_accounts import TechnasAccounts` |

The full package depends on the thin ones, never the reverse: a thin package pulls in nothing from
another product. Inside `technas`, a product is imported the first time you touch it (`t.accounts`
alone never loads the payment code).

## Install

```bash
pip install "technas @ git+https://github.com/Technas-Organization/technas-python@v0.1.0"
```

Python 3.9+. Your secret comes from the [console](https://console.technas.fr) (**Developers ›
Keys**): `tps_test_…` for the sandbox (no real money, sandbox users), `tps_live_…` for production.
Put it in `TECHNAS_SECRET`.

## What is inside

| | |
|---|---|
| `t.pay.payments` | `create`, `get`, `get_by_reference`, `cancel`, `refund`, `list` |
| `t.pay.refunds` / `t.pay.balance` | `get` / `get`, `top_up` |
| `t.pay.webhooks` | `verify`, `handle` (signed webhooks) |
| `t.pay.client` | The whole thin `technas-pay` client, for everything else (payout destination, card account, currency rules, ready-made app routes…) |
| `t.accounts.users` | `resolve`, `get`, `list`, `set_roles`, `disable`, `enable`, `revoke_sessions` |
| `t.accounts.roles` / `t.accounts.tokens` | `list`, `declare` / `verify` |
| `t.accounts.config()` | What your app plugs in to sign users in |

Each product keeps its own documentation: [payments](https://github.com/Technas-Organization/technas-pay-python#readme),
[accounts](https://github.com/Technas-Organization/technas-accounts-python#readme). The full API
reference lives in the console (**Developers › Reference**).

## Tests

```bash
pip install -e ".[test]" && pytest
```

MIT licence.
