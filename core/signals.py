from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import transaction
import logging

logger = logging.getLogger(__name__)
User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if not created or not hasattr(instance, '_profile_role'):
        return
        
    role = instance._profile_role
    logger.info(f"Creating profile for user {instance.username} with role {role}")
    
    try:
        with transaction.atomic():
            # Import local para evitar circular imports
            from .services import UserService
            
            # Crear el perfil
            profile = UserService.create_profile(instance, role)
            
            if profile:
                logger.info(f"Profile {role} created successfully for user {instance.username}")
            else:
                logger.error(f"Profile creation returned None for user {instance.username}")
                
        # Limpiar el atributo temporal solo si todo fue exitoso
        if hasattr(instance, '_profile_role'):
            delattr(instance, '_profile_role')
            
    except Exception as e:
        logger.error(f"Error creating profile for user {instance.username}: {str(e)}")
        # No re-lanzar excepción para no fallar el registro del usuario