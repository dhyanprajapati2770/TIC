from django.db import models
from diseases.models import Disease
from symptoms.models import Symptom


class Medicine(models.Model):
    """Model for storing medicines."""
    name = models.CharField(max_length=200, unique=True)
    generic_name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField()
    dosage_form = models.CharField(
        max_length=50,
        choices=[
            ('tablet', 'Tablet'),
            ('capsule', 'Capsule'),
            ('liquid', 'Liquid'),
            ('injection', 'Injection'),
            ('cream', 'Cream'),
            ('ointment', 'Ointment'),
            ('drops', 'Drops'),
            ('inhaler', 'Inhaler'),
            ('suppository', 'Suppository'),
            ('other', 'Other'),
        ],
        default='tablet'
    )
    strength = models.CharField(max_length=100, blank=True, null=True)
    manufacturer = models.CharField(max_length=200, blank=True, null=True)
    prescription_required = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    stock_quantity = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='medicines/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Related fields
    treats_diseases = models.ManyToManyField(Disease, related_name='medicines', blank=True)
    treats_symptoms = models.ManyToManyField(Symptom, related_name='medicines', blank=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class MedicineRecommendation(models.Model):
    """Model for storing medicine recommendations."""
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='recommendations')
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE, related_name='medicine_recommendations', blank=True, null=True)
    symptom = models.ForeignKey(Symptom, on_delete=models.CASCADE, related_name='medicine_recommendations', blank=True, null=True)
    dosage = models.CharField(max_length=200, blank=True, null=True)
    duration = models.CharField(max_length=200, blank=True, null=True)
    side_effects = models.TextField(blank=True, null=True)
    contraindications = models.TextField(blank=True, null=True)
    effectiveness_score = models.FloatField(default=0.0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-effectiveness_score']
    
    def __str__(self):
        if self.disease:
            return f"{self.medicine.name} for {self.disease.name}"
        elif self.symptom:
            return f"{self.medicine.name} for {self.symptom.name}"
        return f"{self.medicine.name} recommendation"


class MedicineCategory(models.Model):
    """Model for categorizing medicines."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    medicines = models.ManyToManyField(Medicine, related_name='categories', blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Medicine categories'
    
    def __str__(self):
        return self.name
