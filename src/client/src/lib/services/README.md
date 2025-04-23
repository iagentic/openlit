# API Service Integration

This directory contains service modules that interact with the Python API server.

## Overview

The frontend application has been integrated with the Python API server to handle data operations. This integration replaces direct database access via Prisma with API calls to the backend server.

## Available Services

### User Service

The `userService` module provides methods for user-related operations:

- `getCurrentUser()`: Get the current user's profile
- `createUser(email, password)`: Create a new user
- `updateUserProfile(data)`: Update the current user's profile
- `login(email, password)`: Login with email and password
- `logout()`: Logout the current user
- `isAuthenticated()`: Check if the user is authenticated

### Database Config Service

The `dbConfigService` module provides methods for database configuration operations:

- `getDatabaseConfigs()`: Get all database configs for the current user
- `createDatabaseConfig(config)`: Create a new database config
- `getApiKeys()`: Get API keys for the current user
- `createApiKey(data)`: Create a new API key

## API Client

The API client (`api.ts`) handles the communication with the backend server. It provides methods for making HTTP requests and managing authentication tokens.

## Migration Strategy

The integration follows a gradual migration strategy:

1. New code should use the API services directly
2. Existing code has been updated to use the API services while maintaining backward compatibility
3. Legacy functions are marked as deprecated and will be removed in future versions

## Authentication

Authentication is handled via JWT tokens. The API client automatically includes the token in requests when available.

## Environment Configuration

The API URL is configured via the `NEXT_PUBLIC_API_URL` environment variable, which defaults to `http://localhost:9090`. 