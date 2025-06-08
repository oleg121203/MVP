# API Endpoint Test Plan

This document outlines the plan for systematically testing every API endpoint defined in `backend/src/fastapi_app/main.py` as part of TASK-ID-007. The testing will use structures from `docs/API_EXAMPLES.md` for request bodies.

## Project Analysis Endpoints (TASK-ID-007.1)
- **POST /api/project-analysis/analyze**: Test project data analysis.
  - Request Body: JSON with project data (refer to API_EXAMPLES.md).
  - Expected Response: Analysis results or error if data is invalid.
- **POST /api/project-analysis/train**: Test model training for analysis.
  - Request Body: Training data or parameters (refer to API_EXAMPLES.md).
  - Expected Response: Training status or error if parameters are incorrect.

## CRM Endpoints (TASK-ID-007.2)
- **GET /api/crm/customers**: Test retrieval of customer data.
  - Expected Response: List of customers or empty list if no data.
- **POST /api/crm/customers**: Test creation of a new customer.
  - Request Body: Customer data (refer to API_EXAMPLES.md).
  - Expected Response: Created customer details or error if data is invalid.

## Cost Optimization Endpoints (TASK-ID-007.3)
- **POST /api/cost-optimization/analyze**: Test cost analysis for a project.
  - Request Body: Project cost data (refer to API_EXAMPLES.md).
  - Expected Response: Cost optimization suggestions or error if data is invalid.
- **GET /api/cost-optimization/reports**: Test retrieval of cost optimization reports.
  - Expected Response: List of reports or empty list if no data.
