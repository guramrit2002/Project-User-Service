from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (LoginSerializer, UserSerializer, ProjectSerializer, 
                          LogoutSerializer, SignupSerializer,
                          CreateUserSerializer, ListUserSerializer)
from user_module.auth import Authenticate
from .token import ProjectRefreshToken
from .models import ProjectUserMapping
from user_module.exceptions.exceptions import ValidationError
from accounts.token import ProjectRefreshToken
from .models import Users
from project.models import Project
# Create your views here.

class UserViewSet(viewsets.ViewSet):
    
    def list(self, request):
        data = {"message": "List of users"}
        return Response(data)
    
class AuthViewSet(viewsets.ViewSet):
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            user, project = Authenticate.project_user_authenticate(
                project_id=serializer.validated_data["project_id"],
                identifier=serializer.validated_data["identifier"],
                password=serializer.validated_data["password"],
            )

            refresh = ProjectRefreshToken.for_user_and_project(user, project)

            return Response(
                {
                    "user": UserSerializer(user).data,
                    "project": ProjectSerializer(project).data,
                    "tokens": {
                        "type": "Bearer",
                        "access": str(refresh.access_token),
                        "refresh": str(refresh),
                    },
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print(str(e))
            raise e

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token = serializer.validated_data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()

        return Response(
            {"detail": "Logged out successfully"},
            status=status.HTTP_205_RESET_CONTENT,
        )
    
    @action(detail=False, methods=['post'])
    def signup(self, request):
        
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        project = serializer.validated_data["project"]
        password = serializer.validated_data["password"]

        user_serializer = CreateUserSerializer(data={
            "email":serializer.validated_data.get("email"),
            "username":serializer.validated_data.get("username"),
            "password":serializer.validated_data.get("password")
        })
        
        if not user_serializer.is_valid():
            raise ValidationError(user_serializer.errors)
        
        user = user_serializer.save()
        
        ProjectUserMapping.objects.create(
            project=project,
            user=user,
        )

        refresh = ProjectRefreshToken.for_user_and_project(user, project)

        return Response(
            {
                "user": UserSerializer(user).data,
                "project": ProjectSerializer(project).data,
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            },
            status=status.HTTP_201_CREATED,
        )

class UserViewSet(viewsets.ViewSet):
    
    def list(self,request):
        try:
            project_id = request.query_params.get("project")
            users = Users.objects.filter(project_id=project_id)
            serializer = ListUserSerializer(users,many=True)
            return Response({
                "message":"Success",
                "users":serializer.data,
            })
        except Exception as e:
            raise e