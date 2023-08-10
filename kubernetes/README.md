# Netbox-Radius-Proxy

We have chosen to move the ENV's, dynamic_clients and proxy.conf to configmap's instead of being built in to the image

`There are no liveness or health checks in this at the moment!`

# Configuration
- Update Netbox url and token in the [env_configmap](config/env_configmap.yaml)
- Add proxy targets in [proxy.conf](config/proxy_configmap.yaml)
- Update the [dynamic clients](config/dynamic_clients_configmap.yaml) configmap

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

# Build

- This needs to be run from the parent directory
```
cd ..
docker build . -t <your tag goes here> -f kubernetes/Dockerfile
```

# Deploy to Kubernetes

```
kubectl apply -f kubernetes/config/ -n <NAMESPACE>
```

# Adding labels to your nodes

- Target one node
```
kubectl label nodes <NODE_NAME> app=device-radius
```

- Target all nodes with an exsiting label. (workload=remote is the existing label in this example)
```
kubectl get nodes --selector=workload=remote -o custom-columns=NAME:.metadata.name --no-headers | xargs -I {} kubectl label nodes {} app=device-radius
```

- Target all Worker nodes
```
kubectl get nodes -o custom-columns=NAME:.metadata.name --no-headers | grep 'worker' | xargs -I {} kubectl label nodes {} app=device-radius
```

# Removing labels from your nodes

- This will remove the label from one node
```
kubectl label nodes <NODE_NAME> app-
```


- This will remove all `app` labels
```
kubectl get nodes --selector=app=device-radius -o custom-columns=NAME:.metadata.name --no-headers | xargs -I {} kubectl label nodes {} app-
```

