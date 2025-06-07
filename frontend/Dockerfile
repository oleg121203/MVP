# Development Dockerfile for frontend
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Set environment variables
ENV NODE_ENV=development

# Install dependencies with caching
COPY package*.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm install

# Copy source code
COPY . .

# Expose port
EXPOSE 3000

# Start development server
CMD ["npm", "start"]
