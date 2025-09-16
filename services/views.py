from django.forms import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Service
from .forms import ServiceSearchForm


class ServiceListView(ListView):
    """
    Vista para listar servicios disponibles.
    Incluye funcionalidad de búsqueda y filtrado.
    """
    model = Service
    template_name = 'services/service_list.html'
    context_object_name = 'services'
    paginate_by = 12
    
    def get_queryset(self):
        """Obtiene servicios filtrados por búsqueda"""
        queryset = Service.objects.filter(active=True).select_related('freelancer__user')
        
        # Obtener parámetros de búsqueda
        search_query = self.request.GET.get('search', '')
        category = self.request.GET.get('category', '')
        min_price = self.request.GET.get('min_price', '')
        max_price = self.request.GET.get('max_price', '')
        delivery_time = self.request.GET.get('delivery_time', '')
        rating = self.request.GET.get('rating', '')
        
        # Aplicar filtros
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | 
                Q(description__icontains=search_query) |
                Q(freelancer__user__username__icontains=search_query) |
                Q(freelancer__user__first_name__icontains=search_query) |
                Q(freelancer__user__last_name__icontains=search_query)
            )
        
        if category:
            queryset = queryset.filter(category__icontains=category)
            
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
                
        if delivery_time:
            try:
                queryset = queryset.filter(delivery_time__lte=int(delivery_time))
            except ValueError:
                pass
                
        # Filtro por rating sería más complejo y requeriría agregaciones
        if rating:
            try:
                min_rating = float(rating)
                # Aquí podrías agregar lógica para filtrar por rating promedio
                # queryset = queryset.filter(average_rating__gte=min_rating)
            except ValueError:
                pass
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Pasar filtros actuales al template
        context['current_filters'] = {
            'search': self.request.GET.get('search', ''),
            'category': self.request.GET.get('category', ''),
            'min_price': self.request.GET.get('min_price', ''),
            'max_price': self.request.GET.get('max_price', ''),
            'delivery_time': self.request.GET.get('delivery_time', ''),
            'rating': self.request.GET.get('rating', ''),
        }
        
        # Verificar si hay filtros aplicados
        context['has_filters'] = any(context['current_filters'].values())
        
        # Categorías populares para filtros rápidos
        context['popular_categories'] = [
            'Web Development', 'Mobile Development', 'Design', 
            'Marketing', 'Writing', 'Data Analysis'
        ]
        
        return context

class ServiceDetailView(DetailView):
    """
    Vista de detalle de servicio.
    Sigue SRP: Solo maneja visualización de servicio individual.
    """
    model = Service
    template_name = 'services/service_detail.html'
    context_object_name = 'service'
    pk_url_kwarg = 'service_id'
    
    def get_queryset(self):
        return Service.objects.filter(active=True).select_related(
            'freelancer__user'
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = self.get_object()
        
        # Verificar si el usuario es el propietario del servicio
        context['is_owner'] = (
            self.request.user.is_authenticated and
            hasattr(self.request.user, 'freelancerprofile') and
            service.freelancer == self.request.user.freelancerprofile
        )
        
        # Verificar si está en carrito o wishlist
        if self.request.user.is_authenticated:
            try:
                # Verificar si está en carrito usando CartService
                from core.services.cart_service import CartService
                cart_service = CartService()
                cart_items = cart_service.get_cart_items(self.request.user)
                
                context['in_cart'] = any(
                    item.service == service for item in cart_items
                )
                context['cart_count'] = len(cart_items)
                
            except Exception as e:
                context['in_cart'] = False
                context['cart_count'] = 0
                print(f"Error checking cart: {e}")
            
            try:
                # Verificar si está en wishlist usando WishlistService
                from core.services.wishlist_service import WishlistService
                wishlist_service = WishlistService()
                
                context['in_wishlist'] = wishlist_service.is_in_wishlist(
                    self.request.user, service
                )
                context['wishlist_count'] = wishlist_service.get_wishlist_count(
                    self.request.user
                )
                
            except Exception as e:
                context['in_wishlist'] = False
                context['wishlist_count'] = 0
                print(f"Error checking wishlist: {e}")
        else:
            context['in_cart'] = False
            context['in_wishlist'] = False
            context['cart_count'] = 0
            context['wishlist_count'] = 0
        
        return context

class FreelancerServiceListView(LoginRequiredMixin, ListView):
    """
    Vista para que freelancers gestionen sus servicios.
    Sigue SRP: Solo maneja servicios del freelancer actual.
    """
    template_name = 'services/freelancer_service_list.html'
    context_object_name = 'services'
    paginate_by = 10
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_freelancer_profile:
            messages.error(request, "Solo los freelancers pueden acceder a esta sección")
            return redirect('core:multi_profile_detail')
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        return Service.objects.filter(
            freelancer=self.request.user.freelancerprofile
        ).order_by('-created_at')


class CartView(LoginRequiredMixin, ListView):
    """Vista para mostrar el carrito de compras unificado"""
    template_name = 'services/cart.html'
    context_object_name = 'cart_items'
    
    def get_queryset(self):
        """
        Returns only the services for ListView compatibility.
        The full cart data is handled in get_context_data.
        """
        try:
            from core.services.cart_service import CartService
            cart_service = CartService()
            # Get cart data - returns dict with 'services' and 'mentorships'
            cart_items = cart_service.get_cart_items(self.request.user)
            # Return only services for ListView queryset compatibility
            return cart_items
        except Exception as e:
            print(f"Error getting cart items: {e}")
            return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        try:
            from core.services.cart_service import CartService
            cart_service = CartService()  # Cambiar esta línea
            
            # CartService tiene métodos más simples
            context['cart_items'] = cart_service.get_cart_items(self.request.user)
            context['cart_total'] = cart_service.get_cart_total(self.request.user)
            context['cart_count'] = len(context['cart_items'])
            context['is_empty'] = context['cart_count'] == 0
            
            # Remover toda la lógica de mentorships porque CartService solo maneja servicios
            
        except Exception as e:
            # Fallback simplificado
            context.update({
                'cart_items': [],
                'cart_total': 0,
                'cart_count': 0,
                'is_empty': True,
            })
        
        return context
            
class AddToCartView(LoginRequiredMixin, View):
    """Vista para agregar servicios al carrito"""
    
    def post(self, request, service_id):
        try:
            service = get_object_or_404(Service, id=service_id, active=True)
            
            # Usar CartService para agregar al carrito
            from core.services.cart_service import CartService
            cart_service = CartService()
            cart_service.add_to_cart(request.user, service)
            
            messages.success(request, f"'{service.title}' agregado al carrito exitosamente")
            
        except ValidationError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f"Error al agregar al carrito: {str(e)}")
        
        return redirect('services:service_detail', service_id=service_id)
    
    def get(self, request, service_id):
        """Redirect GET requests to service detail"""
        return redirect('services:service_detail', service_id=service_id)


class RemoveFromCartView(LoginRequiredMixin, View):
    """Vista para remover servicios del carrito"""
    
    def post(self, request, service_id):
        try:
            service = get_object_or_404(Service, id=service_id)
            
            # Usar CartService para remover del carrito
            from core.services.cart_service import CartService
            cart_service = CartService()
            cart_service.remove_from_cart(request.user, service)
            
            messages.success(request, f"'{service.title}' removido del carrito")
            
        except Exception as e:
            messages.error(request, str(e))
        
        return redirect('services:cart_view')


class CartView(LoginRequiredMixin, ListView):
    """Vista para mostrar el carrito de compras"""
    template_name = 'services/cart.html'
    context_object_name = 'cart_items'
    
    def get_queryset(self):
        """Obtiene items del carrito usando CartService"""
        try:
            from core.services.cart_service import CartService
            cart_service = CartService()
            return cart_service.get_cart_items(self.request.user)
        except Exception as e:
            print(f"Error getting cart items: {e}")
            return []
    
    def get_context_data(self, **kwargs):
        """Proporciona contexto completo del carrito"""
        context = super().get_context_data(**kwargs)
        
        try:
            from core.services.cart_service import CartService
            cart_service = CartService()
            
            # Obtener datos del carrito usando el servicio
            context['cart_items'] = cart_service.get_cart_items(self.request.user)
            context['cart_total'] = cart_service.get_cart_total(self.request.user)
            context['cart_count'] = len(context['cart_items'])
            context['is_empty'] = context['cart_count'] == 0
            
        except Exception as e:
            print(f"Error getting cart context: {e}")
            context.update({
                'cart_items': [],
                'cart_total': 0,
                'cart_count': 0,
                'is_empty': True,
            })
        
        return context




class AddToWishlistView(LoginRequiredMixin, View):
    """Vista para agregar servicios a la wishlist"""
    
    def post(self, request, service_id):
        print(f"DEBUG: Adding service {service_id} to wishlist for user {request.user}")
        try:
            service = get_object_or_404(Service, id=service_id, active=True)
            print(f"DEBUG: Found service: {service}")
            
            # Usar WishlistService para agregar a wishlist
            from core.services.wishlist_service import WishlistService
            wishlist_service = WishlistService()
            
            # Verificar si ya está en wishlist
            is_in_wishlist = wishlist_service.is_in_wishlist(request.user, service)
            print(f"DEBUG: Service already in wishlist: {is_in_wishlist}")
            
            if is_in_wishlist:
                messages.info(request, f"'{service.title}' ya está en tus favoritos")
            else:
                print(f"DEBUG: Calling add_to_wishlist...")
                result = wishlist_service.add_to_wishlist(request.user, service)
                print(f"DEBUG: add_to_wishlist result: {result}")
                
                # Si el servicio falla, intentar guardarlo directamente
                if not result:
                    print(f"DEBUG: WishlistService failed, trying direct database save...")
                    try:
                        # Importar el modelo directamente y crear el item
                        from services.models import WishlistItem, Wishlist
                        # Primero obtener o crear la wishlist del usuario
                        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
                        # Luego crear el item en esa wishlist
                        wishlist_item, created = WishlistItem.objects.get_or_create(
                            wishlist=wishlist,
                            service=service
                        )
                        print(f"DEBUG: Direct save result - created: {created}, item: {wishlist_item}")
                        
                        if created:
                            result = True
                            print(f"DEBUG: Successfully saved to database directly")
                        else:
                            print(f"DEBUG: Item already existed in database")
                            
                    except Exception as db_error:
                        print(f"DEBUG: Direct database save failed: {db_error}")
                        import traceback
                        traceback.print_exc()
                
                # Verificar que se guardó correctamente
                after_add = wishlist_service.is_in_wishlist(request.user, service)
                print(f"DEBUG: After add, is in wishlist: {after_add}")
                
                # Verificar items en wishlist
                items = wishlist_service.get_wishlist_items(request.user)
                print(f"DEBUG: Items after add: {items}")
                
                if result:
                    messages.success(request, f"'{service.title}' agregado a favoritos exitosamente")
                else:
                    messages.error(request, f"No se pudo agregar '{service.title}' a favoritos")
                
        except ValidationError as e:
            print(f"DEBUG: ValidationError: {e}")
            messages.error(request, str(e))
        except Exception as e:
            print(f"DEBUG: Exception: {e}")
            import traceback
            traceback.print_exc()
            messages.error(request, f"Error al agregar a favoritos: {str(e)}")
        
        return redirect('services:service_detail', service_id=service_id)
    
    def get(self, request, service_id):
        """Redirect GET requests to service detail"""
        return redirect('services:service_detail', service_id=service_id)


class RemoveFromWishlistView(LoginRequiredMixin, View):
    """Vista para remover servicios de la wishlist"""
    
    def post(self, request, service_id):
        try:
            service = get_object_or_404(Service, id=service_id)
            
            # Usar WishlistService para remover de wishlist
            from core.services.wishlist_service import WishlistService
            wishlist_service = WishlistService()
            wishlist_service.remove_from_wishlist(request.user, service)
            
            messages.success(request, f"'{service.title}' removido de favoritos")
            
        except Exception as e:
            messages.error(request, str(e))
        
        return redirect('services:wishlist_view')


class WishlistView(LoginRequiredMixin, TemplateView):
    """Vista para mostrar la wishlist"""
    template_name = 'services/wishlist.html'
    
    def get_context_data(self, **kwargs):
        """Proporciona contexto completo de la wishlist"""
        context = super().get_context_data(**kwargs)
        
        try:
            from core.services.wishlist_service import WishlistService
            wishlist_service = WishlistService()
            
            # Obtener datos de wishlist usando el servicio
            wishlist_data = wishlist_service.get_wishlist_items(self.request.user)
            print(f"DEBUG: Wishlist data from service: {wishlist_data}")
            print(f"DEBUG: Wishlist data type: {type(wishlist_data)}")
            
            # El servicio devuelve un dict, extraer solo los servicios
            if isinstance(wishlist_data, dict):
                wishlist_items = wishlist_data.get('services', [])
            else:
                wishlist_items = wishlist_data if wishlist_data else []
            
            print(f"DEBUG: Processed wishlist items: {wishlist_items}")
            print(f"DEBUG: Wishlist items count: {len(wishlist_items)}")
            
            # Si el servicio no devuelve items, verificar directamente en la base de datos
            if not wishlist_items:
                print(f"DEBUG: Service returned empty, checking database directly...")
                try:
                    from services.models import WishlistItem
                    from services.models import Wishlist
                    # Obtener la wishlist del usuario
                    try:
                        wishlist = Wishlist.objects.get(user=self.request.user)
                        db_items = WishlistItem.objects.filter(wishlist=wishlist).select_related('service')
                        wishlist_items = [item.service for item in db_items if item.service]
                    except Wishlist.DoesNotExist:
                        wishlist_items = []
                    print(f"DEBUG: Found {len(wishlist_items)} items directly from database")
                    for item in wishlist_items:
                        print(f"DEBUG: DB Item: {item}")
                except Exception as db_error:
                    print(f"DEBUG: Direct database check failed: {db_error}")
                    wishlist_items = []
            
            context['wishlist_items'] = wishlist_items
            context['wishlist_count'] = len(wishlist_items)
            context['items'] = wishlist_items  # Para compatibilidad con el template
            
            print(f"DEBUG: Final context wishlist_count: {context['wishlist_count']}")
            
        except Exception as e:
            print(f"Error getting wishlist context: {e}")
            import traceback
            traceback.print_exc()
            context.update({
                'wishlist_items': [],
                'wishlist_count': 0,
                'items': [],
            })
        
        return context


class UnifiedCartView(LoginRequiredMixin, TemplateView):
    """Vista unificada para el carrito que maneja servicios y mentorías"""
    template_name = 'services/unified_cart.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        print(f"=== DEBUG: UnifiedCartView for user {self.request.user} ===")
        
        try:
            from core.services.cart_service import UnifiedCartService
            cart_service = UnifiedCartService()
            cart_items = cart_service.get_cart_items(self.request.user)
            
            print(f"Cart items from service: {cart_items}")
            
            # Also check manually
            try:
                from mentorship.models import MentorshipCartItem
                manual_mentorship_items = MentorshipCartItem.objects.filter(user=self.request.user)
                print(f"Manual mentorship cart items: {list(manual_mentorship_items)}")
                for item in manual_mentorship_items:
                    print(f"  - Item: {item}, Session: {item.session}")
            except Exception as manual_e:
                print(f"Error checking mentorship cart items manually: {manual_e}")
            
            services = cart_items.get('services', [])
            mentorships = cart_items.get('mentorships', [])
            
            print(f"Services: {services}")
            print(f"Mentorships: {mentorships}")
            
            # Calculate totals
            services_total = sum(float(service.price) for service in services)
            mentorships_total = sum(float(mentorship.price) for mentorship in mentorships)
            
            print(f"Services total: {services_total}")
            print(f"Mentorships total: {mentorships_total}")
            
            context.update({
                'services': services,
                'mentorships': mentorships,
                'services_total': services_total,
                'mentorships_total': mentorships_total,
                'cart_total': services_total + mentorships_total,
                'cart_count': len(services) + len(mentorships),
            })
            
        except Exception as e:
            print(f"Error in UnifiedCartView: {e}")
            import traceback
            traceback.print_exc()
            
            # Fallback
            context.update({
                'services': [],
                'mentorships': [],
                'services_total': 0,
                'mentorships_total': 0,
                'cart_total': 0,
                'cart_count': 0,
            })
            
        print(f"Final context cart_count: {context.get('cart_count')}")
        print("=== END DEBUG ===")
        return context