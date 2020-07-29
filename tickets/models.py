from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password,**extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError(
                "Superuser must have is_staff=True."
            )
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                "Superuser must have is_superuser=True."
            )
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField('email address', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    first_login = models.BooleanField(default=True)
    is_manager = models.BooleanField(default=False)
    objects = UserManager()

    def __str__(self):
        return self.email

DEPARTMENTS = (
    ('E', 'Engineering'),
    ('S', 'Sales'),
    ('A', 'Accounts'),
    ('H', 'Human Resource'),
)


class UserInfo(models.Model):
    GENDERS = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=40)
    surname = models.CharField(max_length=40)
    gender = models.CharField(max_length=1, choices=GENDERS)
    date_of_birth = models.DateField()
    profile_pic = models.ImageField(default="profile_pic1.png",
                                    upload_to='profile_images', null=True, blank=True)
    department = models.CharField(max_length=1, choices=DEPARTMENTS)
    contact_line1 = models.CharField(max_length=40)
    contact_line2 = models.CharField(max_length=40, null=True, blank=True)

    def __str__(self):
        return self.firstname + ' ' + self.surname


class Ticket(models.Model):
    PRIORITIES = (
        ('L', 'Low'),
        ('M', 'Medium'),
        ('H', 'High'),
    )
    STATUSES = (
        ('O', 'Open'),
        ('I', 'In progress'),
        ('R', 'Resolved'),
    )

    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by')
    date_created = models.DateTimeField(auto_now_add=True)
    date_resolved = models.DateTimeField(null=True, blank=True)
    priority = models.CharField(max_length=1, choices=PRIORITIES, default='M')
    status = models.CharField(max_length=1, choices=STATUSES, default='O')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_to', null=True)
    department_concerned = models.CharField(max_length=1, choices=DEPARTMENTS)

