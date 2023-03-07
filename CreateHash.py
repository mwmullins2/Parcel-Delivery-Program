# Class that creates a hashmap and allows for the insertion, deletion, and retrieval of data
# Time Complexity for this class overall is O(n) due to the need to resize and rehash the elements
# Space complexity for this class overall is O(n) where n is the capacity of the hash map.
class CreateHashMap:
    # Constructor for CreateHashMap class
    # Takes no arguments and initializes the size of the hashmap to 20
    # Load Factor is the threshold for the hashmap to be resized when the number of items in the hashmap
    # reaches 75% of the capacity of the hashmap
    # Time Complexity: O(n) where n is the capacity of the hashmap
    def __init__(self, initialCapacity=20):
        self.list = [[] for i in range(initialCapacity)]
        self.num_items = 0
        self.load_factor = 0.75  # threshold for resizing

    # Inserts a key and value into the hashmap
    # Time Complexity: O(n) if the hashmap needs to be resized
    # In practice this should be a Time Complexity of O(1) in most circumstances.
    # Space Complexity: O(1)
    def insert(self, key, item):
        bucket = hash(key) % len(self.list)
        bucketList = self.list[bucket]
        # For loop to check if the key already exists in the hashmap
        for keyValue in bucketList:
            if keyValue[0] == key:
                keyValue[1] = item
                return True
        # If the key does not exist in the hashmap, the key and value are appended to the bucket list
        bucketList.append([key, item])
        self.num_items += 1
        # Checks if resizing is necessary
        self.hashResize()
        return True

    # Looks up a key in the hashmap and returns the value associated with the key
    # Time Complexity: O(n) if all the elements are in the same bucket
    # In practice this should be a Time Complexity of O(1) in most circumstances.
    # Space Complexity is O(1)
    def lookup(self, key):
        bucket = hash(key) % len(self.list)
        bucketList = self.list[bucket]
        # For loop to check if the key exists in the hashmap
        for pair in bucketList:
            if key == pair[0]:
                return pair[1]
        return None

    # Removes a key and value from the hashmap
    # Time Complexity: O(n) if all the elements are in the same bucket
    # In practice this should be a Time Complexity of O(1) in most circumstances.
    # Space Complexity is O(1)
    def delete(self, key):
        slot = hash(key) % len(self.list)
        destination = self.list[slot]
        # For loop to check if the key exists and removes the key and value from the hashmap
        if key in destination:
            destination.remove(key)
            self.num_items -= 1
            # Checks if resizing is necessary
            self.hashResize()

    # Checks if the hashmap needs to be resized
    # If the number of items in the hashmap reaches the threshold, the hashmap is resized
    # Time Complexity: O(n) if the hashmap needs to be resized. n is the number of elements in the hashmap
    # Space Complexity of O(n) where n is the number of items in the hashmap.
    def hashResize(self):
        if self.num_items / len(self.list) > self.load_factor:
            # Resizes the hashmap and rehashes the keys
            oldList = self.list
            # New capacity will be 2x the current capacity.
            newCapacity = 2 * len(self.list)
            self.list = [[] for i in range(newCapacity)]
            self.num_items = 0
            for bucket in oldList:
                for key, value in bucket:
                    self.insert(key, value)
