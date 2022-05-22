FROM mosstech/nginx-with-prometheus:1.1
COPY config/default.conf /etc/nginx/conf.d/default.conf
EXPOSE 8080
WORKDIR "/app"
