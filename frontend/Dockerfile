# Build stage
FROM node:18-alpine AS builder

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install --legacy-peer-deps && \
    npm install typescript@5.0.0 ajv@8.11.2 ajv-keywords@5.1.0 react-scripts@5.0.1 --save-exact --legacy-peer-deps

# Copy and build application
COPY . .
RUN npm run build

# Production stage
FROM node:18-alpine

# Install serve for static file serving
RUN npm install -g serve@14.2.1

# Use existing node user for security
USER node

WORKDIR /app
COPY --from=builder /app/build ./build

# Expose port
EXPOSE 3000

# Command to serve the built app
CMD ["serve", "-s", "build", "-l", "3000"]