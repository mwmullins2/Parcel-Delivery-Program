class Truck:
    # Constructor for Truck class
    # Takes maximum_capacity, average_speed, current_load, packages, total_mileage, currentAddress, and depart_time as
    # arguments and assigns them as attributes to the instance of the Truck class being created
    def __init__(self, truckID, maxCapacity, averageSpeed, currentLoad, packages, totalMileage, currentAddress):
        self.truckID = truckID
        self.maxCapacity = maxCapacity
        self.averageSpeed = averageSpeed
        self.currentLoad = currentLoad
        self.packages = packages
        self.totalMileage = totalMileage
        self.currentAddress = currentAddress

    # Returns a string representation of the Truck instance, with its attributes in a specified order
    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s" % (self.truckID, self.maxCapacity, self.averageSpeed, self.currentLoad,
                                               self.packages, self.totalMileage, self.currentAddress)
