# Solo exportar las clases principales que se usan externamente
# Evitar importaciones circulares manteniendo __init__.py simple

__all__ = [
    'UserRegisterView', 'UserLoginView', 'UserLogoutView',
    'ProfileDetailView', 'FreelancerProfileCreateView', 'ClientProfileCreateView',
    'PortfolioListView', 'PortfolioCreateView', 'PortfolioUpdateView', 'PortfolioDeleteView'
]

# Las importaciones se hacen bajo demanda para evitar circularidad
def __getattr__(name):
    if name == 'UserRegisterView':
        from .auth_views import UserRegisterView
        return UserRegisterView
    elif name == 'UserLoginView':
        from .auth_views import UserLoginView
        return UserLoginView
    elif name == 'UserLogoutView':
        from .auth_views import UserLogoutView
        return UserLogoutView
    elif name == 'ProfileDetailView':
        from .profile_views import ProfileDetailView
        return ProfileDetailView
    elif name == 'FreelancerProfileCreateView':
        from .profile_views import FreelancerProfileCreateView
        return FreelancerProfileCreateView
    elif name == 'ClientProfileCreateView':
        from .profile_views import ClientProfileCreateView
        return ClientProfileCreateView
    elif name == 'ProfileImageUpdateView':
        from .image_views import ProfileImageUpdateView
        return ProfileImageUpdateView
    elif name == 'ProfileImageDeleteView':
        from .image_views import ProfileImageDeleteView
        return ProfileImageDeleteView
    elif name == 'PortfolioListView':
        from .portfolio_views import PortfolioListView
        return PortfolioListView
    elif name == 'PortfolioCreateView':
        from .portfolio_views import PortfolioCreateView
        return PortfolioCreateView
    elif name == 'PortfolioUpdateView':
        from .portfolio_views import PortfolioUpdateView
        return PortfolioUpdateView
    elif name == 'PortfolioDeleteView':
        from .portfolio_views import PortfolioDeleteView
        return PortfolioDeleteView
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
