from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class UserSerializer(serializers.ModelSerializer):
    role=serializers.CharField(write_only=True)
    company=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=['username','first_name','last_name','email','password','role','company']
        extra_kwargs={'password':{'write_only':True}}

    def create(self,validated_data):
        role=validated_data.pop('role','')
        company=validated_data.pop('company','')
        user=User.objects.create_user(**validated_data)
        Profile.objects.create(user=user,role=role,company=company)
        return user
