from rest_framework import serializers
from django.contrib.auth import get_user_model


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email']



class RegistrationSerializer(serializers.ModelSerializer):
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
        pw = self.validated_data['password']
        repeated_pw = self.validated_data['confirm_password']

        if pw != repeated_pw:
            raise serializers.ValidationError({'password': ['Die Passwörter stimmen nicht überein!']})
        
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