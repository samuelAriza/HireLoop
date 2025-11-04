> A production-ready freelancing platform connecting clients with talented freelancers through projects, microservices, and mentorship sessions. Built with Django and deployed on Google Kubernetes Engine (GKE).

[![Django](https://img.shields.io/badge/Django-5.2.6-green.svg)](https://www.djangoproject.com/) [![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/) [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://www.postgresql.org/) [![GKE](https://img.shields.io/badge/GKE-Deployed-4285F4.svg)](https://cloud.google.com/kubernetes-engine) [![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Table of Contents

- [Project Overview](#project-overview)
- [Architecture Diagrams](#architecture-diagrams)
  - [Application Architecture (MVT + REST API)](#application-architecture-mvt--rest-api)
  - [Domain Model (Class Diagram)](#domain-model-class-diagram)
  - [Infrastructure & Deployment](#infrastructure--deployment)
- [CI/CD Workflow](#cicd-workflow)
- [Tech Stack](#tech-stack)
- [Functionality & Screenshots](#functionality--screenshots)
- [Folder Structure](#folder-structure)
- [Installation and Setup](#installation-and-setup)
- [Management Commands](#management-commands)
- [Testing](#testing)
- [Contributing](#contributing)

---

## Project Overview

HireLoop is a comprehensive freelancing platform that facilitates professional connections between clients and freelancers. The platform supports multiple engagement models and is built following **clean architecture principles** with **SOLID design patterns**.

### Key Features

- **Multi-Profile System**: Users can maintain both freelancer and client profiles with role-based access
- **Microservices Marketplace**: Browse and purchase fixed-price services with category-based organization
- **Project Management**: Comprehensive project collaboration system with applications, assignments, and status tracking
- **Mentorship Platform**: Schedule and manage one-on-one learning sessions between mentors and mentees
- **Smart Cart System**: Unified shopping cart supporting multiple product types using Generic Foreign Keys
- **Analytics Dashboard**: Real-time market insights with interactive Plotly Dash visualizations
- **Payment Processing**: Secure payment handling through Stripe API integration
- **Portfolio Management**: Showcase work and build professional portfolios
- **REST API**: JSON API for external application integration
- **Advanced Search**: Multi-field search and filtering across all content types

### Architecture Principles

- **Repository Pattern**: Separation of data access logic from business logic
- **Service Layer**: Encapsulation of business rules and domain logic
- **Dependency Inversion Principle (DIP)**: Storage abstraction with Factory Pattern (LocalStorage/GCSStorage)
- **Generic Foreign Keys**: Flexible polymorphic relationships for cart and wishlist
- **MVT + REST API**: Dual architecture serving both web UI and external applications

---

## Architecture Diagrams

### Application Architecture (MVT + REST API)
Clic [Drive](https://drive.google.com/drive/folders/1GnYvcA3UMGRrXTgvmgY9vzVono0-OBej?usp=sharing) for more info.

The application follows Django's **Model-View-Template (MVT)** pattern enhanced with a **REST API layer** for external integrations. The architecture is organized in distinct layers following **clean architecture principles**.

#### Layers Description

**1. External Clients**
- **Web Browser** (LightBlue): Traditional web users accessing the HTML interface
- **Mobile Client** (LightGreen): Mobile applications consuming the web UI
- **Third-Party Apps** (Orange): External applications accessing the REST API

**2. API Layer (REST)**
- **REST API Endpoints**:
  - `GET /api/microservices/`: List all microservices (JSON response)
  - `GET /api/microservices/{id}/`: Retrieve microservice details by ID
- **Serializers**: `MicroServiceSerializer` for JSON data serialization
- **API Views**: `ListAPIView` and `RetrieveAPIView` using Django REST Framework
- **Characteristics**: Public endpoints with no authentication required, CORS enabled for cross-origin access

**3. Presentation Layer**
- **Templates**: Base templates, Core templates, Project templates, Microservices templates, Mentorship templates, Cart templates, Payment templates, Analytics dashboards
- **Static Files**: CSS stylesheets, JavaScript files, images, Font Awesome icons

**4. Application Layer (Views)**
- **Core Views**: Authentication, profile management, portfolio views, homepage
- **Projects Views**: Project listing, detail, creation, application handling
- **Microservices Views**: Service marketplace, creation, freelancer listings
- **Mentorship Views**: Session scheduling, mentor-mentee matching
- **Cart Views**: Shopping cart, wishlist, checkout
- **Payment Views**: Stripe integration, payment processing
- **Analytics Views**: Dashboard rendering, Plotly Dash apps

**5. Business Logic Layer (Services)**
- **Core Services**: User service, profile service, portfolio service, authentication service, image service
- **Project Services**: Project management, assignment handling, image service
- **Microservice Services**: Service creation, listing, image service
- **Mentorship Services**: Session management, booking service
- **Cart Services**: Cart operations, wishlist management
- **Payment Services**: Stripe payment processing
- **Analytics Services**: Data aggregation, metrics calculation, visualization

**6. Data Access Layer (Repositories)**
- **Core Repositories**: User repository, profile repository, portfolio repository
- **Project Repositories**: Project repository, assignment repository, application repository
- **Microservice Repositories**: Microservice repository, category repository
- **Analytics Repositories**: Aggregation repository, metrics repository

**7. Model Layer (Domain)**
- **Core Models**: User, FreelancerProfile, ClientProfile, ItemPortfolio
- **Project Models**: Project, ProjectAssignment, ProjectApplication
- **Microservice Models**: MicroService, Category
- **Mentorship Models**: MentorshipSession
- **Cart Models**: CartItem, WishlistItem
- **Payment Models**: Payment

**8. Infrastructure Layer**
- **Django Framework**: URL Router, Middleware, ORM, Template Engine, Static Server
- **External Services**: Stripe API, File Storage (LocalStorage/GCSStorage), Media Files
- **Database**: SQLite (development), PostgreSQL 15 (production via Cloud SQL)

#### Request Flow

**Traditional Web Flow**:
1. Browser/Mobile → URL Router → Middleware → Views
2. Views → Services → Repositories → Models → ORM → Database
3. Views → Template Engine → Templates (with Static Files) → HTML Response

**REST API Flow**:
1. Browser/Mobile/ThirdParty → REST API Endpoints (ListAPI/DetailAPI)
2. API Endpoints → API Views (ListAPIView/RetrieveAPIView)
3. API Views → Services → Repositories → Models → ORM → Database
4. Services → Serializers → JSON Response (HTTP 200)

**Key Integration Points**:
- Both web UI and REST API share the **same business logic layer** (Services)
- Image services integrate with **File Storage abstraction** (Factory Pattern)
- Payment services communicate with **Stripe API** for transaction processing
- Template engine references **Static Files** for CSS/JS/images

**Testing Infrastructure**:
- **Factory Boy**: Generates test data for all domain models
- Factories: UserFactory, ProfileFactories, ProjectFactories, ServiceFactories
- Integration with all model layers for automated testing

---

### Domain Model (Class Diagram)

The domain model represents the core business entities and their relationships within HireLoop. All entities use **UUIDField** as primary keys for enhanced security and distributed system compatibility.

Clic [Drive](https://drive.google.com/drive/folders/1GnYvcA3UMGRrXTgvmgY9vzVono0-OBej?usp=sharing) for more info.


#### Core Domain

**User** (Central Authentication Entity)
- **Attributes**: 
  - `id` (UUIDField PK), `username` (CharField 150), `email` (EmailField unique)
  - `first_name`, `last_name` (CharField 150)
  - `is_staff`, `is_active` (BooleanField), `date_joined` (DateTimeField)
  - `profile_image` (ImageField)
- **Methods**: 
  - `get_roles()`: Returns list of user roles
  - `get_profile_image_url()`: Returns URL for profile image
- **Note**: Can have both freelancer and client profiles simultaneously

**FreelancerProfile**
- **Attributes**: 
  - `id` (UUIDField PK), `bio` (TextField 1000)
  - `rating` (DecimalField 3,2), `created_at`, `updated_at` (DateTimeField)
  - `skills` (TaggableManager)
- **Relationships**: 
  - One-to-one with User
  - One-to-many with ItemPortfolio, MicroService, MentorshipSession (as mentor)
  - One-to-many with ProjectAssignment, ProjectApplication

**ClientProfile**
- **Attributes**: 
  - `id` (UUIDField PK), `company` (CharField 100)
  - `billing_address` (TextField), `billing_email` (EmailField)
  - `created_at`, `updated_at` (DateTimeField)
- **Relationships**: 
  - One-to-one with User
  - One-to-many with Project, MentorshipSession (as mentee)

**ItemPortfolio**
- **Attributes**: 
  - `id` (UUIDField PK), `title` (CharField 255), `description` (TextField)
  - `url_demo` (URLField), `image_path` (CharField 500)
  - `created_at`, `updated_at` (DateTimeField)
- **Methods**: `get_image_path()`: Returns full image URL
- **Relationship**: Many-to-one with FreelancerProfile

#### Projects Domain

**Project** (Main Business Entity for Collaboration)
- **Attributes**: 
  - `id` (UUIDField PK), `title` (CharField 255), `description` (TextField)
  - `status` (CharField 20): CREATED, IN_PROGRESS, DELIVERED, CANCELLED, COMPLETED
  - `budget` (DecimalField 10,2), `image_path` (CharField 500)
  - `created_at`, `updated_at` (DateTimeField)
- **Methods**: `get_image_path()`, `__str__()`
- **Relationship**: Many-to-one with ClientProfile

**ProjectAssignment**
- **Attributes**: 
  - `id` (UUIDField PK), `role` (CharField 100)
  - `agreed_payment` (DecimalField 12,2)
  - `status` (CharField 20): INVITED, ACCEPTED, REJECTED, REMOVED
  - `created_at`, `updated_at` (DateTimeField)
- **Relationships**: Many-to-one with Project and FreelancerProfile

**ProjectApplication**
- **Attributes**: 
  - `id` (UUIDField PK), `cover_letter` (TextField)
  - `proposed_payment` (DecimalField 12,2)
  - `status` (CharField 20): PENDING, ACCEPTED, REJECTED, WITHDRAWN
  - `created_at`, `updated_at` (DateTimeField)
- **Relationships**: Many-to-one with Project and FreelancerProfile

#### Microservices Domain

**Category**
- **Attributes**: 
  - `id` (UUIDField PK), `name` (CharField 100 unique)
  - `slug` (SlugField unique)
- **Relationship**: One-to-many with MicroService

**MicroService** (Implements PurchasableInterface)
- **Attributes**: 
  - `id` (UUIDField PK), `title` (CharField 255), `description` (TextField)
  - `price` (DecimalField 10,2), `delivery_time` (PositiveIntegerField)
  - `is_active` (BooleanField), `image_path` (CharField 500)
  - `created_at`, `updated_at` (DateTimeField)
- **Methods**: 
  - `get_price()`, `get_title()`, `get_description()`
  - `get_type()`: Returns 'microservice'
  - `get_image_path()`: Returns full image URL
- **Relationships**: 
  - Many-to-one with Category and FreelancerProfile
  - Can be added to CartItem (Generic Foreign Key)

#### Mentorship Domain

**MentorshipSession** (Implements PurchasableInterface)
- **Attributes**: 
  - `id` (UUIDField PK), `topic` (CharField 255)
  - `start_time` (DateTimeField), `duration_minutes` (PositiveIntegerField)
  - `status` (CharField 20): SCHEDULED, COMPLETED, CANCELED, NO_SHOW
  - `image_path` (CharField 500), `created_at`, `updated_at` (DateTimeField)
- **Methods**: 
  - `get_image_path()`, `get_type()`: Returns 'mentorship_session'
- **Relationships**: 
  - Many-to-one with FreelancerProfile (mentor) and ClientProfile (mentee)
  - Can be added to CartItem (Generic Foreign Key)

#### Cart Domain

**CartItem**
- **Attributes**: 
  - `id` (UUIDField PK), `quantity` (PositiveIntegerField)
  - `object_id` (UUIDField), `content_type` (ForeignKey ContentType)
  - `created_at`, `updated_at` (DateTimeField)
- **Methods**: `get_total_price()`: Calculates total based on quantity and item price
- **Relationships**: 
  - Many-to-one with User
  - Generic Foreign Key to MicroService or MentorshipSession

**WishlistItem**
- **Attributes**: 
  - `id` (UUIDField PK), `object_id` (UUIDField)
  - `content_type` (ForeignKey ContentType), `created_at` (DateTimeField)
- **Relationships**: 
  - Many-to-one with User
  - Generic Foreign Key to MicroService or MentorshipSession

#### Payments Domain

**Payment**
- **Attributes**: 
  - `id` (UUIDField PK), `stripe_session_id` (CharField 255)
  - `stripe_payment_intent` (CharField 255)
  - `amount` (DecimalField 10,2), `currency` (CharField 3)
  - `status` (CharField 20): pending, succeeded, failed, canceled
  - `created_at`, `updated_at` (DateTimeField)
- **Relationship**: Many-to-one with User

---

### Infrastructure & Deployment

HireLoop is deployed on **Google Cloud Platform (GCP)** using **Google Kubernetes Engine (GKE)** with a fully automated CI/CD pipeline. The infrastructure follows cloud-native best practices with high availability, auto-scaling, and secure database connections.

Clic [Drive](https://drive.google.com/drive/folders/1GnYvcA3UMGRrXTgvmgY9vzVono0-OBej?usp=sharing) for more info.


#### Google Cloud Platform Resources

**Project**: `hireloop-476222`

**Managed Services**:

1. **Cloud SQL (PostgreSQL 15)**
   - **Instance**: `hireloop-db`
   - **Location**: `us-central1-c`
   - **Machine**: `db-custom-1-3840` (1 vCPU, 3840MB RAM)
   - **Storage**: 10GB SSD
   - **Connection**: Via Cloud SQL Proxy (secure tunnel)
   - **Access**: Private IP within GKE cluster

2. **Google Cloud Storage (GCS)**
   - **Bucket**: `hireloop-media`
   - **Directory Structure**:
     - `/microservices/` - Service images
     - `/portfolios/` - Portfolio item images
     - `/profiles/` - User profile pictures
     - `/projects/` - Project images
     - `/mentorships/` - Mentorship session images
   - **Access**: Public Read, Standard storage class
   - **Integration**: django-storages + GCS SDK

3. **Artifact Registry**
   - **Location**: `us-central1`
   - **Repository**: `hireloop-images` (Docker Repository)
   - **Registry URL**: `us-central1-docker.pkg.dev/hireloop-476222/hireloop-images`
   - **Purpose**: Store and version Docker container images

#### GKE Cluster Configuration

**Cluster**: `hireloop-cluster` (us-central1-a)

**Namespace**: `default`

**External Access**:

1. **Google Cloud Load Balancer**
   - Type: HTTPS Load Balancer (Layer 7)
   - Frontend: `hireloop.software`, `www.hireloop.software`
   - Backend: Routes to Ingress

2. **Ingress** (`hireloop-ingress`)
   - Type: GCE Ingress Controller
   - Domains: `hireloop.software`, `www.hireloop.software`
   - TLS: Managed Certificate (`hireloop-cert`) - automatic renewal
   - Routing: All paths (`/`) → `hireloop-service`

**Internal Service**:

**Service** (`hireloop-service`)
- Type: `ClusterIP` (internal only)
- Selector: `app=hireloop`
- Port Mapping: `80` → `8000` (HTTP)
- Purpose: Internal load balancing across pods

**Application Deployment**:

**Deployment** (`hireloop-deployment`)
- **Update Strategy**: RollingUpdate (MaxUnavailable: 0, MaxSurge: 1)
- **Image Pull Secret**: `gcp-artifact-registry`
- **Service Account**: `hireloop-ksa`

**HorizontalPodAutoscaler** (`hireloop-hpa`)
- **Min Replicas**: 2
- **Max Replicas**: 5
- **Target**: CPU 50%
- **Behavior**: Scales up/down based on CPU utilization

**Pod Specification** (Replica 1 & 2):

*Container 1: Django Application* (`hireloop`)
- **Image**: `hireloop:latest` (from Artifact Registry)
- **Port**: 8000
- **Resources**:
  - Requests: CPU 250m, RAM 512Mi
  - Limits: CPU 500m, RAM 1Gi
- **Dependencies**:
  - ConfigMap: `hireloop-config` (non-sensitive configuration)
  - Secret: `hireloop-secrets` (Django secret key, etc.)
  - Secret: `gcs-credentials` (mounted at `/app/creds/`)
- **Health Probes**:
  - Startup Probe: `/health/` endpoint (max 360s)
  - Readiness Probe: `/health/` (40s delay)
  - Liveness Probe: `/health/` (90s delay)
- **Environment Variables**:
  - `DB_HOST`: `127.0.0.1` (via sidecar proxy)
  - `DB_PORT`: `5432`

*Container 2: Cloud SQL Proxy* (`cloud-sql-proxy`)
- **Image**: `cloud-sql-proxy:2.13.0`
- **Port**: 5432
- **Connection String**: `hireloop-476222:us-central1:hireloop-db`
- **Resources**:
  - Requests: CPU 100m, RAM 128Mi
  - Limits: CPU 200m, RAM 256Mi
- **Dependencies**:
  - Secret: `cloudsql-credentials` (mounted at `/secrets/cloudsql/`)
- **Purpose**: Provides secure, authenticated connection to Cloud SQL

**Pattern**: Sidecar container pattern - Cloud SQL Proxy runs alongside Django app, exposing PostgreSQL on localhost:5432

**Database Migrations**:

**Job** (`django-migrate`)
- **Purpose**: Run Django database migrations and collect static files
- **TTL**: 300s after completion (automatic cleanup)
- **BackoffLimit**: 3 attempts
- **Containers**:
  1. **migrate** (Django):
     - Commands: `python manage.py migrate`, `python manage.py collectstatic`, `python manage.py createsuperuser`
     - Dependencies: Same ConfigMaps/Secrets as deployment
  2. **cloud-sql-proxy** (sidecar): Provides database access
- **Trigger**: Created by CI/CD pipeline after deployment
- **Behavior**: Waits for Cloud SQL Proxy readiness, runs migrations, stops proxy gracefully

#### CI/CD Pipeline (GitHub Actions)

**Workflow Location**: `.github/workflows/deploy.yml`

**Trigger**: Push to `main` branch

**Secrets Required**:
- `GCP_SA_KEY`: Service account JSON key for GCP authentication

**Pipeline Stages**:

**Stage 1: Code Checkout**
- Action: `actions/checkout@v4`
- Purpose: Clone repository code

**Stage 2: GCP Authentication**
- Action: `google-github-actions/auth@v2`
- Credentials: `${{ secrets.GCP_SA_KEY }}`
- Purpose: Authenticate with Google Cloud

**Stage 3: Docker Configuration**
- Command: `gcloud auth configure-docker us-central1-docker.pkg.dev`
- Purpose: Enable Docker to push to Artifact Registry

**Stage 4: Build & Push Docker Image**
- **Build Tags**:
  - `${{ github.sha }}` (commit-specific tag)
  - `latest` (always points to most recent)
- **Build Command**: `docker build -t [IMAGE_FULL] -t [IMAGE_LATEST] .`
- **Push**: Both tags to Artifact Registry
- **Output**: Image full path saved to `$GITHUB_ENV`

**Stage 5: Get GKE Credentials**
- Action: `google-github-actions/get-gke-credentials@v2`
- Cluster: `hireloop-cluster` (us-central1-a)
- Purpose: Configure `kubectl` access

**Stage 6: Deploy to GKE**
- **Update Image**: `kubectl set image deployment/hireloop-deployment hireloop=[IMAGE_FULL]`
- **Force Rollout**: Patch deployment with `redeployed-at` timestamp annotation
- **Purpose**: Trigger rolling update with commit-specific image

**Stage 7: Wait for Rollout**
- Command: `kubectl rollout status deployment/hireloop-deployment --timeout=600s`
- Timeout: 10 minutes
- Purpose: Ensure new pods are running and healthy

**Stage 8: Run Database Migrations**
- **Action**: Create Kubernetes Job (`django-migrate-${{ github.sha }}`)
- **Job Specification**:
  - TTL: 120s after completion
  - BackoffLimit: 2 retries
  - Containers: Django migrate + Cloud SQL Proxy sidecar
- **Migration Steps**:
  1. Wait for Cloud SQL Proxy readiness (20 attempts, 2s interval)
  2. Run `python manage.py migrate --noinput`
  3. Run `python manage.py collectstatic --noinput --clear`
  4. Stop Cloud SQL Proxy gracefully (quitquitquit endpoint)
- **Monitoring**: `kubectl wait --for=condition=complete --timeout=360s`
- **Error Handling**: On failure, display logs from both containers and job status

**Stage 9: Verify Deployment**
- **Commands**:
  - `kubectl get deployment hireloop-deployment`
  - `kubectl get pods -l app=hireloop`
  - `kubectl get events --sort-by='.lastTimestamp' | tail -20`
- **Purpose**: Display deployment status and recent events

**Stage 10: Cleanup Old Resources**
- **Condition**: Only on success
- **Actions**:
  - Delete failed pods (`--field-selector=status.phase=Failed`)
  - Delete completed pods (`--field-selector=status.phase=Succeeded`)
  - Delete old migration jobs (keep only last 3)
- **Purpose**: Maintain clean cluster state

**Deployment Flow Summary**:
1. Code push to main → Trigger workflow
2. Build Docker image → Push to Artifact Registry
3. Update GKE deployment → Rolling update (0 downtime)
4. Run migration Job → Database schema updates
5. Verify health → Monitor rollout status
6. Cleanup → Remove old resources

**High Availability Features**:
- Rolling updates with 0 downtime (MaxUnavailable: 0)
- Health probes ensure traffic only to ready pods
- HPA maintains 2-5 replicas based on load
- Managed certificates with automatic renewal
- Cloud SQL Proxy for secure, authenticated database access

---

## CI/CD Workflow

### Workflow: Deploy to GKE

**File**: `.github/workflows/deploy.yml`

**Trigger**: 
- Event: `push` to `main` branch
- Automatic deployment on every commit to main

**Environment Variables**:
```yaml
PROJECT_ID: hireloop-476222
GAR_LOCATION: us-central1
REPOSITORY: hireloop-images
IMAGE: hireloop
CLUSTER: hireloop-cluster
CLUSTER_ZONE: us-central1-a
DEPLOYMENT_NAME: hireloop-deployment
NAMESPACE: default
```

**Job**: `deploy` (runs on `ubuntu-latest`)

### Pipeline Steps

#### 1. Checkout Code
- **Action**: `actions/checkout@v4`
- **Purpose**: Clone the repository to the runner

#### 2. Set up Google Cloud Authentication
- **Action**: `google-github-actions/auth@v2`
- **Credentials**: Uses `GCP_SA_KEY` secret
- **Purpose**: Authenticate with Google Cloud Platform using service account

#### 3. Configure Docker
- **Command**: `gcloud auth configure-docker us-central1-docker.pkg.dev --quiet`
- **Purpose**: Enable Docker to authenticate with Google Artifact Registry

#### 4. Build & Push Docker Image
- **Build Tags**:
  - `IMAGE_TAG=${{ github.sha }}` (commit SHA)
  - `IMAGE_LATEST=latest`
- **Full Image Path**: `us-central1-docker.pkg.dev/hireloop-476222/hireloop-images/hireloop`
- **Commands**:
  ```bash
  docker build -t $IMAGE_FULL -t $IMAGE_LATEST .
  docker push $IMAGE_FULL
  docker push $IMAGE_LATEST
  ```
- **Output**: Saves `IMAGE_FULL` and `IMAGE_TAG` to `$GITHUB_ENV` for later steps

#### 5. Get GKE Credentials
- **Action**: `google-github-actions/get-gke-credentials@v2`
- **Cluster**: `hireloop-cluster` in `us-central1-a`
- **Purpose**: Configure `kubectl` to interact with the GKE cluster

#### 6. Deploy to GKE
- **Update Image**: 
  ```bash
  kubectl set image deployment/hireloop-deployment \
    hireloop=${{ env.IMAGE_FULL }} -n default
  ```
- **Force Rollout**: Patch deployment with timestamp annotation to trigger update
  ```bash
  kubectl patch deployment hireloop-deployment -n default -p \
    '{"spec":{"template":{"metadata":{"annotations":{"redeployed-at":"$(date +%s)"}}}}}'
  ```
- **Output**: Confirmation message with deployed image tag

#### 7. Wait for Rollout
- **Command**: `kubectl rollout status deployment/hireloop-deployment -n default --timeout=600s`
- **Timeout**: 10 minutes
- **Purpose**: Wait for all pods to be updated and running
- **Success Indicator**: "✅ Rollout completado exitosamente"

#### 8. Run Database Migrations
- **Action**: Create temporary Kubernetes Job
- **Job Name**: `django-migrate-${{ github.sha }}`
- **Job Configuration**:
  - `ttlSecondsAfterFinished: 120` (auto-cleanup after 2 minutes)
  - `backoffLimit: 2` (retry up to 2 times on failure)
  - Service Account: `hireloop-ksa`
  - Image Pull Secret: `gcp-artifact-registry`

**Job Containers**:

*Container 1: Django Migrate*
- **Image**: Same as deployed (`${{ env.IMAGE_FULL }}`)
- **Environment**: From `hireloop-secrets` and `hireloop-config` ConfigMaps
- **Database Connection**: `127.0.0.1:5432` (via sidecar proxy)
- **Steps**:
  1. Wait for Cloud SQL Proxy (up to 20 attempts, 2s interval)
  2. Verify proxy readiness (socket connection test)
  3. Run `python manage.py migrate --noinput`
  4. Run `python manage.py collectstatic --noinput --clear`
  5. Stop Cloud SQL Proxy gracefully (`/quitquitquit` endpoint)
- **Resources**: 
  - Requests: CPU 100m, RAM 256Mi
  - Limits: CPU 500m, RAM 512Mi

*Container 2: Cloud SQL Proxy (Sidecar)*
- **Image**: `gcr.io/cloud-sql-connectors/cloud-sql-proxy:2.13.0`
- **Arguments**:
  - `--address=0.0.0.0`
  - `--port=5432`
  - `--quitquitquit` (enable graceful shutdown endpoint)
  - `--structured-logs`
  - `--credentials-file=/secrets/credentials.json`
  - `hireloop-476222:us-central1:hireloop-db`
- **Volume**: `cloudsql-credentials` secret mounted at `/secrets`
- **Resources**:
  - Requests: CPU 100m, RAM 128Mi
  - Limits: CPU 200m, RAM 256Mi

**Migration Monitoring**:
- **Wait Command**: `kubectl wait --for=condition=complete --timeout=360s job/django-migrate-${{ github.sha }}`
- **Timeout**: 6 minutes
- **Success**: Display last 50 lines of migration logs
- **Failure**: Display logs from both containers (last 100 for Django, last 50 for proxy) and job description

#### 9. Verify Deployment
- **Commands**:
  - Display deployment status
  - List all pods with `app=hireloop` label
  - Show last 20 events sorted by timestamp
- **Purpose**: Provide visibility into deployment state

#### 10. Cleanup Old Resources
- **Condition**: Only runs if previous steps succeeded
- **Actions**:
  1. Delete failed pods (`status.phase=Failed`) with `--grace-period=0 --force`
  2. Delete completed pods (`status.phase=Succeeded`)
  3. Delete old migration jobs (keep only the 3 most recent)
- **Purpose**: Maintain clean cluster, prevent resource accumulation

### Workflow Integration

**How It Works**:
1. Developer pushes code to `main` branch
2. GitHub Actions automatically triggers the workflow
3. Docker image is built with commit SHA tag
4. Image is pushed to Google Artifact Registry
5. GKE deployment is updated with new image
6. Rolling update ensures zero downtime (MaxUnavailable: 0)
7. Migration job runs to update database schema
8. Health probes verify new pods are ready
9. Old pods are terminated only after new ones are healthy
10. Cleanup removes temporary resources

**Safety Features**:
- Commit-specific tags enable easy rollback
- Migration job failures don't affect running application
- Rolling updates maintain availability during deployment
- Health probes prevent traffic to unhealthy pods
- Automatic cleanup prevents resource leaks

**Monitoring & Debugging**:
- Detailed logs at each step
- Pod status and events displayed
- Migration logs captured on success/failure
- Exit codes propagate to GitHub Actions UI

---

## Tech Stack

### Backend
- **Django** 5.2.6 - Web framework
- **Python** 3.11+ - Programming language
- **PostgreSQL** 15 - Production database (Cloud SQL)
- **SQLite3** - Development database
- **django-taggit** - Tag management for skills
- **django-storages** - Cloud storage backend
- **Stripe API** - Payment processing
- **Django REST Framework** - REST API implementation

### Frontend
- **Bootstrap** 5 - CSS framework
- **Font Awesome** 6 - Icon library
- **JavaScript** - Client-side interactivity

### Analytics & Visualization
- **Plotly Dash** 2.18.2 - Interactive dashboards
- **Pandas** 2.3.2 - Data manipulation
- **django-plotly-dash** - Dash integration with Django

### Cloud Infrastructure
- **Google Kubernetes Engine (GKE)** - Container orchestration
- **Google Cloud SQL** - Managed PostgreSQL database
- **Google Cloud Storage** - Media file storage
- **Google Artifact Registry** - Docker image repository
- **Cloud SQL Proxy** - Secure database connections

### Development & Testing Tools
- **Factory Boy** 3.3.3 - Test data generation
- **Faker** 37.8.0 - Fake data generator
- **Black** 25.9.0 - Code formatter
- **Flake8** 6.1.0 - Code linter
- **python-dotenv** - Environment variable management

### DevOps & CI/CD
- **Docker** - Containerization
- **GitHub Actions** - CI/CD pipeline
- **kubectl** - Kubernetes CLI

### File & Image Processing
- **Pillow** - Image manipulation
- **Google Cloud SDK** - GCS integration

---

## Functionality & Screenshots

### Database View

> **Screenshot Placeholder**: Cloud SQL PostgreSQL instance showing:
![WhatsApp Image 2025-11-04 at 1 54 26 PM](https://github.com/user-attachments/assets/909d4438-71c3-4c3e-9cc9-0ff138cb7469)


### Running Containers (GKE)

> **Screenshot Placeholder**: GKE cluster dashboard displaying:
![WhatsApp Image 2025-11-04 at 1 58 06 PM](https://github.com/user-attachments/assets/e75b1f51-269a-4b7b-be4a-89d208f16d67)
![WhatsApp Image 2025-11-04 at 1 58 38 PM](https://github.com/user-attachments/assets/b91a9397-93af-4329-96a7-cd2571c83ec6)
![WhatsApp Image 2025-11-04 at 1 59 23 PM](https://github.com/user-attachments/assets/f57cc182-22b3-4c63-b7f5-9c49efdc3978)
![WhatsApp Image 2025-11-04 at 1 59 32 PM](https://github.com/user-attachments/assets/93935959-ee3a-4d27-b45d-506a5b6abc1b)
![WhatsApp Image 2025-11-04 at 1 59 48 PM](https://github.com/user-attachments/assets/ccde846c-c968-47b0-b00e-cd94953b76e2)
![WhatsApp Image 2025-11-04 at 2 00 02 PM](https://github.com/user-attachments/assets/9c9c764d-332c-4726-b6ca-a09ba142ddfc)

### Storage Bucket (GCS)

> **Screenshot Placeholder**: Google Cloud Storage bucket view:
![WhatsApp Image 2025-11-04 at 2 00 43 PM](https://github.com/user-attachments/assets/589ba194-5ac9-4b38-a75b-55be3c49b371)


### Application Features

> **Screenshot Placeholders**:
> - **Homepage**: Landing page with microservices marketplace
> - **User Dashboard**: Freelancer/Client profile switching
> - **Microservices Listing**: Card-based service catalog with search/filter
> - **Project Details**: Project collaboration interface with assignments
> - **Mentorship Sessions**: Calendar view of scheduled sessions
> - **Shopping Cart**: Multi-item cart with different product types
> - **Analytics Dashboard**: Plotly Dash charts and visualizations
> - **Payment Checkout**: Stripe integration payment flow

### API Endpoints

> **Screenshot Placeholder**: API response examples:
> - `GET /api/microservices/` - JSON list of all microservices
> - `GET /api/microservices/{id}/` - JSON microservice details
> - Response format with serialized data

---

---

## Folder Structure

```
hireloop_project/
├── .github/
│   └── workflows/
│       └── deploy.yml                 # CI/CD pipeline for GKE deployment
│
├── analytics/                         # Analytics dashboard module
│   ├── dash_apps/                     # Plotly Dash application components
│   ├── repositories/                  # Data access layer for analytics
│   ├── services/                      # Business logic for analytics
│   ├── admin.py                       # Django admin configuration
│   ├── models.py                      # Analytics data models
│   ├── urls.py                        # URL routing for analytics
│   └── views.py                       # Dash app rendering views
│
├── cart/                              # Shopping cart and wishlist
│   ├── factory_boy/                   # Test data factories
│   ├── repositories/                  # Cart data access layer
│   ├── services/                      # Cart business logic
│   ├── signals/                       # Cart event handlers
│   ├── templates/cart/                # Cart templates
│   ├── views/                         # Cart view controllers
│   ├── admin.py                       # Admin interface
│   ├── models.py                      # CartItem, WishlistItem models
│   └── urls.py                        # Cart URL patterns
│
├── core/                              # User authentication and profiles
│   ├── factory_boy/                   # User/Profile factories
│   │   └── helpers/                   # Factory helper functions
│   ├── forms/                         # Django forms
│   ├── interfaces/                    # Abstract interfaces (StorageInterface)
│   ├── management/
│   │   └── commands/
│   │       └── populate_db.py         # Database population command
│   ├── mixins/                        # Reusable view mixins
│   ├── repositories/                  # User/Profile data access
│   ├── services/                      # User/Profile business logic
│   │   └── image_service.py           # Image upload service
│   ├── storage/                       # Storage implementations
│   │   ├── factory.py                 # Storage factory (DIP)
│   │   ├── gcs_storage.py             # Google Cloud Storage
│   │   └── local_storage.py           # Local filesystem storage
│   ├── templates/core/                # Core templates
│   ├── templatetags/                  # Custom template tags
│   ├── tests/                         # Unit tests
│   ├── utils/                         # Utility functions
│   ├── views/                         # Core view controllers
│   ├── admin.py                       # User admin
│   ├── context_processors.py          # Template context processors
│   ├── middleware.py                  # Custom middleware
│   ├── models.py                      # User, FreelancerProfile, ClientProfile
│   └── urls.py                        # Core URL patterns
│
├── docs/                              # Project documentation
│   ├── architecture_diagram.plantuml  # Application architecture (MVT + API)
│   ├── class_diagram.plantuml         # Domain model class diagram
│   └── infrastructure.plantuml        # GKE infrastructure diagram
│
├── hireloop/                          # Django project configuration
│   ├── __init__.py
│   ├── asgi.py                        # ASGI configuration
│   ├── settings.py                    # Django settings
│   ├── urls.py                        # Root URL configuration
│   └── wsgi.py                        # WSGI configuration
│
├── mentorship_session/                # Mentorship booking system
│   ├── factory_boy/                   # Mentorship factories
│   ├── forms/                         # Mentorship forms
│   ├── repositories/                  # Mentorship data access
│   ├── services/                      # Mentorship business logic
│   ├── templates/mentorship_session/  # Mentorship templates
│   ├── views/                         # Mentorship view controllers
│   ├── admin.py                       # Mentorship admin
│   ├── models.py                      # MentorshipSession model
│   └── urls.py                        # Mentorship URL patterns
│
├── microservices/                     # Freelancer services marketplace
│   ├── adapters/                      # External integrations
│   ├── api/                           # REST API for microservices
│   │   ├── serializers.py             # MicroServiceSerializer (DRF)
│   │   ├── urls.py                    # API URL patterns
│   │   └── views.py                   # ListAPIView, RetrieveAPIView
│   ├── factory_boy/                   # Microservice factories
│   ├── forms/                         # Microservice forms
│   ├── repositories/                  # Microservice data access
│   ├── services/                      # Microservice business logic
│   ├── templates/microservices/       # Microservice templates
│   ├── tests/                         # Microservice tests
│   ├── views/                         # Microservice view controllers
│   ├── admin.py                       # Microservice admin
│   ├── models.py                      # MicroService, Category models
│   └── urls.py                        # Microservice URL patterns
│
├── payments/                          # Payment processing
│   ├── factory_boy/                   # Payment factories
│   ├── templates/payments/            # Payment templates
│   ├── admin.py                       # Payment admin
│   ├── models.py                      # Payment model
│   ├── urls.py                        # Payment URL patterns
│   └── views.py                       # Stripe integration views
│
├── projects/                          # Project management system
│   ├── factory_boy/                   # Project factories
│   ├── forms/                         # Project forms
│   ├── repositories/                  # Project data access
│   ├── services/                      # Project business logic
│   │   └── image_service.py           # Project image upload
│   ├── templates/projects/            # Project templates
│   ├── views/                         # Project view controllers
│   ├── admin.py                       # Project admin
│   ├── models.py                      # Project, Assignment, Application
│   └── urls.py                        # Project URL patterns
│
├── static/                            # Static source files
│   ├── core/                          # Core static assets
│   └── images/                        # Static images
│
├── staticfiles/                       # Collected static files (deployment)
│
├── templates/                         # Global Django templates
│   ├── base.html                      # Base template
│   ├── navbar.html                    # Navigation bar
│   └── ...
│
├── media/                             # User uploaded files (development)
│   ├── microservices/dummy/           # Dummy microservice images
│   ├── mentorships/dummy/             # Dummy mentorship images
│   ├── portfolios/dummy/              # Dummy portfolio images
│   ├── profiles/dummy/                # Dummy profile images
│   └── projects/dummy/                # Dummy project images
│
├── locale/                            # Internationalization
│   └── es/                            # Spanish translations
│
├── .env                               # Environment variables (not in repo)
├── .gitignore                         # Git ignore rules
├── db.sqlite3                         # SQLite database (development)
├── Dockerfile                         # Docker container definition
├── docker-compose.yaml                # Docker Compose configuration
├── entrypoint.sh                      # Container entrypoint script
├── manage.py                          # Django management script
├── requirements.txt                   # Python dependencies
├── setup.cfg                          # Tool configuration (flake8, etc.)
│
├── artifact-registry-secret.yaml      # Kubernetes: Artifact Registry auth
├── cloudsql-key.json                  # Cloud SQL service account key
├── django-migrate-job.yaml            # Kubernetes: Migration job template
├── gcs-credentials.yaml               # Kubernetes: GCS credentials secret
├── hireloop-cert.yaml                 # Kubernetes: Managed certificate
├── hireloop-configmap.yaml            # Kubernetes: ConfigMap
├── hireloop-deployment.yaml           # Kubernetes: Deployment spec
├── hireloop-hpa.yaml                  # Kubernetes: HPA configuration
├── hireloop-ingress.yaml              # Kubernetes: Ingress resource
├── hireloop-media-key.json            # GCS service account key
├── hireloop-sa-key.json               # GCP service account key
├── hireloop-secrets.yaml              # Kubernetes: Secrets
└── hireloop-service.yaml              # Kubernetes: ClusterIP Service
```

### Key Directories

**Application Modules** (`analytics/`, `cart/`, `core/`, `mentorship_session/`, `microservices/`, `payments/`, `projects/`):
- Each module follows clean architecture with `repositories/`, `services/`, `views/`, `templates/`
- `factory_boy/`: Test data generation with Factory Boy
- `models.py`: Django ORM models
- `admin.py`: Django admin customization
- `urls.py`: URL routing

**Infrastructure**:
- `.github/workflows/`: CI/CD pipelines
- `docs/`: PlantUML architecture diagrams
- Root `*.yaml`: Kubernetes resource definitions
- Root `*.json`: GCP service account keys (not in repo)

**Storage**:
- `static/`: Source static files (CSS, JS, images)
- `staticfiles/`: Collected static files for production
- `media/`: User-uploaded files (local development only)
- GCS bucket `hireloop-media/`: Production media storage

---

## Installation and Setup

### Prerequisites

**Required**:
- Python 3.11+
- pip
- Git

**Recommended**:
- virtualenv or venv
- VS Code or PyCharm

**For Production Deployment**:
- Docker
- Google Cloud SDK (`gcloud`, `kubectl`)
- Access to GCP project `hireloop-476222`

### Local Development Setup

#### 1. Clone the Repository
```bash
git clone https://github.com/samuelAriza/HireLoop.git
cd hireloop_project
```

#### 2. Create Virtual Environment
```bash
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Environment Configuration

Create a `.env` file in the project root:

```bash
# Django Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (Development - SQLite)
# DATABASE_URL is optional for local development

# Storage Backend
STORAGE_BACKEND=local  # Options: local, gcs

# Google Cloud Storage (only if STORAGE_BACKEND=gcs)
# GCS_BUCKET_NAME=hireloop-media
# GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json

# Stripe Payment
STRIPE_PUBLIC_KEY=pk_test_your_public_key
STRIPE_SECRET_KEY=sk_test_your_secret_key
```

#### 5. Database Setup
```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# (Optional) Populate with test data
python manage.py populate_db --users 10 --freelancers 5 --clients 5 --microservices 20
```

#### 6. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

#### 7. Run Development Server
```bash
python manage.py runserver
```

**Access the application**:
- Homepage: http://localhost:8000
- Admin panel: http://localhost:8000/admin/
- Analytics dashboard: http://localhost:8000/analytics/
- API endpoint: http://localhost:8000/api/microservices/

### Production Deployment (GKE)

#### Prerequisites
- GCP account with billing enabled
- `gcloud` CLI installed and authenticated
- `kubectl` installed
- Docker installed

#### 1. Configure GCP Project
```bash
gcloud config set project hireloop-476222
gcloud config set compute/zone us-central1-a
```

#### 2. Create GKE Cluster (if not exists)
```bash
gcloud container clusters create hireloop-cluster \
  --zone us-central1-a \
  --num-nodes 2 \
  --machine-type n1-standard-2 \
  --enable-autoscaling \
  --min-nodes 2 \
  --max-nodes 5
```

#### 3. Create Cloud SQL Instance (if not exists)
```bash
gcloud sql instances create hireloop-db \
  --database-version=POSTGRES_15 \
  --tier=db-custom-1-3840 \
  --region=us-central1 \
  --storage-size=10GB \
  --storage-type=SSD
```

#### 4. Create GCS Bucket (if not exists)
```bash
gsutil mb -c STANDARD -l us-central1 gs://hireloop-media/
gsutil iam ch allUsers:objectViewer gs://hireloop-media
```

#### 5. Apply Kubernetes Resources
```bash
# Create secrets (replace with actual values)
kubectl create secret generic hireloop-secrets \
  --from-literal=SECRET_KEY=your-secret-key \
  --from-literal=DATABASE_PASSWORD=your-db-password \
  --from-literal=STRIPE_SECRET_KEY=your-stripe-key

kubectl create secret generic cloudsql-credentials \
  --from-file=credentials.json=./cloudsql-key.json

kubectl create secret generic gcs-credentials \
  --from-file=key.json=./hireloop-media-key.json

# Apply Kubernetes manifests
kubectl apply -f hireloop-configmap.yaml
kubectl apply -f hireloop-deployment.yaml
kubectl apply -f hireloop-service.yaml
kubectl apply -f hireloop-hpa.yaml
kubectl apply -f hireloop-ingress.yaml
kubectl apply -f hireloop-cert.yaml
```

#### 6. Set Up GitHub Actions
1. Add `GCP_SA_KEY` secret to GitHub repository
2. Push to `main` branch triggers automatic deployment

#### 7. Verify Deployment
```bash
# Check deployment status
kubectl get deployments

# Check pods
kubectl get pods

# Check service
kubectl get services

# Check ingress
kubectl get ingress

# View logs
kubectl logs -l app=hireloop --tail=100
```

---

## Management Commands

### Database Management

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Show migrations
python manage.py showmigrations

# Rollback migrations
python manage.py migrate <app_name> <migration_number>
```

### Static Files

```bash
# Collect static files for production
python manage.py collectstatic --noinput

# Clear collected static files
python manage.py collectstatic --clear --noinput
```

### Custom Management Commands

```bash
# Populate database with test data
python manage.py populate_db --users 10 --freelancers 5 --clients 5 --microservices 20

# Arguments:
#   --users: Number of users to create (default: 10)
#   --freelancers: Number of freelancer profiles (default: 5)
#   --clients: Number of client profiles (default: 5)
#   --microservices: Number of microservices (default: 20)
#   --projects: Number of projects (default: 10)
#   --mentorships: Number of mentorship sessions (default: 15)
```

### Development Server

```bash
# Run development server
python manage.py runserver

# Run on specific port
python manage.py runserver 8080

# Run on specific host and port
python manage.py runserver 0.0.0.0:8000
```

### Shell and Debugging

```bash
# Open Django shell
python manage.py shell

# Open shell with iPython
python manage.py shell -i ipython

# Check for problems
python manage.py check

# Validate models
python manage.py validate
```

---

## Testing

### Unit Tests

HireLoop implements comprehensive unit tests following **Test-Driven Development (TDD)** principles. Tests focus on business logic in the service layer, using **mock objects** to isolate units and avoid database dependencies.

#### Test Coverage

**1. Microservices Tests** (`microservices/tests/test_microservice_service.py`)

Tests the `MicroServiceService` business logic with mocked repository dependencies:

- **`test_create_microservice_calls_repository_with_correct_data`**: 
  - Verifies that `create_microservice()` passes correct data (title, description, price, delivery_time) to the repository
  - Ensures freelancer association is properly handled
  - Uses mock repository to isolate service logic from data access

- **`test_deactivate_microservice_calls_repository_deactivate`**: 
  - Tests that `deactivate_microservice()` delegates correctly to the repository
  - Verifies the microservice `is_active` flag transitions from `True` to `False`
  - Ensures proper return value from the service method

**Key Testing Patterns**:
```python
# Arrange: Setup mocked dependencies
self.mock_repository = Mock()
self.service = MicroServiceService(repository=self.mock_repository)

# Act: Execute service method
result = self.service.create_microservice(freelancer=mock_freelancer, data=test_data)

# Assert: Verify repository was called correctly
self.mock_repository.create.assert_called_once_with(freelancer=mock_freelancer, **test_data)
```

**2. Core Tests** (`core/tests/test_portfolio_service.py`)

Tests the `PortfolioService` business logic with focus on CRUD operations:

- **`test_update_portfolio_modifies_fields_correctly`**: 
  - Verifies selective field updates (only modifies provided fields)
  - Ensures unchanged fields remain intact
  - Validates `save()` method is called once

- **`test_update_portfolio_handles_exception`**: 
  - Tests exception handling when database save fails
  - Verifies service returns `False` on error
  - Ensures error is logged appropriately

- **`test_delete_portfolio_returns_true_on_success`**: 
  - Validates successful deletion returns `True`
  - Confirms `delete()` method is called on the model

- **`test_delete_portfolio_returns_false_on_exception`**: 
  - Tests graceful handling of deletion errors
  - Ensures service doesn't propagate exceptions
  - Validates error logging behavior

**Key Testing Patterns**:
```python
# Exception handling test
mock_portfolio.save.side_effect = Exception("Database error")
result = self.service.update_portfolio(mock_portfolio, update_data)
self.assertFalse(result)  # Service handles error gracefully
```

#### Testing Best Practices

- **Mocking**: All tests use `unittest.mock.Mock` to isolate service logic from dependencies
- **AAA Pattern**: Arrange-Act-Assert structure in all tests
- **No Database Hits**: Pure unit tests that don't touch the database
- **Descriptive Names**: Test names clearly describe what is being tested
- **Spec Objects**: Mocks use `spec=` parameter to ensure type safety

### Run Tests

```bash
# Run all tests
python manage.py test

# Run tests for specific app
python manage.py test core
python manage.py test microservices
python manage.py test cart

# Run specific test class
python manage.py test core.tests.PortfolioServiceTest
python manage.py test microservices.tests.MicroServiceServiceTest

# Run specific test method
python manage.py test core.tests.PortfolioServiceTest.test_update_portfolio_modifies_fields_correctly

# Run with verbose output
python manage.py test --verbosity=2

# Run with coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML report
```

### Code Quality

```bash
# Format code with Black
black .
black --check .  # Check without modifying

# Lint with Flake8
flake8 .
flake8 core/  # Lint specific directory

# Sort imports with isort
isort .
isort --check-only .  # Check without modifying

# Type checking (if using mypy)
mypy .
```

### Pre-commit Checks

```bash
# Run all quality checks before commit
black --check . && flake8 . && isort --check-only . && python manage.py test
```

---

## Third-Party Services

### Stripe Payment Integration

HireLoop integrates **Stripe Checkout** for secure payment processing. The integration is implemented in the `payments/` module and handles the complete payment lifecycle from cart checkout to payment confirmation.

#### Implementation Overview

**Payment Model** (`payments/models.py`)

The `Payment` model tracks all payment transactions with the following key features:

- **UUID Primary Key**: Unique identifier for each payment
- **Stripe References**: 
  - `stripe_session_id`: Unique Checkout Session identifier
  - `stripe_payment_intent`: Payment Intent ID from Stripe
- **Payment Details**:
  - `amount`: Decimal field with minimum value validation (0.01)
  - `currency`: ISO 4217 code (default: USD)
  - `status`: Comprehensive status tracking
- **Status Choices**:
  - `PENDING`: Payment initiated but not completed
  - `SUCCEEDED`: Payment successfully processed
  - `FAILED`: Payment processing failed
  - `CANCELED`: User canceled the payment
  - `REQUIRES_PAYMENT_METHOD`: Additional payment method needed
  - `REQUIRES_CONFIRMATION`: Awaiting confirmation
  - `REQUIRES_ACTION`: User action required (e.g., 3D Secure)
- **Helper Methods**:
  - `is_successful()`: Check if payment succeeded
  - `is_canceled()`: Check if payment was canceled
  - `is_failed()`: Check if payment failed

**Payment Views** (`payments/views.py`)

Three main views handle the payment flow:

**1. CreateCheckoutSessionView** (`POST /payments/checkout/`)

Creates a Stripe Checkout Session from the user's cart:

- **Validation**:
  - Ensures user is authenticated
  - Verifies cart is not empty
  - Validates all cart items have valid content objects
  - Ensures total amount > 0
- **Line Items Construction**:
  - Converts cart items to Stripe line items
  - Extracts price, title, description from purchasable objects
  - Includes product images (if available via `get_image_path()`)
  - Converts prices to cents (Stripe requirement)
- **Session Creation**:
  - Payment method: Card only
  - Mode: One-time payment
  - Success URL: `/payments/success/`
  - Cancel URL: `/payments/cancel/`
  - Metadata: Stores user ID and cart item IDs
  - Expiration: Based on session timeout settings
- **Payment Record**:
  - Creates `Payment` object with `PENDING` status
  - Stores session ID and total amount
  - Links to user for future reference
- **Error Handling**:
  - Catches `stripe.error.StripeError` for API errors
  - Returns user-friendly JSON error messages
  - Logs all errors for debugging

**2. PaymentSuccessView** (`GET /payments/success/`)

Handles successful payment return from Stripe:

- **Session Verification**:
  - Retrieves Checkout Session from Stripe
  - Expands `payment_intent` for full details
  - Verifies `payment_status == "paid"`
- **Cart Clearing**:
  - Deletes all cart items for the user
  - Logs number of items removed
- **Payment Update**:
  - Finds pending payment record
  - Updates status to `SUCCEEDED`
  - Stores final `payment_intent` ID
  - Saves updated payment
- **User Feedback**:
  - Displays success message
  - Renders confirmation page
- **Fallback Logic**:
  - Handles missing `session_id` parameter
  - Finds latest pending payment as backup

**3. PaymentCancelView** (`GET /payments/cancel/`)

Handles canceled payment return:

- **Payment Status Update**:
  - Finds latest pending payment
  - Updates status to `CANCELED`
  - Preserves payment record for audit
- **Cart Preservation**:
  - Does NOT clear cart items
  - Allows user to retry payment
- **User Feedback**:
  - Displays warning message
  - Renders cancellation page

#### Integration Flow

```
1. User adds items to cart (MicroService, MentorshipSession)
2. User clicks "Checkout" → POST /payments/checkout/
3. CreateCheckoutSessionView:
   - Validates cart
   - Creates Stripe Checkout Session
   - Creates Payment record (PENDING)
   - Redirects to Stripe hosted page
4. User completes payment on Stripe
5. Stripe redirects to /payments/success/?session_id=xxx
6. PaymentSuccessView:
   - Verifies payment with Stripe API
   - Clears cart
   - Updates Payment status to SUCCEEDED
   - Shows confirmation
```

#### Configuration

**Environment Variables** (`.env`):
```bash
STRIPE_PUBLIC_KEY=pk_test_...  # Frontend key for Stripe.js
STRIPE_SECRET_KEY=sk_test_...  # Backend API key
```

**Django Settings** (`settings.py`):
```python
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
SESSION_COOKIE_AGE = 1800  # Checkout session expiration
```

#### Security Features

- **API Key Protection**: Secret key stored in environment variables
- **User Authentication**: All views require authenticated users
- **Session Validation**: Verifies payment status with Stripe before confirming
- **Metadata Tracking**: Stores user and cart IDs for audit trail
- **HTTPS Only**: Stripe requires HTTPS in production
- **Idempotency**: Payment records prevent duplicate charges

#### URL Patterns

```python
path('checkout/', CreateCheckoutSessionView.as_view(), name='checkout'),
path('success/', PaymentSuccessView.as_view(), name='success'),
path('cancel/', PaymentCancelView.as_view(), name='cancel'),
```

#### Error Handling

- **Invalid Cart Items**: Returns 400 with error message
- **Empty Cart**: Returns 400 before creating session
- **Stripe API Errors**: Catches and logs with user-friendly messages
- **Network Failures**: Generic 500 with retry message
- **Session Verification Failures**: Redirects to cart with error

#### Logging

All payment operations are logged using Django's logging framework:
```python
logger = logging.getLogger(__name__)
logger.info(f"Checkout session created for user {user.id}")
logger.error(f"Stripe error: {e}")
logger.warning(f"CartItem {item.id} has no content_object")
```

---

## Design Patterns: Dependency Inversion Principle (DIP)

HireLoop implements the **Dependency Inversion Principle** (one of the SOLID principles) to achieve loose coupling between high-level business logic and low-level storage implementations. This allows the application to switch between different storage backends (local filesystem, Google Cloud Storage) without modifying service code.

### DIP Implementation: Storage Abstraction

#### The Problem

The application needs to store user-uploaded images (profiles, portfolios, microservices, projects, mentorships). In development, images are stored on the local filesystem, but in production, they must be stored in Google Cloud Storage (GCS). Without DIP, service classes would be tightly coupled to a specific storage implementation, making it difficult to switch backends.

#### The Solution

**1. Define Abstract Interface** (`core/interfaces/storage_interface.py`)

An abstract base class defines the contract that all storage implementations must follow:

```python
from abc import ABC, abstractmethod
from django.core.files.uploadedfile import UploadedFile

class StorageInterface(ABC):
    """Interface for storage implementations following DIP."""

    @abstractmethod
    def save(self, file: UploadedFile, path: str) -> str:
        """Save file and return the saved path."""
        pass

    @abstractmethod
    def delete(self, path: str) -> bool:
        """Delete file and return success status."""
        pass

    @abstractmethod
    def url(self, path: str) -> str:
        """Get URL for accessing the file."""
        pass

    @abstractmethod
    def exists(self, path: str) -> bool:
        """Check if file exists."""
        pass
```

**Key Characteristics**:
- Inherits from `ABC` (Abstract Base Class)
- All methods decorated with `@abstractmethod`
- Defines behavior contract without implementation
- Forces concrete classes to implement all methods

**2. Concrete Implementation: LocalStorage** (`core/storage/local_storage.py`)

Implementation for local filesystem storage:

```python
from django.core.files.storage import default_storage
from ..interfaces.storage_interface import StorageInterface

class LocalStorage(StorageInterface):
    """Local file system storage implementation."""

    def save(self, file: UploadedFile, path: str) -> str:
        """Save file to local storage."""
        return default_storage.save(path, file)

    def delete(self, path: str) -> bool:
        """Delete file from local storage."""
        try:
            if default_storage.exists(path):
                default_storage.delete(path)
                return True
            return False
        except Exception:
            return False

    def url(self, path: str) -> str:
        """Get URL for local file."""
        return default_storage.url(path)

    def exists(self, path: str) -> bool:
        """Check if file exists locally."""
        return default_storage.exists(path)
```

**Implementation Details**:
- Uses Django's `default_storage` backend (FileSystemStorage in development)
- Implements all abstract methods from `StorageInterface`
- Handles exceptions gracefully in `delete()`
- Returns boolean success/failure for operations

**3. Concrete Implementation: GCSStorage** (`core/storage/gcs_storage.py`)

Implementation for Google Cloud Storage:

```python
from django.core.files.storage import default_storage
from ..interfaces.storage_interface import StorageInterface

class GCSStorage(StorageInterface):
    """Google Cloud Storage implementation using django-storages backend."""

    def save(self, file: UploadedFile, path: str) -> str:
        """Save file to GCS. Returns only the filename for ImageField compatibility."""
        saved_path = default_storage.save(path, file)
        # Return only the filename part (after the last /)
        return saved_path.split('/')[-1] if '/' in saved_path else saved_path

    def delete(self, path: str) -> bool:
        """Delete file from GCS."""
        try:
            if default_storage.exists(path):
                default_storage.delete(path)
                return True
            return False
        except Exception:
            return False

    def url(self, path: str) -> str:
        """Get public URL for GCS file."""
        try:
            return default_storage.url(path)
        except Exception:
            return ""

    def exists(self, path: str) -> bool:
        """Check if file exists in GCS."""
        try:
            return default_storage.exists(path)
        except Exception:
            return False
```

**Implementation Details**:
- Uses `django-storages` with GCS backend (configured in settings)
- Returns only filename from `save()` for Django ImageField compatibility
- Wraps all operations in try-except for network resilience
- Returns empty string from `url()` on error (graceful degradation)

**4. Factory Pattern** (`core/factories/storage_factory.py`)

Factory class creates appropriate storage instance based on configuration:

```python
from django.conf import settings
from ..interfaces.storage_interface import StorageInterface
from ..storage.local_storage import LocalStorage
from ..storage.gcs_storage import GCSStorage

class StorageFactory:
    """Factory for creating storage instances following DIP."""

    @staticmethod
    def create_storage(storage_type: str = None) -> StorageInterface:
        """Create storage instance based on configuration."""
        storage_type = storage_type or getattr(
            settings, "PROFILE_STORAGE_TYPE", "local"
        )

        if storage_type == "local":
            return LocalStorage()
        elif storage_type == "gcs":
            return GCSStorage()
        else:
            raise ValueError(f"Unsupported storage type: {storage_type}")
```

**Factory Responsibilities**:
- Reads configuration from Django settings (`PROFILE_STORAGE_TYPE`)
- Instantiates correct storage class
- Returns interface type (`StorageInterface`), not concrete type
- Centralizes storage creation logic

**5. Service Layer Usage** (`core/services/image_service.py`)

High-level services depend on the interface, not concrete implementations:

```python
from ..interfaces.storage_interface import StorageInterface
from ..factories.storage_factory import StorageFactory

class BaseImageService:
    """Base service for handling images following SRP and DIP."""

    def __init__(self, storage: StorageInterface = None):
        # Depend on interface, not concrete class
        self._storage = storage or StorageFactory.create_storage()

    def upload_image(self, identifier: str, image_file: UploadedFile, 
                     path_prefix: str) -> str:
        """Upload image using injected storage."""
        # Generate unique filename
        file_extension = image_file.name.split(".")[-1]
        filename = f"{path_prefix}_{identifier}_{uuid.uuid4().hex}.{file_extension}"
        path = f"{self.get_upload_directory()}/{filename}"

        # Validate image
        if not self._is_valid_image(image_file):
            raise ValueError("Invalid image file")

        # Save via storage interface - works with any implementation
        full_path = self._storage.save(image_file, path)
        return filename

    def delete_image(self, image_path: str) -> bool:
        """Delete image using injected storage."""
        return self._storage.delete(image_path)
```

**Service Characteristics**:
- Constructor accepts `StorageInterface` (dependency injection)
- Defaults to factory-created storage if none provided
- Never imports or references `LocalStorage` or `GCSStorage` directly
- All storage operations go through interface methods

### DIP Benefits in Practice

**1. Testability**

Services can be tested with mock storage without touching filesystem or GCS:

```python
# In tests
mock_storage = Mock(spec=StorageInterface)
service = ProfileImageService(storage=mock_storage)
service.upload_profile_image(user_id=123, image_file=mock_file)
# Verify storage.save() was called without actual file I/O
```

**2. Environment Flexibility**

Switch storage backend via configuration:

```python
# Development (.env)
PROFILE_STORAGE_TYPE=local

# Production (.env)
PROFILE_STORAGE_TYPE=gcs
```

**3. Easy Extension**

Add new storage backends (S3, Azure Blob) by implementing interface:

```python
class S3Storage(StorageInterface):
    def save(self, file, path):
        # S3-specific implementation
        pass
    # ... implement other methods
```

**4. Loose Coupling**

Services depend on abstractions (interface), not concretions (LocalStorage/GCSStorage). This follows the **Dependency Inversion Principle**:

> High-level modules should not depend on low-level modules.  
> Both should depend on abstractions.

### Architecture Diagram Reference

This DIP implementation is documented in the **Infrastructure Layer** section of the Architecture Diagram:
- **StorageInterface** (abstraction)
- **LocalStorage** and **GCSStorage** (concrete implementations)
- **StorageFactory** (creation logic)
- Used by **Image Services** in the **Business Logic Layer**

---

We welcome contributions to HireLoop! Please follow these guidelines:

### Development Workflow

1. **Fork the repository**
   ```bash
   # Click "Fork" on GitHub
   git clone https://github.com/your-username/HireLoop.git
   cd HireLoop
   ```

2. **Create feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow Django best practices
   - Maintain clean architecture (Repository → Service → View)
   - Write unit tests for new features
   - Update documentation as needed

4. **Run tests and code quality checks**
   ```bash
   python manage.py test
   black .
   flake8 .
   isort .
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Open a Pull Request**
   - Go to the original repository on GitHub
   - Click "New Pull Request"
   - Select your branch
   - Provide a clear description of your changes

### Branch Naming Conventions

```bash
feature/*   # New features
bugfix/*    # Bug fixes
hotfix/*    # Urgent production fixes
docs/*      # Documentation updates
refactor/*  # Code refactoring
test/*      # Adding or updating tests
```

### Commit Message Format

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add user profile image upload
fix: resolve cart total calculation error
docs: update API documentation
refactor: improve service layer architecture
test: add unit tests for payment processing
chore: update dependencies
```

### Code Style Guidelines

- **Python**: Follow PEP 8, use Black formatter
- **Django**: Follow Django coding style
- **Architecture**: Maintain Repository → Service → View pattern
- **Tests**: Write unit tests for all business logic
- **Documentation**: Add docstrings to all public methods

### Pull Request Checklist

- [ ] Code follows project style guidelines
- [ ] All tests pass (`python manage.py test`)
- [ ] Code is formatted with Black
- [ ] No linting errors (Flake8)
- [ ] Documentation updated (if applicable)
- [ ] Commit messages follow conventional format
- [ ] Branch is up to date with main
- [ ] PR description clearly explains changes

---

## License

This project is developed as part of a university software architecture course.

---

## 👥 Authors

- **Samuel Andrés Ariza Gómez** - [GitHub](https://github.com/samuelAriza)

---

## Acknowledgments

- **Django Documentation** - Comprehensive framework documentation
- **Google Cloud Platform** - Infrastructure and deployment
- **Stripe** - Payment processing integration
- **Bootstrap** - UI framework
- **Plotly Dash** - Analytics visualizations
- **Factory Boy** - Test data generation
- **Universidad** - Software Architecture course

---

## Support

For questions or issues:

1. **Check Documentation**: Review this README and architecture diagrams
2. **Search Issues**: Check existing GitHub issues
3. **Create Issue**: Open a new issue with detailed description
4. **Contact**: Reach out via GitHub

---

## 🗺️ Roadmap

### Current Features (v1.0)
- ✅ User authentication and dual profiles
- ✅ Microservices marketplace
- ✅ Project management system
- ✅ Mentorship booking
- ✅ Shopping cart and wishlist
- ✅ Payment processing (Stripe)
- ✅ Analytics dashboard
- ✅ REST API for microservices
- ✅ GKE deployment with CI/CD
- ✅ Cloud SQL and GCS integration

### Future Enhancements
- Video conferencing for mentorship sessions
- AI-powered freelancer matching
- Escrow payment system
- Subscription plans for premium features
- Third-party integrations (Slack, GitHub, etc.)

---

Crafted with ❤️, powered by ☕, and debugged with patience.
