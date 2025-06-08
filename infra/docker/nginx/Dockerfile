FROM nginx:alpine

# Copy custom nginx configuration
COPY infra/docker/nginx/nginx.conf /etc/nginx/nginx.conf

# Create directories for SSL certificates and logs
RUN mkdir -p /etc/nginx/ssl /var/log/nginx

# Copy SSL certificates (if available)
# COPY infra/docker/nginx/ssl/ /etc/nginx/ssl/

# Set proper permissions
RUN chown -R nginx:nginx /var/cache/nginx /var/log/nginx /etc/nginx/ssl

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/health || exit 1

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]
