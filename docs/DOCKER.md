# Docker Setup for Private_GPT

This Docker configuration is designed to work seamlessly when Private_GPT is installed via pip or git+pip, without requiring any external docker directory or entrypoint scripts. It supports the new enhanced authentication system with no-auth mode for flexible deployment scenarios.

## Quick Start

### Build and Run

```bash
# Build the image
docker build -t private_gpt-api .

# Run the container (default port 8000, with authentication)
docker run -p 8000:8000 private_gpt-api

# Run with no authentication required (great for development/demos)
docker run -p 8000:8000 -e WEBSCOUT_NO_AUTH=true private_gpt-api

# Run with no authentication and no rate limiting (maximum openness)
docker run -p 8000:8000 -e WEBSCOUT_NO_AUTH=true -e WEBSCOUT_NO_RATE_LIMIT=true private_gpt-api

# Run with custom port (e.g., 7860)
docker run -p 7860:7860 -e WEBSCOUT_PORT=7860 private_gpt-api

# Run with MongoDB support
docker run -p 8000:8000 -e MONGODB_URL=mongodb://localhost:27017 private_gpt-api
```

### Using Docker Compose

```bash
# Basic setup (with authentication)
docker-compose up private_gpt-api

# No-auth mode for development/demos
docker-compose -f docker-compose.yml -f docker-compose.no-auth.yml up private_gpt-api

# With custom port
WEBSCOUT_PORT=7860 docker-compose up private_gpt-api

# Production setup with Gunicorn
docker-compose --profile production up private_gpt-api-production

# Development setup with hot reload
docker-compose --profile development up private_gpt-api-dev

# MongoDB setup with authentication
docker-compose --profile mongodb up
```

### Using Makefile

```bash
# Quick start (build + run + test)
make quick-start

# Build image
make build

# Start services
make up

# View logs
make logs

# Run health check
make health

# Clean up
make clean
```

## Configuration

### Environment Variables

The Private_GPT server reads the following environment variables at runtime. The server configuration is dynamically determined from code defaults unless explicitly overridden via environment variables.

#### **Core Server Settings**
- `WEBSCOUT_HOST` - Server host (default: 0.0.0.0 from ServerConfig)
- `WEBSCOUT_PORT` - Server port (default: 8000 from ServerConfig)
- `WEBSCOUT_WORKERS` - Number of worker processes (default: 1)
- `WEBSCOUT_LOG_LEVEL` - Log level: debug, info, warning, error, critical (default: info)
- `WEBSCOUT_DEBUG` - Enable debug mode (default: false from ServerConfig)
- `WEBSCOUT_API_TITLE` - FastAPI app title (default: "Private_GPT API" from code)
- `WEBSCOUT_API_DESCRIPTION` - FastAPI app description (default: "OpenAI API compatible interface for various LLM providers" from code)
- `WEBSCOUT_API_VERSION` - FastAPI app version (default: "0.2.0" from code)
- `WEBSCOUT_API_DOCS_URL` - FastAPI docs URL (default: /docs from code)
- `WEBSCOUT_API_REDOC_URL` - FastAPI redoc URL (default: /redoc from code)
- `WEBSCOUT_API_OPENAPI_URL` - FastAPI OpenAPI URL (default: /openapi.json from code)

#### **Authentication & Security** 🔐
- `WEBSCOUT_REQUEST_LOGGING` - Enable request logging (default: true from ServerConfig)
- `WEBSCOUT_API_KEY` - Legacy API key for authentication (optional)

**Dynamic Configuration**: The server also supports configuring the following programmatically through ServerConfig class:
- `auth_required` - Authentication required flag (default: false from ServerConfig)
- `rate_limit_enabled` - Rate limiting enabled flag (default: false from ServerConfig)
- `cors_origins` - CORS allowed origins (default: ["*"] from ServerConfig)
- `max_request_size` - Maximum request size (default: 10MB from ServerConfig)
- `request_timeout` - Request timeout in seconds (default: 300 from ServerConfig)

#### **Database Configuration** 🗄️
- `WEBSCOUT_DATA_DIR` - Data directory for JSON database (default: /app/data from ServerConfig)

#### **Provider Settings**
- `WEBSCOUT_DEFAULT_PROVIDER` - Default LLM provider (default: ChatGPT from ServerConfig)
- `WEBSCOUT_BASE_URL` - Base URL for the API (default: None from ServerConfig)

**Legacy Support**: For backward compatibility, the following legacy environment variables are also supported:
- `PORT` (fallback for `WEBSCOUT_PORT`)
- `API_KEY` (fallback for `WEBSCOUT_API_KEY`)
- `DEFAULT_PROVIDER` (fallback for `WEBSCOUT_DEFAULT_PROVIDER`)
- `BASE_URL` (fallback for `WEBSCOUT_BASE_URL`)
- `DEBUG` (fallback for `WEBSCOUT_DEBUG`)

**Note**: When both WEBSCOUT_* and legacy variables are set, WEBSCOUT_* takes precedence.

### Service Profiles

- **Default**: Basic API server with enhanced authentication system
- **No-Auth**: Development/demo mode with no authentication required 🔓
- **Production**: Gunicorn with multiple workers and optimized settings
- **Development**: Uvicorn with hot reload and debug logging
- **MongoDB**: Full setup with MongoDB database support 🗄️
- **Nginx**: Optional reverse proxy (requires custom nginx.conf)
- **Monitoring**: Optional Prometheus monitoring (requires custom prometheus.yml)

## Features

- ✅ No external docker directory required
- ✅ Works with pip/git installations
- ✅ Multi-stage build for optimized image size
- ✅ Non-root user for security
- ✅ Health checks included
- ✅ Multiple deployment profiles
- ✅ **NEW!** No-auth mode for development/demos 🔓
- ✅ **NEW!** Enhanced authentication system with API key management 🔑
- ✅ **NEW!** MongoDB and JSON database support 🗄️
- ✅ **NEW!** Rate limiting with IP-based fallback 🛡️
- ✅ Comprehensive Makefile for easy management
- ✅ Volume mounts for logs and data persistence

## Health Checks

The setup includes automatic health checks that verify the `/health` endpoint is responding correctly. This endpoint provides comprehensive system status including database connectivity and authentication system status.

## Security

- Runs as non-root user (`private_gpt:private_gpt`)
- Minimal runtime dependencies
- Security-optimized container settings
- **Enhanced authentication system** with API key management 🔑
- **Rate limiting** to prevent abuse 🛡️
- **No-auth mode** for development (use with caution in production) 🔓
- **Database encryption** support with MongoDB
- **Secure API key generation** with cryptographic randomness

## Troubleshooting

### Check container status
```bash
make status
```

### View logs
```bash
make logs
```

### Test endpoints
```bash
make test-endpoints
```

### Access container shell
```bash
make shell
```
