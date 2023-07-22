from django.db import models


class MedicineOrder(models.Model):
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

    @classmethod
    def get_pending_orders(cls):
        return cls.objects.filter(delivery_status='pending')

    def add_recurring_orders(self):
        if self.delivery_recurrence != 'one_time' and self.intervals_recurring is not None:
            # Write logic to add recurring orders to the database based on the delivery_recurrence and
            # intervals_recurring For example, if delivery_recurrence is 'weekly' and intervals_recurring is 4,
            # add 4 weeks of orders

            # Implement your logic here
            pass
