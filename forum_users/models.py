from django.db import models
from django.contrib.auth.models import AbstractUser,UserManager

class CustomUserManager(UserManager):
    def create_user(self, username, password=None,**extra_fields):
        if not username:
            print("Needed Username")

        extra_fields.pop("email",None)
        extra_fields.pop("last_name",None)
        extra_fields.pop("first_name",None)

        user = self.model(
            username = username,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
class CustomUser(AbstractUser):
    date_joined = models.DateTimeField(auto_now_add=True)
    email = None
    last_name = None
    first_name = None
    class UserType(models.IntegerChoices):
        USER = 1, 'User'
        VIP = 2, 'VIP' 
        SVIP = 3, 'Super_VIP'
        MOD = 4, 'Moderator'
        HMOD = 5, 'Head_Moderator'
    user_money = models.IntegerField(default=0)
    user_type = models.IntegerField(choices=UserType.choices , default=UserType.USER)
    objects = CustomUserManager()
    USERNAME_FIELD = "username"

    def __str__(self):
        return self.username
    
    def is_regular_user(self):
        return self.user_type == self.UserType.USER
   
    def is_vip(self):
        return self.user_type == self.UserType.VIP
   
    def is_svip(self):
        return self.user_type == self.UserType.SVIP
        
    def is_mod(self):
        return self.user_type == self.UserType.MOD
        
    def is_head_mod(self): 
        return self.user_type == self.UserType.HMOD