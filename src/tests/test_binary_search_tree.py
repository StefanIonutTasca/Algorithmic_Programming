"""
Test module for the BinarySearchTree implementation.
"""

from src.datastructures.binary_search_tree import BinarySearchTree

class Car:
    """
    A simple Car class for testing the BinarySearchTree with custom objects.
    """
    
    def __init__(self, make: str, model: str, year: int):
        """
        Initialize a Car with the given make, model, and year.
        
        Args:
            make: The make of the car
            model: The model of the car
            year: The year of the car
        """
        self.make = make
        self.model = model
        self.year = year
    
    def __str__(self) -> str:
        """
        Return a string representation of the Car.
        
        Returns:
            A string representation of the Car
        """
        return f"{self.year} {self.make} {self.model}"
    
    def __eq__(self, other):
        """
        Check if the Car is equal to another Car.
        
        Args:
            other: The other Car to compare to
            
        Returns:
            True if the Cars are equal, False otherwise
        """
        if not isinstance(other, Car):
            return False
        return (self.make == other.make and 
                self.model == other.model and 
                self.year == other.year)


def test_binary_search_tree():
    """
    Test the basic functionality of the BinarySearchTree.
    """
    # Create a new BinarySearchTree
    bst = BinarySearchTree[int]()
    
    # Test insert and size
    bst.insert(50)
    bst.insert(30)
    bst.insert(70)
    bst.insert(20)
    bst.insert(40)
    bst.insert(60)
    bst.insert(80)
    
    assert len(bst) == 7
    
    # Test contains
    assert 50 in bst
    assert 30 in bst
    assert 70 in bst
    assert 55 not in bst
    
    # Test search
    assert bst.search(50) == 50
    assert bst.search(30) == 30
    assert bst.search(70) == 70
    assert bst.search(55) is None
    
    # Test traversals
    assert bst.in_order_traversal() == [20, 30, 40, 50, 60, 70, 80]
    assert bst.pre_order_traversal() == [50, 30, 20, 40, 70, 60, 80]
    assert set(bst.post_order_traversal()) == set([20, 40, 30, 60, 80, 70, 50])
    assert set(bst.level_order_traversal()) == set([50, 30, 70, 20, 40, 60, 80])
    
    # Test remove
    assert bst.remove(20) == True
    assert 20 not in bst
    assert len(bst) == 6
    
    assert bst.remove(50) == True
    assert 50 not in bst
    assert len(bst) == 5
    
    assert bst.remove(100) == False
    assert len(bst) == 5
    
    # Test clear
    bst.clear()
    assert len(bst) == 0
    assert bst.is_empty()
    
    print("All BinarySearchTree tests passed!")

def demonstrate_binary_search_tree_with_cars():
    """
    Demonstrate using BinarySearchTree with Car objects.
    """
    # Create a BinarySearchTree that uses the car year as the key
    car_bst = BinarySearchTree[Car](key_function=lambda car: car.year)
    
    # Add some cars
    cars = [
        Car("Honda", "Civic", 2018),
        Car("Toyota", "Camry", 2015),
        Car("Ford", "F-150", 2020),
        Car("Chevrolet", "Malibu", 2012),
        Car("BMW", "X5", 2017),
        Car("Audi", "A4", 2019),
        Car("Mercedes-Benz", "C-Class", 2016)
    ]
    
    for car in cars:
        car_bst.insert(car)
    
    print("Cars in order by year:")
    for car in car_bst.in_order_traversal():
        print(f"- {car}")
    
    # Search for a car by year
    search_year = 2017
    found_car = car_bst.search(search_year)
    if found_car:
        print(f"\nFound car from {search_year}: {found_car}")
    else:
        print(f"\nNo car found from {search_year}")
    
    # Remove a car
    car_to_remove = Car("Toyota", "Camry", 2015)
    if car_bst.remove(2015):
        print(f"\nRemoved: {car_to_remove}")
    
    print("\nUpdated car list:")
    for car in car_bst.in_order_traversal():
        print(f"- {car}")


if __name__ == "__main__":
    test_binary_search_tree()
    print("\n" + "-" * 40 + "\n")
    demonstrate_binary_search_tree_with_cars()
