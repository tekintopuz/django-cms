from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager 
from django.core.validators import RegexValidator
from django.contrib.auth.models import Group




class CustomAccountManager(BaseUserManager):
	
	def create_superuser(self, email, username, first_name, last_name, password,**other_fields):
		other_fields.setdefault('is_staff',True)
		other_fields.setdefault('is_superuser',True)
		other_fields.setdefault('is_active',True)
		if other_fields.get('is_staff') is not True:
			raise ValueError(
				'Superuser must be assigned to is_staff=True.')
		if other_fields.get('is_superuser') is not True:
			raise ValueError(
				'Superuser must be assigned to is_superuser=True.')
		super_user = self.create_user(username,email,first_name, last_name, password, **other_fields)
		return super_user

	def create_user(self, username,email, first_name, last_name, password,**other_fields):
		if not email:
			raise ValueError(_('You must provide an email address'))
		email = self.normalize_email(email)
		user = self.model(username=username, email=email, first_name=first_name, last_name=last_name, **other_fields)
		user.set_password(password)
		user.save()
		return user


def user_directory_path(instance, filename):
	return f'users/{instance.email}/images/{filename}'

class CustomUser(AbstractBaseUser, PermissionsMixin):
	GENDER_CHOICES = (
		('','Choose gender'),
		('Male', 'Male'),
		('Female', 'Female'),
		('Others', 'Others'),
	)
	username = models.CharField(max_length=191,unique=True)
	email = models.EmailField(_('email address'),unique=True)
	first_name = models.CharField(max_length=255,blank=True)
	last_name = models.CharField(max_length=255,blank=True)
	gender = models.CharField(max_length=255, choices=GENDER_CHOICES,blank=True)
	avatar = models.ImageField(upload_to=user_directory_path, default="profile/image/default.jpg")
	dob = models.CharField(max_length=255,blank=True,null=True,help_text="Pattern = dd-mm-yyyy")
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)# Validators should be a list
	groups = models.ManyToManyField(Group,blank=True)
	about = models.TextField(_('about'),max_length=500,blank=True)

	facebook_url = models.URLField(max_length = 255, null=True, blank=True)
	twitter_url = models.URLField(max_length = 255, null=True, blank=True)
	linkedin_url = models.URLField(max_length = 255, null=True, blank=True)
	
	is_staff = models.BooleanField(default=False)
	is_active = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True) #Automatically set the field to now when the object is first created.
	updated_at = models.DateTimeField(auto_now=True) #Automatically set the field to now every time the object is saved.
	
	objects = CustomAccountManager()

	USERNAME_FIELD = 'email'  
	REQUIRED_FIELDS = ['username','first_name','last_name']
	

	def __str__(self):
		return self.username