from phew import server, template
import network
import time
import json

from secrets import stored_ssid, stored_password

def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    tries = 0
    while (not wlan.isconnected() and tries < 5):
        print('Connecting...')
        tries += 1
        time.sleep(5)
    if (wlan.isconnected()):
        print("Connected to wifi")
        print(wlan.ifconfig())
    return wlan


wlan = connect_wifi(stored_ssid, stored_password)


def json_response(json_obj, code):
    return server.Response(json.dumps(json_obj), code, {"Content-Type": "application/json"})


@server.route("/avit", methods=["POST"])
def avit(request):
    print(f"Sent data: {request.data}")
    return json_response({"message": "'ere, tha's earnt it"}, 200)


def ssid_mapper(ssid_b):
        return ssid_b[0].decode('utf-8')


def process_wifi_list(wifi_list):
    out = ""
    for x in wifi_list:
        out += f"{ssid_mapper(x)}, "
    return out


@server.route("/wifi-page", methods=["GET"])
def wifi_page(request):
    wifi_list = wlan.scan()
    wifi_list_string = process_wifi_list(wifi_list)
    return server.Response(
        template.render_template("views/wifi_networks.html",
                                 wifi_list=wifi_list_string),
                                 200,
                                 {"Content-Type": "text/html"})


@server.route("/wifi-list", methods=["GET"])
def wifi_list(request):
    wifi_list = wlan.scan()
    return json_response(list(map(ssid_mapper, wifi_list)), 200)


@server.route("/wifi-connect", methods=["POST"])
def wifi_connect(request):
    ssid = request.data["ssid"]
    password = request.data["password"]
    wlan = connect_wifi(ssid, password)
    if wlan.isconnected():
        return json_response({"status": "Connected", "ip": wlan.ifconfig()[0]}, 200)
    return json_response({"status": "Not Connected"}, 200)


@server.catchall()
def catchall(request):
    return "Not found", 404


server.run()