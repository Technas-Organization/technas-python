"""``t.pay``: the payment client, grouped by resource.

``t.pay.payments.create(...)`` is ``TechnasPay.ask_for_payment(...)`` and so on: the same code
as the thin ``technas-pay`` package, nothing reimplemented. Everything the thin client offers and
this grouping does not name stays reachable as ``t.pay.client``.
"""

from __future__ import annotations

from typing import Any, Optional

from technas_pay import TechnasPay


class _Payments:
    def __init__(self, client: TechnasPay) -> None:
        self._c = client

    def create(self, *, amount: int, reference: str, customer: dict, return_url: str, **options: Any) -> Any:
        """Ask a customer for a payment. Send them to the returned ``checkout_url``."""
        return self._c.ask_for_payment(amount=amount, reference=reference, customer=customer, return_url=return_url, **options)

    def get(self, payment_id: str) -> Any:
        return self._c.get_payment(payment_id)

    def get_by_reference(self, reference: str) -> Any:
        return self._c.get_payment_by_reference(reference)

    def cancel(self, payment_id: str) -> Any:
        return self._c.cancel_payment(payment_id)

    def refund(self, payment_id: str, **options: Any) -> Any:
        return self._c.refund(payment_id, **options)

    def list(self, **options: Any) -> Any:
        return self._c.list_transactions(**options)


class _Refunds:
    def __init__(self, client: TechnasPay) -> None:
        self._c = client

    def get(self, refund_id: str) -> Any:
        return self._c.get_refund(refund_id)


class _Balance:
    def __init__(self, client: TechnasPay) -> None:
        self._c = client

    def get(self) -> Any:
        return self._c.get_balance()

    def top_up(self, **options: Any) -> Any:
        return self._c.top_up_balance(**options)


class _Webhooks:
    def __init__(self, client: TechnasPay) -> None:
        self._c = client

    def verify(self, raw_body: Any, signature_header: Optional[str]) -> Any:
        """The event of a signed webhook, or ``WebhookVerificationError``."""
        return self._c.verify_webhook(raw_body, signature_header)

    def handle(self, raw_body: Any, signature_header: Optional[str], handlers: Any) -> Any:
        return self._c.handle_webhook(raw_body, signature_header, handlers)


class Pay:
    def __init__(self, secret: Optional[str] = None, **options: Any) -> None:
        #: The thin ``technas-pay`` client, for everything not grouped here.
        self.client = TechnasPay(secret, **options)
        self.payments = _Payments(self.client)
        self.refunds = _Refunds(self.client)
        self.balance = _Balance(self.client)
        self.webhooks = _Webhooks(self.client)

    @property
    def test_mode(self) -> bool:
        return self.client.test_mode

    def close(self) -> None:
        self.client.close()
