from copy import deepcopy
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from accounts.models import Users
from .serializers import UserSerializer, LoginSerializer
from user_module.auth import Authenticate
from accounts.token import ProjectOwnerRefreshToken

# Create your views here.

class ProjectAccountViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['post'])
    def create_project_owner(self,request):
        try:
            data = deepcopy(request.data)
            serializer = UserSerializer(data = data)
            if not serializer.is_valid():
                raise Exception(serializer.errors)
            
            user = serializer.save()
            refresh = ProjectOwnerRefreshToken.for_project_owner(user=user)
            
            return Response({
                "message":"Success",
                "user": UserSerializer(user,many=False).data,
                "tokens": {
                        "type": "Bearer",
                        "access": str(refresh.access_token),
                        "refresh": str(refresh),
                    },
            },status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))
            raise e
    
    @action(detail=False,methods=["post"])
    def login_project_owner(self,request):
        
        try:
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            user = Authenticate.project_owner_authenticate(
                email=serializer.validated_data["email"],
                password=serializer.validated_data["password"],
            )
            refresh = ProjectOwnerRefreshToken.for_project_owner(user=user)
            
            return Response(
                {
                    "user": UserSerializer(user).data,
                    "tokens": {
                        "type": "Bearer",
                        "access": str(refresh.access_token),
                        "refresh": str(refresh),
                    },
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            raise e
    


