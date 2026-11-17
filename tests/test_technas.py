"""One secret, two products, each loaded only when used."""

from __future__ import annotations

import json
import subprocess
import sys

import httpx

from technas import Technas

SECRET = "tps_test_pk_demo12345678.whsec_demo"
UID = "7d3f2a10-1111-4222-8333-444455556666"


def _server(seen):
    def answer(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        if request.url.path == "/v1/payments":
            body = json.loads(request.content)
            return httpx.Response(200, json={"id": "9c1f0a10-2222-4333-8444-555566667777", "status": "pending", "reference": body["reference"],
                                             "amount": body["amount"], "currency": "XOF", "mode": "test",
                                             "checkout_url": "https://pay-api.technas.fr/test-checkout/x"})
        if request.url.path == "/v1/accounts/users/resolve":
            return httpx.Response(200, json={"id": UID, "created": True, "phone": "+22890000002", "phone_verified": True,
                                             "email": None, "email_verified": False})
        return httpx.Response(404, json={"code": "not_found", "message": "Not found"})
    return answer


def test_pay_and_accounts_share_the_secret_and_speak_to_their_own_routes():
    seen: list[httpx.Request] = []
    transport = httpx.MockTransport(_server(seen))
    t = Technas(SECRET, http_client=httpx.Client(transport=transport))
    payment = t.pay.payments.create(amount=5000, reference="order-42", customer={"email": "awa@example.com", "name": "Awa Mensah"},
                                    return_url="https://shop.example/thanks", currency="XOF")
    user = t.accounts.users.resolve(phone="+22890000002", proof="verified")
    assert payment.reference == "order-42" and user.id == UID
    assert [r.url.path for r in seen] == ["/v1/payments", "/v1/accounts/users/resolve"]
    assert {r.headers["authorization"] for r in seen} == {"Bearer pk_demo12345678"}
    assert t.pay.test_mode and t.accounts.test_mode


def test_the_secret_comes_from_the_environment(monkeypatch):
    monkeypatch.delenv("TECHNAS_PAY_SECRET", raising=False)
    monkeypatch.setenv("TECHNAS_SECRET", SECRET)
    t = Technas()
    assert t.accounts.test_mode and t.pay.test_mode and "tps_test" not in repr(t)


def test_a_product_is_only_imported_when_touched():
    code = (
        "import sys; from technas import Technas; t = Technas('%s');"
        "assert 'technas_pay' not in sys.modules and 'technas_accounts' not in sys.modules;"
        "t.accounts; assert 'technas_accounts' in sys.modules and 'technas_pay' not in sys.modules;"
        "t.pay; assert 'technas_pay' in sys.modules; print('ok')" % SECRET
    )
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
    assert out.stdout.strip() == "ok", out.stderr
