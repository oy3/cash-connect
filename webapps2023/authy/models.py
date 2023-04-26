from django.db import models
from register.models import CustomUser
from currency.models import Currency
import uuid
from django.utils.timezone import now
from datetime import datetime, timedelta


# Create your models here.
class UserWallet(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, blank=False, null=False, unique=True)
    currency = models.ForeignKey(Currency, related_name="wallet_currency", on_delete=models.CASCADE, blank=True,
                                 null=True, )
    balance = models.DecimalField(default=0.00, max_digits=19, decimal_places=2)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return "{} {} wallet".format(self.user.username, self.currency.code.upper())

    def deposit(self, amount):
        self.balance = float(self.balance) + float(amount)
        return self.save()

    def withdraw(self, amount):
        if (float(self.balance) >= float(amount)):
            self.balance = float(self.balance) - float(amount)
            return self.save()
        else:
            return False

    @classmethod
    def create(cls, user, currency, balance=0.00):
        wallet = cls(user=user, currency=currency, balance=balance)
        return wallet


class Transaction(models.Model):
    transaction_id = models.CharField(unique=True, blank=False, max_length=255, default=uuid.uuid4)
    sent_from = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sender')
    sent_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='receiver')
    currency_from = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='sent_currency')
    currency_to = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='received_currency')
    amount_from = models.DecimalField(max_digits=20, decimal_places=2)
    amount_to = models.DecimalField(max_digits=20, decimal_places=2)
    rate = models.DecimalField(max_digits=10, decimal_places=6)
    transaction_date = models.DateTimeField(default=now)
    remark = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending')

    def __str__(self):
        return "tr-{}".format(self.transaction_id)

    @property
    def is_today(self):
        return self.transaction_date.date() == datetime.today().date()

    @property
    def is_yesterday(self):
        yesterday = datetime.today().date() - timedelta(days=1)
        return self.transaction_date.date() == yesterday

