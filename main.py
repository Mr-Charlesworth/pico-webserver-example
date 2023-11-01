from phew import server
import network
import time

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("andy", "charlesworth")

while (not wlan.isconnected()):
    print('Connecting...')
    time.sleep(5)

print("Connected to wifi")
print(wlan.ifconfig())

@server.route("/random", methods=["GET"])
def random_number(request):
    import random
    min = int(request.query.get("min", 0))
    max = int(request.query.get("max", 100))
    return str(random.randint(min, max))

@server.catchall()
def catchall(request):
    return "Not found", 404

server.run()