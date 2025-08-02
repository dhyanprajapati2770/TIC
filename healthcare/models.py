from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ], blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    emergency_contact = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Symptom(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    severity_level = models.IntegerField(choices=[
        (1, 'Mild'),
        (2, 'Moderate'),
        (3, 'Severe'),
        (4, 'Critical')
    ], default=1)
    category = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Disease(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    symptoms = models.ManyToManyField(Symptom, related_name='diseases')
    treatment = models.TextField(blank=True)
    prevention = models.TextField(blank=True)
    risk_level = models.CharField(max_length=20, choices=[
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical')
    ], default='MEDIUM')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Medicine(models.Model):
    name = models.CharField(max_length=200)
    generic_name = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    dosage_form = models.CharField(max_length=50, choices=[
        ('TABLET', 'Tablet'),
        ('CAPSULE', 'Capsule'),
        ('SYRUP', 'Syrup'),
        ('INJECTION', 'Injection'),
        ('CREAM', 'Cream'),
        ('DROPS', 'Drops'),
        ('INHALER', 'Inhaler')
    ])
    strength = models.CharField(max_length=50, blank=True)
    manufacturer = models.CharField(max_length=200, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(default=0)
    prescription_required = models.BooleanField(default=False)
    side_effects = models.TextField(blank=True)
    uses = models.TextField(blank=True)
    image = models.ImageField(upload_to='medicines/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class DiseasePrediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symptoms = models.ManyToManyField(Symptom)
    predicted_diseases = models.ManyToManyField(Disease, through='DiseasePredictionResult')
    confidence_score = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prediction for {self.user.username} - {self.created_at}"

class DiseasePredictionResult(models.Model):
    prediction = models.ForeignKey(DiseasePrediction, on_delete=models.CASCADE)
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    confidence = models.FloatField()
    rank = models.IntegerField()

    class Meta:
        ordering = ['-confidence']

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

    @property
    def total_amount(self):
        return sum(item.total_price for item in self.cartitem_set.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity}x {self.medicine.name}"

    @property
    def total_price(self):
        return self.medicine.price * self.quantity

class Order(models.Model):
    ORDER_STATUS = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=20, unique=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='PENDING')
    shipping_address = models.TextField()
    phone = models.CharField(max_length=15)
    payment_method = models.CharField(max_length=50, default='COD')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order_number} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.medicine.name}"

class ChatMessage(models.Model):
    MESSAGE_TYPES = [
        ('USER', 'User'),
        ('BOT', 'Bot')
    ]

    session_id = models.CharField(max_length=100)
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.message_type} - {self.session_id}"

class Prescription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor_name = models.CharField(max_length=200)
    diagnosis = models.TextField()
    medicines = models.ManyToManyField(Medicine, through='PrescriptionMedicine')
    prescribed_date = models.DateField()
    next_visit = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prescription for {self.user.username} - {self.prescribed_date}"

class PrescriptionMedicine(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    instructions = models.TextField(blank=True)

    def __str__(self):
        return f"{self.medicine.name} - {self.dosage}"
