from rest_framework import serializers
from .models import CustomUser

    
class UserSerializer(serializers.ModelSerializer):
    user_type = serializers.CharField(default='customer')
    password = serializers.CharField(write_only=True)  # Ensure password is write-only

    def validate_proof_of_address(self, value):
        self.validate_file_type(value)
        return value

    def validate_NIN_doc(self, value):
        self.validate_file_type(value)
        return value

    def validate_other_doc(self, value):
        self.validate_file_type(value)
        return value

    def validate_file_type(self, value):
        import os
        valid_extensions = ['.png', '.jpg', '.jpeg', '.pdf']
        ext = os.path.splitext(value.name)[1]  # Extract file extension
        if ext.lower() not in valid_extensions:
            raise serializers.ValidationError(f'Unsupported file format. Allowed formats: PNG, JPG, JPEG, PDF')

    class Meta:
        model = CustomUser
        fields = "__all__"

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        write_only=True, 
        min_length=8, 
        required=True,
        error_messages={
            'required': 'New password is required.',
            'min_length': 'Password must be at least 8 characters long.'
        }
    )
