def user_profile_type(request):
    user_types = []
    if request.user.is_authenticated:
        if hasattr(request.user, 'freelancer_profile'):
            user_types.append('freelancer')
        if hasattr(request.user, 'client_profile'):
            user_types.append('client')
    return {'user_type': user_types}