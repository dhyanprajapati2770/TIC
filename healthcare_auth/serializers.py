from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser, UserProfile, DoctorProfile


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'password_confirm', 'user_type', 
                 'first_name', 'last_name', 'phone_number', 'date_of_birth')
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = CustomUser.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Must include username and password')
        
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ('user',)


class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = '__all__'
        read_only_fields = ('user', 'rating')


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    doctor_profile = DoctorProfileSerializer(read_only=True)
    
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'user_type',
                 'phone_number', 'date_of_birth', 'address', 'profile_picture',
                 'is_verified', 'profile', 'doctor_profile')
        read_only_fields = ('id', 'is_verified')