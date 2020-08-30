from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# 登録処理
class UserManager(BaseUserManager):
    # ユーザー登録時
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            username = username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # 管理者ユーザー登録時
    def create_superuser(self, username, password):
        user = self.create_user(
            username,
            password=password,
        )
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)
        return user

# カスタムユーザーモデル
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=20, unique=True)
    # user_image = models.ImageField(upload_to="images/profiles/", default="images/profiles/no_image.png")
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELD = []

    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perm(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin
    