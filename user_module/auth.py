from user_module.exceptions.exceptions import ValidationError
from accounts.models import Users, Project, ProjectUserMapping

class Authenticate:
    def __init__(self,project_id,identifier,password):
        self.project_id = project_id
        self.identifier = identifier
        self.password = password
    
    @classmethod
    def project_user_authenticate(cls, project_id, identifier, password):
        
        if not project_id:
            raise ValidationError({"project_id": "Project id is required"})

        if not identifier:
            raise ValidationError({"identifier": "Identifier is required"})

        if not password:
            raise ValidationError({"password": "Password is required"})
        
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise ValidationError("Invalid project")

        if project.auth_type == "email":
            user = Users.objects.filter(email=identifier, is_active=True,
                                        groups__name = "Project User").first()
        elif project.auth_type == "username":
            user = Users.objects.filter(username=identifier, is_active=True, 
                                        groups__name = "Project User").first()
        
        if not user or not user.check_password(password):
            raise ValidationError("Invalid credentials")

        if not ProjectUserMapping.objects.filter(
            project=project,
            user=user
        ).exists():
            raise ValidationError("User not part of this project")

        return user, project
    
    @classmethod
    def project_owner_authenticate(cls, email, password):
        
        try:
            if not email:
                raise ValidationError("email is required")

            if not password:
                raise ValidationError("Password is required")
            
            user = Users.objects.get(email=email)
            
            if not user or not user.check_password(password):
                raise ValidationError("Invalid credentials")
            
            return user
        except Users.DoesNotExist:
            raise ValidationError("User this email does not exists")
        except Exception as e:
            raise e
    
