"""
Test module for the LinkedList implementation.
"""

from src.datastructures.linked_list import LinkedList

def test_linked_list():
    """
    Test the basic functionality of the LinkedList.
    """
    # Create a new LinkedList
    linked_list = LinkedList[int]()
    
    # Test append and length
    linked_list.append(10)
    linked_list.append(20)
    linked_list.append(30)
    assert len(linked_list) == 3
    
    # Test get/set via indexing
    assert linked_list[0] == 10
    assert linked_list[1] == 20
    assert linked_list[2] == 30
    
    linked_list[1] = 25
    assert linked_list[1] == 25
    
    # Test contains
    assert 10 in linked_list
    assert 15 not in linked_list
    
    # Test insert
    linked_list.insert(1, 15)
    assert len(linked_list) == 4
    assert linked_list[0] == 10
    assert linked_list[1] == 15
    assert linked_list[2] == 25
    assert linked_list[3] == 30
    
    # Test prepend
    linked_list.prepend(5)
    assert len(linked_list) == 5
    assert linked_list[0] == 5
    
    # Test remove
    assert linked_list.remove(15) == True
    assert len(linked_list) == 4
    assert linked_list[0] == 5
    assert linked_list[1] == 10
    assert linked_list[2] == 25
    assert linked_list[3] == 30
    
    # Test remove_at
    removed = linked_list.remove_at(1)
    assert removed == 10
    assert len(linked_list) == 3
    assert linked_list[0] == 5
    assert linked_list[1] == 25
    assert linked_list[2] == 30
    
    # Test to_list and from_list
    list_data = linked_list.to_list()
    assert list_data == [5, 25, 30]
    
    new_linked_list = LinkedList[int]()
    new_linked_list.from_list([100, 200, 300])
    assert len(new_linked_list) == 3
    assert new_linked_list[0] == 100
    assert new_linked_list[1] == 200
    assert new_linked_list[2] == 300
    
    # Test clear
    linked_list.clear()
    assert len(linked_list) == 0
    assert linked_list.is_empty()
    
    print("All LinkedList tests passed!")

def demonstrate_linked_list_with_search_history():
    """
    Demonstrate using LinkedList as a search history.
    """
    # Create a search history using LinkedList
    search_history = LinkedList[str]()
    
    # Add some search queries
    search_history.append("Honda Civic brake pads")
    search_history.append("Toyota Camry air filter")
    search_history.append("Ford F-150 oil filter")
    search_history.append("Chevrolet Malibu spark plugs")
    
    print("Search History:")
    for i, query in enumerate(search_history):
        print(f"{i+1}. {query}")
    
    # Add a new search query to the beginning (most recent)
    search_history.prepend("BMW X5 windshield wipers")
    
    print("\nUpdated Search History (new search added to top):")
    for i, query in enumerate(search_history):
        print(f"{i+1}. {query}")
    
    # Remove an item from history
    search_history.remove("Toyota Camry air filter")
    
    print("\nSearch History after removing 'Toyota Camry air filter':")
    for i, query in enumerate(search_history):
        print(f"{i+1}. {query}")


if __name__ == "__main__":
    test_linked_list()
    print("\n" + "-" * 40 + "\n")
    demonstrate_linked_list_with_search_history()
