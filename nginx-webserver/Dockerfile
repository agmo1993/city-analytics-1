FROM nginx:latest

ENV WELCOME_STRING "nginx in Docker"

WORKDIR /usr/share/nginx/html

COPY /city-analytics/nginx-webserver/front-end /usr/share/nginx/html

EXPOSE 80

ARG ip_address

RUN echo ${ip_address} && \
    cp index.html index_backup.html; \
    apt-get update && apt-get install -qy vim; \
    apt-get install -y python3 && \
    apt-get install -y python3-pip && \
    pip3 install folium && \
    pip3 install pandas && \
    pip3 install cloudant && \
    chmod +x htmlupdated.sh && \
    ./htmlupdated.sh ${ip_address}

CMD nginx -g 'daemon off;'
