# HireLoop - Plataforma de Freelancing y Mentoría

**Equipo:** DevLoop Solutions  
**Desarrollador:** Samuel Andrés Ariza Gómez  
**Materia:** Tópicos Especiales en Ingeniería de Software

## Descripción

HireLoop es una plataforma web innovadora que conecta freelancers con clientes y mentores, facilitando la colaboración en proyectos y el intercambio de conocimientos. La aplicación integra tres funcionalidades principales: servicios freelance, gestión de proyectos y sesiones de mentoría, todo bajo una arquitectura MVT robusta y escalable implementada en Django 4.2.

La plataforma maneja múltiples dominios de negocio incluyendo gestión de usuarios con perfiles duales (freelancer/cliente), un sistema unificado de carrito y wishlist que soporta tanto servicios como mentorías, y un complejo sistema de estados para proyectos y sesiones de mentoría.

[Ver documentación completa en la Wiki](wiki.md)

## Características Principales

- 🔐 **Sistema de autenticación** con perfiles duales (Freelancer/Cliente)
- 💼 **Gestión de servicios** freelance con categorización avanzada
- 📋 **Gestión de proyectos** con sistema de aplicaciones y estados
- 🎓 **Plataforma de mentoría** con reservas y evaluaciones
- 🛒 **Sistema unificado** de carrito y wishlist
- 🎨 **Interfaz responsive** con Bootstrap
- 🏗️ **Arquitectura MVT** siguiendo principios SOLID

## Requisitos del Sistema

- Python 3.10+
- Django 4.2 LTS
- SQLite3 (base de datos por defecto)
- Librerías adicionales listadas en `requirements.txt`

## Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/hireloop-platform.git
cd hireloop-platform
```

### 2. Crear y activar entorno virtual
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Linux/Mac:
source venv/bin/activate

# En Windows:
venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar base de datos
```bash
# Aplicar migraciones
python manage.py migrate

# Crear superusuario (opcional)
python manage.py createsuperuser
```

### 5. Cargar datos de prueba (opcional)
```bash
python manage.py shell
>>> from core.factories import create_sample_data
>>> create_sample_data()
>>> exit()
```

### 6. Ejecutar servidor de desarrollo
```bash
python manage.py runserver
```

La aplicación estará disponible en: `http://127.0.0.1:8000/`

## Estructura del Proyecto

```
hireloop-platform/
├── db_new.sqlite3                              # Database file
├── doc.md                                      # Main documentation file
├── manage.py                                   # Django management script
├── requirements.txt                            # Python dependencies
├── wiki.md                                     # Wiki documentation (if created)
│
├── analytics/                                  # Analytics application
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── core/                                       # Core application (users, profiles, base services)
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── context_processors.py
│   ├── forms.py
│   ├── mixins.py
│   ├── models.py
│   ├── services.py                             # Main services file
│   ├── signals.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   ├── __pycache__/                           # Python cache files
│   ├── factories/                             # Data factories for testing
│   ├── management/                            # Django management commands
│   ├── migrations/                            # Database migrations
│   ├── mixins/                               # Custom mixins
│   ├── models/                               # Separated model files
│   ├── repositories/                         # Repository pattern implementations
│   ├── services/                             # Service layer implementations
│   │   ├── __init__.py
│   │   ├── cart_service.py
│   │   ├── wishlist_service.py
│   │   ├── freelancer_project_service.py
│   │   └── [other service files]
│   ├── templates/                            # Core templates
│   │   └── core/
│   │       ├── dashboard.html
│   │       ├── freelancer_projects.html
│   │       ├── login.html
│   │       ├── multi_profile_detail.html
│   │       └── [other core templates]
│   └── validators/                           # Custom validators
│
├── docs/                                      # Documentation and diagrams
│   ├── arquitecture.plantuml                 # Architecture PlantUML diagram
│   ├── class_diagram.plantuml               # Class diagram PlantUML
│   ├── HireLoop_Class_Diagram.svg           # Generated class diagram
│   ├── HireLoop_MVT_Architecture.svg        # Generated architecture diagram
│   ├── logo/                                # Logo assets
│   │   └── logo.png
│   └── screenshots/                         # Application screenshots
│       ├── dashboard.png
│       ├── mentorship_list.png
│       └── projects_management.png
│
├── hireloop/                                 # Django project settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── mentorship/                               # Mentorship application
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── cart_models.py                       # Moved to models.py (deprecated)
│   ├── forms.py
│   ├── models.py
│   ├── services.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   ├── migrations/                          # Database migrations
│   └── templates/                           # Mentorship templates
│       └── mentorship/
│           ├── mentor_list.html
│           ├── session_detail.html
│           ├── session_list.html
│           ├── create_mentorship.html
│           └── [other mentorship templates]
│
├── payments/                                 # Payments application
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── projects/                                 # Projects management application
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── services.py                          # Moved to core/services.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   ├── migrations/                          # Database migrations
│   └── templates/                           # Project templates
│       └── projects/
│           ├── project_list.html
│           ├── project_detail.html
│           ├── create_project.html
│           ├── client_projects.html
│           └── [other project templates]
│
├── services/                                 # Services/freelance application
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   ├── migrations/                          # Database migrations
│   └── templates/                           # Service templates
│       └── services/
│           ├── service_list.html
│           ├── service_detail.html
│           ├── cart.html
│           ├── wishlist.html
│           ├── unified_cart.html
│           └── [other service templates]
│
├── templates/                                # Global templates
│   ├── base.html                            # Base template
│   ├── partials/                            # Reusable template components
│   │   ├── navbar.html
│   │   ├── footer.html
│   │   └── messages.html
│   └── registration/                        # Authentication templates
│       ├── login.html
│       ├── register.html
│       └── password_reset.html
│
├── static/                                   # Static files
│   ├── css/                                 # Stylesheets
│   │   ├── base.css
│   │   ├── dashboard.css
│   │   ├── mentorship.css
│   │   └── [other CSS files]
│   ├── js/                                  # JavaScript files
│   │   ├── base.js
│   │   ├── cart.js
│   │   └── [other JS files]
│   └── images/                              # Image assets
│       ├── logo.png
│       └── [other images]
│
```

## Funcionalidades Principales

### Para Freelancers
- Crear y gestionar servicios
- Aplicar a proyectos de clientes
- Ofrecer sesiones de mentoría
- Gestionar perfil profesional

### Para Clientes
- Publicar proyectos
- Revisar aplicaciones de freelancers
- Contratar servicios
- Reservar sesiones de mentoría

### Para Administradores
- Panel de administración Django
- Gestión completa de usuarios y contenido
- Métricas y reportes de la plataforma

## URLs Principales

- **Home:** `/services/` - Listado de servicios
- **Proyectos:** `/projects/` - Listado de proyectos
- **Mentorías:** `/mentorship/` - Sesiones de mentoría
- **Dashboard:** `/core/dashboard/` - Panel del usuario
- **Admin:** `/admin/` - Panel administrativo

## Arquitectura y Tecnologías

- **Framework:** Django 4.2 LTS
- **Patrón:** MVT (Model-View-Template)
- **Base de datos:** SQLite3
- **Frontend:** Bootstrap 5, HTML5, CSS3, JavaScript
- **Principios:** SOLID, DRY, Clean Architecture

## Testing

```bash
# Ejecutar todas las pruebas
python manage.py test

# Ejecutar pruebas de una aplicación específica
python manage.py test core
python manage.py test mentorship
```

## Contribución

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'feat: agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear un Pull Request

## Licencia

Este proyecto es desarrollado con fines académicos para la materia **Tópicos Especiales en Ingeniería de Software**.

## Contacto

**Samuel Andrés Ariza Gómez**  
Arquitecto de Software - DevLoop Solutions  
Email: [tu-email@dominio.com]

---

## Enlaces Importantes

- [Documentación Completa](wiki.md)
- [Diagramas UML](docs/)
- [Arquitectura del Sistema](docs/HireLoop_MVT_Architecture.svg)
- [Modelo de Dominio](docs/HireLoop_Class_Diagram.svg)

---

*HireLoop Platform - Conectando talento con oportunidades* 🚀