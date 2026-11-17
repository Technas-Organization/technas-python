"""Technas: every Technas product behind one client and one secret.

    from technas import Technas
    t = Technas()                                   # reads TECHNAS_SECRET
    payment = t.pay.payments.create(amount=5000, reference="order-42",
                                    customer={"email": "awa@example.com"}, return_url="https://shop.example/thanks")
    user = t.accounts.users.resolve(phone="+22890123456", proof="verified")

This is the FULL package: it depends on the thin ones (``technas-pay``, ``technas-accounts``) and
adds nothing but this entry point. A product module is imported the first time you touch it:
using ``t.accounts`` only never loads the payment code. If you want one product and nothing else,
install its thin package instead.
"""

from __future__ import annotations

import os
from typing import Any, Optional

from ._version import __version__

__all__ = ["Technas", "__version__"]

_SECRET_ENVS = ("TECHNAS_SECRET", "TECHNAS_PAY_SECRET")


class Technas:
    """One secret, every product. ``t.pay`` and ``t.accounts`` are created on first use."""

    def __init__(self, secret: Optional[str] = None, *, base_url: Optional[str] = None, timeout: Optional[float] = None,
                 http_client: Any = None) -> None:
        """``http_client``: your own ``httpx.Client`` (proxy, tests), shared by every product."""
        self.__secret = secret
        self._options: dict[str, Any] = {}
        if base_url is not None:
            self._options["base_url"] = base_url
        if timeout is not None:
            self._options["timeout"] = timeout
        if http_client is not None:
            self._options["http_client"] = http_client
        self._pay: Any = None
        self._accounts: Any = None

    def __repr__(self) -> str:
        return "Technas()"

    def _resolved_secret(self) -> Optional[str]:
        if self.__secret is not None:
            return self.__secret
        return next((os.environ[name] for name in _SECRET_ENVS if os.environ.get(name)), None)

    @property
    def pay(self) -> "Pay":
        """Payments: mobile money and card."""
        if self._pay is None:
            from .pay import Pay  # imported here: accounts-only code never loads it

            self._pay = Pay(self._resolved_secret(), **self._options)
        return self._pay

    @property
    def accounts(self) -> Any:
        """Your app's users: ``users``, ``roles``, ``tokens``, ``config()``."""
        if self._accounts is None:
            from technas_accounts import TechnasAccounts

            self._accounts = TechnasAccounts(self._resolved_secret(), **self._options)
        return self._accounts

    def close(self) -> None:
        for product in (self._pay, self._accounts):
            if product is not None:
                product.close()

    def __enter__(self) -> "Technas":
        return self

    def __exit__(self, *_: Any) -> None:
        self.close()
