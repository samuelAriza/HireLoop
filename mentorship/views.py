"""
Mentorship Views - Presentation Layer

Following SOLID principles and Clean Architecture:
- Single Responsibility: Each view has one clear purpose
- Separation of Concerns: Views handle only presentation logic
- Dependency Inversion: Depends on service abstractions
- Clean, maintainable code with proper error handling
"""

from django.forms import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.utils import timezone

from core.services import MentorshipService
from .models import MentorshipSession, MentorshipReview, MentorshipCartItem, MentorshipWishlistItem
from .forms import (
    MentorshipSessionForm, 
    MentorshipSearchForm, 
    MentorshipFilterForm,
    get_search_form,
    get_filter_form
)


class MentorshipListView(ListView):
    """
    Vista para listar mentorías disponibles.
    Sigue SRP: Solo maneja listado y búsqueda de mentorías.
    """
    model = MentorshipSession
    template_name = 'mentorship/mentorship_list.html'
    context_object_name = 'mentorships'
    paginate_by = 12
    
    def __init__(self):
        super().__init__()
        self.service = MentorshipService()
    
    def get_queryset(self):
        """Obtiene mentorías filtradas usando el servicio"""
        # Obtener parámetros de búsqueda
        search_query = self.request.GET.get('search', '')
        category = self.request.GET.get('category', '')
        min_price = self.request.GET.get('min_price', '')
        max_price = self.request.GET.get('max_price', '')
        duration = self.request.GET.get('duration', '')
        
        # Usar el servicio para obtener mentorías disponibles
        queryset = self.service.get_available_mentorships(category=category if category else None)
        
        # Aplicar filtros adicionales
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | 
                Q(description__icontains=search_query) |
                Q(mentor__user__username__icontains=search_query) |
                Q(mentor__user__first_name__icontains=search_query) |
                Q(mentor__user__last_name__icontains=search_query)
            )
            
        if min_price:
            try:
                queryset = queryset.filter(price__gte=float(min_price))
            except ValueError:
                pass
                
        if max_price:
            try:
                queryset = queryset.filter(price__lte=float(max_price))
            except ValueError:
                pass
                
        if duration:
            try:
                queryset = queryset.filter(duration_hours=int(duration))
            except ValueError:
                pass
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Usar factory para crear el formulario de búsqueda
        context['search_form'] = get_search_form(
            request_data=self.request.GET,
            user=self.request.user if self.request.user.is_authenticated else None
        )
        
        # Pasar filtros actuales al template
        context['current_filters'] = {
            'search': self.request.GET.get('search', ''),
            'category': self.request.GET.get('category', ''),
            'min_price': self.request.GET.get('min_price', ''),
            'max_price': self.request.GET.get('max_price', ''),
            'duration': self.request.GET.get('duration', ''),
        }
        
        # Verificar si hay filtros aplicados
        context['has_filters'] = any(context['current_filters'].values())
        
        return context


class MentorshipDetailView(DetailView):
    """
    Vista de detalle de mentoría.
    Sigue SRP: Solo maneja visualización de mentoría individual.
    """
    model = MentorshipSession
    template_name = 'mentorship/mentorship_detail.html'
    context_object_name = 'mentorship'
    pk_url_kwarg = 'pk'
    
    def __init__(self):
        super().__init__()
        self.service = MentorshipService()
    
    def get_queryset(self):
        # Si el usuario es mentor o mentee, puede ver incluso si no está disponible
        if self.request.user.is_authenticated and hasattr(self.request.user, 'freelancerprofile'):
            return MentorshipSession.objects.select_related('mentor__user', 'mentee__user')
        
        # Para otros usuarios, solo mentorías disponibles
        return self.service.get_available_mentorships()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mentorship = self.get_object()
        
        # Verificar si el usuario es el propietario
        is_owner = False
        if (self.request.user.is_authenticated and 
            hasattr(self.request.user, 'freelancerprofile')):
            is_owner = mentorship.mentor == self.request.user.freelancerprofile
        
        context['is_owner'] = is_owner
        context['is_mentor'] = is_owner  # Alias para compatibilidad
        
        # Agregar información del carrito y wishlist
        if self.request.user.is_authenticated:
            try:
                from core.services.cart_service import UnifiedCartService
                from core.services.wishlist_service import UnifiedWishlistService
                
                # Create service instances
                cart_service = UnifiedCartService()
                wishlist_service = UnifiedWishlistService()
                
                context['in_cart'] = cart_service.is_in_cart(self.request.user, mentorship)
                context['in_wishlist'] = wishlist_service.is_in_wishlist(self.request.user, mentorship)
                context['cart_count'] = cart_service.get_cart_count(self.request.user)
                context['wishlist_count'] = wishlist_service.get_wishlist_count(self.request.user)
            except Exception as e:
                context['in_cart'] = False
                context['in_wishlist'] = False
                context['cart_count'] = 0
                context['wishlist_count'] = 0
                print(f"Error getting cart/wishlist info: {e}")
        else:
            context['in_cart'] = False
            context['in_wishlist'] = False
            context['cart_count'] = 0
            context['wishlist_count'] = 0
        
        # Agregar reviews si existen
        try:
            context['review'] = mentorship.review
        except MentorshipReview.DoesNotExist:
            context['review'] = None
        
        return context
    
    def post(self, request, *args, **kwargs):
        """Manejar reserva de mentoría o envío de reseña"""
        mentorship = self.get_object()
        action = request.POST.get('action')
        
        if action == 'book':
            return self._handle_booking(request, mentorship)
        elif action == 'review':
            return self._handle_review(request, mentorship)
        
        return redirect('mentorship:mentorship_detail', pk=mentorship.id)
    
    def _handle_booking(self, request, mentorship):
        """Maneja la reserva de mentoría usando el servicio"""
        if not request.user.is_authenticated:
            messages.error(request, "Debes iniciar sesión para reservar mentorías")
            return redirect('core:login')
        
        try:
            # Obtener datos adicionales del POST si existen
            booking_data = {}
            if 'scheduled_date' in request.POST:
                booking_data['scheduled_date'] = request.POST['scheduled_date']
            if 'notes' in request.POST:
                booking_data['notes'] = request.POST['notes']
            
            booking = self.service.book_mentorship(
                mentorship, 
                request.user, 
                booking_data if booking_data else None
            )
            messages.success(request, "¡Mentoría reservada exitosamente!")
        except (PermissionDenied, ValidationError) as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, "Error inesperado al reservar la mentoría")
        
        return redirect('mentorship:mentorship_detail', pk=mentorship.id)
    
    def _handle_review(self, request, mentorship):
        """Maneja el envío de reseñas"""
        from .forms import MentorshipReviewForm
        
        form = MentorshipReviewForm(request.POST)
        if form.is_valid():
            try:
                review = form.save(commit=False)
                review.session = mentorship
                review.reviewer = request.user.freelancerprofile
                review.save()
                messages.success(request, "¡Reseña enviada exitosamente!")
            except Exception as e:
                messages.error(request, str(e))
        else:
            messages.error(request, "Por favor corrige los errores en la reseña")
        
        return redirect('mentorship:mentorship_detail', pk=mentorship.id)


class FreelancerMentorshipsView(LoginRequiredMixin, ListView):
    """
    Vista para que freelancers gestionen sus mentorías.
    Sigue SRP: Solo maneja mentorías del freelancer actual.
    """
    template_name = 'mentorship/freelancer_mentorships.html'
    context_object_name = 'mentorships'
    paginate_by = 10
    
    def __init__(self):
        super().__init__()
        self.service = MentorshipService()
    
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'freelancerprofile'):
            messages.error(request, "Solo los freelancers pueden acceder a esta sección")
            return redirect('core:multi_profile_detail')
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        """Usar el servicio para obtener mentorías del freelancer"""
        return self.service.get_mentor_mentorships(self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener QuerySet base SIN paginación para estadísticas
        all_mentorships = self.service.get_mentor_mentorships(self.request.user)
        
        # Estadísticas usando el QuerySet completo
        context['stats'] = {
            'total_mentorships': all_mentorships.count(),
            'available_mentorships': all_mentorships.filter(status=MentorshipSession.AVAILABLE).count(),
            'booked_mentorships': all_mentorships.filter(status=MentorshipSession.BOOKED).count(),
            'completed_mentorships': all_mentorships.filter(status=MentorshipSession.COMPLETED).count(),
        }
        
        # Reservas donde es mentee y como mentor (si los métodos existen)
        try:
            context['mentee_bookings'] = self.service.get_mentee_bookings(self.request.user)
        except AttributeError:
            # Method doesn't exist, provide empty list
            context['mentee_bookings'] = []
            
        try:
            context['mentor_bookings'] = self.service.get_mentor_bookings(self.request.user)
        except AttributeError:
            # Method doesn't exist, provide empty list
            context['mentor_bookings'] = []
        
        return context


class CreateMentorshipView(LoginRequiredMixin, FormView):
    """
    Vista para crear nuevas mentorías.
    Sigue SRP: Solo maneja creación de mentorías.
    """
    template_name = 'mentorship/create_mentorship.html'
    form_class = MentorshipSessionForm
    success_url = reverse_lazy('mentorship:freelancer_mentorships')
    
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'freelancerprofile'):
            messages.error(request, "Solo los freelancers pueden crear mentorías")
            return redirect('core:multi_profile_detail')
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        """Handle POST request with debugging"""
        print("=== DEBUG: POST request received ===")
        print(f"POST data: {request.POST}")
        print(f"User: {request.user}")
        print(f"User authenticated: {request.user.is_authenticated}")
        
        if hasattr(request.user, 'freelancerprofile'):
            print(f"Freelancer profile: {request.user.freelancerprofile}")
        else:
            print("User has no freelancer profile!")
            
        return super().post(request, *args, **kwargs)
    
    def get_form_kwargs(self):
        """Pass current user to form"""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        """Usar el servicio de core para crear la mentoría"""
        print("=== DEBUG: form_valid called ===")
        print(f"Form data: {form.cleaned_data}")
        print(f"User: {self.request.user}")
        print(f"Has freelancer profile: {hasattr(self.request.user, 'freelancerprofile')}")
        
        try:
            from core.services import MentorshipService
            
            # Crear instancia del servicio
            mentorship_service = MentorshipService()
            print("=== DEBUG: Service created ===")
            
            # Preparar datos para el servicio
            mentorship_data = form.cleaned_data.copy()
            mentorship_data['mentor'] = self.request.user.freelancerprofile
            print(f"=== DEBUG: Mentorship data: {mentorship_data} ===")
            
            # Crear la mentoría usando el servicio
            mentorship = mentorship_service.create_mentorship_session(
                mentor=self.request.user.freelancerprofile,
                **mentorship_data
            )
            print(f"=== DEBUG: Service result: {mentorship} ===")
            
            if mentorship:
                print("=== DEBUG: Mentorship created successfully ===")
                messages.success(
                    self.request,
                    f"¡Mentoría '{mentorship.title}' creada exitosamente!"
                )
                return super().form_valid(form)
            else:
                print("=== DEBUG: Service returned None ===")
                print(f"Service errors: {mentorship_service.errors}")
                messages.error(self.request, f"Error al crear la mentoría: {mentorship_service.errors}")
                return self.form_invalid(form)
                
        except Exception as e:
            print(f"=== DEBUG: Exception in service: {str(e)} ===")
            # Fallback: crear directamente si el servicio falla
            try:
                from mentorship.models import MentorshipSession
                print("=== DEBUG: Trying direct model creation ===")
                
                mentorship = MentorshipSession.objects.create(
                    title=form.cleaned_data['title'],
                    description=form.cleaned_data['description'],
                    category=form.cleaned_data['category'],
                    price=form.cleaned_data['price'],
                    duration_hours=form.cleaned_data['duration_hours'],
                    notes=form.cleaned_data.get('notes', ''),
                    mentor=self.request.user.freelancerprofile,
                )
                print(f"=== DEBUG: Direct creation successful: {mentorship} ===")
                
                messages.success(
                    self.request,
                    f"¡Mentoría '{mentorship.title}' creada exitosamente!"
                )
                return super().form_valid(form)
                
            except Exception as create_error:
                print(f"=== DEBUG: Direct creation failed: {str(create_error)} ===")
                messages.error(self.request, f"Error al crear la mentoría: {str(create_error)}")
                return self.form_invalid(form)
    
    def form_invalid(self, form):
        """Handle form validation errors"""
        print("=== DEBUG: form_invalid called ===")
        print(f"Form errors: {form.errors}")
        print(f"Form non-field errors: {form.non_field_errors}")
        
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        """Add additional context"""
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Crear Nueva Mentoría'
        return context


class UpdateMentorshipView(LoginRequiredMixin, FormView):
    """
    Vista para actualizar mentorías existentes.
    Sigue SRP: Solo maneja edición de mentorías.
    """
    template_name = 'mentorship/update_mentorship.html'
    form_class = MentorshipSessionForm
    
    def __init__(self):
        super().__init__()
        self.service = MentorshipService()
    
    def get_mentorship(self):
        mentorship_id = self.kwargs.get('mentorship_id')
        return get_object_or_404(MentorshipSession, id=mentorship_id)
    
    def dispatch(self, request, *args, **kwargs):
        mentorship = self.get_mentorship()
        if not hasattr(request.user, 'freelancerprofile') or mentorship.mentor.user != request.user:
            raise PermissionDenied("Solo el mentor puede editar esta sesión")
        return super().dispatch(request, *args, **kwargs)
    
    def get_form_kwargs(self):
        """Pass current user to form"""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_initial(self):
        mentorship = self.get_mentorship()
        return {
            'title': mentorship.title,
            'description': mentorship.description,
            'category': mentorship.category,
            'price': mentorship.price,
            'duration_hours': mentorship.duration_hours,
            'notes': mentorship.notes,
        }
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mentorship'] = self.get_mentorship()
        return context
    
    def form_valid(self, form):
        """Usar el servicio para actualizar la mentoría"""
        print("=== DEBUG: UpdateMentorshipView form_valid called ===")
        
        try:
            mentorship = self.get_mentorship()
            
            # Actualizar directamente los campos del objeto
            mentorship.title = form.cleaned_data['title']
            mentorship.description = form.cleaned_data['description']
            mentorship.category = form.cleaned_data['category']
            mentorship.price = form.cleaned_data['price']
            mentorship.duration_hours = form.cleaned_data['duration_hours']
            mentorship.notes = form.cleaned_data.get('notes', '')
            mentorship.save()
            
            print(f"=== DEBUG: Mentorship updated: {mentorship.title} ===")
            
            messages.success(
                self.request,
                f"¡Mentoría '{mentorship.title}' actualizada exitosamente!"
            )
            return redirect('mentorship:freelancer_mentorships')
            
        except Exception as e:
            print(f"=== DEBUG: Error updating mentorship: {str(e)} ===")
            messages.error(self.request, f"Error al actualizar la mentoría: {str(e)}")
            return self.form_invalid(form)
    
    def form_invalid(self, form):
        """Handle form validation errors"""
        print("=== DEBUG: UpdateMentorshipView form_invalid called ===")
        print(f"Form errors: {form.errors}")
        
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        
        return super().form_invalid(form)


class DeleteMentorshipView(LoginRequiredMixin, View):
    """
    Vista para eliminar mentorías.
    Sigue SRP: Solo maneja eliminación de mentorías.
    """
    
    def __init__(self):
        super().__init__()
        self.service = MentorshipService()
    
    def get_mentorship(self, mentorship_id):
        return get_object_or_404(MentorshipSession, id=mentorship_id)
    
    def dispatch(self, request, *args, **kwargs):
        mentorship_id = self.kwargs.get('mentorship_id')
        mentorship = self.get_mentorship(mentorship_id)
        if not hasattr(request.user, 'freelancerprofile') or mentorship.mentor.user != request.user:
            raise PermissionDenied("Solo el mentor puede eliminar esta sesión")
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        """Mostrar página de confirmación de eliminación"""
        mentorship_id = self.kwargs.get('mentorship_id')
        mentorship = self.get_mentorship(mentorship_id)
        
        context = {
            'mentorship': mentorship,
            'page_title': 'Eliminar Mentoría'
        }
        
        return render(request, 'mentorship/delete_mentorship.html', context)
    
    def post(self, request, *args, **kwargs):
        """Eliminar la mentoría"""
        print("=== DEBUG: DeleteMentorshipView POST called ===")
        
        try:
            mentorship_id = self.kwargs.get('mentorship_id')
            mentorship = self.get_mentorship(mentorship_id)
            mentorship_title = mentorship.title
            
            print(f"=== DEBUG: Deleting mentorship: {mentorship_title} ===")
            
            # Eliminar directamente
            mentorship.delete()
            
            print(f"=== DEBUG: Mentorship deleted successfully ===")
            
            messages.success(request, f"Mentoría '{mentorship_title}' eliminada exitosamente")
            return redirect('mentorship:freelancer_mentorships')
            
        except Exception as e:
            print(f"=== DEBUG: Error deleting mentorship: {str(e)} ===")
            messages.error(request, f"Error al eliminar la mentoría: {str(e)}")
            return redirect('mentorship:freelancer_mentorships')


class MentorshipStatusView(LoginRequiredMixin, View):
    """
    Vista para cambiar estado de mentorías (completar, cancelar).
    Sigue SRP: Solo maneja cambios de estado.
    """
    
    def __init__(self):
        super().__init__()
        self.service = MentorshipService()
    
    def post(self, request, mentorship_id):
        mentorship = get_object_or_404(MentorshipSession, id=mentorship_id)
        action = request.POST.get('action')
        
        try:
            if action == 'complete':
                # Para completar necesitamos el booking
                booking = mentorship.mentorshipbooking_set.filter(
                    status='CONFIRMED'
                ).first()
                
                if booking:
                    self.service.complete_mentorship(booking, request.user)
                    messages.success(request, "Sesión marcada como completada")
                else:
                    messages.error(request, "No se encontró una reserva confirmada para completar")
                    
            elif action == 'cancel':
                # Para cancelar también necesitamos el booking
                booking = mentorship.mentorshipbooking_set.filter(
                    status__in=['PENDING', 'CONFIRMED']
                ).first()
                
                if booking:
                    self.service.cancel_booking(booking, request.user)
                    messages.success(request, "Sesión cancelada exitosamente")
                else:
                    messages.error(request, "No se encontró una reserva activa para cancelar")
            else:
                messages.error(request, "Acción no válida")
                
        except (PermissionDenied, ValidationError) as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, "Error inesperado al procesar la acción")
        
        return redirect('mentorship:mentorship_detail', pk=mentorship.id)


class MentorshipBookingListView(LoginRequiredMixin, ListView):
    """
    Vista para listar reservas de mentorías del usuario actual.
    Muestra tanto las reservas como mentor como mentee.
    """
    template_name = 'mentorship/booking_list.html'
    context_object_name = 'bookings'
    paginate_by = 10
    
    def __init__(self):
        super().__init__()
        self.service = MentorshipService()
    
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'freelancerprofile'):
            messages.error(request, "Solo los freelancers pueden acceder a esta sección")
            return redirect('core:multi_profile_detail')
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        """Combinar reservas como mentor y mentee"""
        role = self.request.GET.get('role', 'all')
        
        if role == 'mentor':
            return self.service.get_mentor_bookings(self.request.user)
        elif role == 'mentee':
            return self.service.get_mentee_bookings(self.request.user)
        else:
            # Combinar ambas listas
            mentor_bookings = self.service.get_mentor_bookings(self.request.user)
            mentee_bookings = self.service.get_mentee_bookings(self.request.user)
            
            # Crear lista unificada con información del rol
            all_bookings = []
            for booking in mentor_bookings:
                booking.user_role = 'mentor'
                all_bookings.append(booking)
            for booking in mentee_bookings:
                booking.user_role = 'mentee'
                all_bookings.append(booking)
            
            # Ordenar por fecha de creación
            all_bookings.sort(key=lambda x: x.created_at, reverse=True)
            return all_bookings
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_role'] = self.request.GET.get('role', 'all')
        
        # Filtro form
        context['filter_form'] = get_filter_form(
            request_data=self.request.GET,
            user=self.request.user
        )
        
        return context


# Vistas para carrito y wishlist de mentorías
class AddMentorshipToCartView(LoginRequiredMixin, View):
    """Vista para agregar mentorías al carrito"""
    
    def post(self, request, mentorship_id):
        print(f"=== DEBUG: AddMentorshipToCartView POST ===")
        print(f"User: {request.user}")
        print(f"Mentorship ID: {mentorship_id}")
        
        try:
            from mentorship.models import MentorshipSession
            mentorship = get_object_or_404(MentorshipSession, id=mentorship_id)
            
            print(f"Mentorship found: {mentorship}")
            
            # Verificar que el usuario no sea el creador de la mentoría
            if (hasattr(request.user, 'freelancerprofile') and 
                mentorship.mentor == request.user.freelancerprofile):
                messages.error(request, "No puedes agregar tus propias mentorías al carrito")
                return redirect('mentorship:mentorship_detail', pk=mentorship_id)
            
            print("Owner check passed")
            
            # Verificar que la mentoría esté disponible
            if mentorship.status != MentorshipSession.AVAILABLE:
                messages.error(request, "Esta mentoría no está disponible")
                return redirect('mentorship:mentorship_detail', pk=mentorship_id)
            
            print("Status check passed")
            
            from core.services.cart_service import UnifiedCartService
            # Create service instance
            cart_service = UnifiedCartService()
            
            print("Cart service created")
            
            # Verificar si ya está en el carrito
            if cart_service.is_in_cart(request.user, mentorship):
                print("Already in cart")
                messages.info(request, f"'{mentorship.title}' ya está en tu carrito")
            else:
                print("Adding to cart...")
                result = cart_service.add_to_cart(request.user, mentorship)
                print(f"Add to cart result: {result}")
                
                if result:
                    messages.success(request, f"'{mentorship.title}' agregada al carrito exitosamente")
                else:
                    messages.error(request, f"Error al agregar '{mentorship.title}' al carrito")
            
        except Exception as e:
            print(f"Error in AddMentorshipToCartView: {e}")
            import traceback
            traceback.print_exc()
            messages.error(request, f"Error al agregar al carrito: {str(e)}")
        
        print("=== END DEBUG ===")
        return redirect('mentorship:mentorship_detail', pk=mentorship_id)
    
    def get(self, request, mentorship_id):
        """Redirect GET requests to mentorship detail"""
        return redirect('mentorship:mentorship_detail', pk=mentorship_id)


class RemoveMentorshipFromCartView(LoginRequiredMixin, View):
    """Vista para remover mentorías del carrito"""
    
    def post(self, request, mentorship_id):
        try:
            from mentorship.models import MentorshipSession
            mentorship = get_object_or_404(MentorshipSession, id=mentorship_id)
            
            from core.services.cart_service import UnifiedCartService
            # Create service instance
            cart_service = UnifiedCartService()
            cart_service.remove_from_cart(request.user, mentorship)
            
            messages.success(request, f"'{mentorship.title}' removida del carrito")
        except Exception as e:
            messages.error(request, str(e))
        
        return redirect('services:cart_view')


class AddMentorshipToWishlistView(LoginRequiredMixin, View):
    """Vista para agregar mentorías a la wishlist"""
    
    def post(self, request, mentorship_id):
        try:
            from mentorship.models import MentorshipSession
            mentorship = get_object_or_404(MentorshipSession, id=mentorship_id)
            
            from core.services.wishlist_service import UnifiedWishlistService
            # Create service instance
            wishlist_service = UnifiedWishlistService()
            
            # Verificar si ya está en wishlist
            if wishlist_service.is_in_wishlist(request.user, mentorship):
                messages.info(request, f"'{mentorship.title}' ya está en tus favoritos")
            else:
                wishlist_service.add_to_wishlist(request.user, mentorship)
                messages.success(request, f"'{mentorship.title}' agregada a favoritos exitosamente")
                
        except Exception as e:
            messages.error(request, f"Error al agregar a favoritos: {str(e)}")
            print(f"Wishlist error: {e}")  # Para debugging
        
        return redirect('mentorship:mentorship_detail', pk=mentorship_id)
    
    def get(self, request, mentorship_id):
        """Redirect GET requests to mentorship detail"""
        return redirect('mentorship:mentorship_detail', pk=mentorship_id)


class RemoveMentorshipFromWishlistView(LoginRequiredMixin, View):
    """Vista para remover mentorías de la wishlist"""
    
    def post(self, request, mentorship_id):
        try:
            from mentorship.models import MentorshipSession
            mentorship = get_object_or_404(MentorshipSession, id=mentorship_id)
            
            from core.services.wishlist_service import UnifiedWishlistService
            # Create service instance
            wishlist_service = UnifiedWishlistService()
            wishlist_service.remove_from_wishlist(request.user, mentorship)
            
            messages.success(request, f"'{mentorship.title}' removida de favoritos")
        except Exception as e:
            messages.error(request, str(e))
        
        return redirect('services:wishlist_view')


# API Views para AJAX requests
class MentorshipAPIView(LoginRequiredMixin, View):
    """
    Vista API para operaciones AJAX con mentorías.
    Proporciona endpoints para operaciones rápidas.
    """
    
    def __init__(self):
        super().__init__()
        self.service = MentorshipService()
    
    def post(self, request, mentorship_id):
        """Manejar operaciones POST via AJAX"""
        mentorship = get_object_or_404(MentorshipSession, id=mentorship_id)
        action = request.POST.get('action')
        
        try:
            if action == 'quick_book':
                booking = self.service.book_mentorship(mentorship, request.user)
                return JsonResponse({
                    'success': True,
                    'message': 'Mentoría reservada exitosamente',
                    'booking_id': str(booking.id)
                })
            
            elif action == 'check_availability':
                is_available = mentorship.is_available
                return JsonResponse({
                    'success': True,
                    'available': is_available,
                    'status': mentorship.status
                })
            
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Acción no válida'
                }, status=400)
                
        except (PermissionDenied, ValidationError) as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'Error inesperado'
            }, status=500)