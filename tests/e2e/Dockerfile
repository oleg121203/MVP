FROM node:18-alpine

# Install Playwright dependencies
RUN apk add --no-cache \
    chromium \
    nss \
    freetype \
    freetype-dev \
    harfbuzz \
    ca-certificates \
    ttf-freefont

# Set Playwright environment variables
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
ENV PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1
ENV PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium-browser

# Set working directory
WORKDIR /app

# Copy package files
COPY tests/e2e/package*.json ./

# Install dependencies
RUN npm ci

# Install Playwright
RUN npx playwright install --with-deps

# Copy test files
COPY tests/e2e/ .

# Create reports directory
RUN mkdir -p reports

# Run tests
CMD ["npm", "run", "test:e2e"]
