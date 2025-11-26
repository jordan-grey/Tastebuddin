# Serve static HTML/CSS/JS using nginx
FROM nginx:stable-alpine

# Remove default nginx static files
RUN rm -rf /usr/share/nginx/html/*

# Copy your frontend files
COPY . /usr/share/nginx/html

# Expose nginx port
EXPOSE 80
