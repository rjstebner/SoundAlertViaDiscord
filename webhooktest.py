import requests

webhook_url = "https://discord.com/api/webhooks/1403162415390261359/D_KA7jImNFdkzEsBZd-EMXGoe3PxK5tPzDg3xCwx-rNZRRV9Ouz7tyEwwAikk8zthvR3"

payload = {"content": "Test message from script"}

response = requests.post(webhook_url, json=payload)
print(response.status_code, response.text)