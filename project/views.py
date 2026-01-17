from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from accounts.models import Project
from .serializers import ProjectSerializer
# Create your views here.

class ProjectViewSet(viewsets.ViewSet):
    
    def retrieve(self,request,pk):
        try:
            project = Project.objects.get(id=pk)
            serializer = ProjectSerializer(project)
            return Response({
                "message":"Succesfully fetched Project",
                "project": serializer.data
                },status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({
                "message":"Resource Not Found",
                "error": "No project with this identifier"
            },status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "message":"Exception Occured",
                "error":str(e)
            },status=status.HTTP_400_BAD_REQUEST)