FROM al3xos/nginx-with-prometheus:1.9
COPY config/default.conf /etc/nginx/conf.d/default.conf
EXPOSE 8080
WORKDIR "/app"
