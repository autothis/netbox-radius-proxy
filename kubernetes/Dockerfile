# ---- Base stage ----
# Use freeradius/freeradius-server:latest-alpine as the base image
FROM freeradius/freeradius-server:latest-alpine AS base

# Update and install necessary packages
RUN apk update && apk add python3>=3.8.10-r0 py3-pip>=20.3.4-r0 \
    && pip3 install pynetbox>=6.6.2 \
    && cd /etc/raddb/mods-enabled && ln -s ../mods-available/python3 python3 \
    # Cleanup
    && rm -rf /var/cache/apk/* \
    && rm -rf /root/.cache/pip/*

# ---- Final stage ----
# Use freeradius/freeradius-server:latest-alpine as the final image
FROM freeradius/freeradius-server:latest-alpine AS final

# Copy necessary files from base stage
COPY ../volumes/default /etc/raddb/sites-available/default
COPY ../volumes/python3 /etc/raddb/mods-available/python3
COPY ../volumes/netbox_clients.py /etc/raddb/mods-config/python3/netbox_clients.py

# Default Command
CMD ["freeradius", "-X"]
