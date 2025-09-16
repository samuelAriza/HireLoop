from typing import Optional
from .base import BaseRepository
from ..validators.email_validator import EmailValidator

class FreelancerProfileRepository(BaseRepository):
    """Repositorio específico para FreelancerProfile - SRP"""
    
    def get_by_user(self, user):
        try:
            return user.freelancerprofile
        except AttributeError:
            return None
    
    def create(self, user, data: dict = None):
        from ..models import FreelancerProfile
        return FreelancerProfile.objects.create(
            user=user,
            skills=data.get('skills', []) if data else [],
            bio=data.get('bio', '') if data else ''
        )
    
    def update(self, profile, data: dict):
        if 'skills' in data:
            skills = data['skills']
            if isinstance(skills, list):
                profile.skills = skills
            elif isinstance(skills, str):
                profile.skills = [s.strip() for s in skills.split(',') if s.strip()]
        
        if 'bio' in data:
            profile.bio = data['bio']
        
        profile.save()
        return profile
    
    def delete(self, profile) -> bool:
        profile.delete()
        return True

class ClientProfileRepository(BaseRepository):
    """Repositorio específico para ClientProfile - SRP"""
    
    def get_by_user(self, user):
        try:
            return user.clientprofile
        except AttributeError:
            return None
    
    def create(self, user, data: dict = None):
        from ..models import ClientProfile
        return ClientProfile.objects.create(
            user=user,
            company=data.get('company', '') if data else '',
            billing_email=data.get('billing_email', '') if data else ''
        )
    
    def update(self, profile, data: dict):
        if 'company' in data:
            profile.company = data['company']
        
        if 'billing_email' in data:
            billing_email = data['billing_email']
            if billing_email:
                EmailValidator.validate_unique_email(billing_email, profile.user.id)
            profile.billing_email = billing_email
        
        profile.save()
        return profile
    
    def delete(self, profile) -> bool:
        profile.delete()
        return True