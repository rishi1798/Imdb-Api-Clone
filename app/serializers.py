from django.contrib.auth.models import User
from rest_framework import serializers


class RegistrationSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(write_only=True)
    
    class Meta:
        model=User
        fields=['email','username','password','password2']


    def save(self):
        
        password=self.validated_data['password']
        password2=self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError("Password did not match")
        
        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError("Email already exists")
        
        account=User(email=self.validated_data['email'],username=self.validated_data['username'],password=self.validated_data['password'])

        account.save()

        return account