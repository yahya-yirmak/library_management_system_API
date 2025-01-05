from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate


# Create a Serializer for CustomUser Model
class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email','date_of_membership']

    def create(self, validated_data):
        """
            The method hashes the password before storing it in the database for security.
        """
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
    

    def update(self, instance, validated_data):
        """
            The method hashes the password before storing it in the database for security.
        """
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)



# Create a Serializer for Login
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
            Fetch the username and password, then authenticate the user.
        """
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if not user.is_active:
                raise serializers.ValidationError('User is inactive.')
            return {'user':user}
        raise serializers.ValidationError('Invalid username or password.')



# Create a Serializer for Registration
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email']
    
    def validate(self, data):
        """
            The validate method checks if the username exists. If so, it generates an error.
        """
        username = data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise serializers.ValidationError('username already exists.')
        return data
    

    def validate_email(self, value):
        """
            The validate method makes sure the email provided by the user is unique.
        """
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists.')
        return value


    def create(self, validated_data):
        """
            The method hashes the password before storing it in the database for security.
        """
        validated_data['password'] = make_password(validated_data['password'])
        return CustomUser.objects.create(**validated_data)
    

    def update(self, instance, validated_data):
        """
            The method hashes the password before storing it in the database for security.
        """
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)