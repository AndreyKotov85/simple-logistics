# simple-logistics
A simple project present the idea of logistics, deliver as much as possible packages in one day with multiple couriers.

The idea to optimize the number of delivery and distance.
Using google maps api to get the duration time data.
If service lookup is failed, estimate duration by direct distance between points with speed 20km/h

# Using

Set environment key
SIMPLE_LOGISTICS_KEY : API key for google map service  

dataset.txt
number_of_worker working_duration
hq_latitude hq_longitude
start_latitude start_longitude end_latitude end_longitude
start_latitude start_longitude end_latitude end_longitude
start_latitude start_longitude end_latitude end_longitude
.........................................................

number_of_worker: interger, number of delivery courier
working_duration: working time (in second)
hq_latitude hq_longitude : Start point of workes
start_latitude start_longitude end_latitude end_longitude: point of start and end of package