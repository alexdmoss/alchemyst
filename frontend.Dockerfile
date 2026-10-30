FROM al3xos/nginx-with-prometheus:1.17-3005760348-2026.10.29.2012
USER nginx
COPY config/default.conf /etc/nginx/conf.d/default.conf
EXPOSE 8080
WORKDIR "/app"
