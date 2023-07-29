from django.contrib.auth.models import BaseUserManager
class UserManager(BaseUserManager):

    def create_user(self, email, username, contact,is_admin, password=None,password2=None, department=None, profile_image=None):
        if not email:
            raise ValueError('Users must have an Email address')
        if not username:
            raise ValueError('Users must have an Username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            contact=contact,
            is_admin=is_admin,
            department=department,
            profile_image=profile_image
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, contact,is_admin, password=None):
        user = self.create_user(
            email,
            password=password,
            username=username,
            contact=contact,
            is_admin=is_admin
        )
        user.save(using=self._db)
        return user    