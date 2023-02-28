# Netbox-Radius-Proxy
docker-compose up --build -d

# Configuration
- Update netbox_clients url and token
- Add proxy targets in proxy.conf

# Usage
- Define a custom field with the name of radius_secret to keep per-device secrets. Optionally, set a default value for this attribute.
- Define either a local or inherited context in Netbox defining the nas-type field to be passed to NPS:
```
{
    "nas-type": "junos"
}
```

Default settings allow any client request to be accepted, with any source address from the 10.0.0.0/8 range transposed into the FreeRADIUS-Client-IP-Address variable. FreeRADIUS then polls Netbox via API utilising a Python module to dynamically match against a device with the source address defined as a management IP, and then retrieve the expected client secret from the device's custom fields.

The `nas-type` variable defined within the device's rendered context will be appended to NAS-Client identifier to assist with isolation against per-OS or per-Role NPS policies.
