import requests
import json
from shapely.geometry import Point, MultiPoint
from shapely.ops import nearest_points

response = requests.get("http://api.open-notify.org/iss-now.json")

json_data = response.json()

longitude = json_data['iss_position']['longitude']
latitude = json_data['iss_position']['latitude']

issLocation = Point(latitude, longitude)
print(json_data)

print(f"latitude:{latitude}")
print(f"longitude:{longitude}")

launchSites = { # https://aerospace.csis.org/data/spaceports-of-the-world/
    "Pacific Spaceport Complex-Alaska":{"latitude":57.4, "longitude":152.3},
    "Vandenberg Air Force Base":{"latitude":34.6, "longitude":120.6},
    "Wallops Flight Facility":{"latitude":37.9, "longitude":75.5},
    "Cape Canaveral/Kennedy Space Center":{"latitude":28.6, "longitude":80.6},
    "Guiana Space Centre":{"latitude":5.2, "longitude":52.8},
    "Palmachim Airbase":{"latitude":31.9, "longitude":34.7},
    "Imam Khomeini Space Center":{"latitude":35.2, "longitude":54.0},
    "Shahroud Missile Test Site":{"latitude":36.2, "longitude":55.4},
    "Baikonur Cosmodrome":{"latitude":46.0, "longitude":63.3},
    "Yasny Launch Base":{"latitude":51.1, "longitude":59.8},
    "Plesetsk Cosmodrome":{"latitude":62.9, "longitude":40.6},
    "Satish Dhawan Space Centre":{"latitude":13.7, "longitude":80.2},
    "Wenchang Satellite Launch Center":{"latitude":19.6, "longitude":111.0},
    "Xichang Satellite Launch Center":{"latitude":28.3, "longitude":102.0},
    "Jiuquan Satellite Launch Center":{"latitude":41.0, "longitude":100.3},
    "Taiyuan Satellite Launch Center":{"latitude":38.9, "longitude":111.6},
    "Vostochny Cosmodrome":{"latitude":51.9, "longitude":128.3},
    "Sohae Satellite Launching Station":{"latitude":39.7, "longitude":124.7},
    "Naro Space Center":{"latitude":34.4, "longitude":127.5},
    "Uchinoura Space Center":{"latitude":31.3, "longitude":131.1},
    "Tanegashima Space Center":{"latitude":30.4, "longitude":131.0},
    "Rocket Lab Launch Complex":{"latitude":39.3, "longitude":177.9}
    }

points = [Point(site["latitude"], site["longitude"]) for site in launchSites.values()]
multi_point = MultiPoint(points)

nearestLaunchSite = nearest_points(issLocation, multi_point)
print(f"Closest Launch Pad coordinates to ISS location: {nearestLaunchSite[1]}")
