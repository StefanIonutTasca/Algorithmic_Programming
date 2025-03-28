"""
Vehicle model classes for the Automotive Parts Catalog System.
This module defines the data structures for representing vehicle hierarchies.
"""
from typing import List, Optional, Dict, Set
from src.datastructures.linked_list import LinkedList


class VehicleMake:
    """
    Class representing a vehicle manufacturer (make).
    """
    
    def __init__(self, make_id: int, name: str):
        """
        Initialize a VehicleMake with the given ID and name.
        
        Args:
            make_id: The unique ID of the vehicle make
            name: The name of the vehicle make
        """
        self.make_id: int = make_id
        self.name: str = name
        self.models: Dict[int, 'VehicleModel'] = {}  # {model_id: VehicleModel}
    
    def add_model(self, model: 'VehicleModel') -> None:
        """
        Add a model to this make.
        
        Args:
            model: The VehicleModel to add
        """
        self.models[model.model_id] = model
        model.make = self  # Set the backreference to this make
    
    def get_model(self, model_id: int) -> Optional['VehicleModel']:
        """
        Get a model by its ID.
        
        Args:
            model_id: The ID of the model to get
            
        Returns:
            The VehicleModel with the given ID, or None if not found
        """
        return self.models.get(model_id)
    
    def get_models(self) -> List['VehicleModel']:
        """
        Get all models for this make.
        
        Returns:
            A list of all VehicleModel objects for this make
        """
        return list(self.models.values())
    
    def __str__(self) -> str:
        """
        Return a string representation of the VehicleMake.
        
        Returns:
            A string representation of the VehicleMake
        """
        return self.name
    
    def __eq__(self, other) -> bool:
        """
        Check if this VehicleMake is equal to another.
        
        Args:
            other: The other VehicleMake to compare to
            
        Returns:
            True if the VehicleMakes are equal, False otherwise
        """
        if not isinstance(other, VehicleMake):
            return False
        return self.make_id == other.make_id


class VehicleModel:
    """
    Class representing a vehicle model.
    """
    
    def __init__(self, model_id: int, name: str):
        """
        Initialize a VehicleModel with the given ID and name.
        
        Args:
            model_id: The unique ID of the vehicle model
            name: The name of the vehicle model
        """
        self.model_id: int = model_id
        self.name: str = name
        self.make: Optional[VehicleMake] = None
        self.years: Dict[int, 'VehicleYear'] = {}  # {year: VehicleYear}
    
    def add_year(self, year: 'VehicleYear') -> None:
        """
        Add a year to this model.
        
        Args:
            year: The VehicleYear to add
        """
        self.years[year.year] = year
        year.model = self  # Set the backreference to this model
    
    def get_year(self, year: int) -> Optional['VehicleYear']:
        """
        Get a year by its value.
        
        Args:
            year: The year value to get
            
        Returns:
            The VehicleYear with the given value, or None if not found
        """
        return self.years.get(year)
    
    def get_years(self) -> List['VehicleYear']:
        """
        Get all years for this model.
        
        Returns:
            A list of all VehicleYear objects for this model
        """
        return list(self.years.values())
    
    def __str__(self) -> str:
        """
        Return a string representation of the VehicleModel.
        
        Returns:
            A string representation of the VehicleModel
        """
        return self.name
    
    def __eq__(self, other) -> bool:
        """
        Check if this VehicleModel is equal to another.
        
        Args:
            other: The other VehicleModel to compare to
            
        Returns:
            True if the VehicleModels are equal, False otherwise
        """
        if not isinstance(other, VehicleModel):
            return False
        return self.model_id == other.model_id


class VehicleYear:
    """
    Class representing a specific year for a vehicle model.
    """
    
    def __init__(self, year: int):
        """
        Initialize a VehicleYear with the given year value.
        
        Args:
            year: The year value
        """
        self.year: int = year
        self.model: Optional[VehicleModel] = None
        self.compatible_parts: Set[int] = set()  # Set of part_ids
    
    def add_compatible_part(self, part_id: int) -> None:
        """
        Add a compatible part to this vehicle year.
        
        Args:
            part_id: The ID of the compatible part
        """
        self.compatible_parts.add(part_id)
    
    def is_part_compatible(self, part_id: int) -> bool:
        """
        Check if a part is compatible with this vehicle year.
        
        Args:
            part_id: The ID of the part to check
            
        Returns:
            True if the part is compatible, False otherwise
        """
        return part_id in self.compatible_parts
    
    def get_compatible_parts(self) -> Set[int]:
        """
        Get all compatible parts for this vehicle year.
        
        Returns:
            A set of part IDs compatible with this vehicle year
        """
        return self.compatible_parts
    
    def __str__(self) -> str:
        """
        Return a string representation of the VehicleYear.
        
        Returns:
            A string representation of the VehicleYear
        """
        return str(self.year)
    
    def __eq__(self, other) -> bool:
        """
        Check if this VehicleYear is equal to another.
        
        Args:
            other: The other VehicleYear to compare to
            
        Returns:
            True if the VehicleYears are equal, False otherwise
        """
        if not isinstance(other, VehicleYear):
            return False
        return (self.year == other.year and 
                self.model == other.model)


class VehicleRegistry:
    """
    Class for managing a registry of vehicles by make, model, and year.
    """
    
    def __init__(self):
        """
        Initialize an empty VehicleRegistry.
        """
        self.makes: Dict[int, VehicleMake] = {}  # {make_id: VehicleMake}
        self.search_history: LinkedList[str] = LinkedList()
    
    def add_make(self, make: VehicleMake) -> None:
        """
        Add a make to the registry.
        
        Args:
            make: The VehicleMake to add
        """
        self.makes[make.make_id] = make
    
    def get_make(self, make_id: int) -> Optional[VehicleMake]:
        """
        Get a make by its ID.
        
        Args:
            make_id: The ID of the make to get
            
        Returns:
            The VehicleMake with the given ID, or None if not found
        """
        return self.makes.get(make_id)
    
    def get_makes(self) -> List[VehicleMake]:
        """
        Get all makes in the registry.
        
        Returns:
            A list of all VehicleMake objects in the registry
        """
        return list(self.makes.values())
    
    def add_search_to_history(self, search_query: str) -> None:
        """
        Add a search query to the search history.
        
        Args:
            search_query: The search query to add
        """
        self.search_history.prepend(search_query)
    
    def get_search_history(self) -> LinkedList[str]:
        """
        Get the search history.
        
        Returns:
            The search history as a LinkedList of strings
        """
        return self.search_history
