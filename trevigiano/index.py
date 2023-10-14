import requests

AUTHORIZATION = "dbGmcUmnplpddKgjTpVxWpGxVBpzalIGIWSuwZQoIIZjffITDH"

headers = {
    "authorization": AUTHORIZATION,
}

print(requests.get("https://panoramic-copper-production.up.railway.app/users/1151021206850506805", headers=headers).json())