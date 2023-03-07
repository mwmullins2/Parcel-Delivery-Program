# Parcel Service Routing Program
This program was developed to help a parcel service (WGUPS) determine an efficient route and delivery distribution for their Daily Local Deliveries (DLD) in Salt Lake City, Utah. The goal was to deliver all packages on time while meeting each package’s specific criteria and keeping the combined total distance traveled under 140 miles for both trucks.

## Overview
The program uses a self-adjusting algorithm known as the "Nearest Neighbor Algorithm" to create a delivery route that minimizes the total distance traveled by the trucks. The algorithm works by selecting the closest package to the current location of the truck and delivering it, then selecting the next closest package and repeating the process until all packages are delivered.

The program was written in Python 3 using the PyCharm IDE. It uses a self-adjusting hash table to store and manage package data.

## Complexity Analysis
The time complexity of the program is O(n^2), where n is the number of packages, because the algorithm needs to calculate the distances between each pair of delivery locations. The space complexity is O(n) because the program needs to store the package data in memory.

