# Author: Matthew Mullins -- Student ID: 009750061

# Overall Time Complexity for main.py is O(n^2) where n is the number of packages.
# This is because the function to deliver the packages has a nested loop that iterates through all the packages.
# Overall Space Complexity is O(n) where n is the number of packages. This is because of the Hash Maps used here.
# They are both created with n key-value pairs.

import csv
from DeliveryTruck import Truck
from CreateHash import CreateHashMap
from Package import Package
import datetime

# Open the Package CSV File
with open('CSV_Files/Package.csv') as packageData:
    # Parse the CSV File
    packageReader = csv.reader(packageData, delimiter=',')
    # Creates a hash map using the CreateHashMap function.
    # Package Data will be stored in the hash map using the package ID as the key
    packageHash = CreateHashMap()
    # Iterate through each row in the CSV File
    # Time Complexity: O(n)
    # n = number of rows in the CSV File
    for row in packageReader:
        # Extract the data from each row
        pID = int(row[0])
        address = row[1]
        city = row[2]
        state = row[3]
        zipCode = row[4]
        deadline = row[5]
        weight = row[6]
        notes = row[7]
        status = 'At Hub'
        # Creates a Package object using the data extracted from the row.
        package = Package(pID, address, city, state, zipCode, deadline, weight, notes, status)
        # Insert the Package object into the hash map using the package ID as the key
        packageHash.insert(pID, package)

# Opens the Distance CSV File and saves the data to a list
with open('CSV_Files/Distance.CSV') as distanceFile:
    distanceData = list(csv.reader(distanceFile))

# Opens the Address CSV File and saves the data to a list
with open('CSV_Files/Address.csv') as addressDataFile:
    addressData = list(csv.reader(addressDataFile))


# Function to calculate the distance between two addresses
# Time complexity is O(1)
# Space complexity is O(1). This function doesn't store any extra data and the space used by the function is constant.
def distanceBetween(address1, address2):
    distanceBetween = distanceData[address1][address2]
    # If the distance is blank, the address input is reversed
    # This is because in the Distance CSV file, the distance between address 1 and address 2 is the same as the distance
    # between address 2 and address 1
    if distanceBetween == '':
        distanceBetween = distanceData[address2][address1]
    # Converts the distance to a float
    return float(distanceBetween)


# Function to get the address ID from the address data.
# Time complexity is O(n) where n = the number of elements in addressData
# Space Complexity is O(1).
def getAddress(address):
    # Iterate through each row in the address data
    for row in addressData:
        # If the address is found, return the address ID
        if address in row[2]:
            return int(row[0])


# Creates an empty dictionary to hold packages and their delivery times
packageDeliveryTimes = {}


# Function to deliver the packages. This is the main algorithm for the program.
# This algorithm is a variation of the nearest neighbor algorithm.
# The Time Complexity of this function is O(n^2) where n is the number of packages.
# The for loop within the while loop is O(n) and the while loop is O(n) making the total time complexity O(n^2)
# The Space Complexity for this function is O(n) where n is the number of packages.
# This is due to the list and dictionary used. Each have n elements.
def deliverPackages(truck, departureTime):

    # Initialize the list of packages on the truck that have not been delivered
    notDelivered = []
    for packageID in truck.packages:
        package = packageHash.lookup(packageID)
        notDelivered.append(package)

    # Set the truck's current location as the delivery hub
    currentLocation = "4001 South 700 East"

    # Initialize a dictionary to store the delivery time of each package
    deliveryTimes = {}

    # Repeat the following process until all packages have been delivered
    while len(notDelivered) > 0:

        # Find the package with the shortest distance to the current location
        nextAddress = 1000
        nextPackage = None
        for package in notDelivered:
            distance = distanceBetween(getAddress(currentLocation), getAddress(package.address))
            if distance <= nextAddress:
                nextAddress = distance
                nextPackage = package

        # Remove the package from the list of packages that have not yet been delivered
        notDelivered.remove(nextPackage)

        # Update the truck's total mileage and current location
        truck.totalMileage += nextAddress
        currentLocation = nextPackage.address

        # Calculate the delivery time of the package based on the distance traveled and the truck's departure time
        deliveryTime = datetime.datetime.combine(datetime.date.today(), departureTime) + datetime.timedelta(
            hours=(truck.totalMileage / 18))
        deliveryTime = deliveryTime.time()
        deliveryTimes[nextPackage.package_id] = deliveryTime
        # Adds the package and delivery time to packageDeliveryTimes
        packageDeliveryTimes[nextPackage.package_id] = deliveryTime

    # Calculate the distance back to the hub
    hubDistance = distanceBetween(getAddress(currentLocation), 0)
    truck.totalMileage += hubDistance

    # Calculate the return time to the hub
    returnTime = datetime.datetime.combine(datetime.date.today(), departureTime) + datetime.timedelta(
        hours=(truck.totalMileage / 18))
    returnTime = returnTime.time()
    print("Truck", truck.truckID, "returned to the hub at", returnTime)


# Creates the Trucks and manually loads the packages into the trucks
deliveryTruck1 = Truck(1, 16, 18, None, [1, 13, 14, 15, 16, 19, 20, 21, 29, 30, 31, 34, 37, 40], 0.0,
                       "4001 South 700 East")
deliveryTruck2 = Truck(2, 16, 18, None, [2, 3, 4, 5, 6, 7, 10, 17, 18, 25, 28, 32, 36, 38], 0.0,
                       "4001 South 700 East")
# Sets the departure time for the trucks. Truck 1 will depart at 8:00 AM and Truck 2 will depart at 9:05 AM
# Truck 2 is delayed due to some packages being delayed
departureTimeTruck1 = datetime.time(8, 0, 0)
departureTimeTruck2 = datetime.time(9, 5, 0)

# Delivers the packages for Truck 1 and Truck 2
# This is done first so that a return time for Truck 1 can be determined and the departure time for
# Truck 3 can be set manually in code
print("----------------------------------------")
print("Truck 1 left the hub at", departureTimeTruck1)
print("Truck 1 delivered the following packages: " + str(deliveryTruck1.packages))
deliverPackages(deliveryTruck1, departureTimeTruck1)
print("----------------------------------------")
print("Truck 2 left the hub at", departureTimeTruck2)
print("Truck 2 delivered the following packages: " + str(deliveryTruck2.packages))
deliverPackages(deliveryTruck2, departureTimeTruck2)
print("----------------------------------------")

# The departure time for Truck 3 is set to 10:20 AM when the address for Package: 9 is known.
# Truck 1 returns to the hub from their trip at 9:57 AM. The driver from Truck 1 would be available to deliver
# the packages on Truck 3.
deliveryTruck3 = Truck(3, 16, 18, None, [8, 9, 11, 12, 22, 23, 24, 26, 27, 33, 35, 39], 0.0,
                       "4001 South 700 East")
departureTimeTruck3 = datetime.time(10, 20, 0)
print("Truck 3 left the hub at", departureTimeTruck3)
print("Truck 3 delivered the following packages: " + str(deliveryTruck3.packages))
deliverPackages(deliveryTruck3, departureTimeTruck3)
print("----------------------------------------")
print("\033[92m" "All {} Packages Delivered On Time and According To Their Specifications!!!""\033[0m"
      .format(len(packageDeliveryTimes)))
print("-----------------------------------------")


# Function that takes the packageID as input and returns the truck ID of the truck the package was on
# Time complexity is O(n) where n is the number of trucks.
# Space Complexity is O(1)
def packageTruckNumber(packageID):
    for truck in [deliveryTruck1, deliveryTruck2, deliveryTruck3]:
        if packageID in truck.packages:
            return truck.truckID


# Function that takes in a truck ID and returns the departure time for that truck
# Time complexity O(1). This function doesn't loop or search and will always execute in the same amount of time.
# Space Complexity O(1)
def truckDepartureTime(truckNumber):
    if truckNumber == 1:
        return departureTimeTruck1
    elif truckNumber == 2:
        return departureTimeTruck2
    elif truckNumber == 3:
        return departureTimeTruck3
    else:
        return "Not found"


# Function to return the status of a package at a certain time.
# Time complexity is O(n) where n is the number of trucks. This is due to the packageTruckNumber function.
# Space Complexity is O(1)
def packageStatusAtTime(packageID, time):
    if packageID in packageDeliveryTimes:
        if time < packageDeliveryTimes[packageID] and time < truckDepartureTime(packageTruckNumber(packageID)):
            return "At Hub"
        elif packageDeliveryTimes[packageID] > time > truckDepartureTime(packageTruckNumber(packageID)):
            return "En Route"
        else:
            return "Delivered"
    else:
        return "Not found"


# User Interface - asks the user what they would like to do. Takes user input and displays appropriate information.
# Returns the user to the top menu after displaying requested information.
# Time complexity is O(n^2) if the user chooses option 3. This is because the packageStatusAtTime function is called
# which has a time complexity of O(n). It is called for each package in the packageDeliveryTimes dictionary resulting
# in n calls. n*n = O(n^2)
# Space complexity for the user interface is O(1). This is because the function doesn't use any data structures
# that grow with the size of the input.
def userInterface():
    # Prints available options for the user.
    print("What would you like to do?")
    print("1 -Lookup package information-")
    print("2 -See the status of a package at a specific time-")
    print("3 -See the status of all packages at a specific time-")
    print("4 -See when all packages were delivered-")
    print("5 -See the mileage of the trucks-")
    print("6 -Exit-")
    # Takes the user input and assigns it to a variable.
    userChoice = input("Enter the number of your choice: ")
    # If the user selects option 1, package ID is entered and information for the package is displayed.
    if userChoice == "1":
        packageID = int(input("Enter the package ID: "))
        package = packageHash.lookup(packageID)
        print("----------------------------------------")
        print("Package ID: {}".format(package.package_id))
        print("Address: {}".format(package.address))
        print("City: {}".format(package.city))
        print("Zip Code: {}".format(package.zipcode))
        print("Deadline: {}".format(package.delivery_deadline))
        print("Weight: {}".format(package.weight))
        print("Status: Package delivered at {}".format(packageDeliveryTimes[packageID]))
        print("----------------------------------------")
        userInterface()
    # If the user selects option 2, a package ID and time are entered and the package status at that time is displayed.
    # Error handling for wrong time format.
    elif userChoice == "2":
        packageID = int(input("Enter the package ID: "))
        time = input("Enter the time (HH:MM:SS): ")
        try:
            time = datetime.datetime.strptime(time, "%H:%M:%S").time()
        except ValueError:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("Invalid time format. Please enter time as HH:MM:SS")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            userInterface()
        print("----------------------------------------")
        print("Package ""\033[95m""{} ""\033[0m""has a status of ""\033[94m" "{} "
              "\033[0m" "at {}. It was loaded onto Truck {}."
              .format(packageID, packageStatusAtTime(packageID, time),
                      time, packageTruckNumber(packageID)))
        print("----------------------------------------")
        userInterface()
    # If the user selects option 3, a time is entered and the status for all packages for that time is displayed.
    # Error handling for wrong time format.
    elif userChoice == "3":
        time = input("Enter the time (HH:MM:SS): ")
        try:
            time = datetime.datetime.strptime(time, "%H:%M:%S").time()
        except ValueError:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("Invalid time format. Please enter time as HH:MM:SS")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            userInterface()
        print("----------------------------------------")
        for package in packageDeliveryTimes:
            packageID = packageHash.lookup(package)
            print("Package ""\033[95m" "{} ""\033[0m""has a status of ""\033[94m" "{} "
                  "\033[0m" "at {}.  It was loaded onto Truck {} and delivered at {}"
                  .format(package, packageStatusAtTime(package, time), time, packageTruckNumber(packageID.package_id),
                          packageDeliveryTimes[package]))
        print("----------------------------------------")
        userInterface()
    # If option 4 is selected, displays the time when each package was delivered.
    elif userChoice == "4":
        print("----------------------------------------")
        for package in packageDeliveryTimes:
            packageID = packageHash.lookup(package)
            packageAddress = packageHash.lookup(package)
            print("Package ""\033[95m" "{} ""\033[0m""was delivered at ""\033[94m" "{} ""\033[0m""to ""\033[92m""{}"
                  "\033[0m"" by Truck {}".format(package, packageDeliveryTimes[package], packageAddress.address,
                                                 packageTruckNumber(packageID.package_id)))
        print("----------------------------------------")
        userInterface()
    # If option 5 is selected, displays mileage for each truck and the total mileage to deliver all packages and
    # return to the hub.
    elif userChoice == "5":
        print("----------------------------------------")
        print("Truck 1 Mileage: {}".format(deliveryTruck1.totalMileage))
        print("Truck 2 Mileage: {}".format(deliveryTruck2.totalMileage))
        print("Truck 3 Mileage: {}".format(deliveryTruck3.totalMileage))
        print("\033[92m",
              "Total Mileage: {}""\033[0m".format(deliveryTruck1.totalMileage + deliveryTruck2.totalMileage +
                                                  deliveryTruck3.totalMileage))
        print("----------------------------------------")
        userInterface()
    # If option 6 is selected, the program exits.
    elif userChoice == "6":
        exit()


userInterface()
