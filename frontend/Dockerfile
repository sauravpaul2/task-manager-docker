# Build stage
FROM node:22-alpine as build

WORKDIR /app

# Install dependencies (leverage Docker cache)
COPY package*.json ./
RUN npm install --omit=dev

# Copy source and build
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built files from build stage
COPY --from=build /app/build /usr/share/nginx/html

# Copy custom Nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
    CMD wget --quiet --tries=1 --spider http://localhost:80 || exit 1

# Nginx starts automatically
CMD ["nginx", "-g", "daemon off;"]