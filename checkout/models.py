import uuid
from decimal import Decimal

from django.db import models
from django.db.models import Sum
from django.conf import settings

from django_countries.fields import CountryField

from products.models import ProductVariant
from profiles.models import UserProfile


class Order(models.Model):
    order_number = models.CharField(max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(
        blank_label='Country *',
        null=False,
        blank=False
    )
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=False,
        default=Decimal('0.00')
    )
    discount = models.DecimalField(  # New for member discount
        max_digits=6,
        decimal_places=2,
        null=False,
        default=Decimal('0.00')
    )
    order_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        default=Decimal('0.00')
    )
    grand_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        default=Decimal('0.00')
    )
    original_bag = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(
        max_length=254,
        null=False,
        blank=False,
        default=''
    )

    def _generate_order_number(self):
        """
        Return a unique, random order number using UUID4.

        Used internally when saving a new order for the first time.
        """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Calculate and update the order's totals.

        Adds up line item totals, applies delivery costs
        (if below free delivery threshold), subtracts any discount,
        and saves the grand total.
        """
        self.order_total = self.lineitems.aggregate(
            Sum('lineitem_total')
        )['lineitem_total__sum'] or Decimal('0.00')

        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = (
                self.order_total *
                Decimal(settings.STANDARD_DELIVERY_PERCENTAGE) / 100
            )
        else:
            self.delivery_cost = Decimal('0.00')

        self.grand_total = (
            self.order_total + self.delivery_cost - self.discount
        )
        self.save()

    def save(self, *args, **kwargs):
        """
        Override the default save method to set the order number
        on the first save if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Return the order number as the string representation.
        """
        return self.order_number


class OrderLineItem(models.Model):
    order = models.ForeignKey(
        Order,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='lineitems'
    )
    variant = models.ForeignKey(
        ProductVariant,
        null=False,
        blank=False,
        on_delete=models.CASCADE
    )
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=False,
        blank=False,
        editable=False
    )

    def save(self, *args, **kwargs):
        """
        Override the default save method to calculate the line item total
        using the variant's price multiplied by quantity.
        """
        self.lineitem_total = self.variant.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Return a readable string showing the SKU and related order number.
        """
        return f"SKU {self.variant.sku} on order {self.order.order_number}"
