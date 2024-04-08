from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User
from django.conf import settings


#create a class that defines the user manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extras):
        if not email:
            raise ValueError('Pole Email nie może być puste')
        email = self.normalize_email(email)
        user = self.model(email=email, **extras)
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_superuser(self, email, password=None, **extras):
        extras.setdefault('is_staff', True)
        extras.setdefault('is_superuser', True)

        if extras.get('is_staff') is not True:
            raise ValueError('Superuser musi zawierać is_staff=True.')
        if extras.get('is_superuser') is not True:
            raise ValueError('Superuser musi zawierać is_superuser=True.')
        
        return self.create_user(email, password, **extras)
    
# 'AbstractBaseUser' class provides a basic implementation of the user model
class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username =models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def has_permission(self, permission, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True        

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateField
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)