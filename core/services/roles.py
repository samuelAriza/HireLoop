def get_user_roles(user):
    """
    Return list of user roles based on profile existence.
    """
    roles = []
    if user.has_freelancer_profile:
        roles.append('Freelancer')
    if user.has_client_profile:
        roles.append('Cliente')
    return roles


def get_primary_role(user):
    """
    Return the primary role of the user.
    """
    roles = get_user_roles(user)
    if len(roles) == 1:
        return roles[0]
    elif len(roles) > 1:
        return "Múltiples roles"
    return "Sin rol asignado"