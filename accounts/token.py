from rest_framework_simplejwt.tokens import RefreshToken


class ProjectRefreshToken(RefreshToken):
    @classmethod
    def for_user_and_project(cls, user, project):
        token = cls.for_user(user)
        token["project_id"] = project.id
        token["auth_type"] = project.auth_type
        return token

class ProjectOwnerRefreshToken(RefreshToken):
    
    @classmethod
    def for_project_owner(cls,user):
        
        token = cls.for_user(user)
        token["role"] = "Project Owner"
        token["auth_type"] = "email"
        return token