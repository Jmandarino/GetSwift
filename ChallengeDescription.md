# GetSwift Code Test
This code test is divided into two parts, a code writing portion, and an analysis portion, where you'll discuss your implementation and how it can be extended.

## The scenario
You run a drone delivery company. Packages arrive at your depo to be delivered by your fleet of drones.

## The problem
Your solution should take two inputs: a list of drones, and a list of packages; and produce two outputs: a list of assignments of packages to drones, and a list of packages that could not be assigned. For example, you could produce the following output:

```javascript
{
  assignments: [{droneId: 1593, packageId: 1029438}, {droneId: 1251, packageId: 1029439}]
  unassignedPackageIds: [109533, 109350, 109353]
}
```

### Constraints
There's a number of constraints that your solution must obey:

- The depo is located at 303 Collins Street, Melbourne, VIC 3000
- Drones might already be carrying a package. The time to deliver this package should be taken into account when comparing drones.
- Once a drone is assigned a package, it will fly in a straight line to its current destination (if it already has a package), then to the depo, then to the new destination
- Packages must only be assigned to a drone that can complete the delivery by the package's delivery deadline
- Packages should be assigned to the drone that can deliver it soonest
- A drone should only appear in the assignment list at most once; this is a dispatching problem, not a routing problem. For example, this is allowed:
```javascript
{
  assignments: [{droneId: 1593, packageId: 1029438}, {droneId: 1251, packageId: 1029439}]
  unassignedPackageIds: [109533, 109350, 109353]
}
```
but this is not allowed:
```javascript
{
  assignments: [{droneId: 1593, packageId: 1029438}, {droneId: 1593, packageId: 1029439}]
  unassignedPackageIds: [109533, 109350, 109353]
}
```

### Assumptions
You can make the following simplifying assumptions:

- Drones have unlimited range
- Drones travel at a fixed speed of 50km/h
- Packages are all the same weight and volume
- Packages can be delivered early
- Drones can only carry one item at a time

You should integrate with [this API](https://codetest.kube.getswift.co/drones) which generates randomized data.

You can use any language and/or framework to solve this. Please also give an indication of how you envisage your solution will be deployed, and what other components it might interact with.

## The API
The API lives at https://codetest.kube.getswift.co/drones. You'll need to use two methods:

### `GET /drones`
This returns a randomized list of drones. A drone can have up to one package assigned to it.

```javascript
[
    {
        "droneId": 321361,
        "location": {
            "latitude": -37.78290448241537,
            "longitude": 144.85335277520906
        },
        "packages": [
            {
                "destination": {
                    "latitude": -37.78389758422243,
                    "longitude": 144.8574574322506
                },
                "packageId": 7645,
                "deadline": 1500422916
            }
        ]
    },
    {
        "droneId": 493959,
        "location": {
            "latitude": -37.77718638788778,
            "longitude": 144.8603578487479
        },
        "packages": []
    }
]
```

### `GET /packages`
This returns a randomized list of packages. You will need to assign the packages from this endpoint to the drones returned from the other endpoint. The deadline here is a Unix timestamp.

```javascript
[
    {
        "destination": {
            "latitude": -37.78404125474984,
            "longitude": 144.85238118232522
        },
        "packageId": 8041,
        "deadline": 1500425202
    },
    {
        "destination": {
            "latitude": -37.77058198385452,
            "longitude": 144.85157121265505
        },
        "packageId": 8218,
        "deadline": 1500423287
    }
]
```

## Analysis
After you've implemented your solution, try answering the following questions. We're not really looking for a particular answer; we're more interested in how well you understand your choices, and how well you can justify them.

- How did you implement your solution?
- Why did you implement it this way?
- Let's assume we need to handle dispatching thousands of jobs per second to thousands of drivers. Would the solution you've implemented still work? Why or why not? What would you modify? Feel free to describe a completely different solution than the one you've developed.

### Assessment
As a rough guide, we look at the following points to assess an analysis:

1. Are there any logical errors?
2. Are there any outright factual errors?
3. Are important tradeoffs identified and analysed? Is the effort put into each tradeoff proportionate to its severity, or is a lot of time spent on analysing a trivial problem, while more pressing concerns are left untouched?
4. What doesn't the analysis cover? How is the scope of the solution framed? Do we get a get sense of where the solution is situated in the solution space, and where we can we move to?

## Submission
Please create a *new repository* (don't fork this one) and then email us the url.
