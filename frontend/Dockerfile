# Build stage
FROM node:16.14.2-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install typescript@4.9.5 --save-exact && \
    npm install ajv@8.11.2 ajv-keywords@5.1.0 --save-exact && \
    npm install react-scripts@5.0.1 --save-exact --legacy-peer-deps
COPY . .
RUN npm run build

# Production stage
FROM node:16.14.2-alpine
WORKDIR /app
ENV NODE_ENV production
COPY --from=builder /app/build ./build
COPY --from=builder /app/node_modules ./node_modules
EXPOSE 3000
CMD ["npm", "start"]