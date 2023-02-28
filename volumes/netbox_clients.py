#!/usr/libexec/platform-python

import radiusd
import pynetbox
import os

url = os.environ.get('NETBOX_URL')
token = os.environ.get('NETBOX_TOKEN')

nb    = pynetbox.api(url, token=token)

def instantiate(p):
  print("*** instantiate ***")
  radiusd.radlog(radiusd.L_INFO, '*** netbox_clients instantiate ***')
  print(p)

def authorize(p):
  print("*** authorize ***")
  radiusd.radlog(radiusd.L_INFO, '*** radlog call in authorize ***')

  # check to have an IP address
  for avpair in p['request']:
    (attribute, value) = avpair
    if (attribute=="FreeRADIUS-Client-IP-Address"):
      address = value

  # Get information for that address from netbox
  try:
      nbaddress = nb.ipam.ip_addresses.get(address=address)
  except:
      radiusd.radlog(radiusd.L_INFO, f"*** NETBOX: Unable to find IP address... Dropping packet ***")
      return radiusd.RLM_MODULE_REJECT

  # Fail if IP address unknown to netbox
  if not nbaddress:
      radiusd.radlog(radiusd.L_INFO, f"*** NETBOX: Address not found... Dropping packet ***")
      return radiusd.RLM_MODULE_REJECT

  # Get information abount the device.
  try:
      nbdevice = nb.dcim.devices.get(name=nbaddress.assigned_object.device.name)
  except:
      radiusd.radlog(radiusd.L_INFO, f"*** NETBOX: Address not associated to device... Dropping packet ***")
      return radiusd.RLM_MODULE_REJECT

  # Known device. Update the shared secret from config_context of the device.
  try:
      nbdevice['custom_fields']['radius_secret']
  except:
      radiusd.radlog(radiusd.L_INFO, f"*** NETBOX: Device does not have a shared secret... Dropping packet ***")
      return radiusd.RLM_MODULE_REJECT

  _nas_type = "other"
  try:
      if nbdevice['config_context']['nas-type']:
          _nas_type = nbdevice['config_context']['nas-type']
          radiusd.radlog(radiusd.L_INFO, f"*** NETBOX: NAS-Type found, using {_nas_type} ***")
  except:
      radiusd.radlog(radiusd.L_INFO, f"*** NETBOX: NAS-Type not found, using other ***")

  update_dict = {
    "config": ( ('FreeRADIUS-Client-Secret', nbdevice['custom_fields']['radius_secret']),
                ('FreeRADIUS-Client-Shortname', nbdevice['name']), 
                ('FreeRADIUS-Client-NAS-Type', _nas_type), ),
  }
  return radiusd.RLM_MODULE_OK, update_dict

def detach(p):
  print("*** goodbye from dynclients.py ***")
  return radiusd.RLM_MODULE_OK
