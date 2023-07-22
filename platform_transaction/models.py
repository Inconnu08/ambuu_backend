from django.db import models


class PlatformTransaction(models.Model):
    DELIVERY_STATUS_CHOICES = [
        ('pending', 'pending'),
        ('prescription_received', 'Prescription Received'),
        ('dispatched', 'Dispatched'),
        ('complete', 'Complete'),
        ('cancelled', 'Cancelled'),
    ]

    DELIVERY_RECURRENCE_CHOICES = [
        ('one_time', 'One Time'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]

    name = models.CharField(max_length=100)
    uid = models.CharField(max_length=200)
    prescription_picture_url = models.URLField()
    phone_number = models.CharField(max_length=15)
    area = models.CharField(max_length=60, choices=[
        ('Bashundhara', 'Bashundhara'),
        ('Bailey Road', 'Bailey Road'),
        # Add other districts of Bangladesh here
    ])
    address = models.TextField()
    delivery_status = models.CharField(max_length=40, choices=DELIVERY_STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, null=True)
    deliveryman_name = models.CharField(max_length=100, blank=True, null=True)
    deliveryman_phone = models.CharField(max_length=15, blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    delivery_recurrence = models.CharField(max_length=10, choices=DELIVERY_RECURRENCE_CHOICES, default='one_time')
    intervals_recurring = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f"Medicine Order by {self.name}"
