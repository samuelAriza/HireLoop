![architecture_diagram](https://github.com/user-attachments/assets/b893d80f-b482-4edc-a639-c18715155a4d)# HireLoop

> A production-ready freelancing platform connecting clients with talented freelancers through projects, microservices, and mentorship sessions. Built with Django and deployed on Google Kubernetes Engine (GKE).

[![Django](https://img.shields.io/badge/Django-5.2.6-green.svg)](https://www.djangoproject.com/) [![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/) [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://www.postgresql.org/) [![GKE](https://img.shields.io/badge/GKE-Deployed-4285F4.svg)](https://cloud.google.com/kubernetes-engine) [![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## 📋 Table of Contents

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
![Uplo<?xml version="1.0" encoding="us-ascii" standalone="no"?><svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" contentStyleType="text/css" height="1846px" preserveAspectRatio="none" style="width:12169px;height:1846px;background:#FFFFFF;" version="1.1" viewBox="0 0 12169 1846" width="12169px" zoomAndPan="magnify"><defs/><g><text fill="#000000" font-family="Verdana" font-size="22" font-weight="bold" lengthAdjust="spacing" textLength="567" x="5796.5" y="38.5181">HireLoop Architecture - MVT + REST API Integration</text><!--cluster API Layer (REST)--><g id="cluster_API Layer (REST)"><path d="M4367.5,102.5441 L4481.5,102.5441 A3.75,3.75 0 0 1 4484,105.0441 L4491,127.612 L5701.5,127.612 A2.5,2.5 0 0 1 5704,130.112 L5704,633.0441 A2.5,2.5 0 0 1 5701.5,635.5441 L4367.5,635.5441 A2.5,2.5 0 0 1 4365,633.0441 L4365,105.0441 A2.5,2.5 0 0 1 4367.5,102.5441 " fill="#FFFFE0" style="stroke:#000000;stroke-width:1.0;"/><line style="stroke:#000000;stroke-width:1.0;" x1="4365" x2="4491" y1="127.612" y2="127.612"/><text fill="#000000" font-family="Verdana" font-size="14" font-weight="bold" lengthAdjust="spacing" textLength="113" x="4369" y="119.51">API Layer (REST)</text></g><!--cluster RESTAPI--><g id="cluster_RESTAPI"><rect fill="#FFFFFF" height="160" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="526" x="5146" y="177.0441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="5652" y="182.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="5650" y="184.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="5650" y="188.0441"/><text fill="#000000" font-family="Verdana" font-size="14" font-weight="bold" lengthAdjust="spacing" textLength="135" x="5341.5" y="205.01">REST API Endpoints</text></g><!--cluster APIComponents--><g id="cluster_APIComponents"><rect fill="#FFFFFF" height="463" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="477" x="4637" y="148.5441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="5094" y="153.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="5092" y="155.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="5092" y="159.5441"/><text fill="#000000" font-family="Verdana" font-size="14" font-weight="bold" lengthAdjust="spacing" textLength="117" x="4817" y="176.51">API Components</text></g><!--cluster Serializers--><g id="cluster_Serializers"><rect fill="#FFFFFF" height="125" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="222" x="4741" y="194.5441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="4943" y="199.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="4941" y="201.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="4941" y="205.5441"/><text fill="#000000" font-family="Verdana" font-size="14" font-weight="bold" lengthAdjust="spacing" textLength="70" x="4817" y="222.51">Serializers</text></g><!--cluster APIViews--><g id="cluster_APIViews"><rect fill="#FFFFFF" height="125" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="331" x="4695" y="462.5441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="5006" y="467.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="5004" y="469.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="5004" y="473.5441"/><text fill="#000000" font-family="Verdana" font-size="14" font-weight="bold" lengthAdjust="spacing" textLength="68" x="4826.5" y="490.51">API Views</text></g><!--cluster Presentation Layer--><g id="cluster_Presentation Layer"><path d="M9319.5,1252.0441 L9451.5,1252.0441 A3.75,3.75 0 0 1 9454,1254.5441 L9461,1277.112 L10352.5,1277.112 A2.5,2.5 0 0 1 10355,1279.612 L10355,1836.5441 A2.5,2.5 0 0 1 10352.5,1839.0441 L9319.5,1839.0441 A2.5,2.5 0 0 1 9317,1836.5441 L9317,1254.5441 A2.5,2.5 0 0 1 9319.5,1252.0441 " fill="#FFFFFF" style="stroke:#000000;stroke-width:1.0;"/><line style="stroke:#000000;stroke-width:1.0;" x1="9317" x2="9461" y1="1277.112" y2="1277.112"/><text fill="#000000" font-family="Verdana" font-size="14" font-weight="bold" lengthAdjust="spacing" textLength="131" x="9321" y="1269.01">Presentation Layer</text></g><!--cluster Templates--><g id="cluster_Templates"><rect fill="#FFFFFF" height="373" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="660" x="9349" y="1306.0441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="9989" y="1311.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="9987" y="1313.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="9987" y="1317.0441"/><text fill="#000000" font-family="Verdana" font-size="14" font-weight="bold" lengthAdjust="spacing" textLength="72" x="9643" y="1334.01">Templates</text></g><!--cluster StaticFiles--><g id="cluster_StaticFiles"><rect fill="#FFFFFF" height="269" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="274" x="10049" y="1538.0441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="10303" y="1543.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="10301" y="1545.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="10301" y="1549.0441"/><text fill="#000000" font-family="Verdana" font-size="14" font-weight="bold" lengthAdjust="spacing" textLength="74" x="10149" y="1566.01">Static Files</text></g><!--cluster Application Layer (Views)--><g id="cluster_Application Layer (Views)"><path d="M5501.5,686.5441 L5677.5,686.5441 A3.75,3.75 0 0 1 5680,689.0441 L5687,711.612 L8167.5,711.612 A2.5,2.5 0 0 1 8170,714.112 L8170,1198.5441 A2.5,2.5 0 0 1 8167.5,1201.0441 L5501.5,1201.0441 A2.5,2.5 0 0 1 5499,1198.5441 L5499,689.0441 A2.5,2.5 0 0 1 5501.5,686.5441 " fill="#FFFFFF" style="stroke:#000000;stroke-width:1.0;"/><line style="stroke:#000000;stroke-width:1.0;" x1="5499" x2="5687" y1="711.612" y2="711.612"/><text fill="#000000" font-family="Verdana" font-size="14" font-weight="bold" lengthAdjust="spacing" textLength="175" x="5503" y="703.51">Application Layer (Views)</text></g><!--cluster CoreViews--><g id="cluster_CoreViews"><rect fill="#FFFFFF" height="428.5" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="355" x="6373" y="740.5441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="6708" y="745.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="6706" y="747.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="6706" y="751.5441"/><text fill="#000000" font-family="Verdana" font-size="14" font-weight="bold" lengthAdjust="spacing" textLength="76" x="6512.5" y="768.51">Core Views</text></g><!--cluster ProjectViews--><g id="cluster_ProjectViews"><rect fill="#FFFFFF" height="428.5" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="388" x="5531" y="740.5441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="5899" y="745.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="5897" y="747.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="5897" y="751.5441"/><text fill="#000000" font-family="Verdana" font-size="14" font-weight="bold" lengthAdjust="spacing" textLength="100" x="5675" y="768.51">Projects Views</text></g><!--cluster MicroViews--><g id="cluster_MicroViews"><rect fill="#FFFFFF" height="141" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="374" x="5959" y="740.5441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="6313" y="745.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="6311" y="747.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="6311" y="751.5441"/><text fill="#000000" font-family="Verdana" font-size="14" font-weight="bold" lengthAdjust="spacing" textLength="138" x="6077" y="768.51">Microservices Views</text></g><!--cluster MentorViews--><g id="cluster_MentorViews"><rect fill="#FFFFFF" height="141" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="201" x="7445" y="740.5441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="7626" y="745.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="7624" y="747.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="7624" y="751.5441"/><text fill="#000000" font-family="Verdana" font-size="14" font-weight="bold" lengthAdjust="spacing" textLength="124" x="7483.5" y="768.51">Mentorship Views</text></g><!--cluster CartViews--><g id="cluster_CartViews"><rect fill="#FFFFFF" height="141" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="452" x="7686" y="740.5441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="8118" y="745.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="8116" y="747.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="8116" y="751.5441"/><text fill="#000000" font-family="Verdana" font-size="14" font-weight="bold" lengthAdjust="spacing" textLength="73" x="7875.5" y="768.51">Cart Views</text></g><!--cluster PaymentViews--><g id="cluster_PaymentViews"><rect fill="#FFFFFF" height="141" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="227" x="6768" y="740.5441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="6975" y="745.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="6973" y="747.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="6973" y="751.5441"/><text fill="#000000" font-family="Verdana" font-size="14" font-weight="bold" lengthAdjust="spacing" textLength="106" x="6828.5" y="768.51">Payment Views</text></g><!--cluster AnalyticsViews--><g id="cluster_AnalyticsViews"><rect fill="#FFFFFF" height="141" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="370" x="7035" y="740.5441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="7385" y="745.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="7383" y="747.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="7383" y="751.5441"/><text fill="#000000" font-family="Verdana" font-size="14" font-weight="bold" lengthAdjust="spacing" textLength="107" x="7166.5" y="768.51">Analytics Views</text></g><!--cluster Business Logic Layer (Services)--><g id="cluster_Business Logic Layer (Services)"><path d="M362.5,686.5441 L576.5,686.5441 A3.75,3.75 0 0 1 579,689.0441 L586,711.612 L3305.5,711.612 A2.5,2.5 0 0 1 3308,714.112 L3308,1198.5441 A2.5,2.5 0 0 1 3305.5,1201.0441 L362.5,1201.0441 A2.5,2.5 0 0 1 360,1198.5441 L360,689.0441 A2.5,2.5 0 0 1 362.5,686.5441 " fill="#FFFFFF" style="stroke:#000000;stroke-width:1.0;"/><line style="stroke:#000000;stroke-width:1.0;" x1="360" x2="586" y1="711.612" y2="711.612"/><text fill="#000000" font-family="Verdana" font-size="14" font-weight="bold" lengthAdjust="spacing" textLength="213" x="364" y="703.51">Business Logic Layer (Services)</text></g><!--cluster CoreServices--><g id="cluster_CoreServices"><rect fill="#FFFFFF" height="428.5" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="386" x="392" y="740.5441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="758" y="745.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="756" y="747.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="756" y="751.5441"/><text fill="#000000" font-family="Verdana" font-size="14" font-weight="bold" lengthAdjust="spacing" textLength="92" x="539" y="768.51">Core Services</text></g><!--cluster ProjectServices--><g id="cluster_ProjectServices"><rect fill="#FFFFFF" height="141" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="426" x="2525" y="740.5441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="2931" y="745.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="2929" y="747.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="2929" y="751.5441"/><text fill="#000000" font-family="Verdana" font-size="14" font-weight="bold" lengthAdjust="spacing" textLength="109" x="2683.5" y="768.51">Project Services</text></g><!--cluster MicroServices--><g id="cluster_MicroServices"><rect fill="#FFFFFF" height="141" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="504" x="1724" y="740.5441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="2208" y="745.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="2206" y="747.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="2206" y="751.5441"/><text fill="#000000" font-family="Verdana" font-size="14" font-weight="bold" lengthAdjust="spacing" textLength="147" x="1902.5" y="768.51">Microservice Services</text></g><!--cluster MentorshipServices--><g id="cluster_MentorshipServices"><rect fill="#FFFFFF" height="141" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="285" x="2991" y="740.5441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="3256" y="745.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="3254" y="747.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="3254" y="751.5441"/><text fill="#000000" font-family="Verdana" font-size="14" font-weight="bold" lengthAdjust="spacing" textLength="140" x="3063.5" y="768.51">Mentorship Services</text></g><!--cluster CartServices--><g id="cluster_CartServices"><rect fill="#FFFFFF" height="141" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="368" x="818" y="740.5441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="1166" y="745.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="1164" y="747.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="1164" y="751.5441"/><text fill="#000000" font-family="Verdana" font-size="14" font-weight="bold" lengthAdjust="spacing" textLength="89" x="957.5" y="768.51">Cart Services</text></g><!--cluster PaymentServices--><g id="cluster_PaymentServices"><rect fill="#FFFFFF" height="141" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="217" x="2268" y="740.5441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="2465" y="745.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="2463" y="747.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="2463" y="751.5441"/><text fill="#000000" font-family="Verdana" font-size="14" font-weight="bold" lengthAdjust="spacing" textLength="122" x="2315.5" y="768.51">Payment Services</text></g><!--cluster AnalyticsServices--><g id="cluster_AnalyticsServices"><rect fill="#FFFFFF" height="141" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="458" x="1226" y="740.5441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="1664" y="745.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="1662" y="747.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="1662" y="751.5441"/><text fill="#000000" font-family="Verdana" font-size="14" font-weight="bold" lengthAdjust="spacing" textLength="123" x="1393.5" y="768.51">Analytics Services</text></g><!--cluster Data Access Layer (Repositories)--><g id="cluster_Data Access Layer (Repositories)"><path d="M3334.5,974.0441 L3559.5,974.0441 A3.75,3.75 0 0 1 3562,976.5441 L3569,999.112 L5146.5,999.112 A2.5,2.5 0 0 1 5149,1001.612 L5149,1476.5441 A2.5,2.5 0 0 1 5146.5,1479.0441 L3334.5,1479.0441 A2.5,2.5 0 0 1 3332,1476.5441 L3332,976.5441 A2.5,2.5 0 0 1 3334.5,974.0441 " fill="#FFFFFF" style="stroke:#000000;stroke-width:1.0;"/><line style="stroke:#000000;stroke-width:1.0;" x1="3332" x2="3569" y1="999.112" y2="999.112"/><text fill="#000000" font-family="Verdana" font-size="14" font-weight="bold" lengthAdjust="spacing" textLength="224" x="3336" y="991.01">Data Access Layer (Repositories)</text></g><!--cluster CoreRepos--><g id="cluster_CoreRepos"><rect fill="#FFFFFF" height="419" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="432" x="3364" y="1028.0441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="3776" y="1033.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="3774" y="1035.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="3774" y="1039.0441"/><text fill="#000000" font-family="Verdana" font-size="14" font-weight="bold" lengthAdjust="spacing" textLength="122" x="3519" y="1056.01">Core Repositories</text></g><!--cluster ProjectRepos--><g id="cluster_ProjectRepos"><rect fill="#FFFFFF" height="419" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="458" x="4145" y="1028.0441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="4583" y="1033.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="4581" y="1035.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="4581" y="1039.0441"/><text fill="#000000" font-family="Verdana" font-size="14" font-weight="bold" lengthAdjust="spacing" textLength="139" x="4304.5" y="1056.01">Project Repositories</text></g><!--cluster MicroRepos--><g id="cluster_MicroRepos"><rect fill="#FFFFFF" height="141" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="269" x="3836" y="1028.0441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="4085" y="1033.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="4083" y="1035.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="4083" y="1039.0441"/><text fill="#000000" font-family="Verdana" font-size="14" font-weight="bold" lengthAdjust="spacing" textLength="177" x="3882" y="1056.01">Microservice Repositories</text></g><!--cluster AnalyticsRepos--><g id="cluster_AnalyticsRepos"><rect fill="#FFFFFF" height="141" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="474" x="4643" y="1028.0441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="5097" y="1033.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="5095" y="1035.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="5095" y="1039.0441"/><text fill="#000000" font-family="Verdana" font-size="14" font-weight="bold" lengthAdjust="spacing" textLength="153" x="4803.5" y="1056.01">Analytics Repositories</text></g><!--cluster Model Layer (Domain)--><g id="cluster_Model Layer (Domain)"><path d="M9674.5,687.0441 L9828.5,687.0441 A3.75,3.75 0 0 1 9831,689.5441 L9838,712.112 L11481.5,712.112 A2.5,2.5 0 0 1 11484,714.612 L11484,1198.0441 A2.5,2.5 0 0 1 11481.5,1200.5441 L9674.5,1200.5441 A2.5,2.5 0 0 1 9672,1198.0441 L9672,689.5441 A2.5,2.5 0 0 1 9674.5,687.0441 " fill="#FFFFFF" style="stroke:#000000;stroke-width:1.0;"/><line style="stroke:#000000;stroke-width:1.0;" x1="9672" x2="9838" y1="712.112" y2="712.112"/><text fill="#000000" font-family="Verdana" font-size="14" font-weight="bold" lengthAdjust="spacing" textLength="153" x="9676" y="704.01">Model Layer (Domain)</text></g><!--cluster CoreModels--><g id="cluster_CoreModels"><rect fill="#FFFFFF" height="427.5" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="300" x="10798" y="741.0441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="11078" y="746.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="11076" y="748.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="11076" y="752.0441"/><text fill="#000000" font-family="Verdana" font-size="14" font-weight="bold" lengthAdjust="spacing" textLength="86" x="10905" y="769.01">Core Models</text></g><!--cluster ProjectModels--><g id="cluster_ProjectModels"><rect fill="#FFFFFF" height="427.5" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="314" x="11138" y="741.0441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="11432" y="746.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="11430" y="748.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="11430" y="752.0441"/><text fill="#000000" font-family="Verdana" font-size="14" font-weight="bold" lengthAdjust="spacing" textLength="103" x="11243.5" y="769.01">Project Models</text></g><!--cluster MicroModels--><g id="cluster_MicroModels"><rect fill="#FFFFFF" height="140" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="288" x="9704" y="741.0441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="9972" y="746.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="9970" y="748.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="9970" y="752.0441"/><text fill="#000000" font-family="Verdana" font-size="14" font-weight="bold" lengthAdjust="spacing" textLength="141" x="9777.5" y="769.01">Microservice Models</text></g><!--cluster MentorshipModels--><g id="cluster_MentorshipModels"><rect fill="#FFFFFF" height="140" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="216" x="10032" y="741.0441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="10228" y="746.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="10226" y="748.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="10226" y="752.0441"/><text fill="#000000" font-family="Verdana" font-size="14" font-weight="bold" lengthAdjust="spacing" textLength="134" x="10073" y="769.01">Mentorship Models</text></g><!--cluster CartModels--><g id="cluster_CartModels"><rect fill="#FFFFFF" height="140" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="285" x="10288" y="741.0441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="10553" y="746.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="10551" y="748.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="10551" y="752.0441"/><text fill="#000000" font-family="Verdana" font-size="14" font-weight="bold" lengthAdjust="spacing" textLength="83" x="10389" y="769.01">Cart Models</text></g><!--cluster PaymentModels--><g id="cluster_PaymentModels"><rect fill="#FFFFFF" height="140" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="145" x="10613" y="741.0441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="10738" y="746.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="10736" y="748.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="10736" y="752.0441"/><text fill="#000000" font-family="Verdana" font-size="14" font-weight="bold" lengthAdjust="spacing" textLength="116" x="10627.5" y="769.01">Payment Models</text></g><!--cluster Infrastructure Layer--><g id="cluster_Infrastructure Layer"><path d="M8196.5,974.0441 L8336.5,974.0441 A3.75,3.75 0 0 1 8339,976.5441 L8346,999.112 L9290.5,999.112 A2.5,2.5 0 0 1 9293,1001.612 L9293,1476.5441 A2.5,2.5 0 0 1 9290.5,1479.0441 L8196.5,1479.0441 A2.5,2.5 0 0 1 8194,1476.5441 L8194,976.5441 A2.5,2.5 0 0 1 8196.5,974.0441 " fill="#FFFFFF" style="stroke:#000000;stroke-width:1.0;"/><line style="stroke:#000000;stroke-width:1.0;" x1="8194" x2="8346" y1="999.112" y2="999.112"/><text fill="#000000" font-family="Verdana" font-size="14" font-weight="bold" lengthAdjust="spacing" textLength="139" x="8198" y="991.01">Infrastructure Layer</text></g><!--cluster Django--><g id="cluster_Django"><rect fill="#FFFFFF" height="419" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="480" x="8226" y="1028.0441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="8686" y="1033.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="8684" y="1035.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="8684" y="1039.0441"/><text fill="#000000" font-family="Verdana" font-size="14" font-weight="bold" lengthAdjust="spacing" textLength="133" x="8399.5" y="1056.01">Django Framework</text></g><!--cluster External--><g id="cluster_External"><rect fill="#FFFFFF" height="141" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="515" x="8746" y="1028.0441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="9241" y="1033.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="9239" y="1035.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="9239" y="1039.0441"/><text fill="#000000" font-family="Verdana" font-size="14" font-weight="bold" lengthAdjust="spacing" textLength="117" x="8945" y="1056.01">External Services</text></g><!--cluster FactoryBoy--><g id="cluster_FactoryBoy"><rect fill="#FFFFFF" height="427" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="393" x="9247" y="454.5441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="9620" y="459.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="9618" y="461.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="9618" y="465.5441"/><text fill="#000000" font-family="Verdana" font-size="14" font-weight="bold" lengthAdjust="spacing" textLength="82" x="9402.5" y="482.51">Factory Boy</text></g><g id="elem_GMN15"><path d="M4381,238.5441 L4381,319.3682 L4621,319.3682 L4621,248.5441 L4611,238.5441 L4381,238.5441 " fill="#FFFFFF" style="stroke:#000000;stroke-width:1.0;"/><path d="M4611,238.5441 L4611,248.5441 L4621,248.5441 L4611,238.5441 " fill="#FFFFFF" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="200" x="4387" y="257.4411">REST API for external integrations</text><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="102" x="4387" y="275.1471">- JSON responses</text><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="219" x="4387" y="292.8531">- Public endpoints (no auth required)</text><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="184" x="4387" y="310.5592">- CORS enabled for cross-origin</text></g><!--entity ListAPI--><g id="elem_ListAPI"><rect fill="#87CEEB" height="68.1358" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="198" x="5189" y="245.0441"/><rect fill="#87CEEB" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="5367" y="250.0441"/><rect fill="#87CEEB" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="5365" y="252.0441"/><rect fill="#87CEEB" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="5365" y="256.0441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="139" x="5204" y="280.01">MicroService List API</text><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="158" x="5204" y="299.078">GET /api/microservices/</text></g><!--entity DetailAPI--><g id="elem_DetailAPI"><rect fill="#87CEEB" height="68.1358" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="226" x="5422" y="245.0441"/><rect fill="#87CEEB" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="5628" y="250.0441"/><rect fill="#87CEEB" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="5626" y="252.0441"/><rect fill="#87CEEB" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="5626" y="256.0441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="155" x="5437" y="280.01">MicroService Detail API</text><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="186" x="5437" y="299.078">GET /api/microservices/{id}/</text></g><!--entity MicroSerializer--><g id="elem_MicroSerializer"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="189" x="4757.5" y="254.5441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="4926.5" y="259.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="4924.5" y="261.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="4924.5" y="265.5441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="149" x="4772.5" y="289.51">MicroServiceSerializer</text></g><!--entity ListAPIView--><g id="elem_ListAPIView"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="116" x="4711" y="522.5441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="4807" y="527.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="4805" y="529.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="4805" y="533.5441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="76" x="4726" y="557.51">ListAPIView</text></g><!--entity RetrieveAPIView--><g id="elem_RetrieveAPIView"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="148" x="4862" y="522.5441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="4990" y="527.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="4988" y="529.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="4988" y="533.5441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="108" x="4877" y="557.51">RetrieveAPIView</text></g><!--entity BaseTemplates--><g id="elem_BaseTemplates"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="146" x="9400" y="1374.0441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="9526" y="1379.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="9524" y="1381.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="9524" y="1385.0441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="106" x="9415" y="1409.01">Base Templates</text></g><!--entity CoreTemplates--><g id="elem_CoreTemplates"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="145" x="9581.5" y="1374.0441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="9706.5" y="1379.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="9704.5" y="1381.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="9704.5" y="1385.0441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="105" x="9596.5" y="1409.01">Core Templates</text></g><!--entity ProjectTemplates--><g id="elem_ProjectTemplates"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="160" x="9762" y="1374.0441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="9902" y="1379.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="9900" y="1381.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="9900" y="1385.0441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="120" x="9777" y="1409.01">Project Templates</text></g><!--entity MicroTemplates--><g id="elem_MicroTemplates"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="199" x="9373.5" y="1606.0441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="9552.5" y="1611.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="9550.5" y="1613.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="9550.5" y="1617.0441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="159" x="9388.5" y="1641.01">Microservice Templates</text></g><!--entity MentorTemplates--><g id="elem_MentorTemplates"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="192" x="9608" y="1606.0441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="9780" y="1611.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="9778" y="1613.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="9778" y="1617.0441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="152" x="9623" y="1641.01">Mentorship Templates</text></g><!--entity CartTemplates--><g id="elem_CartTemplates"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="142" x="9835" y="1606.0441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="9957" y="1611.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="9955" y="1613.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="9955" y="1617.0441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="102" x="9850" y="1641.01">Cart Templates</text></g><!--entity CSS--><g id="elem_CSS"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="65" x="10092.5" y="1606.0441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="10137.5" y="1611.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="10135.5" y="1613.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="10135.5" y="1617.0441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="25" x="10107.5" y="1641.01">CSS</text></g><!--entity JS--><g id="elem_JS"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="106" x="10193" y="1606.0441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="10279" y="1611.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="10277" y="1613.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="10277" y="1617.0441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="66" x="10208" y="1641.01">JavaScript</text></g><!--entity Images--><g id="elem_Images"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="90" x="10092" y="1734.0441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="10162" y="1739.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="10160" y="1741.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="10160" y="1745.0441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="50" x="10107" y="1769.01">Images</text></g><!--entity AuthViews--><g id="elem_AuthViews"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="114" x="6409" y="808.5441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="6503" y="813.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="6501" y="815.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="6501" y="819.5441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="74" x="6424" y="843.51">Auth Views</text></g><!--entity ProfileViews--><g id="elem_ProfileViews"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="125" x="6558.5" y="808.5441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="6663.5" y="813.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="6661.5" y="815.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="6661.5" y="819.5441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="85" x="6573.5" y="843.51">Profile Views</text></g><!--entity PortfolioViews--><g id="elem_PortfolioViews"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="138" x="6397" y="1096.0441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="6515" y="1101.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="6513" y="1103.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="6513" y="1107.0441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="98" x="6412" y="1131.01">Portfolio Views</text></g><!--entity ImageViews--><g id="elem_ImageViews"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="125" x="6570.5" y="1096.0441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="6675.5" y="1101.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="6673.5" y="1103.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="6673.5" y="1107.0441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="85" x="6585.5" y="1131.01">Image Views</text></g><!--entity ProjectCRUD--><g id="elem_ProjectCRUD"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="128" x="5574" y="808.5441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="5682" y="813.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="5680" y="815.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="5680" y="819.5441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="88" x="5589" y="843.51">Project CRUD</text></g><!--entity ApplicationViews--><g id="elem_ApplicationViews"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="158" x="5737" y="808.5441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="5875" y="813.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="5873" y="815.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="5873" y="819.5441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="118" x="5752" y="843.51">Application Views</text></g><!--entity AssignmentViews--><g id="elem_AssignmentViews"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="162" x="5574" y="1096.0441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="5716" y="1101.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="5714" y="1103.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="5714" y="1107.0441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="122" x="5589" y="1131.01">Assignment Views</text></g><!--entity ServiceCRUD--><g id="elem_ServiceCRUD"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="130" x="6179" y="808.5441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="6289" y="813.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="6287" y="815.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="6287" y="819.5441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="90" x="6194" y="843.51">Service CRUD</text></g><!--entity CategoryViews--><g id="elem_CategoryViews"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="142" x="6002" y="808.5441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="6124" y="813.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="6122" y="815.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="6122" y="819.5441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="102" x="6017" y="843.51">Category Views</text></g><!--entity SessionCRUD--><g id="elem_SessionCRUD"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="133" x="7488.5" y="808.5441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="7601.5" y="813.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="7599.5" y="815.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="7599.5" y="819.5441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="93" x="7503.5" y="843.51">Session CRUD</text></g><!--entity CartMgmt--><g id="elem_CartMgmt"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="162" x="7952" y="808.5441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="8094" y="813.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="8092" y="815.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="8092" y="819.5441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="122" x="7967" y="843.51">Cart Management</text></g><!--entity WishlistMgmt--><g id="elem_WishlistMgmt"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="187" x="7729.5" y="808.5441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="7896.5" y="813.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="7894.5" y="815.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="7894.5" y="819.5441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="147" x="7744.5" y="843.51">Wishlist Management</text></g><!--entity StripeViews--><g id="elem_StripeViews"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="160" x="6811" y="808.5441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="6951" y="813.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="6949" y="815.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="6949" y="819.5441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="120" x="6826" y="843.51">Stripe Integration</text></g><!--entity DashApps--><g id="elem_DashApps"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="112" x="7269" y="808.5441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="7361" y="813.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="7359" y="815.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="7359" y="819.5441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="72" x="7284" y="843.51">Dash Apps</text></g><!--entity DashboardViews--><g id="elem_DashboardViews"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="156" x="7078" y="808.5441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="7214" y="813.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="7212" y="815.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="7212" y="819.5441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="116" x="7093" y="843.51">Dashboard Views</text></g><!--entity ProfileService--><g id="elem_ProfileService"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="135" x="416.5" y="808.5441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="531.5" y="813.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="529.5" y="815.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="529.5" y="819.5441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="95" x="431.5" y="843.51">Profile Service</text></g><!--entity PortfolioService--><g id="elem_PortfolioService"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="148" x="587" y="808.5441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="715" y="813.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="713" y="815.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="713" y="819.5441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="108" x="602" y="843.51">Portfolio Service</text></g><!--entity ImageService--><g id="elem_ImageService"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="135" x="416.5" y="1096.0441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="531.5" y="1101.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="529.5" y="1103.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="529.5" y="1107.0441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="95" x="431.5" y="1131.01">Image Service</text></g><!--entity ActionDispatcher--><g id="elem_ActionDispatcher"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="159" x="586.5" y="1096.0441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="725.5" y="1101.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="723.5" y="1103.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="723.5" y="1107.0441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="119" x="601.5" y="1131.01">Action Dispatcher</text></g><!--entity ProjectService--><g id="elem_ProjectService"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="138" x="2789" y="808.5441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="2907" y="813.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="2905" y="815.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="2905" y="819.5441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="98" x="2804" y="843.51">Project Service</text></g><!--entity ProjectImageService--><g id="elem_ProjectImageService"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="185" x="2568.5" y="808.5441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="2733.5" y="813.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="2731.5" y="815.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="2731.5" y="819.5441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="145" x="2583.5" y="843.51">Project Image Service</text></g><!--entity MicroServiceService--><g id="elem_MicroServiceService"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="178" x="2026" y="808.5441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="2184" y="813.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="2182" y="815.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="2182" y="819.5441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="138" x="2041" y="843.51">MicroService Service</text></g><!--entity MicroserviceImageService--><g id="elem_MicroserviceImageService"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="224" x="1767" y="808.5441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="1971" y="813.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="1969" y="815.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="1969" y="819.5441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="184" x="1782" y="843.51">Microservice Image Service</text></g><!--entity MentorshipImageService--><g id="elem_MentorshipImageService"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="217" x="3034.5" y="808.5441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="3231.5" y="813.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="3229.5" y="815.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="3229.5" y="819.5441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="177" x="3049.5" y="843.51">Mentorship Image Service</text></g><!--entity CartService--><g id="elem_CartService"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="120" x="1042" y="808.5441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="1142" y="813.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="1140" y="815.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="1140" y="819.5441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="80" x="1057" y="843.51">Cart Service</text></g><!--entity WishlistService--><g id="elem_WishlistService"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="145" x="861.5" y="808.5441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="986.5" y="813.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="984.5" y="815.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="984.5" y="819.5441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="105" x="876.5" y="843.51">Wishlist Service</text></g><!--entity PaymentService--><g id="elem_PaymentService"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="150" x="2311" y="808.5441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="2441" y="813.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="2439" y="815.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="2439" y="819.5441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="110" x="2326" y="843.51">Payment Service</text></g><!--entity AnalyticsService--><g id="elem_AnalyticsService"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="152" x="1508" y="808.5441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="1640" y="813.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="1638" y="815.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="1638" y="819.5441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="112" x="1523" y="843.51">Analytics Service</text></g><!--entity MarketAnalyticsService--><g id="elem_MarketAnalyticsService"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="203" x="1269.5" y="808.5441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="1452.5" y="813.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="1450.5" y="815.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="1450.5" y="819.5441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="163" x="1284.5" y="843.51">Market Analytics Service</text></g><!--entity ProfileRepo--><g id="elem_ProfileRepo"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="158" x="3407" y="1096.0441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="3545" y="1101.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="3543" y="1103.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="3543" y="1107.0441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="118" x="3422" y="1131.01">Profile Repository</text></g><!--entity PortfolioRepo--><g id="elem_PortfolioRepo"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="171" x="3600.5" y="1096.0441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="3751.5" y="1101.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="3749.5" y="1103.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="3749.5" y="1107.0441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="131" x="3615.5" y="1131.01">Portfolio Repository</text></g><!--entity BaseRepo--><g id="elem_BaseRepo"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="147" x="3412.5" y="1374.0441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="3539.5" y="1379.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="3537.5" y="1381.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="3537.5" y="1385.0441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="107" x="3427.5" y="1409.01">Base Repository</text></g><!--entity ProjectRepo--><g id="elem_ProjectRepo"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="161" x="4188.5" y="1096.0441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="4329.5" y="1101.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="4327.5" y="1103.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="4327.5" y="1107.0441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="121" x="4203.5" y="1131.01">Project Repository</text></g><!--entity AssignmentRepo--><g id="elem_AssignmentRepo"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="195" x="4384.5" y="1096.0441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="4559.5" y="1101.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="4557.5" y="1103.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="4557.5" y="1107.0441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="155" x="4399.5" y="1131.01">Assignment Repository</text></g><!--entity ApplicationRepo--><g id="elem_ApplicationRepo"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="191" x="4188.5" y="1374.0441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="4359.5" y="1379.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="4357.5" y="1381.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="4357.5" y="1385.0441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="151" x="4203.5" y="1409.01">Application Repository</text></g><!--entity MicroServiceRepo--><g id="elem_MicroServiceRepo"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="201" x="3879.5" y="1096.0441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="4060.5" y="1101.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="4058.5" y="1103.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="4058.5" y="1107.0441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="161" x="3894.5" y="1131.01">MicroService Repository</text></g><!--entity MicroAnalyticsRepo--><g id="elem_MicroAnalyticsRepo"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="228" x="4865" y="1096.0441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="5073" y="1101.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="5071" y="1103.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="5071" y="1107.0441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="188" x="4880" y="1131.01">MicroService Analytics Repo</text></g><!--entity CartRepo--><g id="elem_CartRepo"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="143" x="4686.5" y="1096.0441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="4809.5" y="1101.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="4807.5" y="1103.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="4807.5" y="1107.0441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="103" x="4701.5" y="1131.01">Cart Repository</text></g><!--entity UserModel--><g id="elem_UserModel"><path d="M10853.5,819.0441 C10853.5,809.0441 10879,809.0441 10879,809.0441 C10879,809.0441 10904.5,809.0441 10904.5,819.0441 L10904.5,847.112 C10904.5,857.112 10879,857.112 10879,857.112 C10879,857.112 10853.5,857.112 10853.5,847.112 L10853.5,819.0441 " fill="#FFFFFF" style="stroke:#000000;stroke-width:1.0;"/><path d="M10853.5,819.0441 C10853.5,829.0441 10879,829.0441 10879,829.0441 C10879,829.0441 10904.5,829.0441 10904.5,819.0441 " fill="none" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="31" x="10863.5" y="848.01">User</text></g><!--entity FreelancerModel--><g id="elem_FreelancerModel"><path d="M10940,819.0441 C10940,809.0441 11007,809.0441 11007,809.0441 C11007,809.0441 11074,809.0441 11074,819.0441 L11074,847.112 C11074,857.112 11007,857.112 11007,857.112 C11007,857.112 10940,857.112 10940,847.112 L10940,819.0441 " fill="#FFFFFF" style="stroke:#000000;stroke-width:1.0;"/><path d="M10940,819.0441 C10940,829.0441 11007,829.0441 11007,829.0441 C11007,829.0441 11074,829.0441 11074,819.0441 " fill="none" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="114" x="10950" y="848.01">FreelancerProfile</text></g><!--entity ClientModel--><g id="elem_ClientModel"><path d="M10830,1106.5441 C10830,1096.5441 10881,1096.5441 10881,1096.5441 C10881,1096.5441 10932,1096.5441 10932,1106.5441 L10932,1134.612 C10932,1144.612 10881,1144.612 10881,1144.612 C10881,1144.612 10830,1144.612 10830,1134.612 L10830,1106.5441 " fill="#FFFFFF" style="stroke:#000000;stroke-width:1.0;"/><path d="M10830,1106.5441 C10830,1116.5441 10881,1116.5441 10881,1116.5441 C10881,1116.5441 10932,1116.5441 10932,1106.5441 " fill="none" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="82" x="10840" y="1135.51">ClientProfile</text></g><!--entity PortfolioModel--><g id="elem_PortfolioModel"><path d="M10967.5,1106.5441 C10967.5,1096.5441 11021,1096.5441 11021,1096.5441 C11021,1096.5441 11074.5,1096.5441 11074.5,1106.5441 L11074.5,1134.612 C11074.5,1144.612 11021,1144.612 11021,1144.612 C11021,1144.612 10967.5,1144.612 10967.5,1134.612 L10967.5,1106.5441 " fill="#FFFFFF" style="stroke:#000000;stroke-width:1.0;"/><path d="M10967.5,1106.5441 C10967.5,1116.5441 11021,1116.5441 11021,1116.5441 C11021,1116.5441 11074.5,1116.5441 11074.5,1106.5441 " fill="none" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="87" x="10977.5" y="1135.51">ItemPortfolio</text></g><!--entity ProjectModel--><g id="elem_ProjectModel"><path d="M11181,819.0441 C11181,809.0441 11214,809.0441 11214,809.0441 C11214,809.0441 11247,809.0441 11247,819.0441 L11247,847.112 C11247,857.112 11214,857.112 11214,857.112 C11214,857.112 11181,857.112 11181,847.112 L11181,819.0441 " fill="#FFFFFF" style="stroke:#000000;stroke-width:1.0;"/><path d="M11181,819.0441 C11181,829.0441 11214,829.0441 11214,829.0441 C11214,829.0441 11247,829.0441 11247,819.0441 " fill="none" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="46" x="11191" y="848.01">Project</text></g><!--entity AssignmentModel--><g id="elem_AssignmentModel"><path d="M11282,819.0441 C11282,809.0441 11355,809.0441 11355,809.0441 C11355,809.0441 11428,809.0441 11428,819.0441 L11428,847.112 C11428,857.112 11355,857.112 11355,857.112 C11355,857.112 11282,857.112 11282,847.112 L11282,819.0441 " fill="#FFFFFF" style="stroke:#000000;stroke-width:1.0;"/><path d="M11282,819.0441 C11282,829.0441 11355,829.0441 11355,829.0441 C11355,829.0441 11428,829.0441 11428,819.0441 " fill="none" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="126" x="11292" y="848.01">ProjectAssignment</text></g><!--entity ApplicationModel--><g id="elem_ApplicationModel"><path d="M11181,1106.5441 C11181,1096.5441 11252,1096.5441 11252,1096.5441 C11252,1096.5441 11323,1096.5441 11323,1106.5441 L11323,1134.612 C11323,1144.612 11252,1144.612 11252,1144.612 C11252,1144.612 11181,1144.612 11181,1134.612 L11181,1106.5441 " fill="#FFFFFF" style="stroke:#000000;stroke-width:1.0;"/><path d="M11181,1106.5441 C11181,1116.5441 11252,1116.5441 11252,1116.5441 C11252,1116.5441 11323,1116.5441 11323,1106.5441 " fill="none" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="122" x="11191" y="1135.51">ProjectApplication</text></g><!--entity MicroServiceModel--><g id="elem_MicroServiceModel"><path d="M9862,819.0441 C9862,809.0441 9915,809.0441 9915,809.0441 C9915,809.0441 9968,809.0441 9968,819.0441 L9968,847.112 C9968,857.112 9915,857.112 9915,857.112 C9915,857.112 9862,857.112 9862,847.112 L9862,819.0441 " fill="#FFFFFF" style="stroke:#000000;stroke-width:1.0;"/><path d="M9862,819.0441 C9862,829.0441 9915,829.0441 9915,829.0441 C9915,829.0441 9968,829.0441 9968,819.0441 " fill="none" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="86" x="9872" y="848.01">MicroService</text></g><!--entity CategoryModel--><g id="elem_CategoryModel"><path d="M9747,819.0441 C9747,809.0441 9787,809.0441 9787,809.0441 C9787,809.0441 9827,809.0441 9827,819.0441 L9827,847.112 C9827,857.112 9787,857.112 9787,857.112 C9787,857.112 9747,857.112 9747,847.112 L9747,819.0441 " fill="#FFFFFF" style="stroke:#000000;stroke-width:1.0;"/><path d="M9747,819.0441 C9747,829.0441 9787,829.0441 9787,829.0441 C9787,829.0441 9827,829.0441 9827,819.0441 " fill="none" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="60" x="9757" y="848.01">Category</text></g><!--entity MentorshipModel--><g id="elem_MentorshipModel"><path d="M10075.5,819.0441 C10075.5,809.0441 10150,809.0441 10150,809.0441 C10150,809.0441 10224.5,809.0441 10224.5,819.0441 L10224.5,847.112 C10224.5,857.112 10150,857.112 10150,857.112 C10150,857.112 10075.5,857.112 10075.5,847.112 L10075.5,819.0441 " fill="#FFFFFF" style="stroke:#000000;stroke-width:1.0;"/><path d="M10075.5,819.0441 C10075.5,829.0441 10150,829.0441 10150,829.0441 C10150,829.0441 10224.5,829.0441 10224.5,819.0441 " fill="none" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="129" x="10085.5" y="848.01">MentorshipSession</text></g><!--entity CartItemModel--><g id="elem_CartItemModel"><path d="M10470.5,819.0441 C10470.5,809.0441 10510,809.0441 10510,809.0441 C10510,809.0441 10549.5,809.0441 10549.5,819.0441 L10549.5,847.112 C10549.5,857.112 10510,857.112 10510,857.112 C10510,857.112 10470.5,857.112 10470.5,847.112 L10470.5,819.0441 " fill="#FFFFFF" style="stroke:#000000;stroke-width:1.0;"/><path d="M10470.5,819.0441 C10470.5,829.0441 10510,829.0441 10510,829.0441 C10510,829.0441 10549.5,829.0441 10549.5,819.0441 " fill="none" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="59" x="10480.5" y="848.01">CartItem</text></g><!--entity WishlistItemModel--><g id="elem_WishlistItemModel"><path d="M10331,819.0441 C10331,809.0441 10383,809.0441 10383,809.0441 C10383,809.0441 10435,809.0441 10435,819.0441 L10435,847.112 C10435,857.112 10383,857.112 10383,857.112 C10383,857.112 10331,857.112 10331,847.112 L10331,819.0441 " fill="#FFFFFF" style="stroke:#000000;stroke-width:1.0;"/><path d="M10331,819.0441 C10331,829.0441 10383,829.0441 10383,829.0441 C10383,829.0441 10435,829.0441 10435,819.0441 " fill="none" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="84" x="10341" y="848.01">WishlistItem</text></g><!--entity PaymentModel--><g id="elem_PaymentModel"><path d="M10656,819.0441 C10656,809.0441 10695,809.0441 10695,809.0441 C10695,809.0441 10734,809.0441 10734,819.0441 L10734,847.112 C10734,857.112 10695,857.112 10695,857.112 C10695,857.112 10656,857.112 10656,847.112 L10656,819.0441 " fill="#FFFFFF" style="stroke:#000000;stroke-width:1.0;"/><path d="M10656,819.0441 C10656,829.0441 10695,829.0441 10695,829.0441 C10695,829.0441 10734,829.0441 10734,819.0441 " fill="none" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="58" x="10666" y="848.01">Payment</text></g><!--entity Database--><g id="elem_Database"><path d="M8730,1384.5441 C8730,1374.5441 8795,1374.5441 8795,1374.5441 C8795,1374.5441 8860,1374.5441 8860,1384.5441 L8860,1412.612 C8860,1422.612 8795,1422.612 8795,1422.612 C8795,1422.612 8730,1422.612 8730,1412.612 L8730,1384.5441 " fill="#FFFFFF" style="stroke:#000000;stroke-width:1.0;"/><path d="M8730,1384.5441 C8730,1394.5441 8795,1394.5441 8795,1394.5441 C8795,1394.5441 8860,1394.5441 8860,1384.5441 " fill="none" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="110" x="8740" y="1413.51">SQLite Database</text></g><!--entity MediaFiles--><g id="elem_MediaFiles"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="116" x="8895" y="1374.0441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="8991" y="1379.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="8989" y="1381.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="8989" y="1385.0441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="76" x="8910" y="1409.01">Media Files</text></g><!--entity URLRouter--><g id="elem_URLRouter"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="115" x="8458.5" y="1096.0441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="8553.5" y="1101.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="8551.5" y="1103.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="8551.5" y="1107.0441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="75" x="8473.5" y="1131.01">URL Router</text></g><!--entity Middleware--><g id="elem_Middleware"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="120" x="8269" y="1374.0441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="8369" y="1379.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="8367" y="1381.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="8367" y="1385.0441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="80" x="8284" y="1409.01">Middleware</text></g><!--entity ORM--><g id="elem_ORM"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="73" x="8608.5" y="1096.0441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="8661.5" y="1101.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="8659.5" y="1103.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="8659.5" y="1107.0441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="33" x="8623.5" y="1131.01">ORM</text></g><!--entity TemplateEngine--><g id="elem_TemplateEngine"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="154" x="8269" y="1096.0441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="8403" y="1101.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="8401" y="1103.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="8401" y="1107.0441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="114" x="8284" y="1131.01">Template Engine</text></g><!--entity StripeAPI--><g id="elem_StripeAPI"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="106" x="8944" y="1096.0441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="9030" y="1101.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="9028" y="1103.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="9028" y="1107.0441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="66" x="8959" y="1131.01">Stripe API</text></g><!--entity FileStorage--><g id="elem_FileStorage"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="119" x="8789.5" y="1096.0441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="8888.5" y="1101.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="8886.5" y="1103.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="8886.5" y="1107.0441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="79" x="8804.5" y="1131.01">File Storage</text></g><!--entity StaticServer--><g id="elem_StaticServer"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="151" x="9085.5" y="1096.0441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="9216.5" y="1101.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="9214.5" y="1103.0441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="9214.5" y="1107.0441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="111" x="9100.5" y="1131.01">Static File Server</text></g><!--entity UserFactory--><g id="elem_UserFactory"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="123" x="9284.5" y="522.5441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="9387.5" y="527.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="9385.5" y="529.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="9385.5" y="533.5441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="83" x="9299.5" y="557.51">User Factory</text></g><!--entity ProfileFactories--><g id="elem_ProfileFactories"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="147" x="9442.5" y="522.5441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="9569.5" y="527.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="9567.5" y="529.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="9567.5" y="533.5441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="107" x="9457.5" y="557.51">Profile Factories</text></g><!--entity ProjectFactories--><g id="elem_ProjectFactories"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="150" x="9271" y="808.5441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="9401" y="813.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="9399" y="815.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="9399" y="819.5441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="110" x="9286" y="843.51">Project Factories</text></g><!--entity ServiceFactories--><g id="elem_ServiceFactories"><rect fill="#FFFFFF" height="49.0679" rx="2.5" ry="2.5" style="stroke:#000000;stroke-width:1.0;" width="152" x="9456" y="808.5441"/><rect fill="#FFFFFF" height="10" style="stroke:#000000;stroke-width:1.0;" width="15" x="9588" y="813.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="9586" y="815.5441"/><rect fill="#FFFFFF" height="2" style="stroke:#000000;stroke-width:1.0;" width="4" x="9586" y="819.5441"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="112" x="9471" y="843.51">Service Factories</text></g><!--entity Browser--><g id="elem_Browser"><ellipse cx="8354" cy="802.0441" fill="#ADD8E6" rx="8" ry="8" style="stroke:#000000;stroke-width:1.0;"/><path d="M8354,810.0441 L8354,837.0441 M8341,818.0441 L8367,818.0441 M8354,837.0441 L8341,852.0441 M8354,837.0441 L8367,852.0441 " fill="none" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="89" x="8309.5" y="869.01">Web Browser</text></g><!--entity Mobile--><g id="elem_Mobile"><ellipse cx="8230" cy="802.0441" fill="#90EE90" rx="8" ry="8" style="stroke:#000000;stroke-width:1.0;"/><path d="M8230,810.0441 L8230,837.0441 M8217,818.0441 L8243,818.0441 M8230,837.0441 L8217,852.0441 M8230,837.0441 L8243,852.0441 " fill="none" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="89" x="8185.5" y="869.01">Mobile Client</text></g><!--entity ThirdParty--><g id="elem_ThirdParty"><ellipse cx="287" cy="802.0441" fill="#FFA500" rx="8" ry="8" style="stroke:#000000;stroke-width:1.0;"/><path d="M287,810.0441 L287,837.0441 M274,818.0441 L300,818.0441 M287,837.0441 L274,852.0441 M287,837.0441 L300,852.0441 " fill="none" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="14" lengthAdjust="spacing" textLength="113" x="230.5" y="869.01">Third-Party Apps</text></g><g id="elem_GMN205"><path d="M11500.5,1089.0441 L11500.5,1152.1622 L11699.5,1152.1622 L11699.5,1099.0441 L11689.5,1089.0441 L11500.5,1089.0441 " fill="#FFFFFF" style="stroke:#000000;stroke-width:1.0;"/><path d="M11689.5,1089.0441 L11689.5,1099.0441 L11699.5,1099.0441 L11689.5,1089.0441 " fill="#FFFFFF" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="144" x="11506.5" y="1107.9411">Django MVT Framework</text><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="166" x="11506.5" y="1125.6471">Handles HTTP, URL routing,</text><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="178" x="11506.5" y="1143.3531">ORM, and template rendering</text></g><g id="elem_GMN208"><path d="M5719.5,176.5441 L5719.5,381.3103 L5942.5,381.3103 L5942.5,186.5441 L5932.5,176.5441 L5719.5,176.5441 " fill="#FFFFFF" style="stroke:#000000;stroke-width:1.0;"/><path d="M5932.5,176.5441 L5932.5,186.5441 L5942.5,186.5441 L5932.5,176.5441 " fill="#FFFFFF" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="131" x="5725.5" y="195.4411">RESTful API Endpoints</text><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="153" x="5725.5" y="213.1471">- Django REST Framework</text><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="112" x="5725.5" y="230.8531">- JSON serialization</text><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="202" x="5725.5" y="248.5592">- Public access (no authentication)</text><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="183" x="5725.5" y="266.2652">- Used by external applications</text><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="3" x="5725.5" y="283.9712">&#160;</text><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="64" x="5725.5" y="301.6772">Endpoints:</text><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="148" x="5725.5" y="319.3832">&#8226; GET /api/microservices/</text><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="135" x="5731.5" y="337.0892">&#8594; List all microservices</text><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="174" x="5725.5" y="354.7953">&#8226; GET /api/microservices/{id}/</text><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="155" x="5731.5" y="372.5013">&#8594; Get microservice details</text></g><g id="elem_GMN211"><path d="M11500.5,766.0441 L11500.5,899.9862 L11693.5,899.9862 L11693.5,776.0441 L11683.5,766.0441 L11500.5,766.0441 " fill="#FFFFFF" style="stroke:#000000;stroke-width:1.0;"/><path d="M11683.5,766.0441 L11683.5,776.0441 L11693.5,776.0441 L11683.5,766.0441 " fill="#FFFFFF" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="115" x="11506.5" y="784.9411">Business logic layer</text><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="172" x="11506.5" y="802.6471">Implements SOLID principles</text><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="134" x="11506.5" y="820.3531">Dependency Inversion</text><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="3" x="11506.5" y="838.0592">&#160;</text><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="95" x="11506.5" y="855.7652">Shared by both:</text><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="89" x="11506.5" y="873.4712">- Web UI (MVT)</text><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="59" x="11506.5" y="891.1772">- REST API</text></g><g id="elem_GMN214"><path d="M11735,1089.0441 L11735,1152.1622 L11963,1152.1622 L11963,1099.0441 L11953,1089.0441 L11735,1089.0441 " fill="#FFFFFF" style="stroke:#000000;stroke-width:1.0;"/><path d="M11953,1089.0441 L11953,1099.0441 L11963,1099.0441 L11953,1089.0441 " fill="#FFFFFF" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="140" x="11741" y="1107.9411">Data access abstraction</text><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="113" x="11741" y="1125.6471">Repository pattern</text><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="207" x="11741" y="1143.3531">Separates business logic from data</text></g><g id="elem_GMN217"><path d="M11998,1089.0441 L11998,1152.1622 L12162,1152.1622 L12162,1099.0441 L12152,1089.0441 L11998,1089.0441 " fill="#FFFFFF" style="stroke:#000000;stroke-width:1.0;"/><path d="M12152,1089.0441 L12152,1099.0441 L12162,1099.0441 L12152,1089.0441 " fill="#FFFFFF" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="143" x="12004" y="1107.9411">Third-party integrations</text><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="118" x="12004" y="1125.6471">Stripe for payments</text><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="129" x="12004" y="1143.3531">File storage for media</text></g><g id="elem_GMN220"><path d="M11,757.0441 L11,908.6922 A0,0 0 0 0 11,908.6922 L195,908.6922 A0,0 0 0 0 195,908.6922 L195,837.0441 L230.44,833.0441 L195,829.0441 L195,767.0441 L185,757.0441 L11,757.0441 A0,0 0 0 0 11,757.0441 " fill="#FFFFFF" style="stroke:#000000;stroke-width:1.0;"/><path d="M185,757.0441 L185,767.0441 L195,767.0441 L185,757.0441 " fill="#FFFFFF" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="125" x="17" y="775.9411">External Applications</text><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="80" x="17" y="793.6471">- Mobile apps</text><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="128" x="17" y="811.3531">- Partner integrations</text><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="104" x="17" y="829.0592">- Data consumers</text><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="93" x="17" y="846.7652">- Analytics tools</text><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="3" x="17" y="864.4712">&#160;</text><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="114" x="17" y="882.1772">Access via REST API</text><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="163" x="17" y="899.8832">No authentication required</text></g><!--link RESTAPI to GMN15--><g id="link_RESTAPI_GMN15"><path d="M5145.8572,265.6888 C5145.7447,265.5111 5145.631,265.3319 5145.5161,265.1512 C5144.5976,263.7055 5143.6076,262.1622 5142.5477,260.5287 C5140.4279,257.2615 5138.0286,253.6334 5135.362,249.7032 C5124.6959,233.9822 5109.7556,213.4279 5091.3388,191.8116 C5054.505,148.5791 5003.765,101.0991 4945.5,79.5441 C4906.53,65.1241 4797.82,66.0941 4758.5,79.5441 C4666.73,110.9341 4582.35,189.8041 4536.65,238.4441 " fill="none" id="RESTAPI-GMN15" style="stroke:#000000;stroke-width:1.0;stroke-dasharray:7.0,7.0;"/></g><!--link Browser to URLRouter--><g id="link_Browser_URLRouter"><path d="M8398.64,840.7241 C8484.64,854.5941 8668.06,889.4341 8705,939.0441 C8710.04,945.8141 8710.76,951.8641 8705,958.0441 C8687.68,976.6241 8612.06,951.8441 8591,966.0441 C8546.36,996.1341 8528.5437,1054.8402 8521.2437,1089.8802 " fill="none" id="Browser-to-URLRouter" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="8520.02,1095.7541,8525.7715,1087.7591,8521.0398,1090.8592,8517.9397,1086.1275,8520.02,1095.7541" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="139" x="8710" y="953.9411">HTTP Request (Web UI)</text></g><!--link Mobile to URLRouter--><g id="link_Mobile_URLRouter"><path d="M8256.49,873.2241 C8266.49,885.8941 8278.69,899.1941 8292,909.0441 C8319.86,929.6741 8333.02,923.4941 8364,939.0441 C8378.78,946.4641 8380.5,952.2841 8396,958.0441 C8415.04,965.1241 8424.78,953.8141 8441,966.0441 C8483.74,998.2741 8502.1526,1055.5174 8510.0826,1089.9274 " fill="none" id="Mobile-to-URLRouter" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="8511.43,1095.7741,8513.3067,1086.1057,8510.3072,1090.9018,8505.511,1087.9023,8511.43,1095.7741" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="139" x="8397" y="953.9411">HTTP Request (Web UI)</text></g><!--link Browser to ListAPI--><g id="link_Browser_ListAPI"><path d="M8349.65,792.9341 C8343.42,756.9741 8328.33,705.3041 8292,678.5441 C8216.42,622.8641 7956.45,682.4241 7871,643.5441 C7751.99,589.4041 7780.52,489.2341 7660,438.5441 C7428.97,341.3741 5638.68,472.1641 5405,381.5441 C5368.9,367.5441 5340.4068,341.6312 5318.8768,317.7412 " fill="none" id="Browser-to-ListAPI" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="5314.86,313.2841,5317.9138,322.6476,5318.2073,316.9983,5323.8565,317.2919,5314.86,313.2841" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="140" x="7872" y="543.4411">GET /api/microservices/</text><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="91" x="7896.5" y="561.1471">(JSON Request)</text></g><!--link Mobile to ListAPI--><g id="link_Mobile_ListAPI"><path d="M8216.67,792.9341 C8201.83,756.1541 8173.98,703.1841 8130,678.5441 C8116.18,670.8041 7860.8,671.6941 7845,670.5441 C7572.72,650.6341 5654.7,491.9241 5405,381.5441 C5370.08,366.1041 5341.9979,340.9467 5320.2579,317.6967 " fill="none" id="Mobile-to-ListAPI" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="5316.16,313.3141,5319.3852,322.6199,5319.5749,316.9662,5325.2286,317.156,5316.16,313.3141" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="140" x="7511" y="543.4411">GET /api/microservices/</text><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="91" x="7535.5" y="561.1471">(JSON Request)</text></g><!--link ThirdParty to ListAPI--><g id="link_ThirdParty_ListAPI"><path d="M304.55,792.7641 C322.88,756.6841 355.24,704.9241 400,678.5441 C1194.57,210.1941 1537.93,476.0641 2458,411.5441 C2533.57,406.2441 5115.07,410.6641 5185,381.5441 C5218.37,367.6441 5243.1227,342.0229 5261.6027,318.0929 " fill="none" id="ThirdParty-to-ListAPI" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="5265.27,313.3441,5256.6032,318.0225,5262.2139,317.3014,5262.935,322.9122,5265.27,313.3441" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="140" x="959" y="543.4411">GET /api/microservices/</text><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="91" x="983.5" y="561.1471">(JSON Request)</text></g><!--link Browser to DetailAPI--><g id="link_Browser_DetailAPI"><path d="M8363.17,793.0341 C8379.3,713.4641 8402.48,532.0841 8305,438.5441 C8200.63,338.3941 5841.03,421.4641 5702,381.5441 C5654.72,367.9641 5612.2184,340.8063 5580.0884,316.6863 " fill="none" id="Browser-to-DetailAPI" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="5575.29,313.0841,5580.0861,321.6863,5579.2887,316.0859,5584.889,315.2884,5575.29,313.0841" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="166" x="8378" y="543.4411">GET /api/microservices/{id}/</text><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="91" x="8415.5" y="561.1471">(JSON Request)</text></g><!--link Mobile to DetailAPI--><g id="link_Mobile_DetailAPI"><path d="M8209.73,792.8441 C8158.8,694.4741 8028.92,444.5441 8021,438.5441 C7976.05,404.4741 7953.04,417.9641 7897,411.5441 C7775.84,397.6641 5819.21,415.2341 5702,381.5441 C5654.72,367.9541 5612.2178,340.797 5580.0978,316.677 " fill="none" id="Mobile-to-DetailAPI" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="5575.3,313.0741,5580.0949,321.677,5579.2982,316.0765,5584.8987,315.2798,5575.3,313.0741" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="166" x="8130" y="543.4411">GET /api/microservices/{id}/</text><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="91" x="8167.5" y="561.1471">(JSON Request)</text></g><!--link ThirdParty to DetailAPI--><g id="link_ThirdParty_DetailAPI"><path d="M303.58,793.0041 C321.48,756.2841 353.79,703.3541 400,678.5441 C417.35,669.2241 1088.34,644.6641 1108,643.5441 C2704.29,552.5141 3101.4,496.9941 4698,411.5441 C4776.51,407.3441 5331.21,408.7041 5405,381.5441 C5443.7,367.3041 5475.7001,341.1589 5500.0501,317.3489 " fill="none" id="ThirdParty-to-DetailAPI" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="5504.34,313.1541,5495.1085,316.5863,5500.765,316.6498,5500.7016,322.3063,5504.34,313.1541" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="166" x="4207" y="543.4411">GET /api/microservices/{id}/</text><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="91" x="4244.5" y="561.1471">(JSON Request)</text></g><!--link ListAPI to ListAPIView--><g id="link_ListAPI_ListAPIView"><path d="M5260,313.4841 C5240.63,335.0341 5213.33,362.4941 5185,381.5441 C5139.24,412.3141 5124.81,418.4741 5071,430.5441 C5046.48,436.0441 4867.11,426.6041 4845,438.5441 C4811.62,456.5841 4791.9904,490.934 4780.6204,516.724 " fill="none" id="ListAPI-to-ListAPIView" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="4778.2,522.2141,4785.4907,515.5925,4780.217,517.639,4778.1706,512.3653,4778.2,522.2141" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="98" x="5133" y="426.4411">Process Request</text></g><!--link DetailAPI to RetrieveAPIView--><g id="link_DetailAPI_RetrieveAPIView"><path d="M5499.16,313.2541 C5474.23,334.9841 5439.42,362.7341 5405,381.5441 C5273.82,453.2341 5111.1957,501.7195 5016.0157,526.5495 " fill="none" id="DetailAPI-to-RetrieveAPIView" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="5010.21,528.0641,5019.9282,529.6627,5015.0481,526.802,5017.9088,521.9218,5010.21,528.0641" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="98" x="5345" y="426.4411">Process Request</text></g><!--link ListAPIView to MicroSerializer--><g id="link_ListAPIView_MicroSerializer"><path d="M4770.38,522.2441 C4772.46,494.9941 4777.45,449.2441 4789,411.5441 C4801.08,372.0941 4820.3616,334.784 4834.9216,309.094 " fill="none" id="ListAPIView-to-MicroSerializer" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="4837.88,303.8741,4829.9624,309.7317,4835.4146,308.224,4836.9223,313.6763,4837.88,303.8741" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="79" x="4790" y="426.4411">Serialize Data</text></g><!--link MicroSerializer to ListAPIView--><g id="link_MicroSerializer_ListAPIView"><path d="M4831.33,303.8141 C4812.23,325.1841 4782.57,356.9141 4754,381.5441 C4736.63,396.5241 4722.5,391.1441 4712,411.5441 C4692.62,449.2041 4718.8805,490.4041 4742.2005,517.6741 " fill="none" id="MicroSerializer-to-ListAPIView" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="4746.1,522.2341,4743.2907,512.7944,4742.8504,518.4341,4737.2107,517.9937,4746.1,522.2341" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="62" x="4713" y="426.4411">JSON Data</text></g><!--link RetrieveAPIView to MicroSerializer--><g id="link_RetrieveAPIView_MicroSerializer"><path d="M4953.22,522.3241 C4970.72,495.1341 4993.23,449.4541 4978,411.5441 C4959.61,365.7741 4921.6212,330.5921 4891.0112,307.2521 " fill="none" id="RetrieveAPIView-to-MicroSerializer" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="4886.24,303.6141,4890.9715,312.252,4890.216,306.6458,4895.8222,305.8903,4886.24,303.6141" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="79" x="4983" y="426.4411">Serialize Data</text></g><!--link MicroSerializer to RetrieveAPIView--><g id="link_MicroSerializer_RetrieveAPIView"><path d="M4859.45,303.6541 C4875.39,354.1241 4910.8338,466.3424 4926.7538,516.7724 " fill="none" id="MicroSerializer-to-RetrieveAPIView" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="4928.56,522.4941,4929.6651,512.7074,4927.0548,517.726,4922.0362,515.1158,4928.56,522.4941" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="62" x="4900" y="426.4411">JSON Data</text></g><!--link ListAPIView to MicroServices--><g id="link_ListAPIView_MicroServices"><path d="M4710.82,553.1341 C4481.78,572.8841 3620.08,644.6941 2909,670.5441 C2900.96,670.8341 1757.01,673.1941 1751,678.5441 C1725.725,701.0391 1720.7275,738.5766 1722.17,770.8991 C1722.3503,774.9394 1722.6313,778.8982 1722.9858,782.736 C1723.1631,784.6549 1723.3587,786.5435 1723.5694,788.397 C1723.6748,789.3237 1723.7839,790.2416 1723.8963,791.1501 C1723.9244,791.3772 1723.2013,785.6509 1723.2299,785.8769 " fill="none" id="ListAPIView-to-MicroServices" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="1723.9812,791.8296,1726.8227,782.3996,1723.3551,786.869,1718.8857,783.4014,1723.9812,791.8296" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="122" x="3318" y="666.4411">Get All Microservices</text></g><!--link RetrieveAPIView to MicroServices--><g id="link_RetrieveAPIView_MicroServices"><path d="M4949.71,571.9641 C4963.59,599.6741 4979.66,644.8241 4954,670.5441 C4938.29,686.2941 1767.65,663.7941 1751,678.5441 C1725.675,700.9841 1720.6775,738.5191 1722.1325,770.8541 C1722.3144,774.896 1722.5971,778.8566 1722.9535,782.6963 C1723.1317,784.6162 1723.3283,786.5059 1723.54,788.3603 C1723.6459,789.2876 1723.7555,790.206 1723.8684,791.115 C1723.8966,791.3423 1723.1708,785.6165 1723.1995,785.8426 " fill="none" id="RetrieveAPIView-to-MicroServices" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="1723.9537,791.795,1726.7907,782.3636,1723.3252,786.8347,1718.8541,783.3692,1723.9537,791.795" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="133" x="4966" y="666.4411">Get Microservice by ID</text></g><!--link ListAPIView to Browser--><g id="link_ListAPIView_Browser"><path d="M4742.95,571.5641 C4716.15,598.4841 4681.99,642.4741 4710,670.5441 C4727.57,688.1541 8271.39,664.6141 8292,678.5441 C8329.62,703.9841 8343.4745,750.5691 8349.2945,787.0391 " fill="none" id="ListAPIView-to-Browser" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="8350.24,792.9641,8352.7717,783.4462,8349.4521,788.0266,8344.8717,784.7069,8350.24,792.9641" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="98" x="4711" y="666.4411">HTTP 200 (JSON)</text></g><!--link ListAPIView to Mobile--><g id="link_ListAPIView_Mobile"><path d="M4710.95,560.9141 C4635.45,580.0541 4518.92,619.3541 4570,670.5441 C4587.46,688.0441 8108.28,666.7341 8130,678.5441 C8174.43,702.6941 8200.0336,750.4785 8214.7336,787.4585 " fill="none" id="ListAPIView-to-Mobile" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="8216.95,793.0341,8217.3425,783.1931,8215.103,788.3877,8209.9083,786.1482,8216.95,793.0341" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="98" x="4571" y="666.4411">HTTP 200 (JSON)</text></g><!--link ListAPIView to ThirdParty--><g id="link_ListAPIView_ThirdParty"><path d="M4710.63,550.8441 C4473.02,562.2941 3555.39,607.0841 2801,651.5441 C2671.62,659.1741 2639.53,666.0741 2510,670.5441 C2495.36,671.0541 413.06,671.9041 400,678.5441 C353.09,702.3741 323.4435,750.3988 305.7535,787.4788 " fill="none" id="ListAPIView-to-ThirdParty" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="303.17,792.8941,310.6555,786.4935,305.3229,788.3814,303.4351,783.0488,303.17,792.8941" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="98" x="2802" y="666.4411">HTTP 200 (JSON)</text></g><!--link RetrieveAPIView to Browser--><g id="link_RetrieveAPIView_Browser"><path d="M5010.09,551.1641 C5304.17,563.5441 6417.64,610.5841 7334,651.5441 C7516.68,659.7041 7562.22,664.9841 7745,670.5441 C7760.19,671.0041 8279.46,669.9541 8292,678.5441 C8329.34,704.1341 8343.2382,750.4117 8349.1482,786.8017 " fill="none" id="RetrieveAPIView-to-Browser" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="8350.11,792.7241,8352.6155,783.1993,8349.3085,787.7888,8344.719,784.4817,8350.11,792.7241" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="98" x="7746" y="666.4411">HTTP 200 (JSON)</text></g><!--link RetrieveAPIView to Mobile--><g id="link_RetrieveAPIView_Mobile"><path d="M5010.22,553.2141 C5296.42,572.8741 6355.99,643.3341 7230,670.5441 C7242.49,670.9341 8119.04,672.5341 8130,678.5441 C8174.21,702.7641 8199.7822,750.263 8214.5422,787.173 " fill="none" id="RetrieveAPIView-to-Mobile" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="8216.77,792.7441,8217.1423,782.9023,8214.9135,788.1015,8209.7142,785.8727,8216.77,792.7441" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="98" x="7231" y="666.4411">HTTP 200 (JSON)</text></g><!--link RetrieveAPIView to ThirdParty--><g id="link_RetrieveAPIView_ThirdParty"><path d="M4916.58,571.7841 C4889.05,604.6541 4839.22,661.0741 4814,670.5441 C4785.3,681.3141 427.34,664.6841 400,678.5441 C353.07,702.3241 323.4218,750.368 305.7418,787.458 " fill="none" id="RetrieveAPIView-to-ThirdParty" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="303.16,792.8741,310.6434,786.4711,305.3115,788.3607,303.4219,783.0287,303.16,792.8741" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="98" x="4841" y="666.4411">HTTP 200 (JSON)</text></g><!--link URLRouter to Middleware--><g id="link_URLRouter_Middleware"><path d="M8503.09,1145.0841 C8490.3,1165.8541 8468.63,1194.9641 8441,1209.0441 C8421.34,1219.0641 8357.54,1201.3641 8342,1217.0441 C8300.86,1258.5441 8311.2075,1329.1976 8320.7275,1367.9176 " fill="none" id="URLRouter-to-Middleware" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="8322.16,1373.7441,8323.8955,1364.0494,8320.9662,1368.8887,8316.1269,1365.9594,8322.16,1373.7441" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="88" x="8343" y="1231.9411">Route Request</text></g><!--link Middleware to CoreViews--><g id="link_Middleware_CoreViews"><path d="M8268.98,1394.1241 C8067.1,1381.5541 7416.14,1332.1041 7253,1209.0441 C7146.52,1128.7241 7232.02,1014.4541 7122,939.0441 C7055.42,893.4041 6827.44,953.4041 6760,909.0441 C6744.71,898.9891 6734.8475,881.0791 6728.7425,865.2829 C6728.5517,864.7892 6728.3646,864.2977 6728.1811,863.8085 C6728.1352,863.6862 6730.1831,869.1869 6730.1377,869.0649 " fill="none" id="Middleware-to-CoreViews" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="6728.0442,863.442,6727.4358,873.272,6729.7887,868.1278,6734.933,870.4807,6728.0442,863.442" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="87" x="7254" y="1125.9411">Auth Requests</text></g><!--link Middleware to ProjectViews--><g id="link_Middleware_ProjectViews"><path d="M8268.81,1396.2741 C7847.97,1387.0741 5359.9,1327.7641 5258,1209.0441 C5187.66,1127.0941 5200.1,1057.2141 5258,966.0441 C5294.41,908.7141 5363.05,875.8416 5423.3738,857.2391 C5453.5356,847.9379 5481.6184,842.2041 5502.5539,838.7644 C5513.0216,837.0446 5521.7025,835.8982 5527.9631,835.1663 C5528.7456,835.0748 5529.4904,834.9897 5530.1961,834.9109 C5530.3725,834.8911 5524.5828,835.5307 5524.7543,835.5117 " fill="none" id="Middleware-to-ProjectViews" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="5530.718,834.8529,5521.3332,831.8654,5525.7482,835.4019,5522.2117,839.817,5530.718,834.8529" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="100" x="5259" y="1125.9411">Project Requests</text></g><!--link Middleware to MicroViews--><g id="link_Middleware_MicroViews"><path d="M8268.92,1395.9541 C7862.12,1384.9041 5523.99,1316.7941 5423,1209.0441 C5349.15,1130.2441 5351.2,1046.7241 5423,966.0441 C5495.59,884.4841 5816.41,963.5641 5911,909.0441 C5928.46,898.9841 5942.145,881.0741 5951.615,865.2791 C5953.9825,861.3304 5956.0866,857.5138 5957.9203,853.9851 C5958.1495,853.544 5958.3745,853.1074 5958.5953,852.6757 C5958.7057,852.4598 5956.101,857.5962 5956.2093,857.3827 " fill="none" id="Middleware-to-MicroViews" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="5958.9232,852.0316,5951.2849,858.249,5956.6616,856.4909,5958.4197,861.8676,5958.9232,852.0316" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="133" x="5424" y="1125.9411">Microservice Requests</text></g><!--link Middleware to MentorViews--><g id="link_Middleware_MentorViews"><path d="M8268.73,1383.7041 C8177.66,1360.3841 8003.2,1306.0241 7886,1209.0441 C7774.7,1116.9441 7827.85,1015.0641 7705,939.0441 C7616.21,884.1041 7550.13,978.3141 7472,909.0441 C7465.7675,903.5191 7461.4394,896.271 7458.4588,888.4585 C7457.7136,886.5054 7457.0527,884.517 7456.4672,882.5114 C7456.3941,882.2607 7457.9505,887.7845 7457.8797,887.5333 " fill="none" id="Middleware-to-MentorViews" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="7456.2512,881.7585,7454.844,891.5063,7457.6082,886.5709,7462.5437,889.3351,7456.2512,881.7585" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="128" x="7887" y="1125.9411">Mentorship Requests</text></g><!--link Middleware to CartViews--><g id="link_Middleware_CartViews"><path d="M8298.9,1373.8341 C8257.74,1340.3341 8183.3,1275.7741 8133,1209.0441 C8051.26,1100.6141 8102.38,1015.2641 7990,939.0441 C7887.88,869.7841 7807.64,989.4041 7714,909.0441 C7707.66,903.6041 7703.2181,896.3997 7700.1267,888.6047 C7699.3539,886.656 7698.6654,884.6703 7698.0528,882.6661 C7697.9762,882.4155 7699.6018,887.9186 7699.5276,887.6675 " fill="none" id="Middleware-to-CartViews" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="7697.8266,881.9137,7696.5421,891.6784,7699.2441,886.7085,7704.2139,889.4105,7697.8266,881.9137" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="83" x="8134" y="1125.9411">Cart Requests</text></g><!--link Middleware to PaymentViews--><g id="link_Middleware_PaymentViews"><path d="M8268.98,1392.5641 C8087.86,1376.3941 7551.33,1319.9541 7422,1209.0441 C7324.74,1125.6441 7424.15,1015.0341 7321,939.0441 C7226.74,869.6041 6885.31,983.5541 6795,909.0441 C6788.575,903.7441 6784.1475,896.6122 6781.1269,888.8466 C6780.3717,886.9052 6779.7045,884.9242 6779.116,882.9223 C6779.0424,882.672 6778.9701,882.4215 6778.8989,882.1706 C6778.8634,882.0452 6780.4373,887.6999 6780.4024,887.5743 " fill="none" id="Middleware-to-PaymentViews" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="6778.7932,881.7941,6777.3536,891.5372,6780.1342,886.6109,6785.0604,889.3916,6778.7932,881.7941" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="112" x="7423" y="1125.9411">Payment Requests</text></g><!--link Middleware to AnalyticsViews--><g id="link_Middleware_AnalyticsViews"><path d="M8268.9,1388.6141 C8116.24,1364.8541 7718.73,1295.9441 7621,1209.0441 C7524.54,1123.2641 7618.31,1015.0741 7514,939.0441 C7432.65,879.7441 7139.35,973.4641 7062,909.0441 C7055.6,903.7141 7051.1856,896.5666 7048.1705,888.7946 C7047.4167,886.8516 7046.7503,884.8695 7046.1623,882.8671 C7046.0888,882.6168 7046.0165,882.3662 7045.9454,882.1153 C7045.9099,881.9898 7047.4828,887.6448 7047.4478,887.5192 " fill="none" id="Middleware-to-AnalyticsViews" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="7045.8397,881.7387,7044.3982,891.4815,7047.1798,886.5558,7052.1055,889.3373,7045.8397,881.7387" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="111" x="7622" y="1125.9411">Analytics Requests</text></g><!--link CoreViews to CoreServices--><g id="link_CoreViews_CoreServices"><path d="M6728.0347,806.128 C6728.0779,805.9487 6728.121,805.7688 6728.1641,805.5883 C6728.2504,805.2272 6728.3364,804.8635 6728.4222,804.4974 C6729.1087,801.5681 6729.7808,798.4788 6730.4132,795.2617 C6731.6779,788.8274 6732.7834,781.8816 6733.5263,774.6816 C6736.4975,745.8816 6733.665,713.0141 6712,692.5441 C6652.41,636.2541 875.42,643.1541 810,692.5441 C797.6525,701.8666 788.9181,714.7235 782.7761,728.9011 C781.2406,732.4455 779.8671,736.0725 778.6397,739.7474 C778.4863,740.2068 780.1799,734.9576 780.031,735.4184 " fill="none" id="CoreViews-to-CoreServices" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="778.1862,741.1277,784.7597,733.7936,779.7236,736.3699,777.1472,731.3338,778.1862,741.1277" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="87" x="5322.5" y="666.4411">Business Logic</text></g><!--link ProjectViews to ProjectServices--><g id="link_ProjectViews_ProjectServices"><path d="M5530.987,832.3595 C5530.5475,832.3218 5530.0903,832.2827 5529.6154,832.2421 C5528.6657,832.1608 5527.6453,832.0735 5526.5551,831.9804 C5524.3746,831.7943 5521.9145,831.5846 5519.1804,831.3522 C5508.2438,830.4225 5492.9224,829.1285 5473.572,827.5142 C5434.8713,824.2857 5380.0544,819.7764 5311.9675,814.3394 C5175.7937,803.4654 4986.54,788.8804 4766.975,773.4091 C4327.845,742.4666 3767.47,707.9791 3268,692.5441 C3188.59,690.0941 2613,640.4741 2553,692.5441 C2541.6475,702.3941 2534.5694,715.5272 2530.3733,729.8196 C2529.8488,731.6061 2529.3693,733.4108 2528.9321,735.2294 C2528.7135,736.1387 2528.5055,737.0515 2528.3078,737.9673 C2528.2089,738.4252 2528.1126,738.8838 2528.0187,739.3431 C2527.9718,739.5728 2529.0937,733.9174 2529.0481,734.1474 " fill="none" id="ProjectViews-to-ProjectServices" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="2527.8799,740.0326,2533.5556,731.9836,2528.8534,735.1282,2525.7087,730.426,2527.8799,740.0326" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="87" x="5416.5" y="666.4411">Business Logic</text></g><!--link MicroViews to MicroServices--><g id="link_MicroViews_MicroServices"><path d="M5958.9961,773.3217 C5958.9394,773.0927 5958.8824,772.8635 5958.825,772.6341 C5951.475,743.2716 5937.515,710.5191 5911,692.5441 C5863.18,660.1241 1794.51,654.5241 1751,692.5441 C1728.39,712.3041 1723.015,745.1391 1723.5825,774.0991 C1723.618,775.9091 1723.6767,777.704 1723.7558,779.4796 C1723.7954,780.3673 1723.84,781.2503 1723.8895,782.128 C1723.9142,782.5668 1723.5684,777.0158 1723.5955,777.4519 " fill="none" id="MicroViews-to-MicroServices" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="1723.9672,783.4404,1727.402,774.2098,1723.6575,778.45,1719.4173,774.7054,1723.9672,783.4404" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="87" x="5677.5" y="666.4411">Business Logic</text></g><!--link MentorViews to MentorshipServices--><g id="link_MentorViews_MentorshipServices"><path d="M7444.9961,773.3217 C7444.9394,773.0927 7444.8824,772.8635 7444.825,772.6341 C7437.475,743.2716 7423.515,710.5191 7397,692.5441 C7346.66,658.4141 3063.8,652.5241 3018,692.5441 C2995.39,712.3041 2990.015,745.1391 2990.5825,774.0991 C2990.618,775.9091 2990.6767,777.704 2990.7558,779.4796 C2990.7954,780.3673 2990.84,781.2503 2990.8895,782.128 C2990.9142,782.5668 2990.5684,777.0158 2990.5955,777.4519 " fill="none" id="MentorViews-to-MentorshipServices" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="2990.9672,783.4404,2994.402,774.2098,2990.6575,778.45,2986.4173,774.7054,2990.9672,783.4404" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="87" x="5836.5" y="666.4411">Business Logic</text></g><!--link CartViews to CartServices--><g id="link_CartViews_CartServices"><path d="M7685.9961,773.3217 C7685.9394,773.0927 7685.8824,772.8635 7685.825,772.6341 C7678.475,743.2716 7664.515,710.5191 7638,692.5441 C7598.95,666.0741 880.52,661.5041 845,692.5441 C822.39,712.3041 817.015,745.1391 817.5825,774.0991 C817.618,775.9091 817.6767,777.704 817.7558,779.4796 C817.7954,780.3673 817.84,781.2503 817.8895,782.128 C817.9142,782.5668 817.5684,777.0158 817.5955,777.4519 " fill="none" id="CartViews-to-CartServices" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="817.9672,783.4404,821.402,774.2098,817.6575,778.45,813.4173,774.7054,817.9672,783.4404" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="87" x="5228.5" y="666.4411">Business Logic</text></g><!--link PaymentViews to PaymentServices--><g id="link_PaymentViews_PaymentServices"><path d="M6767.8138,741.1277 C6767.6649,740.6669 6767.5137,740.2068 6767.3603,739.7474 C6766.1329,736.0725 6764.7594,732.4455 6763.2239,728.9011 C6757.0819,714.7235 6748.3475,701.8666 6736,692.5441 C6686.77,655.3741 2341.45,651.9541 2295,692.5441 C2272.39,712.3041 2267.015,745.1391 2267.5825,774.0991 C2267.618,775.9091 2267.6767,777.704 2267.7558,779.4796 C2267.7954,780.3673 2267.84,781.2503 2267.8895,782.128 C2267.9142,782.5668 2267.5684,777.0158 2267.5955,777.4519 " fill="none" id="PaymentViews-to-PaymentServices" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="2267.9672,783.4404,2271.402,774.2098,2267.6575,778.45,2263.4173,774.7054,2267.9672,783.4404" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="87" x="6324.5" y="666.4411">Business Logic</text></g><!--link AnalyticsViews to AnalyticsServices--><g id="link_AnalyticsViews_AnalyticsServices"><path d="M7034.9961,773.3217 C7034.9394,773.0927 7034.8824,772.8635 7034.825,772.6341 C7027.475,743.2716 7013.515,710.5191 6987,692.5441 C6921.09,647.8641 1314.14,640.3541 1254,692.5441 C1242.6475,702.3941 1235.5694,715.5272 1231.3733,729.8196 C1230.8488,731.6061 1230.3693,733.4108 1229.9321,735.2294 C1229.7135,736.1387 1229.5055,737.0515 1229.3078,737.9673 C1229.2089,738.4252 1229.1126,738.8838 1229.0187,739.3431 C1228.9718,739.5728 1230.0937,733.9174 1230.0481,734.1474 " fill="none" id="AnalyticsViews-to-AnalyticsServices" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="1228.8799,740.0326,1234.5556,731.9836,1229.8534,735.1282,1226.7087,730.426,1228.8799,740.0326" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="87" x="5134.5" y="666.4411">Business Logic</text></g><!--link CoreServices to CoreRepos--><g id="link_CoreServices_CoreRepos"><path d="M778.0067,861.2771 C778.0517,861.3958 778.097,861.5147 778.1424,861.6338 C778.5062,862.5865 778.8836,863.5507 779.275,864.5241 C785.5375,880.0991 795.38,898.0391 810,909.0441 C893.5,971.9141 936.5,943.5041 1040,958.0441 C1552.405,1030.0041 2132.86,1070.3466 2586.4788,1092.7154 C2813.2881,1103.8997 3008.3884,1110.5907 3147.4189,1114.4936 C3216.9341,1116.4451 3272.4319,1117.6996 3310.8671,1118.4703 C3330.0847,1118.8556 3345.0367,1119.12 3355.3424,1119.2901 C3357.9188,1119.3326 3360.2048,1119.3693 3362.1945,1119.4004 C3362.692,1119.4082 3357.1716,1119.323 3357.6319,1119.3301 " fill="none" id="CoreServices-to-CoreRepos" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="3363.6312,1119.4228,3354.694,1115.2842,3358.6317,1119.3455,3354.5705,1123.2833,3363.6312,1119.4228" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="70" x="1041" y="953.9411">Data Access</text></g><!--link ProjectServices to ProjectRepos--><g id="link_ProjectServices_ProjectRepos"><path d="M2536.2811,881.5504 C2536.4253,882.0531 2536.5743,882.5546 2536.7281,883.0548 C2537.3437,885.0555 2538.038,887.0341 2538.8202,888.9718 C2541.9488,896.7222 2546.4825,903.8166 2553,909.0441 C2584.28,934.1241 3234.01,936.2141 3274,939.0441 C3358.65,945.0341 3379.27,953.2841 3464,958.0441 C3481.56,959.0341 4082.66,955.8741 4097,966.0441 C4111.5775,976.3816 4122.3719,990.9272 4130.3622,1006.9838 C4134.3573,1015.0121 4137.6515,1023.4181 4140.367,1031.8647 C4141.7247,1036.088 4142.9378,1040.3214 4144.0216,1044.5229 C4144.2925,1045.5732 4143.1339,1040.7924 4143.3889,1041.8381 " fill="none" id="ProjectServices-to-ProjectRepos" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="4144.8104,1047.6673,4146.5642,1037.9759,4143.6258,1042.8097,4138.792,1039.8712,4144.8104,1047.6673" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="70" x="3465" y="953.9411">Data Access</text></g><!--link MicroServices to MicroRepos--><g id="link_MicroServices_MicroRepos"><path d="M1736.6744,881.773 C1736.7109,881.8989 1736.7476,882.0248 1736.7847,882.1506 C1736.8587,882.4023 1736.9338,882.6538 1737.0099,882.9051 C1737.1621,883.4078 1737.3186,883.9098 1737.4794,884.4109 C1737.8009,885.413 1738.1397,886.4112 1738.4967,887.4036 C1741.3525,895.3429 1745.37,902.9066 1751,909.0441 C1795.84,957.9341 1826.61,946.8641 1892,958.0441 C1904.98,960.2641 3777.23,958.4741 3788,966.0441 C3802.6225,976.3191 3813.4394,990.8335 3821.4381,1006.8783 C3825.4375,1014.9007 3828.7323,1023.3058 3831.4461,1031.7548 C3832.803,1035.9793 3834.0146,1040.2149 3835.0963,1044.4191 C3835.3668,1045.4701 3834.2115,1040.6891 3834.4659,1041.7355 " fill="none" id="MicroServices-to-MicroRepos" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="3835.8835,1047.5657,3837.6439,1037.8754,3834.7022,1042.7072,3829.8704,1039.7655,3835.8835,1047.5657" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="70" x="1893" y="953.9411">Data Access</text></g><!--link CartServices to CoreRepos--><g id="link_CartServices_CoreRepos"><path d="M828.8708,881.7032 C828.9057,881.8287 828.941,881.9543 828.9765,882.0797 C829.0476,882.3307 829.1198,882.5813 829.1933,882.8316 C829.7812,884.8343 830.447,886.8169 831.2,888.7608 C834.2119,896.5366 838.6175,903.6941 845,909.0441 C880.09,938.4641 1211.12,929.9441 1256,939.0441 C1281.76,944.2641 1286.26,952.7541 1312,958.0441 C1760.025,1050.1091 2272.76,1090.5291 2674.615,1107.9104 C2875.5425,1116.601 3048.75,1119.5319 3172.2887,1120.2789 C3234.0581,1120.6525 3283.4103,1120.48 3317.6017,1120.2085 C3334.6974,1120.0728 3348.0029,1119.9123 3357.1753,1119.783 C3359.4684,1119.7506 3355.5039,1119.8136 3357.275,1119.7861 " fill="none" id="CartServices-to-CoreRepos" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="3363.2742,1119.6926,3354.2131,1115.8332,3358.2748,1119.7705,3354.3376,1123.8323,3363.2742,1119.6926" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="70" x="1313" y="953.9411">Data Access</text></g><!--link PaymentServices to CoreRepos--><g id="link_PaymentServices_CoreRepos"><path d="M2279.6969,881.77 C2279.7327,881.8957 2279.7688,882.0213 2279.8052,882.1468 C2280.3876,884.1556 2281.0425,886.1505 2281.778,888.1139 C2284.72,895.9679 2288.9525,903.3191 2295,909.0441 C2382.87,992.1991 2648.615,1044.6541 2894.125,1076.4041 C3016.88,1092.2791 3134.5763,1102.9779 3222.45,1109.7497 C3266.3869,1113.1357 3302.8681,1115.5399 3328.7983,1117.1186 C3341.7634,1117.9079 3352.0907,1118.4908 3359.3933,1118.8869 C3360.3061,1118.9364 3361.1717,1118.983 3361.9892,1119.0267 C3362.398,1119.0486 3356.8032,1118.7517 3357.1878,1118.7721 " fill="none" id="PaymentServices-to-CoreRepos" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="3363.1794,1119.0901,3354.4041,1114.6187,3358.1864,1118.8251,3353.98,1122.6075,3363.1794,1119.0901" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="70" x="2369" y="953.9411">Data Access</text></g><!--link AnalyticsServices to AnalyticsRepos--><g id="link_AnalyticsServices_AnalyticsRepos"><path d="M1237.8201,881.9137 C1237.8944,882.1647 1237.9698,882.4155 1238.0464,882.6661 C1238.6592,884.6703 1239.3479,886.656 1240.1211,888.6047 C1243.2138,896.3997 1247.6575,903.6041 1254,909.0441 C1292.52,942.0741 1657.34,955.2441 1708,958.0441 C1718.01,958.5941 4586.79,960.2841 4595,966.0441 C4609.63,976.3091 4620.4506,990.8179 4628.4508,1006.86 C4632.4509,1014.8811 4635.7458,1023.2856 4638.4593,1031.7346 C4639.816,1035.9591 4641.0274,1040.1948 4642.1088,1044.3992 C4642.3791,1045.4503 4641.2244,1040.6692 4641.4787,1041.7158 " fill="none" id="AnalyticsServices-to-AnalyticsRepos" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="4642.8957,1047.546,4644.6571,1037.856,4641.7149,1042.6875,4636.8834,1039.7453,4642.8957,1047.546" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="70" x="1709" y="953.9411">Data Access</text></g><!--link CoreRepos to CoreModels--><g id="link_CoreRepos_CoreModels"><path d="M3363.9455,1079.284 C3363.9168,1079.0579 3363.8883,1078.8312 3363.86,1078.6039 C3363.7469,1077.6946 3363.6372,1076.776 3363.5312,1075.8486 C3363.3192,1073.9937 3363.1223,1072.1037 3362.9438,1070.1834 C3362.5868,1066.3429 3362.3036,1062.3816 3362.1213,1058.3391 C3360.6625,1025.9991 3365.66,988.4641 3391,966.0441 C3408.66,950.4241 10158.27,964.2941 10181,958.0441 C10196.95,953.6541 10197.18,943.8641 10213,939.0441 C10327.33,904.2041 10644.69,965.5741 10750,909.0441 C10767.755,899.5141 10781.4475,881.6191 10790.8475,865.6991 C10793.1975,861.7191 10795.2792,857.8625 10797.0891,854.291 C10797.3153,853.8445 10797.5373,853.4025 10797.755,852.9653 C10797.8094,852.856 10795.1982,858.1225 10795.2521,858.0138 " fill="none" id="CoreRepos-to-CoreModels" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="10797.9175,852.6383,10790.3358,858.9246,10795.6964,857.1179,10797.5031,862.4784,10797.9175,852.6383" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="87" x="10214" y="953.9411">Query/Update</text></g><!--link ProjectRepos to ProjectModels--><g id="link_ProjectRepos_ProjectModels"><path d="M4144.9482,1079.2868 C4144.9195,1079.0607 4144.8911,1078.8339 4144.8628,1078.6067 C4144.7498,1077.6975 4144.6401,1076.7789 4144.5341,1075.8515 C4144.3223,1073.9967 4144.1254,1072.1068 4143.947,1070.1866 C4143.5902,1066.3463 4143.3072,1062.3852 4143.125,1058.3429 C4141.6675,1026.0041 4146.665,988.4691 4172,966.0441 C4188.4,951.5341 10456.89,963.8541 10478,958.0441 C10493.95,953.6541 10494.17,943.8341 10510,939.0441 C10633.53,901.6741 10976.16,969.8441 11090,909.0441 C11107.775,899.5491 11121.47,881.6566 11130.8663,865.7291 C11133.2153,861.7472 11135.2957,857.8882 11137.104,854.3138 C11137.33,853.867 11137.5518,853.4247 11137.7694,852.9871 C11137.8237,852.8777 11135.2162,858.146 11135.2701,858.0372 " fill="none" id="ProjectRepos-to-ProjectModels" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="11137.9317,852.6598,11130.3544,858.9514,11135.7137,857.1409,11137.5242,862.5003,11137.9317,852.6598" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="87" x="10511" y="953.9411">Query/Update</text></g><!--link MicroRepos to MicroModels--><g id="link_MicroRepos_MicroModels"><path d="M3835.9482,1079.2868 C3835.9195,1079.0607 3835.8911,1078.8339 3835.8628,1078.6067 C3835.7498,1077.6975 3835.6401,1076.7789 3835.5341,1075.8515 C3835.3223,1073.9967 3835.1254,1072.1068 3834.947,1070.1866 C3834.5902,1066.3463 3834.3072,1062.3852 3834.125,1058.3429 C3832.6675,1026.0041 3837.665,988.4691 3863,966.0441 C3876.67,953.9441 9104.39,962.8941 9122,958.0441 C9137.95,953.6541 9138.2,943.9241 9154,939.0441 C9353.98,877.2341 9429.99,987.6141 9624,909.0441 C9647.07,899.6991 9668.4375,881.8116 9684.3387,865.8491 C9692.2894,857.8679 9698.8734,850.3679 9703.6205,844.6575 C9703.6946,844.5683 9699.938,849.0978 9700.0112,849.0094 " fill="none" id="MicroRepos-to-MicroModels" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="9703.8416,844.3912,9695.0172,848.7649,9700.6496,848.2397,9701.1749,853.8721,9703.8416,844.3912" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="87" x="9155" y="953.9411">Query/Update</text></g><!--link AnalyticsRepos to MicroModels--><g id="link_AnalyticsRepos_MicroModels"><path d="M4642.951,1079.2895 C4642.9223,1079.0634 4642.8939,1078.8367 4642.8656,1078.6094 C4642.7526,1077.7003 4642.643,1076.7818 4642.5371,1075.8544 C4642.3253,1073.9998 4642.1286,1072.1099 4641.9503,1070.1899 C4641.5937,1066.3498 4641.3108,1062.3888 4641.1288,1058.3466 C4639.6725,1026.0091 4644.67,988.4741 4670,966.0441 C4681.91,955.5041 9235.66,962.2641 9251,958.0441 C9266.95,953.6541 9267.26,944.1141 9283,939.0441 C9427.81,892.3741 9483.68,967.8441 9624,909.0441 C9646.96,899.4241 9668.325,881.5266 9684.2525,865.6279 C9692.2162,857.6785 9698.8206,850.2288 9703.5853,844.5633 C9703.6598,844.4748 9699.8769,848.9829 9699.9505,848.8952 " fill="none" id="AnalyticsRepos-to-MicroModels" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="9703.8073,844.2991,9694.9579,848.6221,9700.5933,848.1292,9701.0862,853.7645,9703.8073,844.2991" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="87" x="9284" y="953.9411">Query/Update</text></g><!--link AnalyticsRepos to CartModels--><g id="link_AnalyticsRepos_CartModels"><path d="M4642.9482,1079.2868 C4642.9195,1079.0607 4642.8911,1078.8339 4642.8628,1078.6067 C4642.7498,1077.6975 4642.6401,1076.7789 4642.5341,1075.8515 C4642.3223,1073.9967 4642.1254,1072.1068 4641.947,1070.1866 C4641.5902,1066.3463 4641.3072,1062.3852 4641.125,1058.3429 C4639.6675,1026.0041 4644.665,988.4691 4670,966.0441 C4683.12,954.4341 9699.11,962.6941 9716,958.0441 C9731.95,953.6541 9732.19,943.9041 9748,939.0441 C9852.7,906.8441 10143.62,961.0941 10240,909.0441 C10257.73,899.4691 10271.4225,881.5741 10280.8288,865.6654 C10283.1803,861.6882 10285.264,857.8351 10287.0759,854.2672 C10287.3024,853.8213 10287.5246,853.3797 10287.7426,852.943 C10287.7971,852.8338 10285.1811,858.098 10285.2351,857.9894 " fill="none" id="AnalyticsRepos-to-CartModels" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="10287.9053,852.6163,10280.3179,858.8958,10285.6801,857.0939,10287.482,862.4561,10287.9053,852.6163" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="87" x="9749" y="953.9411">Query/Update</text></g><!--link CoreModels to ORM--><g id="link_CoreModels_ORM"><path d="M10797.8691,852.5513 C10797.815,852.6595 10797.7606,852.7681 10797.7059,852.877 C10797.4872,853.3126 10797.2643,853.753 10797.0372,854.1978 C10795.2201,857.7564 10793.1316,861.601 10790.7762,865.5716 C10781.355,881.4541 10767.665,899.3541 10750,909.0441 C10671.07,952.3441 10432.52,914.1741 10346,939.0441 C10328.61,944.0441 10327.55,953.6541 10310,958.0441 C10288.82,963.3441 8757,955.2841 8738,966.0441 C8688.53,994.0841 8664.0955,1054.4197 8653.1255,1090.0497 " fill="none" id="CoreModels-to-ORM" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="8651.36,1095.7841,8657.8312,1088.3596,8652.8313,1091.0055,8650.1854,1086.0055,8651.36,1095.7841" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="126" x="10347" y="953.9411">Database Operations</text></g><!--link ProjectModels to ORM--><g id="link_ProjectModels_ORM"><path d="M11137.9637,852.0986 C11137.8559,852.3127 11137.7469,852.5281 11137.6369,852.7446 C11137.417,853.1777 11137.1927,853.6157 11136.9643,854.0581 C11135.1366,857.5973 11133.0381,861.4238 11130.675,865.3804 C11121.2225,881.2066 11107.535,899.1141 11090,909.0441 C10996.12,962.2041 10714.73,952.3641 10607,958.0441 C10594.04,958.7241 8749.29,959.6541 8738,966.0441 C8688.52,994.0641 8664.0841,1054.4093 8653.1241,1090.0393 " fill="none" id="ProjectModels-to-ORM" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="8651.36,1095.7741,8657.8293,1088.3479,8652.8301,1090.9951,8650.1829,1085.9958,8651.36,1095.7741" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="126" x="10986" y="953.9411">Database Operations</text></g><!--link MicroModels to ORM--><g id="link_MicroModels_ORM"><path d="M9703.9352,843.8347 C9703.7885,844.005 9703.64,844.1771 9703.4897,844.351 C9698.6794,849.9135 9692.0238,857.2466 9684.0275,865.1216 C9668.035,880.8716 9646.68,898.7891 9624,909.0441 C9538.89,947.5141 9504.82,910.1541 9416,939.0441 C9398.8,944.6441 9397.53,953.5841 9380,958.0441 C9362.72,962.4441 8753.48,957.1941 8738,966.0441 C8688.63,994.2641 8664.1627,1054.5219 8653.1627,1090.0919 " fill="none" id="MicroModels-to-ORM" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="8651.39,1095.8241,8657.8704,1088.4076,8652.8672,1091.0473,8650.2276,1086.0441,8651.39,1095.8241" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="126" x="9417" y="953.9411">Database Operations</text></g><!--link MentorshipModels to ORM--><g id="link_MentorshipModels_ORM"><path d="M10031.8691,852.5464 C10031.815,852.6546 10031.7606,852.7632 10031.7059,852.8721 C10031.4872,853.3076 10031.2643,853.7478 10031.0372,854.1925 C10029.2201,857.7504 10027.1316,861.5941 10024.7762,865.5641 C10015.355,881.4441 10001.665,899.3441 9984,909.0441 C9905.87,951.9441 9669.66,914.3941 9584,939.0441 C9566.61,944.0441 9565.54,953.6041 9548,958.0441 C9526.19,963.5641 8757.55,954.9041 8738,966.0441 C8688.59,994.2041 8664.1403,1054.4912 8653.1503,1090.0812 " fill="none" id="MentorshipModels-to-ORM" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="8651.38,1095.8141,8657.8574,1088.395,8652.8552,1091.0367,8650.2135,1086.0346,8651.38,1095.8141" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="126" x="9585" y="953.9411">Database Operations</text></g><!--link CartModels to ORM--><g id="link_CartModels_ORM"><path d="M10287.8471,852.5053 C10287.7929,852.6134 10287.7383,852.7217 10287.6836,852.8304 C10287.4644,853.2651 10287.2411,853.7046 10287.0135,854.1486 C10285.1927,857.7004 10283.1006,861.5385 10280.7425,865.5041 C10271.31,881.3666 10257.62,899.2691 10240,909.0441 C10169.99,947.8741 9957.84,916.5741 9881,939.0441 C9863.64,944.1241 9862.55,953.6341 9845,958.0441 C9815.18,965.5441 8764.74,950.8541 8738,966.0441 C8688.56,994.1341 8664.1179,1054.4505 8653.1379,1090.0605 " fill="none" id="CartModels-to-ORM" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="8651.37,1095.7941,8657.8443,1088.3723,8652.8433,1091.0161,8650.1994,1086.0151,8651.37,1095.7941" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="126" x="9882" y="953.9411">Database Operations</text></g><!--link PaymentModels to ORM--><g id="link_PaymentModels_ORM"><path d="M10612.9126,852.6285 C10612.8587,852.7372 10612.8045,852.8461 10612.75,852.9554 C10612.5322,853.3924 10612.3101,853.8342 10612.0838,854.2804 C10610.2731,857.8504 10608.1906,861.7054 10605.84,865.6841 C10596.4375,881.5991 10582.745,899.4941 10565,909.0441 C10463.86,963.4841 10159.64,908.2041 10049,939.0441 C10031.57,943.9041 10030.55,953.6441 10013,958.0441 C9978.65,966.6641 8768.8,948.5641 8738,966.0441 C8688.54,994.1141 8664.106,1054.4399 8653.136,1090.0599 " fill="none" id="PaymentModels-to-ORM" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="8651.37,1095.7941,8657.8418,1088.3701,8652.8417,1091.0156,8650.1962,1086.0154,8651.37,1095.7941" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="126" x="10050" y="953.9411">Database Operations</text></g><!--link ORM to Database--><g id="link_ORM_Database"><path d="M8657.79,1145.0741 C8686.2,1197.3541 8751.4045,1317.3326 8779.5945,1369.1926 " fill="none" id="ORM-to-Database" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="8782.46,1374.4641,8781.6761,1364.6465,8780.0721,1370.0712,8774.6474,1368.4671,8782.46,1374.4641" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="73" x="8707" y="1231.9411">SQL Queries</text></g><!--link CoreViews to TemplateEngine--><g id="link_CoreViews_TemplateEngine"><path d="M6728.0065,863.4963 C6728.0518,863.6184 6728.0974,863.7407 6728.1432,863.8631 C6728.3264,864.3529 6728.5132,864.845 6728.7038,865.3391 C6734.8,881.1516 6744.665,899.0591 6760,909.0441 C6836.19,958.6441 7078.22,924.7741 7168,939.0441 C7202.81,944.5741 7210.03,953.6541 7245,958.0441 C7259.06,959.8041 8252.9,958.6841 8265,966.0441 C8311.98,994.6241 8331.7753,1054.6214 8340.0553,1090.0714 " fill="none" id="CoreViews-to-TemplateEngine" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="8341.42,1095.9141,8343.2681,1086.2402,8340.2828,1091.0451,8335.4778,1088.0598,8341.42,1095.9141" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="108" x="7246" y="953.9411">Render Templates</text></g><!--link ProjectViews to TemplateEngine--><g id="link_ProjectViews_TemplateEngine"><path d="M5921.2197,961.2035 C5937.5989,961.8049 5954.2665,962.3373 5971.1677,962.8059 C6038.7726,964.6806 6110.1166,965.5369 6181.7062,965.7229 C6468.065,966.4666 6758.355,956.4841 6829,958.0441 C6838.97,958.2641 8256.47,960.8741 8265,966.0441 C8312.01,994.5741 8331.7976,1054.5908 8340.0676,1090.0608 " fill="none" id="ProjectViews-to-TemplateEngine" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="8341.43,1095.9041,8343.2819,1086.2309,8340.2947,1091.0347,8335.4909,1088.0474,8341.43,1095.9041" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="108" x="6830" y="953.9411">Render Templates</text></g><!--link MicroViews to TemplateEngine--><g id="link_MicroViews_TemplateEngine"><path d="M5969.567,881.5682 C5969.7046,882.0708 5969.8469,882.5724 5969.9943,883.0725 C5970.5838,885.0731 5971.253,887.0515 5972.0116,888.9886 C5975.0456,896.7372 5979.5075,903.8266 5986,909.0441 C6027.64,942.5041 6893.89,933.3541 6947,939.0441 C6993.28,944.0041 7003.66,953.6541 7050,958.0441 C7066.8,959.6341 8250.58,957.2841 8265,966.0441 C8312,994.5941 8331.7857,1054.6113 8340.0657,1090.0713 " fill="none" id="MicroViews-to-TemplateEngine" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="8341.43,1095.9141,8343.2787,1086.2403,8340.2931,1091.0451,8335.4883,1088.0594,8341.43,1095.9141" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="108" x="7051" y="953.9411">Render Templates</text></g><!--link MentorViews to TemplateEngine--><g id="link_MentorViews_TemplateEngine"><path d="M7456.147,881.8826 C7456.2179,882.1337 7456.29,882.3845 7456.3633,882.6351 C7456.9496,884.6395 7457.6123,886.6256 7458.3603,888.5752 C7461.3525,896.3735 7465.71,903.5866 7472,909.0441 C7519.44,950.1941 7690.6,932.0041 7753,939.0441 C7824.16,947.0641 7841.57,953.0041 7913,958.0441 C7932.51,959.4241 8248.36,955.7541 8265,966.0441 C8311.77,994.9741 8331.6403,1054.8249 8339.9903,1090.1649 " fill="none" id="MentorViews-to-TemplateEngine" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="8341.37,1096.0041,8343.1933,1086.3255,8340.2203,1091.1381,8335.4077,1088.165,8341.37,1096.0041" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="108" x="7914" y="953.9411">Render Templates</text></g><!--link CartViews to TemplateEngine--><g id="link_CartViews_TemplateEngine"><path d="M7697.6474,881.6166 C7697.684,881.7422 7697.7208,881.8678 7697.758,881.9933 C7697.8322,882.2443 7697.9077,882.495 7697.9843,882.7454 C7698.5975,884.7488 7699.2872,886.7329 7700.062,888.6793 C7703.1613,896.4647 7707.6225,903.6466 7714,909.0441 C7768.02,954.7541 7961.69,924.7841 8031,939.0441 C8057.98,944.5941 8062.89,953.1541 8090,958.0441 C8109.16,961.5041 8248.57,955.6141 8265,966.0441 C8311.3,995.4241 8331.3012,1054.7818 8339.8112,1090.0118 " fill="none" id="CartViews-to-TemplateEngine" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="8341.22,1095.8441,8342.995,1086.1565,8340.046,1090.9839,8335.2186,1088.0349,8341.22,1095.8441" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="108" x="8091" y="953.9411">Render Templates</text></g><!--link PaymentViews to TemplateEngine--><g id="link_PaymentViews_TemplateEngine"><path d="M6778.7754,881.8163 C6778.8104,881.9419 6778.8456,882.0674 6778.8812,882.1928 C6778.9523,882.4437 6779.0247,882.6942 6779.0982,882.9444 C6779.6869,884.9462 6780.3544,886.9269 6781.11,888.8677 C6784.1325,896.631 6788.565,903.7566 6795,909.0441 C6843.83,949.1641 7300.53,929.4741 7363,939.0441 C7396.56,944.1841 7403.33,953.6241 7437,958.0441 C7459.81,961.0341 8245.36,954.0741 8265,966.0441 C8311.95,994.6641 8331.7646,1054.6515 8340.0446,1090.0815 " fill="none" id="PaymentViews-to-TemplateEngine" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="8341.41,1095.9241,8343.2569,1086.25,8340.2722,1091.0553,8335.4668,1088.0705,8341.41,1095.9241" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="108" x="7438" y="953.9411">Render Templates</text></g><!--link AnalyticsViews to TemplateEngine--><g id="link_AnalyticsViews_TemplateEngine"><path d="M7045.8175,881.7719 C7045.8524,881.8975 7045.8877,882.023 7045.9232,882.1484 C7045.9943,882.3993 7046.0666,882.6499 7046.1401,882.9001 C7046.7283,884.9022 7047.395,886.8835 7048.1494,888.8255 C7051.1669,896.5935 7055.5875,903.7316 7062,909.0441 C7104.26,944.0541 7500.71,931.0041 7555,939.0441 C7591.15,944.3941 7598.73,953.5641 7635,958.0441 C7652.37,960.1941 8250.07,956.9141 8265,966.0441 C8311.91,994.7341 8331.7307,1054.6924 8340.0307,1090.1024 " fill="none" id="AnalyticsViews-to-TemplateEngine" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="8341.4,1095.9441,8343.2405,1086.2688,8340.2589,1091.076,8335.4516,1088.0944,8341.4,1095.9441" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="108" x="7636" y="953.9411">Render Templates</text></g><!--link TemplateEngine to Templates--><g id="link_TemplateEngine_Templates"><path d="M8363.27,1145.2741 C8380.31,1166.4941 8408.47,1196.1741 8441,1209.0441 C8463.01,1217.7541 9269.34,1216.4741 9293,1217.0441 C9370.81,1218.9141 9937.59,1189.3841 9993,1244.0441 C10016.935,1267.6591 10019.2475,1305.2141 10015.4238,1337.2654 C10014.4678,1345.2782 10013.1284,1352.947 10011.6474,1359.968 C10010.9069,1363.4785 10010.131,1366.8271 10009.35,1369.9758 C10009.2523,1370.3693 10010.6228,1364.9422 10010.525,1365.3294 " fill="none" id="TemplateEngine-to-Templates" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="10009.0569,1371.1471,10015.1375,1363.3994,10010.2803,1366.299,10007.3807,1361.4419,10009.0569,1371.1471" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="95" x="9978" y="1231.9411">Load Templates</text></g><!--link TemplateEngine to Browser--><g id="link_TemplateEngine_Browser"><path d="M8353.01,1095.9141 C8364.81,1060.7741 8392.27,995.6941 8441,966.0441 C8460.8,953.9941 8529.25,975.0541 8545,958.0441 C8595.37,903.6541 8475.3025,863.9024 8404.3425,845.7324 " fill="none" id="TemplateEngine-to-Browser" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="8398.53,844.2441,8406.2565,850.3516,8403.3737,845.4844,8408.2409,842.6016,8398.53,844.2441" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="140" x="8556" y="953.9411">HTTP Response (HTML)</text></g><!--link TemplateEngine to Mobile--><g id="link_TemplateEngine_Mobile"><path d="M8340.59,1095.9741 C8331.37,1061.5241 8309.17,998.0441 8265,966.0441 C8247.84,953.6141 8231.67,974.2341 8218,958.0441 C8198.47,934.9041 8202.0015,905.6892 8210.9215,878.7892 " fill="none" id="TemplateEngine-to-Mobile" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="8212.81,873.0941,8206.1806,880.3777,8211.2363,877.84,8213.774,882.8957,8212.81,873.0941" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="140" x="8219" y="953.9411">HTTP Response (HTML)</text></g><!--link Templates to StaticFiles--><g id="link_Templates_StaticFiles"><path d="M10009.0643,1432.6654 C10009.1414,1432.982 10009.2189,1433.3003 10009.2968,1433.6204 C10009.6085,1434.9005 10009.9269,1436.2078 10010.2514,1437.5407 C10015.4441,1458.866 10022.2281,1486.7279 10029.0113,1514.5866 C10035.7944,1542.4454 10042.5766,1570.301 10047.7655,1591.6138 C10048.0898,1592.9458 10048.4079,1594.2523 10048.7193,1595.5317 C10048.7972,1595.8515 10047.4553,1590.3399 10047.5324,1590.6563 " fill="none" id="Templates-to-StaticFiles" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="10048.9517,1596.4861,10050.7092,1586.7953,10047.7689,1591.628,10042.9362,1588.6877,10048.9517,1596.4861" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="100" x="10028" y="1509.9411">Reference Assets</text></g><!--link StaticServer to Browser--><g id="link_StaticServer_Browser"><path d="M9154.33,1095.8541 C9143.04,1060.6341 9116.49,995.4541 9068,966.0441 C9044.39,951.7241 8971.34,961.9241 8944,958.0441 C8905.24,952.5441 8896.27,947.2541 8858,939.0441 C8688.47,902.6541 8492.3182,862.327 8404.4082,844.337 " fill="none" id="StaticServer-to-Browser" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="8398.53,843.1341,8406.5453,848.8573,8403.4285,844.1365,8408.1492,841.0197,8398.53,843.1341" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="172" x="8945" y="953.9411">Static Assets (CSS/JS/Images)</text></g><!--link PaymentServices to StripeAPI--><g id="link_PaymentServices_StripeAPI"><path d="M2278.7932,881.7941 C2278.8281,881.9197 2278.8634,882.0452 2278.8989,882.1706 C2278.9701,882.4215 2279.0424,882.672 2279.116,882.9223 C2279.7045,884.9242 2280.3717,886.9052 2281.1269,888.8466 C2284.1475,896.6122 2288.575,903.7441 2295,909.0441 C2331.91,939.4941 3107.17,956.6541 3155,958.0441 C3165.01,958.3341 8917.56,960.6441 8926,966.0441 C8971.13,994.9341 8987.0025,1054.7276 8992.9625,1090.0776 " fill="none" id="PaymentServices-to-StripeAPI" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="8993.96,1095.9941,8996.4081,1086.4543,8993.1287,1091.0637,8988.5194,1087.7844,8993.96,1095.9941" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="109" x="3156" y="953.9411">Process Payments</text></g><!--link CoreServices to FileStorage--><g id="link_CoreServices_FileStorage"><path d="M778.1056,863.3515 C778.1512,863.4732 778.197,863.5952 778.243,863.7173 C778.4272,864.2056 778.6149,864.6963 778.8062,865.1891 C784.93,880.9591 794.79,898.8741 810,909.0441 C866.8,947.0141 1050.25,920.4541 1116,939.0441 C1134.55,944.2941 1136.21,953.7041 1155,958.0441 C1180.82,964.0141 8764,951.2741 8786,966.0441 C8829.53,995.2641 8842.3091,1054.5652 8846.4591,1089.8452 " fill="none" id="CoreServices-to-FileStorage" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="8847.16,1095.8041,8850.0812,1086.3984,8846.5759,1090.8383,8842.136,1087.333,8847.16,1095.8041" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="91" x="1156" y="953.9411">Upload Images</text></g><!--link ProjectServices to FileStorage--><g id="link_ProjectServices_FileStorage"><path d="M2536.2256,881.6193 C2536.3699,882.1218 2536.5189,882.6233 2536.6729,883.1233 C2537.289,885.1234 2537.9844,887.1008 2538.7681,889.0364 C2541.9031,896.7791 2546.4525,903.8541 2553,909.0441 C2595.99,943.1241 3485.17,937.1441 3540,939.0441 C3757.81,946.5741 3812.1,953.6341 4030,958.0441 C4046.51,958.3741 8772.29,956.8341 8786,966.0441 C8829.52,995.2741 8842.2974,1054.5754 8846.4574,1089.8554 " fill="none" id="ProjectServices-to-FileStorage" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="8847.16,1095.8141,8850.0786,1086.4076,8846.5745,1090.8485,8842.1336,1087.3444,8847.16,1095.8141" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="91" x="4031" y="953.9411">Upload Images</text></g><!--link MicroServices to FileStorage--><g id="link_MicroServices_FileStorage"><path d="M1734.9994,881.5568 C1735.0343,881.6824 1735.0695,881.808 1735.105,881.9335 C1735.1759,882.1845 1735.2481,882.4353 1735.3214,882.6858 C1735.9081,884.6897 1736.5716,886.6749 1737.3209,888.623 C1740.3181,896.4154 1744.6875,903.6141 1751,909.0441 C1772.08,927.1741 2221.23,956.6641 2249,958.0441 C2260.33,958.6041 8776.58,959.7141 8786,966.0441 C8829.53,995.2641 8842.3091,1054.5652 8846.4591,1089.8452 " fill="none" id="MicroServices-to-FileStorage" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="8847.16,1095.8041,8850.0812,1086.3984,8846.5759,1090.8383,8842.136,1087.333,8847.16,1095.8041" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="91" x="2250" y="953.9411">Upload Images</text></g><!--link MentorshipServices to FileStorage--><g id="link_MentorshipServices_FileStorage"><path d="M3001.5115,881.6415 C3001.6491,882.144 3001.7916,882.6455 3001.9391,883.1454 C3002.5291,885.1454 3003.1994,887.1225 3003.9595,889.0575 C3007,896.7979 3011.4775,903.8666 3018,909.0441 C3045.56,930.9241 5515.81,957.6641 5551,958.0441 C5562.23,958.1641 8776.68,959.7741 8786,966.0441 C8829.51,995.2941 8842.2974,1054.5754 8846.4574,1089.8554 " fill="none" id="MentorshipServices-to-FileStorage" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="8847.16,1095.8141,8850.0786,1086.4076,8846.5745,1090.8485,8842.1336,1087.3444,8847.16,1095.8141" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="91" x="5552" y="953.9411">Upload Images</text></g><!--link FileStorage to MediaFiles--><g id="link_FileStorage_MediaFiles"><path d="M8857.87,1145.0741 C8877.47,1197.0941 8922.1739,1315.7497 8941.8939,1368.0697 " fill="none" id="FileStorage-to-MediaFiles" style="stroke:#000000;stroke-width:1.0;"/><polygon fill="#000000" points="8944.01,1373.6841,8944.5787,1363.8517,8942.2465,1369.0054,8937.0928,1366.6732,8944.01,1373.6841" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="61" x="8892" y="1231.9411">Store Files</text></g><!--link FactoryBoy to CoreModels--><g id="link_FactoryBoy_CoreModels"><path d="M9640.2707,548.2045 C9645.094,548.3081 9651.9637,548.4677 9660.7103,548.7015 C9678.2034,549.1691 9703.2038,549.9332 9734.3538,551.1379 C9796.6538,553.5472 9883.5525,557.7191 9984.19,564.8066 C10185.465,578.9816 10441.695,604.8191 10666,651.5441 C10704.39,659.5441 10721.74,651.3541 10750,678.5441 C10775.76,703.3241 10789.7275,740.8966 10797.2713,772.6666 C10797.507,773.6594 10796.4043,768.7963 10796.6277,769.7772 " fill="none" id="FactoryBoy-to-CoreModels" style="stroke:#000000;stroke-width:1.0;stroke-dasharray:7.0,7.0;"/><polygon fill="#000000" points="10797.9598,775.6275,10799.8618,765.964,10796.8497,770.7523,10792.0614,767.7402,10797.9598,775.6275" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="114" x="10741" y="666.4411">Generate Test Data</text></g><!--link FactoryBoy to ProjectModels--><g id="link_FactoryBoy_ProjectModels"><path d="M9640.7098,548.6587 C9641.0462,548.6825 9641.3921,548.707 9641.7475,548.7322 C9647.433,549.1348 9655.5328,549.7108 9665.8502,550.4506 C9686.4851,551.9302 9715.9908,554.065 9752.7953,556.7783 C9826.4044,562.205 9929.2088,569.946 10048.6325,579.3879 C10287.48,598.2716 10592.805,623.9591 10864,651.5441 C10964.64,661.7841 11010.71,615.7341 11090,678.5441 C11104.0075,689.6416 11114.5119,704.5735 11122.3891,720.7804 C11126.3277,728.8838 11129.6095,737.306 11132.3439,745.727 C11133.7112,749.9375 11134.9416,754.1477 11136.0489,758.3176 C11136.6025,760.4026 11137.1254,762.4775 11137.6192,764.5373 C11137.7426,765.0523 11136.4994,759.7236 11136.6192,760.2366 " fill="none" id="FactoryBoy-to-ProjectModels" style="stroke:#000000;stroke-width:1.0;stroke-dasharray:7.0,7.0;"/><polygon fill="#000000" points="11137.9841,766.0793,11139.8319,756.4053,11136.8467,761.2104,11132.0416,758.2252,11137.9841,766.0793" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="114" x="11077" y="666.4411">Generate Test Data</text></g><!--link FactoryBoy to MicroModels--><g id="link_FactoryBoy_MicroModels"><path d="M9640.0322,576.5629 C9640.1292,576.9074 9640.227,577.2545 9640.3255,577.6041 C9640.5225,578.3033 9640.7223,579.0126 9640.9249,579.7316 C9641.33,581.1698 9641.7463,582.6473 9642.173,584.1619 C9643.0264,587.1912 9643.9217,590.3693 9644.8542,593.6797 C9652.3147,620.1629 9662.1594,655.1116 9672.0038,690.0591 C9681.8481,725.0066 9691.6922,759.9529 9699.1514,786.431 C9700.0838,789.7407 9700.9789,792.9182 9701.8322,795.9468 C9702.2588,797.4611 9702.6749,798.9382 9703.08,800.376 C9703.2825,801.0949 9703.4823,801.804 9703.6792,802.503 C9703.7777,802.8525 9702.2484,797.4243 9702.3454,797.7687 " fill="none" id="FactoryBoy-to-MicroModels" style="stroke:#000000;stroke-width:1.0;stroke-dasharray:7.0,7.0;"/><polygon fill="#000000" points="9703.9725,803.5439,9705.382,793.7964,9702.6166,798.7312,9697.6818,795.9658,9703.9725,803.5439" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="114" x="9665" y="666.4411">Generate Test Data</text></g><!--link FactoryBoy to MentorshipModels--><g id="link_FactoryBoy_MentorshipModels"><path d="M9640.3883,548.6401 C9640.5753,548.6554 9640.7653,548.671 9640.9582,548.6869 C9641.7298,548.7507 9642.5479,548.8201 9643.4112,548.8954 C9650.3175,549.4975 9660.1166,550.4779 9672.1388,552.0154 C9696.1831,555.0904 9729.12,560.3941 9765.5925,569.3591 C9838.5375,587.2891 9925.625,619.8641 9984,678.5441 C10009.21,703.8841 10023.17,741.4641 10030.8475,773.0979 C10031.0874,774.0864 10031.3212,775.0692 10031.549,776.0455 C10031.6629,776.5337 10030.4374,771.1714 10030.5483,771.6563 " fill="none" id="FactoryBoy-to-MentorshipModels" style="stroke:#000000;stroke-width:1.0;stroke-dasharray:7.0,7.0;"/><polygon fill="#000000" points="10031.8862,777.5053,10033.7787,767.8399,10030.7713,772.6312,10025.9801,769.6238,10031.8862,777.5053" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="114" x="9970" y="666.4411">Generate Test Data</text></g><!--link FactoryBoy to CartModels--><g id="link_FactoryBoy_CartModels"><path d="M9640.6724,548.7687 C9641.2361,548.817 9641.8259,548.8678 9642.4414,548.921 C9643.6722,549.0274 9645.0057,549.1435 9646.4383,549.2696 C9649.3035,549.5216 9652.5655,549.813 9656.1973,550.144 C9670.7244,551.4681 9691.1684,553.4268 9715.8063,556.0414 C9765.0819,561.2707 9831.1325,569.1235 9900.1725,579.7704 C10038.2525,601.0641 10188.29,633.5341 10240,678.5441 C10253.48,690.2766 10263.7169,705.531 10271.4905,721.8632 C10275.3773,730.0293 10278.6482,738.4648 10281.4009,746.8643 C10282.7772,751.064 10284.0239,755.2548 10285.1533,759.3983 C10285.7179,761.4701 10286.2532,763.53 10286.7607,765.5734 C10287.0145,766.5951 10287.2613,767.6127 10287.5013,768.6255 C10287.6213,769.1319 10286.3866,763.7917 10286.5032,764.2956 " fill="none" id="FactoryBoy-to-CartModels" style="stroke:#000000;stroke-width:1.0;stroke-dasharray:7.0,7.0;"/><polygon fill="#000000" points="10287.8563,770.1411,10289.7237,760.4709,10286.7287,765.2699,10281.9297,762.2749,10287.8563,770.1411" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="114" x="10226" y="666.4411">Generate Test Data</text></g><!--link FactoryBoy to PaymentModels--><g id="link_FactoryBoy_PaymentModels"><path d="M9640.5735,548.063 C9641.2735,548.0659 9642.0147,548.0693 9642.7964,548.0731 C9649.0499,548.1037 9657.8953,548.1659 9669.0041,548.2916 C9691.2216,548.543 9722.4927,549.0485 9760.1891,550.0635 C9835.5819,552.0935 9936.6762,556.1616 10042.4475,564.3116 C10253.99,580.6116 10484.24,613.2391 10565,678.5441 C10578.8975,689.7816 10589.3462,704.7847 10597.202,721.0194 C10601.1299,729.1368 10604.4096,737.562 10607.1479,745.9784 C10608.5171,750.1865 10609.751,754.3925 10610.8629,758.5567 C10611.4189,760.6387 10611.9444,762.7104 10612.441,764.7666 C10612.5652,765.2806 10612.6876,765.7937 10612.8082,766.3058 C10612.8685,766.5618 10611.5694,760.9735 10611.6288,761.229 " fill="none" id="FactoryBoy-to-PaymentModels" style="stroke:#000000;stroke-width:1.0;stroke-dasharray:7.0,7.0;"/><polygon fill="#000000" points="10612.9877,767.0731,10614.8454,757.401,10611.8553,762.203,10607.0533,759.2129,10612.9877,767.0731" style="stroke:#000000;stroke-width:1.0;"/><text fill="#000000" font-family="Verdana" font-size="13" lengthAdjust="spacing" textLength="114" x="10543" y="666.4411">Generate Test Data</text></g><!--link Django to GMN205--><g id="link_Django_GMN205"><path d="M8225.9656,1067.3172 C8225.9236,1066.7491 8225.8828,1066.1784 8225.8434,1065.6053 C8225.7646,1064.4591 8225.6911,1063.3032 8225.6234,1062.1385 C8225.4879,1059.809 8225.3758,1057.4441 8225.2908,1055.0506 C8225.1209,1050.2636 8225.06,1045.3621 8225.14,1040.4004 C8225.78,1000.7066 8235.44,957.1591 8270.5,937.5441 C8308.75,916.1441 11386.23,920.2341 11426.5,937.5441 C11498.29,968.4041 11554.32,1045.2041 11581.66,1088.8741 " fill="none" id="Django-GMN205" style="stroke:#000000;stroke-width:1.0;stroke-dasharray:7.0,7.0;"/></g><!--link RESTAPI to GMN208--><g id="link_RESTAPI_GMN208"><path d="M5145.9079,241.8811 C5145.8603,241.6031 5145.8129,241.324 5145.7655,241.0439 C5145.3866,238.8026 5145.0138,236.492 5144.6524,234.1207 C5143.9294,229.3782 5143.2515,224.3925 5142.6587,219.2316 C5141.473,208.9097 5140.6278,197.8866 5140.4438,186.7041 C5139.7075,141.9741 5149.55,94.6941 5190.5,79.5441 C5238.02,61.9641 5598.98,61.9641 5646.5,79.5441 C5695.39,97.6341 5736.45,137.2741 5767.33,176.4941 " fill="none" id="RESTAPI-GMN208" style="stroke:#000000;stroke-width:1.0;stroke-dasharray:7.0,7.0;"/></g><!--link CoreServices to GMN211--><g id="link_CoreServices_GMN211"><path d="M774.0251,739.6654 C774.0886,739.3659 774.1527,739.0664 774.2175,738.7671 C774.3472,738.1683 774.4795,737.5699 774.6145,736.972 C774.8845,735.776 775.1653,734.5818 775.4572,733.3902 C776.0411,731.0069 776.6698,728.6341 777.3461,726.2786 C780.0514,716.8568 783.52,707.7129 787.9444,699.2935 C796.7931,682.4547 809.465,668.5141 827.5,661.0441 C861.5,646.9641 11392.5,646.9641 11426.5,661.0441 C11477.78,682.2841 11521.5,727.3541 11551.84,766.0241 " fill="none" id="CoreServices-GMN211" style="stroke:#000000;stroke-width:1.0;stroke-dasharray:7.0,7.0;"/></g><!--link CoreRepos to GMN214--><g id="link_CoreRepos_GMN214"><path d="M3363.9656,1067.3172 C3363.9236,1066.7491 3363.8828,1066.1784 3363.8434,1065.6053 C3363.7646,1064.4591 3363.6911,1063.3032 3363.6234,1062.1385 C3363.4879,1059.809 3363.3758,1057.4441 3363.2908,1055.0506 C3363.1209,1050.2636 3363.06,1045.3621 3363.14,1040.4004 C3363.78,1000.7066 3373.44,957.1591 3408.5,937.5441 C3458.75,909.4341 11647.48,912.8641 11699.5,937.5441 C11765.66,968.9241 11812.24,1045.5141 11834.38,1089.0141 " fill="none" id="CoreRepos-GMN214" style="stroke:#000000;stroke-width:1.0;stroke-dasharray:7.0,7.0;"/></g><!--link External to GMN217--><g id="link_External_GMN217"><path d="M8745.9656,1067.3172 C8745.9236,1066.7491 8745.8828,1066.1784 8745.8434,1065.6053 C8745.7646,1064.4591 8745.6911,1063.3032 8745.6234,1062.1385 C8745.4879,1059.809 8745.3758,1057.4441 8745.2908,1055.0506 C8745.1209,1050.2636 8745.06,1045.3621 8745.14,1040.4004 C8745.78,1000.7066 8755.44,957.1591 8790.5,937.5441 C8828.96,916.0241 11924.87,916.3441 11963.5,937.5441 C12022.27,969.7941 12055.64,1045.6741 12070.51,1088.9141 " fill="none" id="External-GMN217" style="stroke:#000000;stroke-width:1.0;stroke-dasharray:7.0,7.0;"/></g><!--SRC=[jLlDRkCu4hxxARZkmoROpcImnm2xG3hk7pUSJiPEfh70N6YRiJKjInf9xeot4M1F-m3p2FDeyoHB5l-A54aBOsqEHbJaHzOVYyMYz9TsotQCL3dDYb6RjJaZ7xAQpSgo8jVrQfkrRDNkQqOkoEsF3-HlPFvsyK2kxwTaMhHiKzCsAulHwA_a7oVySVZRNrjM5pGdDtd6YhOvTKIwQikQZ3-p9NbJbyyDgyU4Dlf_ycgMRRRjctpFTC_RSfbnuUNqq5THPDVtDME5xlkmpUhrnJsjsmEvhge6kWDHqbxTrRJOi07K8XJzdhRicHx8Z1vOVUgG5LrzeHj6nc9a696S2PEUZvMW_s9vNZwJRoF2_-1dLUwgik1Q8MDZ_BV5kYepRYSGNP05LO8yp6ssgii5gxzcAqPcMTEA0Nugthzz89UqoYvtehsHxSqbZ2TwYV5UBRuSm4R7XfsmbcPvSk1lsVf5ZYuxTyP_2KeikjteHoaj9rbAM6RELqRpxD-ibX3qZ009YIn0kg9gKZGpmajeSi7oZnbxDjp2GtnUfMtH2sjVFCSWSzRM6VlACCoZUJmYxHPboqWjV8sKJzftJ7VZOazyfJ4T5J8RR1hJzO9yNDnz8ZLhE5yDmmtt-sMUhGZJRahEYfBGVRlblN_Pym2tFaUzR-xc2zwNBdEsXdc5upGN9MUIHqNHXmy4V8zU1bZKzvnZhaQGPk1LtHrwp0tlE_K3s_60tp8LkFHJs9VVq8OHX91_8fRo1aCF8M_AEemK3KdaVLt-pFST3yoHgY49laNhdhYYGbCQp7_BkjbcbG-5XhIyFFY7vUKDBlAbOvE5CDgAlEDRZeePG83di65k5Wiz1qooM8HwVQHVwM9LPvNSr3u6Eqrtt7iKnxoJV5IC3k7nV9Faon5v9Jc3e7G-t7OMco7a_-2ODaIAHpz6udWgmeRghHGaI429EE-JI1mqHBgj8CKXPTq-bNbM8guCBOe2Co7EjEKieEjcQW4rU299IcX0ByUR-UC4kRKY2sfGRyWaI1U879NikccoJR4J_nln1DIGKoBYzO_b17f2IfrC62dbnYreCH5l-8BUbFK1owTfIHPjb47y0J7989UVArCo2Dm1mN3NdGX24l9q_fYO07hVqeBxq0woO1I_RZUxDeJvd3NRN6Hr6CSnccvm0L-a1snYuL6Iaj81Jp8gXWyVAbWASahbrpoDEF20YZt2q18JJcYpLKc-SNn14wHO_sL9wpMQnz0mWqF4rJVx9Yku4v1PkU6RXmfyoca7ZAv7ved6MDt3X5bDYCOPY9ogrvZWuAc8wV1fa3Y09f0oXABvR1HDeAvN4DGcMLFHThLLIRgaMc8w0hkwKSIZwi78RYHEgKXXFO4jjYDpEh2wxEEZIzFZ6EXAu0sGaCBXe2iARkuZZut2hZI6VaGaYm_mOXfxS0A1rrqid9AU7MESI9tGdmdMc5DDJBEeWxNhjf9un6rTP01uD6GxanfoUjeE6gqNVuYWTMdzXRKaC8omBZG6XnaciazeItb4MK7GLMKQLfLDnfqg6pAq7vie6jjnBnFVWPWExWPtSEExeAU3EqRY-1v3midLdSwUN0qe7g4x4gg6j90kzE2TN6EyeepN4zEsHB4eqVR1jYaXi1DMEr93Qq9c9x9xy-Es10DsaNLcDqrzEN37ibmu0qK3QiTTt5Cyac68LNvRhbckbzsatD6i66vbXmQFhcReRDUnV4JQNlCmiHJhQVm8jNHVEO8Ae03YNSrOJeiLgzLIXsaiDOQJjNY3qMO0QWmpRTdE10Q3CHGBYozxf0f5IcX3zHXxwi30ECekxR5tlZq6jClQN-Of2PrrZiG4Ua98lBuwopfgFNKEHhc992Gvj2aLvizGKqoYh0sEnI5eAl_2Iq0SUEDJYMRXQ4xQ9GWnNUWKIu9GpkM2ubaNzab9IlcaxD7fFM3WcXPFDMtQUYyl1uSjOeS63mMkoS-qs9GyaD0TUoxhB_AiBOd1VU9nFYFpSj-Q02O2rtmcIU6DPRtEsJEjdQEAfeKGT_FRpiR1QQ6kkY9CtXORVhfsQl6I574ASrVgfCM6cggRNDzFSSrOKl7r2uAyWwCuNptSA5PyGLN4y3ocZ0tigREn94i2biewxUA7MSPrCL44LJUH3zqeiSweBfKhgmWIK0RnxpdxPS_uEUcTk0kz89_Pyb9T1p_KT9s9G4lpKwVHbz4N5_-qRaYkoFZ3myEzOU5Ct64_Ji_78yL1x_w3gq5SovqPFqERpkdd4QqB8iNJDy14Y1UvqVsfE8FxFyKaKj19Ww1x_3y_Y2-FlNEEZm8tr4U5Ec4aJx8JHXfPhI0TYUecy7a5YGeSAHLcFBAp2OHtMHn4ZFnX1T2x2HT0ymJnOZpon-u96-PbZTRK88VP55CwaCKFOJnHfyXpf_xLf1NXO9syS7aWqybGwfYhktc88ASEwHinudhWgzAc8KJ0zH0Yg72qc7Mq_VlttnDO5Nmr16raLsrV25gU8KZGd4Su2tf0chCGv1XdTZEIBgOJ9D4R6j2YHgsYixrxrHp1TQlgtupz_ivbfOuqgkGIWQ1xFpM5L- -8uT1zdCBPqqaKPQ_Oz6oghX0J25zvIO5KpX-5UDTMLsxzH8DENy1W_w43ccTmxGCc96cjkLTEuv5dUEGB21h0UTRlni38V9xrhKFWUu40phE_TedZyhb-W5mZBP_d38v_u3Zluqvt3-qMBQxC3kSahiQqdyWge5OYAbuR3q4uv2GQvuEwlc0yn4xbWxe6xSDUnvezG5rJEWQMI1yqHDvlxCcjYmg9GnWMYQire8ePMWK_x5bzk7oi-EcG6Rjg63AgWNKmdW6DJT547OodrJ-BGRMZC6QeiZ6tZ3aW3s0Mp3C8SZU_rQu5H_IxYgatC8rDBEOOmDVaSO1Vypi6yFL-N0QdaDO3C1ADS7BIhLTGjo32lkA-OW3JcgBGd1LhFcgn-Jzik6wL2R8qc0szl1ZQR_l00jjjBrXtj-q32soslMJhxhLzO86jjWziv7N2E0ZUivAkCI3Gt-RvjjoZJbPd7nvkP-T1b4trewW1qW3qukgfercrABFWbs11kK-iPeMuvMiQ9h9SN5ZqJqImF2LtiZivkraiBZykBkKBheE8RyfXK_oA-ed3TdC5fGrLhdLhBAgtM0-Tl0bmg6OhS8zLBZnElVGRo9jwWBfvKnzGzyMQuw0HRfPfk2xrIWEBwqjP2nx0dE_W4vy3ULCUu4k01twO6Y08uxAwdK7UWyfdCU4tlz0jRbLrXp6-QbMqKUGT2zcCNbiGL4ECNNnsK88QHUdqtqKfgaMzS0DQ2R_xhflmoIfK8VPP1lfMfHWFraav-i4wYKTFc9z-z8Draf2UilcfI0Hskdz_AjlJmxJx1O-ySGFtK9Tluaj1Soi73HzeiHOBLcn2hyNb1QdBlLXOhw6P9rQl2Uz2Mft-r2RzCP_UZE8V3ed_d_Qv-sdQI7xSetY2xufSfjJtGusg3yfF6PtlXwXyBqf_FCHDf2uypbK_lXRNec9gFbIYw5B4Vl9aUBg2np_-ypk95DpLdTeV__rDVYj7yvmuFOuD01LxD8gex-8UP0s5-2QgLxo7m3YcSf33oxyvd0D5mvJR2bxuvil-RZQTa8eRR9LLkG9EM2MiMAmEV7Fa-tEZzGi_YosjfVAMPRkzKWgLbrVaZBkGrh7-8Yp9CPo_vApYAAmCHvTDMzELCImwrrQq5IQJhB2Arf1sB5rPd-fo1tUKqRdrzW_ZoEz2AoYKThvOKpUmObEfr8ODTBWgRTJ-9bftOd_p9ypP4yndIx7IiKANSKflAlkZ-aLrxjKSnuDAbxSBgRKLVzxlkA4KqPOLsxBCaJ-hzmM_PjHQHz0_-Ul4V6vdvVaV]--></g></svg>ading architecture_diagram.svg…]()




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
> - Database name: `hireloop-db`
> - Version: PostgreSQL 15
> - Instance type: db-custom-1-3840
> - Storage: 10GB SSD
> - Tables: Users, Profiles, Projects, Microservices, MentorshipSessions, Cart, Payments

### Running Containers (GKE)

> **Screenshot Placeholder**: GKE cluster dashboard displaying:
> - Cluster name: `hireloop-cluster`
> - Running pods: 2-5 replicas (HPA controlled)
> - Deployment: `hireloop-deployment` status
> - Container images: Django app + Cloud SQL Proxy sidecar
> - Pod health status (startup, readiness, liveness probes)
> - Resource utilization (CPU/Memory)

### Storage Bucket (GCS)

> **Screenshot Placeholder**: Google Cloud Storage bucket view:
> - Bucket name: `hireloop-media`
> - Directory structure:
>   - `/microservices/` - Microservice images
>   - `/portfolios/` - Portfolio images
>   - `/profiles/` - User profile pictures
>   - `/projects/` - Project images
>   - `/mentorships/` - Mentorship session images
> - Total objects and storage size
> - Access control: Public Read

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
