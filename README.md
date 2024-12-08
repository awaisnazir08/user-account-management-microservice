# User Account Management Microservice
## Overview
This microservice provides user registration, authentication, and profile management functionality with secure JWT-based authentication.

## Prerequisites
* Docker
* Google Cloud SDK
* Google Cloud account

Deployment to Google Cloud Run

1. Initial Setup
```bash 
# Initialize Google Cloud
gcloud init

# Enable required Google Cloud services
gcloud services enable containerregistry.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

2. Clone Repository
```bash
git clone https://github.com/awaisnazir08/user-account-management-microservice.git
cd user-account-management-microservice/
```

3. Build and Push Docker Image
```bash
# Build Docker image (replace PROJECT_ID with your Google Cloud project ID)
docker build -t gcr.io/PROJECT_ID/user-management-service:v1 .

# Configure Docker authentication
gcloud auth configure-docker

# Push image to Google Container Registry
docker push gcr.io/PROJECT_ID/user-management-service:v1
```

4. Deploy to Cloud Run

```bash
gcloud run deploy user-management-service \
    --image gcr.io/PROJECT_ID/user-management-service:v1 \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --set-env-vars MONGO_URI="mongodb-URL",JWT_SECRET_KEY="your-secret-key" \
    --port=5000
```

## Local Development
Build Docker Image
```bash
docker build -t user-management-service .
```

### Run Locally
```bash
docker run -p 5000:5000 user-management-service
```

## API Endpoints
### User Registration

* URL: /api/users/register
* Method: POST
* Headers: Content-Type: application/json
Request Body:

```json
{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "SecurePassword123!"
    }
```

### User Login

* URL: /api/users/login
* Method: POST
* Headers: Content-Type: application/json
Request Body:

```json
{
    "identifier": "johndoe",
    "password": "SecurePassword123!"
}
```

Response: Access token

### User Profile

* URL: /api/users/profile
* Method: GET
* Headers: Authorization: Bearer <access-token>
Response:

```json
{
    "_id": "675587bd7eb7b76a26212f41",
    "created_at": "Sun, 08 Dec 2024 11:49:17 GMT",
    "email": "john@example.com",
    "is_active": true,
    "last_login": "Sun, 08 Dec 2024 15:58:19 GMT",
    "username": "johndoe"
}
```

## Environment Variables

* MONGO_URI: MongoDB connection string
* JWT_SECRET_KEY: Secret key for JWT token generation

## Security Considerations

Use strong, unique passwords
Keep your JWT secret key confidential
Use HTTPS in production
Implement additional security measures as needed

## Contributing
Please read the contributing guidelines before making pull requests.