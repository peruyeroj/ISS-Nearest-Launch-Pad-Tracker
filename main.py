import requests
import json
from shapely.geometry import Point, MultiPoint
from shapely.ops import nearest_points
import math
import numpy as np
from geopy import distance 

def main():

    response = requests.get("http://api.open-notify.org/iss-now.json")

    json_data = response.json()

    iss_longitude = float(json_data['iss_position']['longitude'])
    iss_latitude = float(json_data['iss_position']['latitude'])

    iss_location = Point(iss_latitude, iss_longitude)
    iss_data = (iss_latitude, iss_longitude)

    print(json_data)

    print(f"latitude:{iss_latitude}")
    print(f"longitude:{iss_longitude}")

    launch_sites = { # https://aerospace.csis.org/data/spaceports-of-the-world/ and google earth for altitude measured in meters above sea level
        "Pacific Spaceport Complex-Alaska":{"latitude":57.4, "longitude":152.3, "altitude": 30},
        "Vandenberg Air Force Base":{"latitude":34.6, "longitude":120.6, "altitude":153},
        "Wallops Flight Facility":{"latitude":37.9, "longitude":75.5,"altitude":10},
        "Cape Canaveral/Kennedy Space Center":{"latitude":28.6, "longitude":80.6,"altitude":5},
        "Guiana Space Centre":{"latitude":5.2, "longitude":52.8,"altitude":10},
        "Palmachim Airbase":{"latitude":31.9, "longitude":34.7, "altitude":60},#double check
        "Imam Khomeini Space Center":{"latitude":35.2, "longitude":54.0,"altitude":968},
        "Shahroud Missile Test Site":{"latitude":36.2, "longitude":55.4,"altitude":1328},
        "Baikonur Cosmodrome":{"latitude":46.0, "longitude":63.3,"altitude":130},
        "Yasny Launch Base":{"latitude":51.1, "longitude":59.8,"altitude":350},
        "Plesetsk Cosmodrome":{"latitude":62.9, "longitude":40.6,"altitude":111},
        "Satish Dhawan Space Centre":{"latitude":13.7, "longitude":80.2,"altitude":25},
        "Wenchang Satellite Launch Center":{"latitude":19.6, "longitude":111.0,"altitude":8},
        "Xichang Satellite Launch Center":{"latitude":28.3, "longitude":102.0,"altitude":2064},
        "Jiuquan Satellite Launch Center":{"latitude":41.0, "longitude":100.3,"altitude":1074},
        "Taiyuan Satellite Launch Center":{"latitude":38.9, "longitude":111.6,"altitude":1472},
        "Vostochny Cosmodrome":{"latitude":51.9, "longitude":128.3,"altitude":270},
        "Sohae Satellite Launching Station":{"latitude":39.7, "longitude":124.7,"altitude":61},
        "Naro Space Center":{"latitude":34.4, "longitude":127.5,"altitude":175},
        "Uchinoura Space Center":{"latitude":31.3, "longitude":131.1,"altitude":-9},
        "Tanegashima Space Center":{"latitude":30.4, "longitude":131.0,"altitude":47},
        "Rocket Lab Launch Complex":{"latitude":39.3, "longitude":177.9,"altitude":103}
        }

    points = [Point(site["latitude"], site["longitude"]) for site in launch_sites.values()]
    multi_point = MultiPoint(points)

    nearest_launch_site = nearest_points(iss_location, multi_point)
    print(f"Closest Launch Pad coordinates to ISS location: {nearest_launch_site[1]}")


    launch_latitude = nearest_launch_site[1].x
    launch_longitude = nearest_launch_site[1].y

    for site, coordinates in launch_sites.items():
        if coordinates["latitude"] == launch_latitude and coordinates["longitude"] == launch_longitude:
            print(f"Matching coordinates found for {site}: Latitude {launch_latitude}, Longitude {launch_longitude}")
            launch_site_altitude = launch_sites[site]["altitude"]
            print(f"The launch altitude is {launch_site_altitude}")

    iss_altitude = 400000 #average iss altiutde is 400 km
    launch_data = (launch_latitude, launch_longitude)
    
    distance_2d= distance.distance(iss_data,launch_data).m #2d distance between iss and launch pad
    print(distance_2d)

    #3D euclidean distance
    distance_3d = math.sqrt(distance_2d ** 2 + (iss_altitude - launch_site_altitude) ** 2)

    print(distance_3d)

if __name__  == "__main__":
    main()