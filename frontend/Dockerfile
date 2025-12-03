FROM nginx:alpine

# Copy our custom config first
COPY nginx.conf /etc/nginx/nginx.conf

# Copy entire frontend folder
COPY . /usr/share/nginx/html
