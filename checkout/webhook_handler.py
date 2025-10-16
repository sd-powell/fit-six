import json
import time
from decimal import Decimal

import stripe
from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from .models import Order, OrderLineItem
from products.models import ProductVariant
from profiles.models import UserProfile

MEMBER_DISCOUNT_RATE = Decimal('0.10')


class StripeWH_Handler:
    """
    Handles incoming Stripe webhooks for payment events.

    This class processes successful and failed payment intents,
    verifies or creates
    corresponding Order records, applies discounts for members,
    sends confirmation
    emails, and updates user profiles with saved delivery details.
    """

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        """
        Send an order confirmation email to the customer using
        predefined email subject and body templates.
        """
        cust_email = order.email
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order},
        )
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL},
        )
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email],
        )

    def handle_event(self, event):
        """
        Default handler for unrecognised webhook events.
        Returns a 200 response to acknowledge receipt.
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200,
        )

    def handle_payment_intent_succeeded(self, event):
        """
        Handle Stripe's payment_intent.succeeded event.

        - Attempts to find an existing matching order.
        - If not found, creates a new Order and related OrderLineItems.
        - Applies member discounts if applicable.
        - Saves user profile data if requested.
        - Sends confirmation email to the customer.
        """
        intent = event.data.object
        pid = intent.id
        bag = intent.metadata.bag
        save_info = intent.metadata.save_info

        # Retrieve charge and billing details
        stripe_charge = stripe.Charge.retrieve(intent.latest_charge)
        billing_details = stripe_charge.billing_details
        shipping_details = intent.shipping
        grand_total = Decimal(stripe_charge.amount) / 100

        # Clean shipping data
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        # Attempt to link to user profile
        profile = None
        username = intent.metadata.username
        if username != 'AnonymousUser':
            try:
                profile = UserProfile.objects.get(user__username=username)
                if save_info:
                    profile.default_phone_number = shipping_details.phone
                    profile.default_country = shipping_details.address.country
                    profile.default_postcode = (
                        shipping_details.address.postal_code
                    )
                    profile.default_town_or_city = (
                        shipping_details.address.city
                    )
                    profile.default_street_address1 = (
                        shipping_details.address.line1
                    )
                    profile.default_street_address2 = (
                        shipping_details.address.line2
                    )
                    profile.default_county = shipping_details.address.state
                    profile.save()
            except UserProfile.DoesNotExist:
                profile = None

        # Try to find the existing order (may have been created pre‑webhook)
        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    country__iexact=shipping_details.address.country,
                    postcode__iexact=shipping_details.address.postal_code,
                    town_or_city__iexact=shipping_details.address.city,
                    street_address1__iexact=shipping_details.address.line1,
                    street_address2__iexact=shipping_details.address.line2,
                    county__iexact=shipping_details.address.state,
                    grand_total=grand_total,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)

        if order_exists:
            self._send_confirmation_email(order)
            return HttpResponse(
                content=(
                    f'Webhook received: {event["type"]} | SUCCESS: '
                    'Verified existing order.'
                ),
                status=200,
            )

        # --- Create a new order if not found ---
        order = None
        try:
            # Apply member discount if applicable
            discount = Decimal('0.00')
            if profile and profile.is_member:
                discount = grand_total * MEMBER_DISCOUNT_RATE

            order_total = grand_total - discount

            # Estimate delivery using same logic as contexts.py
            if order_total < settings.FREE_DELIVERY_THRESHOLD:
                delivery_cost = order_total * Decimal(
                    settings.STANDARD_DELIVERY_PERCENTAGE / 100
                )
            else:
                delivery_cost = Decimal('0.00')

            order = Order.objects.create(
                full_name=shipping_details.name,
                user_profile=profile,
                email=billing_details.email,
                phone_number=shipping_details.phone,
                country=shipping_details.address.country,
                postcode=shipping_details.address.postal_code,
                town_or_city=shipping_details.address.city,
                street_address1=shipping_details.address.line1,
                street_address2=shipping_details.address.line2,
                county=shipping_details.address.state,
                order_total=order_total,
                delivery_cost=delivery_cost,
                discount=round(discount, 2),
                grand_total=grand_total,
                original_bag=bag,
                stripe_pid=pid,
            )

            bag_items = json.loads(bag)
            for item_id, item_data in bag_items.items():
                for variant_key, quantity in (
                    item_data['items_by_variant'].items()
                ):
                    size, colour = variant_key.split('_')
                    variant = ProductVariant.objects.get(
                        product_id=item_id,
                        size__iexact=size,
                        colour__iexact=colour,
                    )
                    OrderLineItem.objects.create(
                        order=order,
                        variant=variant,
                        quantity=quantity,
                    )

        except Exception as e:
            if order:
                order.delete()
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | ERROR: {e}',
                status=500,
            )

        self._send_confirmation_email(order)
        return HttpResponse(
            content=(
                f'Webhook received: {event["type"]} | SUCCESS: '
                'Order created via webhook.'
            ),
            status=200,
        )

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle Stripe's payment_intent.payment_failed event.
        No further action is taken except logging acknowledgment.
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200,
        )
