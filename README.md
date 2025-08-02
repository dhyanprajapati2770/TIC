# 🏥 Modern Healthcare Web Application

A comprehensive, full-featured healthcare web application built with Django (Backend) and React (Frontend) featuring AI-powered symptom checking, disease prediction, medicine recommendations, pharmacy store, and real-time doctor chatbot.

## ✨ Features

### 🔬 Core Healthcare Features
- **Symptom Checker**: AI-powered disease prediction based on symptoms
- **Disease Predictor**: ML-based disease prediction with confidence scores
- **Medicine Recommendations**: Personalized medicine suggestions
- **Pharmacy Store**: Complete e-commerce with cart and checkout
- **Doctor Chatbot**: Real-time WebSocket-based AI healthcare assistant
- **User Dashboard**: Comprehensive health tracking and history

### 🛠️ Technical Features
- **Modern UI/UX**: Lamborghini-style premium visuals with glassmorphism
- **Responsive Design**: Mobile-first, tablet, and desktop optimized
- **Real-time Communication**: WebSocket-based chat functionality
- **Authentication**: JWT-based secure authentication
- **Admin Panel**: Comprehensive Django admin interface
- **RESTful API**: Complete REST API with Django REST Framework

## 🚀 Tech Stack

### Backend
- **Django 5.2.1**: Core web framework
- **Django REST Framework**: RESTful API development
- **Django Channels**: WebSocket support for real-time chat
- **JWT Authentication**: Secure token-based authentication
- **SQLite**: Database (can be easily switched to PostgreSQL/MySQL)
- **Pillow**: Image processing for medicine images

### Frontend
- **React 18**: Modern UI library
- **TailwindCSS**: Utility-first CSS framework
- **Framer Motion**: Smooth animations and transitions
- **React Router**: Client-side routing
- **Axios**: HTTP client for API requests
- **Socket.io-client**: WebSocket client for real-time chat
- **React Hot Toast**: Beautiful toast notifications
- **Lucide React**: Modern icon library

## 📦 Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd healthcare-app
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

4. **Run database migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create superuser (optional)**
```bash
python manage.py createsuperuser
```

6. **Populate sample data**
```bash
python manage.py populate_data
```

7. **Run the Django server**
```bash
python manage.py runserver
```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Start the development server**
```bash
npm start
```

The frontend will be available at `http://localhost:3000`

## 🗄️ Database Schema

### Core Models
- **UserProfile**: Extended user information
- **Symptom**: Medical symptoms with severity levels
- **Disease**: Diseases with symptoms, treatments, and risk levels
- **Medicine**: Pharmaceutical products with pricing and stock
- **DiseasePrediction**: AI prediction results
- **Cart/CartItem**: Shopping cart functionality
- **Order/OrderItem**: Order management
- **ChatMessage**: Real-time chat messages
- **Prescription**: Medical prescriptions

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/token/` - JWT token obtain
- `POST /api/token/refresh/` - JWT token refresh

### Healthcare
- `GET /api/symptoms/` - List all symptoms
- `GET /api/diseases/` - List all diseases
- `POST /api/symptom-checker/` - Disease prediction
- `GET /api/medicines/` - List all medicines
- `POST /api/medicine-recommendations/` - Medicine suggestions

### E-commerce
- `GET /api/cart/` - Get user cart
- `POST /api/cart/` - Add item to cart
- `PUT /api/cart/items/{id}/` - Update cart item
- `DELETE /api/cart/items/{id}/` - Remove cart item
- `GET /api/orders/` - List user orders
- `POST /api/orders/create/` - Create new order

### Chat
- `GET /api/chat/history/` - Chat history
- `POST /api/chat/bot/` - Send message to chatbot
- WebSocket: `ws://localhost:8000/ws/chat/` - Real-time chat

## 🎨 UI/UX Features

### Design System
- **Color Palette**: Primary (Blue), Secondary (Purple), Success (Green), Warning (Orange), Danger (Red)
- **Typography**: Inter font family
- **Animations**: Framer Motion for smooth transitions
- **Glassmorphism**: Modern glass effect on auth pages
- **Gradients**: Premium gradient backgrounds

### Components
- **Responsive Navbar**: Mobile-friendly navigation
- **Protected Routes**: Authentication-based routing
- **Toast Notifications**: Beautiful feedback messages
- **Loading States**: Smooth loading indicators
- **Form Validation**: Client-side and server-side validation

## 🔐 Security Features

- **JWT Authentication**: Secure token-based auth
- **CORS Configuration**: Cross-origin resource sharing
- **Input Validation**: Comprehensive form validation
- **SQL Injection Protection**: Django ORM protection
- **XSS Protection**: Built-in Django security

## 🚀 Deployment

### Backend Deployment
1. Set `DEBUG = False` in settings
2. Configure production database
3. Set up static files serving
4. Use Gunicorn or uWSGI
5. Configure reverse proxy (Nginx)

### Frontend Deployment
1. Build the application: `npm run build`
2. Serve static files
3. Configure environment variables
4. Set up CDN for assets

## 📱 Mobile Responsiveness

The application is fully responsive with:
- **Mobile-first design**
- **Touch-friendly interfaces**
- **Optimized navigation**
- **Responsive grids and layouts**
- **Mobile-specific interactions**

## 🔧 Development

### Adding New Features
1. Create Django models in `healthcare/models.py`
2. Add serializers in `healthcare/serializers.py`
3. Create views in `healthcare/views.py`
4. Add URL patterns in `healthcare/urls.py`
5. Create React components in `frontend/src/components/`
6. Add pages in `frontend/src/pages/`

### Code Style
- **Backend**: PEP 8 Python style guide
- **Frontend**: ESLint configuration
- **Components**: Functional components with hooks
- **State Management**: Context API and local state

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support, email support@healthcare.com or create an issue in the repository.

---

**Built with ❤️ for modern healthcare solutions**