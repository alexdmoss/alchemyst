FROM al3xos/nginx-with-prometheus:1.17-3014332921-2026.11.01.1059
USER nginx
COPY config/default.conf /etc/nginx/conf.d/default.conf
EXPOSE 8080
WORKDIR "/app"
