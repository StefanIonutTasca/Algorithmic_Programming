"""
Test module for the ArrayList implementation.
"""

from src.datastructures.array_list import ArrayList

def test_array_list():
    """
    Test the basic functionality of the ArrayList.
    """
    # Create a new ArrayList
    array_list = ArrayList[int]()
    
    # Test append and length
    array_list.append(10)
    array_list.append(20)
    array_list.append(30)
    assert len(array_list) == 3
    
    # Test get/set via indexing
    assert array_list[0] == 10
    assert array_list[1] == 20
    assert array_list[2] == 30
    
    array_list[1] = 25
    assert array_list[1] == 25
    
    # Test contains
    assert 10 in array_list
    assert 15 not in array_list
    
    # Test insert
    array_list.insert(1, 15)
    assert len(array_list) == 4
    assert array_list[0] == 10
    assert array_list[1] == 15
    assert array_list[2] == 25
    assert array_list[3] == 30
    
    # Test remove
    assert array_list.remove(15) == True
    assert len(array_list) == 3
    assert array_list[0] == 10
    assert array_list[1] == 25
    assert array_list[2] == 30
    
    # Test remove_at
    removed = array_list.remove_at(1)
    assert removed == 25
    assert len(array_list) == 2
    assert array_list[0] == 10
    assert array_list[1] == 30
    
    # Test clear
    array_list.clear()
    assert len(array_list) == 0
    assert array_list.is_empty()
    
    print("All ArrayList tests passed!")

def demonstrate_array_list_with_car_parts():
    """
    Demonstrate using ArrayList with car parts.
    """
    # Create a list of car parts
    parts = ArrayList[str]()
    
    # Add some car parts
    parts.append("Engine")
    parts.append("Transmission")
    parts.append("Brakes")
    parts.append("Suspension")
    parts.append("Exhaust")
    
    print("Car Parts List:")
    for part in parts:
        print(f"- {part}")
    
    # Sort the parts
    parts.sort()
    
    print("\nSorted Car Parts List:")
    for part in parts:
        print(f"- {part}")
    
    # Find a part
    search_part = "Brakes"
    index = parts.index_of(search_part)
    if index != -1:
        print(f"\nFound '{search_part}' at index {index}")
    else:
        print(f"\n'{search_part}' not found")
    
    # Remove a part
    parts.remove("Exhaust")
    
    print("\nCar Parts List after removing 'Exhaust':")
    for part in parts:
        print(f"- {part}")


if __name__ == "__main__":
    test_array_list()
    print("\n" + "-" * 40 + "\n")
    demonstrate_array_list_with_car_parts()
