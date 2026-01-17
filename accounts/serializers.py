from django.contrib.auth.models import Group
from rest_framework import serializers
from project.models import Project
from .models import Users, ProjectUserMapping

class LoginSerializer(serializers.Serializer):
    project_id = serializers.IntegerField()
    identifier = serializers.CharField()
    password = serializers.CharField()
    
class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Users
        fields = '__all__'
        
class ListUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Users
        fields = ('email',)

class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"}
    )
    
    class Meta:
        model = Users
        fields = '__all__'
    
    def create(self, validated_data):
        password = validated_data.pop("password")

        user = Users(**validated_data)
        user.set_password(password)
        user.save()
        project_owner_group = Group.objects.get(name="Project User")
        user.groups.add(project_owner_group)

        
        return user
    
    

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

class SignupSerializer(serializers.Serializer):
    project_id = serializers.IntegerField()
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)
    password = serializers.CharField(min_length=6)

    def validate(self, data):
        project = Project.objects.filter(id=data["project_id"]).first()
        if not project:
            raise serializers.ValidationError("Invalid project")

        if project.auth_type == "email" and not data.get("email"):
            raise serializers.ValidationError("Email is required for this project")

        if project.auth_type == "username" and not data.get("username"):
            raise serializers.ValidationError("Username is required for this project")

        # Prevent duplicate membership
        if project.auth_type == "email":
            user = Users.objects.filter(email=data["email"]).first()
        else:
            user = Users.objects.filter(username=data["username"]).first()

        if user and ProjectUserMapping.objects.filter(
            project=project, user=user
        ).exists():
            raise serializers.ValidationError("User already exists in this project")

        data["project"] = project
        data["existing_user"] = user
        return data
    
