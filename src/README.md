# Mergington High School Activities

A comprehensive web-based management system for extracurricular activities at Mergington High School. This application provides teachers with powerful tools to manage student registrations and allows everyone to explore available activities with advanced filtering and search capabilities.

## Features

### Activity Management
- Browse all available extracurricular activities with detailed information
- View activity descriptions, schedules, and current enrollment
- Track participant capacity with visual indicators
- Display participant lists for each activity

### Advanced Filtering & Search
- **Category Filters**: Sports, Arts, Academic, Community, Technology
- **Day Filters**: Filter activities by specific days of the week
- **Time Filters**: Before School, After School, Weekend activities
- **Search**: Find activities by name, description, or schedule details

### Teacher Authentication & Registration
- Secure teacher login system with role-based access
- Teachers can register students for activities
- Teachers can unregister students from activities
- Session management with automatic validation

### Modern User Interface
- Responsive design that works on desktop and mobile devices
- Interactive modal dialogs for registration
- Real-time activity filtering without page reloads
- Visual capacity indicators and participant tracking

## Technical Details

### Backend
- **Framework**: FastAPI with Python
- **Database**: MongoDB for persistent data storage
- **Authentication**: Teacher-based login system with session management
- **API**: RESTful endpoints for activities and authentication

### Frontend
- **Technologies**: HTML5, CSS3, JavaScript (ES6+)
- **Design**: Responsive, mobile-first approach
- **Features**: Dynamic filtering, search, modal dialogs, real-time updates

### Data Storage
- Activity details including schedules, descriptions, and capacity limits
- Teacher accounts with role-based permissions
- Student registration tracking with participant lists
- All data persists between server restarts via MongoDB

## Development Guide

For detailed setup and development instructions, please refer to our [Development Guide](../docs/how-to-develop.md).
