# Use lightweight nginx server
FROM nginx:alpine

# Remove default nginx static files
RUN rm -rf /usr/share/nginx/html/*

# Copy your HTML, CSS, JS into the nginx web directory
COPY . /usr/share/nginx/html

# Expose port 80
EXPOSE 80

