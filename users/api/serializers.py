from rest_framework import serializers
from django.contrib.auth import get_user_model


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer for the user model.

    This serializer is designed to handle the serialization and deserialization 
    of user data. It works with the active user model, making it compatible 
    with custom user models.
    """
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email']



class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    This serializer handles the registration of new users by ensuring:
    - Passwords match.
    - The email is used as both the `email` and `username` fields.
    - The user is initially created as inactive with `is_active` and `is_email_verified` set to False.
    """
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def save(self):
        """
        Overridden save method to handle custom user creation.

        - Validates that the passwords match.
        - Uses the email as the username.
        - Creates a new inactive user.
        """
        pw = self.validated_data['password']
        repeated_pw = self.validated_data['confirm_password']

        if pw != repeated_pw:
            raise serializers.ValidationError({'password': ['The passwords do not match!']})
        
        self.validated_data.pop('confirm_password')

        email = self.validated_data['email']
        self.validated_data['username'] = email

        user = get_user_model().objects.create_user(
            email=email,
            username=email,
            password=self.validated_data['password'],
        )

        user.is_active = False
        user.is_email_verified = False
        user.save()

        return user