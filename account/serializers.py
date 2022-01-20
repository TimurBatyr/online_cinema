from django.contrib.auth import authenticate
from rest_framework import serializers
from account.utils import send_activation_code

from .models import MyUser


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, write_only=True)
    password_confirm = serializers.CharField(min_length=6, write_only=True)

    class Meta:
        model = MyUser
        fields = ('email', 'password', 'password_confirm')

    def validate(self, validated_data):
        password = validated_data.get('password')
        password_confirm = validated_data.get('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Passwords do not match')
        return validated_data

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        user = MyUser.objects.create_user(email=email, password=password)
        send_activation_code.delay(email=user.email, activation_code=user.activation_code)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        label='Password',
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            if not user:
                message = 'Unable to log in with provided credentials'
                raise serializers.ValidationError(message, code='authorization')

        else:
            message = 'Must include "email" and "password". '
            raise serializers.ValidationError(message, code='authorization')

        attrs['user'] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(min_length=6)
    new_pass = serializers.CharField(min_length=6)
    new_pass_confirm = serializers.CharField(min_length=6)

    def validate_old_password(self, old_password):
        user = self.context.get('request').user
        if not user.check_password(old_password):
            raise serializers.ValidationError('Enter the correct current password')
        return old_password

    def validate(self, validated_data):
        new_pass = validated_data.get('new_pass')
        new_pass_confirm = validated_data.get('new_pass_confirm')
        if new_pass != new_pass_confirm:
            raise serializers.ValidationError('Wrong password or confirmation')
        return validated_data

    def set_new_pass(self):
        new_pass = self.validated_data.get('new_pass')
        user = self.context.get('request').user
        user.set_password(new_pass)
        user.save()

