# VentAI API Examples

## Authentication

### Register a User
```http
POST /api/auth/register
Content-Type: application/json

{
  "username": "newuser",
  "email": "user@example.com",
  "password": "securepassword123"
}
```

### Get Access Token
```http
POST /api/auth/token
Content-Type: application/x-www-form-urlencoded

username=newuser&password=securepassword123
```

## Projects

### Create Project
```http
POST /api/projects/
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "My HVAC Project",
  "description": "Residential building ventilation"
}
```

### Get Project
```http
GET /api/projects/{project_id}
Authorization: Bearer <token>
```

## AI Services

### Generate Content
```http
POST /api/ai/generate
Authorization: Bearer <token>
Content-Type: application/json

{
  "prompt": "Design ventilation for 100m2 apartment"
}
```

### Check Task Status
```http
GET /api/ai/tasks/{task_id}
Authorization: Bearer <token>
```
