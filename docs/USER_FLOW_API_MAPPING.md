# User Flow to API Endpoint Mapping

This document maps user interaction flows from `CLAUDE_USER_GUIDE.md` to their corresponding backend API endpoints in the VentAI application.

## Authentication Flow
- **User Login**: 
  - Flow: User enters credentials to log in.
  - Endpoint: `POST /api/auth/token`
- **User Registration**: 
  - Flow: User signs up with username, email, and password.
  - Endpoint: `POST /api/auth/register`

## Project Management Flow
- **Create Project**: 
  - Flow: User creates a new project with name and description.
  - Endpoint: `POST /api/projects/`
- **View Projects**: 
  - Flow: User views list of all projects.
  - Endpoint: `GET /api/projects/`

## AI Interaction Flow
- **Generate AI Content**: 
  - Flow: User submits a prompt for AI content generation.
  - Endpoint: `POST /api/ai/generate`
- **Check Task Status**: 
  - Flow: User checks the status of an AI task.
  - Endpoint: `GET /api/ai/tasks/{taskId}`
