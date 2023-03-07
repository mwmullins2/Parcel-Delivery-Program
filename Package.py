class Package:
    # Constructor for Package class
    # Takes package_id, address, city, state, zipcode, delivery_deadline, weight, and delivery_status as arguments
    # and assigns them as attributes to the instance of the Package class being created
    def __init__(self, package_id, address, city, state, zipcode, delivery_deadline, weight, notes,  delivery_status):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.delivery_deadline = delivery_deadline
        self.weight = weight
        self.notes = notes
        self.delivery_status = delivery_status

    # Returns a string representation of the Package instance, with its attributes in a specified order
    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.package_id, self.address, self.city, self.state,
                                                       self.zipcode, self.delivery_deadline, self.weight, self.notes,
                                                       self.delivery_status)
