# GetSwift Coding Challenge:

This is my submission for GetSwift's take home coding challenge. 

#### How to install

This program has only been tested on Python 3.5+ however older versions of python should work fine with some modification

Dependencies required:
*geopy*

install via pip: `pip install geopy`

###### Please also give an indication of how you envisage your solution will be deployed, and what other components it might interact with."

My algorithm can be deployed as a smaller part of a larger system. This solution does not handle streaming data well
but manages data given in groups. Streaming data would require a different a different approach to maintain effectiveness

I imagine this can be useful for testing but real world will have many more factors, drone speed will change, drones 
need to recharge, drones can also deliver multiple packages, etc. Real world dynamics might require more complicated 
solutions as they have more complicated variables

#### How did you implement your solution?


I treated this as a scheduling problem but instead of doing exhaustive shcduleing (O(2<sup>n</sup>)) I choose to use a 
more efficient route. 

Overview:
1. Calculate when a package needs to leave by
2. Calculate when a Drone can leave the depot
3. Create a sorted list of packages, sorted by needing to leave soonest
4. Create a sorted list of drones, sorted by soonest available
5. for each package, if the soonest  available drone can't deliver the package it is undeliverable
6. print results



I used python 3.5 with the help of geopy module. 

Assumptions I made:
1. A drone with an initial package will not be able to deliver another package
    * A drone should only appear in the assignment list at most once"
2. The coordinates of the depot are lat:-37.816664, long:144.9638476
    * This was taken from Google Maps' gps location

I acquired this distance with the help of geopy and its use of "Vicinity Distance" which takes into account earth's
 spherical shape [reference](https://geopy.readthedocs.io/en/1.10.0/#module-geopy.distance "Geopy Docs")
 
 
There were two important components to this algorithm. First is the latest possible time a package can leave and still be 
on time (`Package.latest_departure`) and the time it takes for a drone to get to the depot in order to deliver the package
(`Drone.available`). Both of these times are stored in Unix timestamp

drone's are stored in either 2 possible lists: `available_drones_list` or `busy_drones`. An available drone has no package
a busy drone has a package. 

the last bit of logic was if the next soonest drone can deliver it add the drone to the list of `busy_drones` and remove 
the package from the list. if the enxt soonest drone can't deliver it, the package is undeliverable


print the results

**RunTime O(d(Log(d)) + p(log(p)))** Where d = drones and p = packages



#### Why did you implement it this way?

Simply put python is my current favorite language for problem solving and the modules are great for any sort of math problem
such as calculating the distance between two coordinates. 

I chose to turn this into a scheduling problem because I feel that it is the most efficient way to handle this sort of problem
with the results nearest to perfect (at least from my experience). I know this algorithm works well for simpler problems where as if this 
problem was more realistic my solution might fall flat given all the factors affecting delivery. 
 
I chose not to use exhaustive schduling because the runtime isn't saleable at all if we took this coding challenge and
 made it into a real world siutation. 
 
#### Let's assume we need to handle dispatching thousands of jobs per second to thousands of drivers. Would the solution you've implemented still work? Why or why not? What would you modify? Feel free to describe a completely different solution than the one you've developed.

I don't think my solution would work. My solution also does not handle streaming data well and that would be important given
the example above. I think the best solution would be the use of Approximate Dynamic Programming (ADP) 

In this situation we have states (who is handling which package), as well as decisions to make (which route should 
a package go on, or which packages should go together) (even possibly adding a classic traveling salesmen algo, "which 
route should a driver take") and finally there is noise (traffic, when packages arrive, when packages must leave). ADP 
is a good way to handle complex systems like this were a lot of factors are affecting the decisions the algorithm needs to make

This algo design has been used in handling large scale fleet management

implementing this would be no easy task, however a complex problem sometimes requires a complex solution

I have never worked in a problem so complex, however I think given all the factors you might want to opt for a less 
optimal (not as correct) solution with a faster runtime. Treating this as streaming data. Though, At the end of the day 
if any trade offs were made the most important factor is how fast the system is compared to how correct it is. 






