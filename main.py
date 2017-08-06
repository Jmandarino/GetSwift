# python 3.5
import json
import geopy.distance
import time
import requests


class Location:
    """Location's is any latitude point and longitude point
    
    Location objects are used to store locations of both packages and drones
    
    Attributes:
        lat (:obj: `float`): Describes the latitude of a location
        long (:obj: `float`): Describes the longitude of a location

    """

    def __init__(self, lat, long):
        self.lat = lat
        self.long = long



class Package:
    """A deliverable parcel for drones to carry
    
    A package is any object that a drone can take from the Depot to any given location
    
    Attributes:
        package_id (:obj: `int`): The unique ID used to identify a package
        destination (:obj: `Location`): The destination a package needs to get to
        deadline (:obj: `int`): The time (Unix timestamp) that a package must arrive to its destination
        latest_departure (:obj: `int`): The time can leave the depot in order to be on time

    """

    def __init__(self, package_id, destination, deadline):
        self.package_id = package_id
        self.destination = destination
        self.deadline = deadline

        # the latest time a package can leave and still be on time
        self.latest_departure = None

    def set_latest_departure(self, velcocity, start_location):
        # use goepy to get distance between self.destination obj and start_location obj

        # logic convert km/hr to km/s, then figure out how many seconds before you need to leave
        distance = geopy.distance.vincenty((start_location.lat, start_location.long), (DEPOT.lat, DEPOT.long)).km
        # v = D / T
        time = distance / velcocity

        # get how many seconds sooner the drone needs to leave
        self.latest_departure = int(self.deadline - time)

    def __str__(self):
        return str(self.package_id)

    def __repr__(self):
        return self.__str__()




class Drone:
    """The Object used to carry a package to its destintion
    
    Drones have a set speed of 50km/h as defined in the guidelines. They can only be used once and have unlimited range
    
    Attributes:
        velocity(:obj: `float`): A km/s equivalent for the drone's speed. 
        drone_id(:obj: `int`): A unique ID for the drone
        location(:obj: `Location`): The location of the drone when we pull the API data
        packages(:obj: `Package`): The package in the drone's current possession

    """

    def __init__(self, drone_id, location, packages):
        self.velocity = DRONE_SPEED_kms
        self.drone_id = drone_id
        self.location = location
        self.packages = packages

        self.set_time_to_avail(
            self.velocity)  # The time until its available not when its availible. Will have to add current time
        # to know when its availible.

    def set_time_to_avail(self, velocity):

        if self.packages is None:
            distance = geopy.distance.vincenty((self.location.lat, self.location.long), (DEPOT.lat, DEPOT.long)).km

            # cast to an  int to round to a whole number
            self.available = int(distance / velocity)
        else:
            # complete the package delivery and then set availability.
            p_distance = geopy.distance.vincenty((self.location.lat, self.location.long),
                                                 (self.packages.destination.lat, self.packages.destination.long)).km

            p_delivary_time = p_distance / velocity

            return_distance = geopy.distance.vincenty((DEPOT.lat, DEPOT.long),
                                                      (
                                                      self.packages.destination.lat, self.packages.destination.long)).km

            return_time = return_distance / velocity
            # cast to an  int to round to a whole number
            self.available = int(p_delivary_time + return_time)

    def __str__(self):
        return "{droneId: " + str(self.drone_id) +", "+str(self.packages)+"}"

    def __repr__(self):
        return self.__str__()



# constants
available_drones_list = []
packages_list = []
busy_drones = []
not_delivariable = []

DEPOT = Location(-37.816664, 144.9638476)
DRONE_SPEED_kmh = 50
DRONE_SPEED_kms = DRONE_SPEED_kmh / 3600


def get_drones(drones, now):
    """A method that parses the JSON Data for drones
    
    Parses the inputted JSON and populates the busy_drones list and the available_drones_list.
    Those drones with initial packages are sent into the busy_drone_list because Drones can only make one delivary in 
    this example
    
    :param drones: A JSON Representation of the Drones obj
    :param now: The current time in Unix timestamp
    :return: 
    """
    for drone in drones:
        id = drone["droneId"]
        lat = drone["location"]["latitude"]
        long = drone["location"]["longitude"]
        d = Drone(id, Location(lat, long), None)

        if drone["packages"] == []:
            available_drones_list.append(d)
            continue

        # as per the documations the packages array should be singular
        package_data = drone["packages"][0]

        # TODO: make a function that takes in the data and makes a package?
        p_id = package_data["packageId"]
        p_lat = package_data["destination"]["latitude"]
        p_long = package_data["destination"]["longitude"]
        deadline = package_data["deadline"]
        # append package to drone
        d.packages = Package(p_id, Location(p_lat, p_long), deadline)
        busy_drones.append(d)


def get_packages(packages):
    """A method that parses the JSON Data for packages

    Parses the inputted JSON and populates the packages_list list 

    :param drones: A JSON Representation of the package objects
    :return: 
    """
    for package in package_data:
        p_id = package["packageId"]
        p_lat = package["destination"]["latitude"]
        p_long = package["destination"]["longitude"]
        deadline = package["deadline"]

        p = Package(p_id, Location(p_lat, p_long), deadline)
        p.set_latest_departure(DRONE_SPEED_kms, DEPOT)
        packages_list.append(p)


if __name__ == '__main__':
    # get current time
    now = int(time.time())
    drone_url = "https://codetest.kube.getswift.co/drones"
    packages_url ="https://codetest.kube.getswift.co/packages"

    drone_file = requests.get(drone_url)

    if drone_file.ok:
        drone_data = json.loads(drone_file.content)
    else:
        # if not 200 status
        drone_file.raise_for_status()

    # parse json data
    get_drones(drone_data, now)

    packages_file = requests.get(packages_url)
    if packages_file.ok:

        package_data = json.loads(packages_file.content)
    else:
        # if not 200 status
        packages_file.raise_for_status()

    # parse json data
    get_packages(package_data)

    # sort list by which packages need to leave first to get to their destination on time
    packages_list.sort(key=lambda x: x.latest_departure)
    # sort the list by drones that are free the soonest.

    # this is done after we parse the json to make sure all drones "start" at the same time
    for drone in available_drones_list:
       drone.available += now

    # sort drones by which are available the soonest
    available_drones_list.sort(key=lambda x: x.available)

    # logic: go through all the available drones, when those are no longer an option we need to start searching the
    # soonest available drones in the "busy drone list" and start using those.

    while (available_drones_list != [] and packages_list != []):
        # check that the package can depart after the drone is ready
        departure = packages_list[0].latest_departure
        available = available_drones_list[0].available


        # if depature is a later date
        if departure >= available:
            # remove first item of packages list and attach it to the drone
            available_drones_list[0].packages = packages_list.pop(0)
            # drone is now done for this problem
            busy_drones.append(available_drones_list.pop(0))

        else:
            # if the soonest available drone can't deliver the package no other drones will be able to
            not_delivariable.append(packages_list.pop(0))

    # if there are any other drones append it to the list of those that can't be delivered
    for x in packages_list:
        not_delivariable.append(x)


    # for printing purposes

    results = {}
    results["assignments"] = busy_drones
    results["unassignedPackageIds"] = not_delivariable

    print(results)

