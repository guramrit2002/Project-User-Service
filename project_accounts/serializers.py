from django.contrib.auth.models import Group
from rest_framework import serializers
from accounts.models import Users

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Users
        fields = '__all__'
    
    def create(self, validated_data):
        password = validated_data.pop("password")

        user = Users(**validated_data)
        user.is_staff = True
        user.set_password(password)
        user.save()
        project_owner_group = Group.objects.get(name="Project Owner")
        user.groups.add(project_owner_group)

        return user

class LoginSerializer(serializers.Serializer):
    
    email = serializers.EmailField()
    password = serializers.CharField()
    