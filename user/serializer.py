from rest_framework import serializers,status
from .models import Customuser
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    id = serializers.CharField(read_only=True)
    conf_pass = serializers.CharField(write_only=True)
    class Meta:
        model = Customuser
        fields = ['id','first_name','last_name','username','phone_number','adress','password','conf_pass']

    def validate(self, data):
        password = data.get('password')
        conf_pass = data.get('conf_pass')

        if password and conf_pass and password != conf_pass:
            raise ValidationError('Parollar mos emas')
        return data

    def validate_username(self,username):
        if username[0].isdigit():
            raise ValidationError('Username raqam bilan boshlanmasin')
        return username

    def create(self, validated_data):
        validated_data.pop('conf_pass')
        user = Customuser.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        user = super().to_representation(instance)
        return{
            'msg': "Royxatdan otdingiz",
            'user': user
        }

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True,write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username,password=password)
        if not user:
            raise ValidationError(detail='Parol yoki username xato')

        data['user'] = user
        return data

    def to_representation(self, instance):
        user = instance.get('user')

        token,_ = Token.objects.get_or_create(user=user)

        return{
            'username':instance.get('username'),
            'token': token.key
        }

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customuser
        fields = ['id','first_name','last_name','email','username','phone_number']

class ProfileUpdateSerializer(ProfileSerializer):
    id = serializers.CharField(read_only=True)

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    conf_password = serializers.CharField()

    def validate(self, attrs):
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')
        conf_password = attrs.get('conf_password')

        request = self.context['request']
        current_user = authenticate(
            username=request.user.username,
            password=old_password
        )

        if current_user is None:
            raise ValidationError(detail='Eski parol xato')

        if new_password and old_password and new_password == old_password:
            raise ValidationError(detail='Yangi parol eskisiga teng bolmasin')

        if conf_password and new_password and conf_password != new_password:
            raise ValidationError(detail='Yangi parollar mos emas')

        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()

        return instance
    def to_representation(self, instance):
        return {
            'msg': "Parol ozgartirildi"
        }
            