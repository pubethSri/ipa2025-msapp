from bson import json_util
from router_client import get_interfaces
from database import save_interface_status


def callback(ch, method, props, body):
    job = json_util.loads(body.decode())
    router_ip = job["ip"]
    router_username = job["username"]
    router_password = job["password"]
    print(f"Received job for router {router_ip}")
    try:
        output = get_interfaces(router_ip, router_username, router_password)
        save_interface_status(router_ip, output)
        print(f"Stored interface status for {router_ip}")
    except Exception as e:
        print(f" Error: {e}")
