"""
Part model classes for the Automotive Parts Catalog System.
This module defines the data structures for representing automotive parts.
"""
from typing import List, Dict, Set, Optional
from src.datastructures.array_list import ArrayList


class Part:
    """
    Class representing an automotive part.
    """
    
    def __init__(self, part_id: int, name: str, category: str, price: float, description: str = ""):
        """
        Initialize a Part with the given attributes.
        
        Args:
            part_id: The unique ID of the part
            name: The name of the part
            category: The category of the part
            price: The price of the part
            description: A description of the part (optional)
        """
        self.part_id: int = part_id
        self.name: str = name
        self.category: str = category
        self.price: float = price
        self.description: str = description
        self.compatible_vehicles: Set[str] = set()  # Set of "make:model:year" strings
    
    def add_compatible_vehicle(self, make: str, model: str, year: int) -> None:
        """
        Add a compatible vehicle to this part.
        
        Args:
            make: The make of the compatible vehicle
            model: The model of the compatible vehicle
            year: The year of the compatible vehicle
        """
        vehicle_key = f"{make}:{model}:{year}"
        self.compatible_vehicles.add(vehicle_key)
    
    def is_compatible_with(self, make: str, model: str, year: int) -> bool:
        """
        Check if this part is compatible with the specified vehicle.
        
        Args:
            make: The make of the vehicle to check
            model: The model of the vehicle to check
            year: The year of the vehicle to check
            
        Returns:
            True if the part is compatible, False otherwise
        """
        vehicle_key = f"{make}:{model}:{year}"
        return vehicle_key in self.compatible_vehicles
    
    def get_compatible_vehicles(self) -> Set[str]:
        """
        Get all compatible vehicles for this part.
        
        Returns:
            A set of "make:model:year" strings representing compatible vehicles
        """
        return self.compatible_vehicles
    
    def __str__(self) -> str:
        """
        Return a string representation of the Part.
        
        Returns:
            A string representation of the Part
        """
        return f"{self.name} (ID: {self.part_id}, Category: {self.category}, Price: ${self.price:.2f})"
    
    def __eq__(self, other) -> bool:
        """
        Check if this Part is equal to another.
        
        Args:
            other: The other Part to compare to
            
        Returns:
            True if the Parts are equal, False otherwise
        """
        if not isinstance(other, Part):
            return False
        return self.part_id == other.part_id


class PartCategory:
    """
    Class representing a category of automotive parts.
    """
    
    def __init__(self, category_id: int, name: str, description: str = ""):
        """
        Initialize a PartCategory with the given attributes.
        
        Args:
            category_id: The unique ID of the category
            name: The name of the category
            description: A description of the category (optional)
        """
        self.category_id: int = category_id
        self.name: str = name
        self.description: str = description
        self.parts: Set[int] = set()  # Set of part_ids in this category
    
    def add_part(self, part_id: int) -> None:
        """
        Add a part to this category.
        
        Args:
            part_id: The ID of the part to add
        """
        self.parts.add(part_id)
    
    def get_parts(self) -> Set[int]:
        """
        Get all parts in this category.
        
        Returns:
            A set of part IDs in this category
        """
        return self.parts
    
    def __str__(self) -> str:
        """
        Return a string representation of the PartCategory.
        
        Returns:
            A string representation of the PartCategory
        """
        return f"{self.name} (ID: {self.category_id})"
    
    def __eq__(self, other) -> bool:
        """
        Check if this PartCategory is equal to another.
        
        Args:
            other: The other PartCategory to compare to
            
        Returns:
            True if the PartCategories are equal, False otherwise
        """
        if not isinstance(other, PartCategory):
            return False
        return self.category_id == other.category_id


class PartCatalog:
    """
    Class for managing a catalog of automotive parts.
    """
    
    def __init__(self):
        """
        Initialize an empty PartCatalog.
        """
        self.parts: Dict[int, Part] = {}  # {part_id: Part}
        self.categories: Dict[int, PartCategory] = {}  # {category_id: PartCategory}
        self.category_by_name: Dict[str, PartCategory] = {}  # {category_name: PartCategory}
    
    def add_part(self, part: Part) -> None:
        """
        Add a part to the catalog.
        
        Args:
            part: The Part to add
        """
        self.parts[part.part_id] = part
        
        # Add to category if it exists
        category = self.category_by_name.get(part.category)
        if category:
            category.add_part(part.part_id)
    
    def get_part(self, part_id: int) -> Optional[Part]:
        """
        Get a part by its ID.
        
        Args:
            part_id: The ID of the part to get
            
        Returns:
            The Part with the given ID, or None if not found
        """
        return self.parts.get(part_id)
    
    def get_parts(self) -> List[Part]:
        """
        Get all parts in the catalog.
        
        Returns:
            A list of all Part objects in the catalog
        """
        return list(self.parts.values())
    
    def get_parts_by_category(self, category_name: str) -> List[Part]:
        """
        Get all parts in the specified category.
        
        Args:
            category_name: The name of the category to get parts for
            
        Returns:
            A list of Part objects in the category
        """
        category = self.category_by_name.get(category_name)
        if not category:
            return []
        
        result = ArrayList[Part]()
        for part_id in category.get_parts():
            part = self.parts.get(part_id)
            if part:
                result.append(part)
        
        return result.to_list()
    
    def add_category(self, category: PartCategory) -> None:
        """
        Add a category to the catalog.
        
        Args:
            category: The PartCategory to add
        """
        self.categories[category.category_id] = category
        self.category_by_name[category.name] = category
    
    def get_category(self, category_id: int) -> Optional[PartCategory]:
        """
        Get a category by its ID.
        
        Args:
            category_id: The ID of the category to get
            
        Returns:
            The PartCategory with the given ID, or None if not found
        """
        return self.categories.get(category_id)
    
    def get_categories(self) -> List[PartCategory]:
        """
        Get all categories in the catalog.
        
        Returns:
            A list of all PartCategory objects in the catalog
        """
        return list(self.categories.values())
    
    def search_parts(self, query: str) -> ArrayList[Part]:
        """
        Search for parts by name or description.
        
        Args:
            query: The search query
            
        Returns:
            An ArrayList of Part objects matching the search query
        """
        query = query.lower()
        result = ArrayList[Part]()
        
        for part in self.parts.values():
            if (query in part.name.lower() or 
                query in part.description.lower() or
                query in part.category.lower()):
                result.append(part)
        
        return result
    
    def find_compatible_parts(self, make: str, model: str, year: int) -> ArrayList[Part]:
        """
        Find all parts compatible with the specified vehicle.
        
        Args:
            make: The make of the vehicle
            model: The model of the vehicle
            year: The year of the vehicle
            
        Returns:
            An ArrayList of Part objects compatible with the vehicle
        """
        result = ArrayList[Part]()
        
        for part in self.parts.values():
            if part.is_compatible_with(make, model, year):
                result.append(part)
        
        return result
