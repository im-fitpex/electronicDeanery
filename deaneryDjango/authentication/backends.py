from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User as DjangoUser
from core.models import User as CustomUser
import hashlib


class CustomUserBackend(BaseBackend):
    """
    Custom authentication backend that works with our existing users table
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Get user from our custom users table
            custom_user = CustomUser.objects.get(username=username)
            
            # Simple password verification (you should implement proper password hashing)
            # For now, we'll just check if the password matches the stored hash
            if self.check_password(password, custom_user.password_hash, custom_user.salt):
                # Create or get Django user
                django_user, created = DjangoUser.objects.get_or_create(
                    username=username,
                    defaults={
                        'email': custom_user.email,
                        'is_active': custom_user.is_active,
                    }
                )
                return django_user
        except CustomUser.DoesNotExist:
            return None
        except Exception:
            return None
    
    def check_password(self, password, stored_hash, salt):
        """
        Simple password checking - you should implement your actual password verification logic
        """
        # This is a placeholder - implement your actual password hashing logic
        test_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        return test_hash == stored_hash
    
    def get_user(self, user_id):
        try:
            return DjangoUser.objects.get(pk=user_id)
        except DjangoUser.DoesNotExist:
            return None