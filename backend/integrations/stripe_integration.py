"""
Stripe Payment Integration using the official `stripe` Python SDK.

Rewritten 2026-07-13: the private `emergentintegrations.payments.stripe`
wrapper (and its transitive `litellm` dependency + 7 accepted CVEs) has been
removed. We now call `stripe.checkout.Session` directly. The public surface is
unchanged: `PACKAGES`, `create_session(package_id, host_url, metadata)` ->
{"url","session_id","package"}, and `get_status(session_id)` ->
{"status","payment_status","amount_total","currency"}.

The `stripe` SDK is synchronous, so calls are wrapped in `asyncio.to_thread`
to keep the async API the server expects. AED amounts are converted to fils
(smallest currency unit) as integers — Stripe requires integer minor units.
"""
import logging
import os
import asyncio
from typing import Dict, Any, Optional

import stripe

logger = logging.getLogger(__name__)


class StripeIntegration:
    def __init__(self):
        self.api_key = os.getenv("STRIPE_API_KEY", "sk_test_emergent")
        self.stripe_checkout = None  # kept for backward-compat; unused by direct SDK path

        # Payment packages (amounts in AED)
        self.PACKAGES = {
            "starter": {"amount": 2500.00, "currency": "aed", "name": "Starter Package"},
            "growth": {"amount": 5000.00, "currency": "aed", "name": "Growth Package"},
            "enterprise": {"amount": 10000.00, "currency": "aed", "name": "Enterprise Package"}
        }

    def initialize(self, webhook_url: str):
        """Backward-compat hook. Previously built the emergentintegrations
        checkout client; now just ensures the SDK key is set. Safe to call."""
        stripe.api_key = self.api_key
        self.stripe_checkout = True  # marker so create_session's guard passes

    async def create_session(self, package_id: str, host_url: str, metadata: Optional[Dict] = None):
        try:
            if not self.stripe_checkout:
                self.initialize(f"{host_url}/api/integrations/payments/webhook")

            if package_id not in self.PACKAGES:
                return {"error": "Invalid package"}

            pkg = self.PACKAGES[package_id]
            currency = pkg["currency"]
            # Stripe expects the amount in the smallest currency unit. AED has
            # 2 decimal places (100 fils = 1 AED), so multiply by 100 and round.
            unit_amount = int(round(pkg["amount"] * 100))

            def _create():
                return stripe.checkout.Session.create(
                    mode="payment",
                    line_items=[{
                        "price_data": {
                            "currency": currency,
                            "product_data": {"name": pkg["name"]},
                            "unit_amount": unit_amount,
                        },
                        "quantity": 1,
                    }],
                    success_url=f"{host_url}/payment-success?session_id={{CHECKOUT_SESSION_ID}}",
                    cancel_url=f"{host_url}/payment-cancel",
                    metadata=metadata or {"package_id": package_id},
                )

            session = await asyncio.to_thread(_create)
            return {"url": session.url, "session_id": session.id, "package": pkg}
        except Exception as e:
            logger.error(f"Stripe session error: {e}")
            return {"error": str(e)}

    async def get_status(self, session_id: str):
        try:
            def _retrieve():
                return stripe.checkout.Session.retrieve(session_id)
            status = await asyncio.to_thread(_retrieve)
            return {
                "status": status.status,
                "payment_status": status.payment_status,
                "amount_total": status.amount_total,
                "currency": status.currency,
            }
        except Exception as e:
            return {"error": str(e)}

stripe_integration = StripeIntegration()