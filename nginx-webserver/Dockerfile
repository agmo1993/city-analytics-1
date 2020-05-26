FROM nginx:latest

ENV WELCOME_STRING "nginx in Docker"

WORKDIR /usr/share/nginx/html

COPY ["/city-analytics/nginx-webserver/front-end/map.py", "/usr/share/nginx/html"]

EXPOSE 8081

RUN cp index.html index_backup.html; \
    apt-get update && apt-get install -qy vim; \
    apt-get install -y python3 && \
    apt-get install -y python3-pip && \
    pip3 install folium && \
    pip3 install pandas && \
    pip3 install cloudant && \
    python3 map.py

CMD nginx -g 'daemon off;'
