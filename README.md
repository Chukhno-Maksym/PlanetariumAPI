
# Planetarium API

Planetarium API is a RESTful API for booking tickets, managing show sessions, planetariums, and astronomy shows. The project is built with Django and Django REST Framework, using PostgreSQL as the database.

## Tech Stack
- **Django** — web framework.
- **Django REST Framework** — for creating RESTful APIs.
- **PostgreSQL** — relational database.
- **Python 3.x** — programming language.
- **Docker** (optional) — for containerization.

## Features

- **Ticket Booking**: Users can book tickets for astronomy shows, specifying the time and location for specific sessions.
- **Show Session Management**: Administrators can create, view, update, and delete astronomy show sessions.
- **Dynamic Management of Planetariums and Shows**: Support for multiple planetariums and shows, allowing location selection for each session.
- **Authentication and Authorization**: API is protected using tokens, where users authenticate to access private endpoints.
- **API Testing**: Built-in tests to verify the functionality of the API.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/planetarium-api.git
   cd planetarium-api
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # for Linux / macOS
   venv\Scripts\activate  # for Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure .env:**
   Ensure there is a `.env` file in the root of the project containing the `SECRET_KEY`:
   ```
   SECRET_KEY=your_secret_key_here
   ```

5. **Run database migrations:**
   Run migrations to create all necessary tables:
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser:**
   Create a superuser to access the Django admin panel:
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the server:**
   Start the server:
   ```bash
   python manage.py runserver
   ```

## Using the API

### Authentication

To access the API, you need to authenticate via a token. To do this, request a token by sending a POST request to the authentication endpoint (e.g., using Django Rest Framework Token Authentication):

1. Authentication using the token:
   - POST `/api/token/`
   - Request body:
     ```json
     {
       "username": "your_username",
       "password": "your_password"
     }
     ```
   - Response:
     ```json
     {
       "access": "your_access_token",
       "refresh": "your_refresh_token"
     }
     ```

2. To use the token, include it in the `Authorization` header when making API requests:
   ```
   Authorization: Bearer your_access_token
   ```

### Available Endpoints:

#### 1. **Show Sessions (ShowSession)**

- **GET** `/api/planetarium/show-session/` — list of all sessions.
- **GET** `/api/planetarium/show-session/{id}/` — retrieve a specific session.
- **POST** `/api/planetarium/show-session/` — create a new session.

#### 2. **Tickets**

- **POST** `/api/planetarium/tickets/` — create a ticket for a session (must specify seat). After creating a ticket, it automatically downloaded in pdf file.

#### 3. **Reservations**

- **POST** `/api/planetarium/reservation/` — create a reservation (automatically created when a ticket is created).

#### 4. **Planetarium Domes**

- **GET** `/api/planetarium/planetarium-dome/` — list of all planetarium domes.

#### 5. **Astronomy Shows**

- **GET** `/api/planetarium/astronomy-show/` — list of all astronomy shows.

#### 6. **Show Themes**

- **GET** `/api/planetarium/show-theme/` — list of all show themes.

## Testing

To test the API, Django TestCase is used, and all tests can be run with:
```bash
python manage.py test
```

## Docker (optional)

1. **Build the container:**
   ```bash
   docker build -t planetarium-api .
   ```

2. **Run the container:**
   ```bash
   docker run -d -p 8001:8000 planetarium-api
   ```
![image](https://github.com/user-attachments/assets/f4895b5a-d6ba-4dca-8b09-ee6b07d0ca9d)
![image](https://github.com/user-attachments/assets/2144f3a7-3913-4144-a4b1-e8662773bc96)
![image](https://github.com/user-attachments/assets/be7a3cbf-4c5e-45e3-b42d-fcff6c9261fe)
![image](https://github.com/user-attachments/assets/3142a32f-94d0-4715-9b57-b0083ce785ec)
![image](https://github.com/user-attachments/assets/bf17a46f-ebd1-4638-a4c8-fa37dff330cd)
![image](https://github.com/user-attachments/assets/cbfc7c95-b5a5-4b79-998c-8b6db5fab47e)
![image](https://github.com/user-attachments/assets/1a968693-615f-420f-b97f-54b18abda2e1)
