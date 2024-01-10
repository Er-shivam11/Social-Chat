# Social-Chat
# Django Social App

Developed a Django ASGI WebSocket application for a social platform. The application allows users to connect, share posts, comment, update their profiles, like posts, and engage in real-time chat with each other.

The application uses Django Channels for handling WebSocket connections, enabling real-time features. Django authentication and authorization mechanisms are implemented to ensure secure access.

## Features
- User registration and login
- User profiles with update functionality
- Post creation, update, and deletion
- Real-time chat functionality using Django Channels
- Post liking and commenting
- Admin dashboard for managing user data

## Technologies Used
The app is built using the following technologies:
- Python 3.6+
- Django 3.2+
- Django Channels for WebSocket functionality
- HTML/CSS
- Bootstrap

## How to Use

### Local Development

1. **Clone the repository:**
   ```bash
   git clone url
   cd filename


Install the necessary dependencies:

Copy code
pip install -r requirements.txt


Apply migrations and start the server:

Copy code
python manage.py migrate
python manage.py runserver


Using Docker

1. **Clone the repository:**
   ```bash
   git clone url
   cd filename


2. **Build and run the Docker container:**

bash
Copy code
docker-compose up --build 



Open a browser and navigate to http://localhost:8000/ to access the social app.

WebSocket and Real-Time Features
This application leverages Django Channels to enable real-time features. WebSocket connections are used for instant updates, including real-time chat. The chat functionality is secure and private, allowing users to communicate seamlessly.

Explore the application's WebSocket-related code, authentication mechanisms, and Django Channels settings for a deeper understanding of the real-time functionality.

Feel free to reach out for any questions or improvements!
