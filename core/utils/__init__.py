import errno
import ipaddress
import os

import geocoder
from user_agents import parse


def mkdir_log(directory: str):
    # PARENT
    parent_dir: str = os.getcwd()

    path: str = os.path.abspath(os.path.join(parent_dir, directory))

    try:
        os.makedirs(path, exist_ok=True)
    except TypeError:
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise


def get_loc_by_ip(ip):
    ip_info = geocoder.ip(ip)

    if not ip_info.address:
        ip_info.address = "UNKNOWN"

    return ip_info


def get_ip_address(request):
    x_forwarded_for_ip = request.headers.get("x-forwarded-for")
    x_original_forwarded_for_ip = request.headers.get("x-original-forwarded-for")
    ip_info_dict = dict(
        x_forwarded_for=x_forwarded_for_ip,
        x_original_forwarded_for=x_original_forwarded_for_ip,
    )
    ip = ""

    if x_forwarded_for_ip:
        ip = get_public_ip(x_forwarded_for_ip.split(",")[0])
        if ip:
            return ip
    if x_original_forwarded_for_ip:
        ip = get_public_ip(x_original_forwarded_for_ip)
        if ip:
            return ip

    ip = request.client.host
    ip_info_dict.update(client_host=ip)
    # logger.info("message fields", extra={"json_field": ip_info_dict})
    return ip


def get_user_agent(user_agent):
    ua = str(parse(user_agent))
    return ua


def get_public_ip(ip):
    is_public = ipaddress.ip_address(ip).is_global
    if is_public:
        return ip
