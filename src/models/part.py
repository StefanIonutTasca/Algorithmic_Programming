"""
Part model class for the Automotive Parts Catalog System.
This class defines the structure of automotive parts in the catalog.
"""
from typing import List, Dict, Any, Set


class Part:
    """
    Class representing an automotive part.
    
    This class stores information about an automotive part including its
    specifications and compatibility information.
    """
    
    def __init__(self, part_id: str, name: str, category: str, price: float, 
                 manufacturer: str = "", description: str = ""):
        """
        Initialize a Part object.
        
        Args:
            part_id: Unique identifier for the part
            name: Name of the part
            category: Category of the part (e.g., "Engine", "Brakes", "Electrical")
            price: Price of the part
            manufacturer: Manufacturer of the part
            description: Description of the part
        """
        self._part_id = part_id
        self._name = name
        self._category = category
        self._price = price
        self._manufacturer = manufacturer
        self._description = description
        self._specifications: Dict[str, Any] = {}
        self._compatible_vehicles: Set[str] = set()  # Set of "make_id:model_id:year" strings
        
    def get_id(self) -> str:
        """Get the part ID."""
        return self._part_id
    
    def get_name(self) -> str:
        """Get the part name."""
        return self._name
    
    def get_category(self) -> str:
        """Get the part category."""
        return self._category
    
    def get_price(self) -> float:
        """Get the part price."""
        return self._price
    
    def get_manufacturer(self) -> str:
        """Get the part manufacturer."""
        return self._manufacturer
    
    def get_description(self) -> str:
        """Get the part description."""
        return self._description
    
    def set_price(self, price: float) -> None:
        """
        Set the part price.
        
        Args:
            price: The new price
        """
        self._price = price
    
    def set_description(self, description: str) -> None:
        """
        Set the part description.
        
        Args:
            description: The new description
        """
        self._description = description
    
    def get_specifications(self) -> Dict[str, Any]:
        """Get the part specifications."""
        return self._specifications
    
    def add_specification(self, key: str, value: Any) -> None:
        """
        Add a specification to the part.
        
        Args:
            key: The specification name
            value: The specification value
        """
        self._specifications[key] = value
    
    def get_compatible_vehicles(self) -> Set[str]:
        """Get the set of compatible vehicle identifiers."""
        return self._compatible_vehicles
    
    def add_compatible_vehicle(self, make_id: str, model_id: str, year: int) -> None:
        """
        Add a compatible vehicle to the part.
        
        Args:
            make_id: The make ID
            model_id: The model ID
            year: The model year
        """
        vehicle_key = f"{make_id}:{model_id}:{year}"
        self._compatible_vehicles.add(vehicle_key)
    
    def is_compatible_with(self, make_id: str, model_id: str, year: int) -> bool:
        """
        Check if the part is compatible with the specified vehicle.
        
        Args:
            make_id: The make ID
            model_id: The model ID
            year: The model year
            
        Returns:
            True if the part is compatible, False otherwise
        """
        vehicle_key = f"{make_id}:{model_id}:{year}"
        return vehicle_key in self._compatible_vehicles
    
    def __str__(self) -> str:
        """String representation of the part."""
        return f"{self._name} ({self._category}) - ${self._price:.2f}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "part_id": self._part_id,
            "name": self._name,
            "category": self._category,
            "price": self._price,
            "manufacturer": self._manufacturer,
            "description": self._description,
            "specifications": self._specifications,
            "compatible_vehicles": list(self._compatible_vehicles)
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Part':
        """Create a Part object from a dictionary."""
        part = cls(
            data["part_id"],
            data["name"],
            data["category"],
            data["price"],
            data.get("manufacturer", ""),
            data.get("description", "")
        )
        
        # Add specifications
        for key, value in data.get("specifications", {}).items():
            part.add_specification(key, value)
        
        # Add compatible vehicles
        for vehicle_key in data.get("compatible_vehicles", []):
            part._compatible_vehicles.add(vehicle_key)
            
        return part
