"""
Vehicle model classes for the Automotive Parts Catalog System.
These classes define the hierarchical structure of vehicle make, model, and year.
"""
from typing import List, Optional, Dict, Any

class CarMake:
    """
    Class representing a car manufacturer (make).
    
    This class stores information about a car manufacturer and its associated models.
    """
    
    def __init__(self, make_id: str, name: str, country: str = ""):
        """
        Initialize a CarMake object.
        
        Args:
            make_id: Unique identifier for the make
            name: Name of the car manufacturer
            country: Country of origin for the manufacturer
        """
        self._make_id = make_id
        self._name = name
        self._country = country
        self._models: List[CarModel] = []
        
    def get_id(self) -> str:
        """Get the make ID."""
        return self._make_id
    
    def get_name(self) -> str:
        """Get the make name."""
        return self._name
    
    def get_country(self) -> str:
        """Get the country of origin."""
        return self._country
    
    def get_models(self) -> List['CarModel']:
        """Get the list of car models for this make."""
        return self._models
    
    def add_model(self, model: 'CarModel') -> None:
        """Add a car model to this make."""
        self._models.append(model)
        
    def find_model_by_id(self, model_id: str) -> Optional['CarModel']:
        """Find a model by its ID."""
        for model in self._models:
            if model.get_id() == model_id:
                return model
        return None
    
    def __str__(self) -> str:
        """String representation of the car make."""
        return f"{self._name} ({self._country})"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "make_id": self._make_id,
            "name": self._name,
            "country": self._country,
            "models": [model.to_dict() for model in self._models]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CarMake':
        """Create a CarMake object from a dictionary."""
        make = cls(data["make_id"], data["name"], data.get("country", ""))
        
        for model_data in data.get("models", []):
            model = CarModel.from_dict(model_data)
            make.add_model(model)
            
        return make


class CarModel:
    """
    Class representing a specific car model.
    
    This class stores information about a car model and its available years.
    """
    
    def __init__(self, model_id: str, name: str, make_id: str, body_style: str = ""):
        """
        Initialize a CarModel object.
        
        Args:
            model_id: Unique identifier for the model
            name: Name of the car model
            make_id: ID of the car make this model belongs to
            body_style: Body style of the model (sedan, SUV, etc.)
        """
        self._model_id = model_id
        self._name = name
        self._make_id = make_id
        self._body_style = body_style
        self._years: List[ModelYear] = []
        
    def get_id(self) -> str:
        """Get the model ID."""
        return self._model_id
    
    def get_name(self) -> str:
        """Get the model name."""
        return self._name
    
    def get_make_id(self) -> str:
        """Get the associated make ID."""
        return self._make_id
    
    def get_body_style(self) -> str:
        """Get the body style."""
        return self._body_style
    
    def get_years(self) -> List['ModelYear']:
        """Get the list of available years for this model."""
        return self._years
    
    def add_year(self, year: 'ModelYear') -> None:
        """Add a year to this model."""
        self._years.append(year)
        
    def find_year_by_value(self, year_value: int) -> Optional['ModelYear']:
        """Find a year by its value."""
        for year in self._years:
            if year.get_year() == year_value:
                return year
        return None
    
    def __str__(self) -> str:
        """String representation of the car model."""
        return f"{self._name} ({self._body_style})"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "model_id": self._model_id,
            "name": self._name,
            "make_id": self._make_id,
            "body_style": self._body_style,
            "years": [year.to_dict() for year in self._years]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CarModel':
        """Create a CarModel object from a dictionary."""
        model = cls(
            data["model_id"],
            data["name"],
            data["make_id"],
            data.get("body_style", "")
        )
        
        for year_data in data.get("years", []):
            year = ModelYear.from_dict(year_data)
            model.add_year(year)
            
        return model


class ModelYear:
    """
    Class representing a specific year of a car model.
    
    This class stores information about a specific year of a car model.
    """
    
    def __init__(self, year: int, model_id: str, features: List[str] = None):
        """
        Initialize a ModelYear object.
        
        Args:
            year: The year value
            model_id: ID of the car model this year belongs to
            features: List of features for this model year
        """
        self._year = year
        self._model_id = model_id
        self._features = features or []
        
    def get_year(self) -> int:
        """Get the year value."""
        return self._year
    
    def get_model_id(self) -> str:
        """Get the associated model ID."""
        return self._model_id
    
    def get_features(self) -> List[str]:
        """Get the list of features."""
        return self._features
    
    def add_feature(self, feature: str) -> None:
        """Add a feature to this model year."""
        self._features.append(feature)
        
    def __str__(self) -> str:
        """String representation of the model year."""
        return str(self._year)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "year": self._year,
            "model_id": self._model_id,
            "features": self._features
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ModelYear':
        """Create a ModelYear object from a dictionary."""
        return cls(
            data["year"],
            data["model_id"],
            data.get("features", [])
        )
