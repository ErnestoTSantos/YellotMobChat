import re
from rest_framework import serializers

from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "password", "password_confirm"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Username is already taken.")
        return username

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email is already taken.")
        return email

    def validate_first_name(self, first_name):
        if len(first_name) < 3:
            raise serializers.ValidationError("First name must be at least 3 characters long.")

        return first_name

    def validate_last_name(self, last_name):
        if len(last_name) < 5:
            raise serializers.ValidationError("Last name must be at least 5 characters long.")

        return last_name

    def validate_password(self, password):
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[\W_]).+$'
        if len(password) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")

        if not bool(re.match(pattern, password)):
            raise serializers.ValidationError(
                "Password must contain at least one uppercase letter, one lowercase letter, and one special character."
            )

        return password

    def validate(self, data):
        if data["password"] != data["password_confirm"]:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            password=validated_data["password"],
        )
        return user
