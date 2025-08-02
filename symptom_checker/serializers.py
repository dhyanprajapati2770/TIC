from rest_framework import serializers
from .models import Symptom, SymptomCheck, UserSymptom, SymptomAnalysis


class SymptomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symptom
        fields = '__all__'


class UserSymptomSerializer(serializers.ModelSerializer):
    symptom_name = serializers.CharField(source='symptom.name', read_only=True)
    symptom_category = serializers.CharField(source='symptom.category', read_only=True)
    
    class Meta:
        model = UserSymptom
        fields = ['symptom', 'symptom_name', 'symptom_category', 'severity', 'notes']


class SymptomCheckSerializer(serializers.ModelSerializer):
    symptoms_data = UserSymptomSerializer(source='usersymptom_set', many=True, read_only=True)
    analysis = serializers.SerializerMethodField()
    
    class Meta:
        model = SymptomCheck
        fields = ['id', 'additional_info', 'duration', 'created_at', 'symptoms_data', 'analysis']
    
    def get_analysis(self, obj):
        try:
            return SymptomAnalysisSerializer(obj.analysis).data
        except SymptomAnalysis.DoesNotExist:
            return None


class SymptomAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = SymptomAnalysis
        fields = '__all__'


class SymptomCheckCreateSerializer(serializers.Serializer):
    symptoms = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField()
        )
    )
    additional_info = serializers.CharField(required=False, allow_blank=True)
    duration = serializers.CharField(required=False, allow_blank=True)
    
    def validate_symptoms(self, value):
        if not value:
            raise serializers.ValidationError("At least one symptom is required")
        
        for symptom_data in value:
            if 'symptom_id' not in symptom_data or 'severity' not in symptom_data:
                raise serializers.ValidationError("Each symptom must have symptom_id and severity")
            
            try:
                severity = int(symptom_data['severity'])
                if severity < 1 or severity > 5:
                    raise serializers.ValidationError("Severity must be between 1 and 5")
            except (ValueError, TypeError):
                raise serializers.ValidationError("Severity must be a valid integer")
        
        return value