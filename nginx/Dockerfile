FROM nginx:1.12.2

ARG NGINX_UID

RUN rm /etc/nginx/nginx.conf /etc/nginx/mime.types
COPY nginx.conf /etc/nginx/nginx.conf
COPY basic.conf /etc/nginx/basic.conf
COPY mime.types /etc/nginx/mime.types
RUN mkdir /etc/nginx/ssl
COPY default /etc/nginx/sites-enabled/default
COPY default-ssl /etc/nginx/sites-available/default-ssl
COPY directive-only /etc/nginx/directive-only
COPY location /etc/nginx/location
COPY cert.pem /etc/nginx/
COPY key.pem /etc/nginx/

COPY proxy /etc/nginx/sites-available

RUN ln -s /etc/nginx/sites-available/proxy /etc/nginx/sites-enabled/proxy \
    && usermod -u $NGINX_UID nginx

VOLUME /efs/projects
VOLUME /usr/share/nginx/html/compbio

EXPOSE 80 443 5000

CMD ["nginx"]
