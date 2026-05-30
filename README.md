# UNZA Congregation Management System

A comprehensive management system for the New Apostolic Church UNZA Congregation, built with Django REST Framework and modern web technologies.

## Features

### 🔐 Authentication & User Management
- **Custom User Model** with comprehensive member information
- **JWT Authentication** for secure API access
- **Role-based Access Control** (Super Users, Admin Users, High Privilege Users, Members)
- **Password Reset** functionality via email
- **Profile Picture Upload** with automatic resizing

### 👥 User Hierarchy
- **Super Users (Developers)**: Full system access
- **Admin Users (Ministers/Youth Leaders)**: Can assign functionality to subordinates
- **High Privilege Users (Committee/Section Leaders)**: Can assign functionality to subordinates
- **Members**: Basic user access

### 🏛️ Committee Management
Nine specialized committees:
1. **Catering Committee** - Food and catering services organization
2. **Music Committee** - Musical services and orchestra
3. **Organizing Committee** - Event planning and transportation
4. **Finance Committee** - Budget management and fund collection
5. **DRAPO Committee** - Drama and poetry entertainment
6. **Communication Committee** - Sound systems and audio management
7. **Testify Committee** - Doctrinal issues and faith preparation
8. **Flowering Committee** - Church beautification
9. **Secretarial Committee** - Records and documentation management

### 📅 Calendar & Events
- **Event Calendar** for congregational activities
- **Birthday Calendar** for all members
- **Event Registration** and attendance tracking
- **Automatic Reminders** for upcoming events
- **Event Categories** and filtering

### 🔔 Notification System
- **Real-time Notifications** for events, birthdays, and announcements
- **Multiple Delivery Methods** (Email, SMS, Push, In-App)
- **Bulk Notifications** for mass communication
- **Notification Preferences** per user
- **Announcement Board** for congregation-wide messages

### 💬 Social Media Features
- **Member Posts** with privacy controls
- **Comments and Replies** system
- **Like/React** functionality
- **Prayer Requests** with support system
- **Testimonies** with approval workflow
- **Media Gallery** for photos and documents

### 📊 Profile Management
- **Comprehensive User Profiles** with all required fields
- **Privacy Settings** for personal information
- **Committee Memberships** and preferences
- **Academic Information** tracking
- **Spiritual Milestones** (Baptism, Sealing dates)

## Technology Stack

- **Backend**: Django 4.2+ with Django REST Framework
- **Authentication**: JWT with Simple JWT
- **Database**: PostgreSQL (configurable)
- **Media Handling**: Pillow for image processing
- **Task Queue**: Celery with Redis
- **Notifications**: django-notifications-hq
- **Social Features**: django-taggit, django-activity-stream

## Installation & Setup

### Prerequisites
- Python 3.8+
- PostgreSQL
- Redis (for Celery tasks)
- Node.js (for frontend, if applicable)

### 1. Clone the Repository
```bash
git clone https://github.com/Akende1/UNZANAC-Management-System.git
cd UNZANAC-Management-System
```

### 2. Create Virtual Environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the backend directory:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
POSTGRES_DB=unza_congregation
POSTGRES_USER=your-db-user
POSTGRES_PASSWORD=your-db-password
```

### 5. Database Setup
```bash
cd backend
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
```

### 7. Populate Initial Data
```bash
python manage.py populate_initial_data
```

### 8. Run Development Server
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

## API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `POST /api/auth/token/refresh/` - Refresh JWT token
- `POST /api/auth/password-reset/` - Request password reset
- `POST /api/auth/password-reset-confirm/<uidb64>/<token>/` - Confirm password reset

### User Management
- `GET /api/auth/profile/` - Get current user profile
- `PUT /api/auth/profile/` - Update user profile
- `GET /api/auth/dashboard/` - User dashboard data
- `GET /api/auth/search-users/` - Search users

### Committees
- `GET /api/committees/` - List all committees
- `GET /api/committees/<id>/` - Get committee details
- `POST /api/committees/<id>/join/` - Join a committee
- `DELETE /api/committees/<id>/leave/` - Leave a committee

### Events
- `GET /api/events/` - List all events
- `POST /api/events/` - Create new event (admin/high privilege)
- `GET /api/events/<id>/` - Get event details
- `POST /api/events/<id>/register/` - Register for event
- `GET /api/events/calendar/` - Calendar view of events

### Notifications
- `GET /api/notifications/` - Get user notifications
- `POST /api/notifications/<id>/mark-read/` - Mark notification as read
- `GET /api/notifications/announcements/` - Get announcements

## User Data Fields

### Required Registration Fields
- **Basic Info**: First Name, Last Name, Username, Email, Password
- **Personal**: Gender, Date of Birth
- **Contact**: Phone Number (optional)
- **Addresses**: 
  - Residential Address
  - Residential Apostle Area
  - School Residential Address (on/off campus)
- **Spiritual**: Date of Baptism, Date of Sealing
- **Academic**: Programme of Study, Year of Study
- **Church**: Roles in Church, Committee Preferences

### Optional Profile Fields
- Profile Picture
- Bio/About Me
- Interests and Skills
- Privacy Preferences
- Notification Settings

## Committee Descriptions

### 1. Catering Committee
Handles all food-related organization with Elite as the main concern. Responsible for planning and organizing catering services during special programs.

### 2. Music Committee
Makes every service beautiful through music. The UNZA congregation is renowned for their singing, with orchestra adding heavenly glory to every musical aspect.

### 3. Organizing Committee
The most organized committee that structures all programs properly. Responsible for planning, supporting, and organizing congregational youth activities and transport arrangements.

### 4. Finance Committee
Creates congregational budgets and ensures proper fund collection flow and management.

### 5. DRAPO Committee
Composed of talented members who reach hearts through entertainment and teaching. DRAPO combines drama and poetry to unleash talent at the right time and place.

### 6. Communication Committee
Handles sound dissemination from conveyance to reception points, making every church activity come alive through proper audio management.

### 7. Testify Committee
Helps members understand their faith stance while preparing for Christ's return. Also handles all doctrinal issues in the congregation.

### 8. Flowering Committee
Responsible for beautifying the house of God during all church activities.

### 9. Secretarial Committee
Maintains all church records and documentation, managing data records for both membership and the church at large.

## Development

### Running Tests
```bash
python manage.py test
```

### Code Style
The project follows PEP 8 guidelines. Use black for formatting:
```bash
pip install black
black .
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Security Features

- JWT token-based authentication
- Role-based permissions
- Input validation and sanitization
- CSRF protection
- Password strength validation
- Secure file upload handling
- Privacy controls for user data

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please contact the development team or create an issue in the repository.

## Acknowledgments

- New Apostolic Church UNZA Congregation
- Django REST Framework community
- All contributors and committee members
A collaborative project building a church management system with Django (backend) and React (frontend).

## Suggestions / Future Features

The following features are planned or suggested for future development:

- Mobile App Integration (Android/iOS)
- Analytics Dashboard (attendance, engagement, donations)
- Online Payments/Donations (integrate payment gateways)
- QR Code Attendance Tracking
- Push Notifications (mobile devices)
- Document Management (uploads, sharing, versioning)
- Volunteer Tracking (roles, hours, assignments)
- Public API for Third-Party Integration
- Multi-Language Support (internationalization)
- Accessibility Improvements (WCAG compliance)
- Automated Backups (database, media)
- Query Optimization (select_related, prefetch_related, indexes)
- API Documentation (drf-spectacular, OpenAPI)
- Deployment Documentation (production setup, Docker, CI/CD)
- Advanced Notification Preferences (per event/type)
- Role-Based Custom Dashboards
- Advanced Reporting (export to PDF/Excel)
- Integration with External Church Systems
- SMS Gateway Integration
- Calendar Sync (Google/Outlook)
- Attendance Analytics
- Gamification/Recognition Features
- Audit Logs for Admin Actions
- Enhanced Security (2FA, OAuth)
- Customizable Member Fields
- Bulk Data Import/Export
- Geo-location Features (map members/events)
- Event Ticketing/RSVP
- Resource Booking (rooms, equipment)
- Feedback/Survey System
- Scheduled Tasks/Reminders
- Integration with WhatsApp/Telegram
- Advanced Media Gallery (albums, tagging)
- Customizable Email Templates
- Admin Analytics Dashboard

