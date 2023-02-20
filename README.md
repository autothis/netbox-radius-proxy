# freeradius
docker-compose up --build -d

# Configuration
- Update netbox_clients url and token
- Add proxy targets in proxy.conf

# Usage
Define a local context in Netbox matching the following format:
```
{
    "nas-type": "junos",
    "radius_server": [
        {
            "secret": "testing123"
        }
    ]
}

Default settings allow any client request to be accepted, with any source address from the 10.0.0.0/8 range transposed into the FreeRADIUS-Client-IP-Address variable. FreeRADIUS then polls Netbox via API utilising a Python module to dynamically match against a device with the source address defined as a management IP, and then retrieve the NAS-type and expected client secret from the local context.
