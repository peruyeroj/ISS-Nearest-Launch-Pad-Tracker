import requests
import json
from shapely.geometry import Point, MultiPoint
from shapely.ops import nearest_points
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def main():

    response = requests.get("http://api.open-notify.org/iss-now.json")

    json_data = response.json()

    iss_longitude = float(json_data['iss_position']['longitude'])
    iss_latitude = float(json_data['iss_position']['latitude'])

    iss_location = Point(iss_latitude, iss_longitude)
    print(json_data)

    print(f"latitude:{iss_latitude}")
    print(f"longitude:{iss_longitude}")

    launch_sites = { # https://aerospace.csis.org/data/spaceports-of-the-world/
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

    points = [Point(site["latitude"], site["longitude"]) for site in launch_sites.values()]
    multi_point = MultiPoint(points)

    nearest_launch_site = nearest_points(iss_location, multi_point)
    print(f"Closest Launch Pad coordinates to ISS location: {nearest_launch_site[1]}")

    near_latitude = nearest_launch_site[1].x
    near_longitude = nearest_launch_site[1].y

    for site, coordinates in launch_sites.items():
        if coordinates["latitude"] == near_latitude and coordinates["longitude"] == near_longitude:
            print(f"Matching coordinates found for {site}: Latitude {near_latitude}, Longitude {near_longitude}")

    iss_altitude = float(400)
    earth_radius = 6371
    launch_altitude = 0 

    launch_lat_cartesian, launch_long_cartesian, launch_alt_cartesian = to_cartesian(near_latitude, near_longitude, launch_altitude, earth_radius)

    iss_lat_cartesian, iss_long_cartesian, iss_alt_cartesian = to_cartesian(iss_latitude, iss_longitude, iss_altitude, earth_radius)
    print(f"launch latitude in cartesian coords: {launch_lat_cartesian}, launch longitude in cartesian coords: {launch_long_cartesian}, launch altitude in cartesian coords: {launch_alt_cartesian}")
    print(f"iss latitude in cartesian coords: {iss_lat_cartesian}, iss longitude in cartesian coords: {iss_long_cartesian}, iss altitude in cartesian coords: {iss_alt_cartesian}")
    
    # Create a figure and a 3D axis
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot the first point (in blue)
    ax.scatter(launch_lat_cartesian, launch_long_cartesian, launch_alt_cartesian, c='blue', marker='o', label='Point 1')

    # Plot the second point (in red)
    ax.scatter(iss_lat_cartesian, iss_long_cartesian, iss_alt_cartesian, c='red', marker='^', label='Point 2')

    # Label the axes
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Add a legend
    ax.legend()

    # Show the plot
    plt.show()



def to_cartesian(latitude, longitude, altitude, earth_radius):
    # Radius of the Earth in kilometers (mean value)
    # You can adjust this radius based on your specific use case

    # Convert latitude and longitude from degrees to radians
    lat_rad = math.radians(latitude)
    lon_rad = math.radians(longitude)

    # Calculate Cartesian coordinates
    x = earth_radius * math.cos(lat_rad) * math.cos(lon_rad)
    y = earth_radius * math.cos(lat_rad) * math.sin(lon_rad)
    z = earth_radius * math.sin(lat_rad) + altitude  # Altitude is added to the Z coordinate

    return x, y, z

if __name__  == "__main__":
    main()