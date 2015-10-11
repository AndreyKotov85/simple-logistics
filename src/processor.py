__author__ = 'afterlastangel@gmail.com'
class Journey:
    """An object to store the journey"""
    length = 0
    data = []

    def __init__(self):
        self.length = 0
        self.data = []

def find_shortest_journey(journey_array):
    shortest_length = float("inf")
    shortest_journey = None
    for i in range(1, len(journey_array)):
        journey = journey_array[i]
        if journey.length < shortest_length and journey.length != 0:
            shortest_length = journey.length
            shortest_journey = journey.data[:]
    return shortest_journey

def process_data(data, max_length):
    size = len(data)
    # init journey_array
    journey_array = [[Journey() for _ in range(size)] for _ in range(size)]

    # init data for first trip
    for j in range(1, size):
        i = 0
        if data[i][j] != 0 and data[i][j] <= max_length:
            journey_array[i][j].data.append(j)
            journey_array[i][j].length = data[i][j]

    # loop for next trips
    for i in range(1, size-1):
        found = False
        # loop for number of destinations exclude starter
        for j in range(1, size):
            # check for previous step, find the shortest
            shortest_length = float("inf")
            shortest_journey_data = None
            for k in range(1, size):
                if j not in journey_array[i-1][k].data and data[k][j] != 0:
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
def main():
    data = [[0, 1, 1, 1],
            [0, 0, 1, 1],
            [0, 1, 0, 1],
            [0, 1, 1, 0]]

    journey = process_data(data, 1)
    print journey
    remove_journey(data, journey)
    journey = process_data(data, 2)
    print journey
    remove_journey(data, journey)
    journey = process_data(data, 1)
    print journey



if __name__ == "__main__":
 main()



