FROM freeradius/freeradius-server:latest-alpine

RUN apk update && apk add python3>=3.8.10-r0 py3-pip>=20.3.4-r0 \
    && pip3 install pynetbox>=6.6.2 \
    && cd /etc/raddb/mods-enabled && ln -s ../mods-available/python3 python3

CMD ["freeradius", "-X"] # Set default command
