def user_profile_type(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'freelancer_profile'):
            return {'user_type': 'freelancer'}
        elif hasattr(request.user, 'client_profile'):
            return {'user_type': 'client'}
    return {'user_type': 'guest'}