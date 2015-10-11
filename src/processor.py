__author__ = 'afterlastangel@gmail.com'
from math import hypot
import googlemaps
import os
from math import radians, cos, sin, asin, sqrt


class Journey:
    """An object to store the journey"""
    length = 0
    data = []

    def __init__(self):
        self.length = 0
        self.data = []

class Point:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude


class DeliveryRequest:
    def __init__(self, start, end):
        self.start = start
        self.end = end


def find_shortest_journey(journey_array):
    shortest_length = float("inf")
    shortest_journey = None
    for i in range(1, len(journey_array)):
        journey = journey_array[i]
        if 0 < journey.length < shortest_length :
            shortest_length = journey.length
            shortest_journey = journey.data[:]
    return shortest_journey, shortest_length

def process_data(data, max_length):
    size = len(data)
    # init journey_array
    journey_array = [[Journey() for _ in range(size)] for _ in range(size)]

    # init data for first trip
    for j in range(1, size):
        i = 0
        if 0 < data[i][j] <= max_length:
            journey_array[i][j].data.append(j)
            journey_array[i][j].length = data[i][j]

    # loop for next trips
    for i in range(1, size-1):
        found = False
        # loop for number of destinations exclude starter (HQ)
        for j in range(1, size):
            # check for previous step, find the shortest
            shortest_length = float("inf")
            shortest_journey_data = None
            for k in range(1, size):
                if journey_array[i-1][k].data and j not in journey_array[i-1][k].data and data[k][j] > 0:
                    new_length = journey_array[i-1][k].length + data[k][j]
                    if new_length <= max_length and new_length < shortest_length:
                        shortest_journey_data = journey_array[i-1][k].data[:]
                        shortest_length = new_length
            if shortest_length != float("inf"):
                journey_array[i][j].data = shortest_journey_data[:]
                journey_array[i][j].data.append(j)
                journey_array[i][j].length = shortest_length
                found = True
        if not found:
            return find_shortest_journey(journey_array[i-1])
    return find_shortest_journey(journey_array[size-2])

def remove_journey(data, journey):
    for k in journey:
        for i in range(len(data)):
            for j in range(len(data[i])):
                if i == k or j == k:
                    data[i][j] = 0


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6367 * c
    return km


def duration(point1, point2):
    """
    Find duration https://developers.google.com/maps/documentation/distance-matrix/intro
    """
    gmaps = googlemaps.Client(key=os.environ.get('SIMPLE_LOGISTICS_KEY'))
    result = gmaps.distance_matrix([(point1.latitude,point1.longitude)], [(point2.latitude,point2.longitude)])
    if result['status'] == u'OK':
        if result['rows'][0]['elements'][0]['status'] == u'OK':
            return result['rows'][0]['elements'][0]['duration']['value']
    # in case of google maps fail, use estimation and speed 20km/h
    return haversine(point1.longitude, point1.latitude, point2.longitude, point2.latitude) * 180

def calculate_request(hq, requests):
    data = [[0 for _ in range(len(requests)+1)] for _ in range(len(requests)+1)]
    for j in range(1, len(requests)+1):
        data[0][j] = duration(hq, requests[j-1].start) \
            + duration(requests[j-1].start, requests[j-1].end)

    for i in range(1, len(requests)+1):
        for j in range(1, len(requests)+1):
            if i != j:
                data[i][j] = duration(requests[i-1].end, requests[j-1].start) \
                    + duration(requests[j-1].start, requests[j-1].end)

    return data

def read_data():
    f = open('dataset.txt', 'r')
    lineno = 0
    requests = []
    for line in f:
        if lineno == 0:
            worker = int(line.split(" ")[0])
            max_travel = float(line.split(" ")[1])
        elif lineno == 1:
            hq = Point(float(line.split(" ")[0]), float(line.split(" ")[1]))
        else:
            start = Point(float(line.split(" ")[0]), float(line.split(" ")[1]))
            end = Point(float(line.split(" ")[2]), float(line.split(" ")[3]))
            requests.append(DeliveryRequest(start, end))
        lineno = lineno + 1
    return worker, max_travel, hq, requests

def main():
    """
    Test data
    data = [[0, 1, 4, 1],
            [0, 0, 1, 3],
            [0, 1, 0, 1],
            [0, 1, 1, 0]]
    """

    worker, max_travel, hq, requests = read_data()
    data = calculate_request(hq, requests)
    """
    data = [[0, 5, 7, 12, 6],
            [0, 0, 5, 7, 3],
            [0, 7, 0, 5, 4],
            [0, 4, 5, 0, 4],
            [0, 8, 5, 8, 4]]
    max_travel = 100
    """
    for i in range(worker):
        journey, length = process_data(data, max_travel)
        if journey:
            print journey, length
            remove_journey(data, journey)
        else:
            break


if __name__ == "__main__":
 main()



