from typing import List, Optional
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.contrib import messages

from .action_handlers import ActionHandler
from .profile_service import ProfileService

class ActionDispatcher:
    """
    Dispatcher for handling different actions - Open/Closed Principle.
    Easy to extend with new handlers without modifying existing code.
    """
    def __init__(self, profile_service: ProfileService):
        self.profile_service = profile_service
        self.handlers: List[ActionHandler] = []
        self._register_default_handlers()
    
    def _register_default_handlers(self):
        """Register all default action handlers - Dependency Inversion Principle."""
        from .action_handlers import (
            ProfileImageUpdateHandler,
            ProfileImageDeleteHandler,
            ProfileDeleteHandler,
            ProfileUpdateHandler,
            PortfolioUpdateHandler,
            PortfolioDeleteHandler
        )
        
        self.handlers = [
            ProfileImageUpdateHandler(self.profile_service),
            ProfileImageDeleteHandler(self.profile_service),
            ProfileDeleteHandler(self.profile_service),
            PortfolioUpdateHandler(),
            PortfolioDeleteHandler(),
            ProfileUpdateHandler(self.profile_service),  # Default handler, should be last
        ]
    
    def register_handler(self, handler: ActionHandler):
        """Register a new action handler - Open/Closed Principle."""
        self.handlers.insert(-1, handler)  # Insert before default handler
    
    def dispatch(self, request: HttpRequest, action: str, **kwargs) -> HttpResponse:
        """
        Dispatch action to appropriate handler.
        Follows Single Responsibility and Open/Closed Principles.
        """
        for handler in self.handlers:
            if handler.can_handle(action):
                return handler.handle(request, **kwargs)
        
        # No handler found
        messages.error(request, f'Unknown action: {action}')
        return redirect('core:profile_detail')