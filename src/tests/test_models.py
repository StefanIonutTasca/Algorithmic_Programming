"""
Test module for the vehicle and part model classes.
"""

from src.models.vehicle import VehicleMake, VehicleModel, VehicleYear, VehicleRegistry
from src.models.part import Part, PartCategory, PartCatalog
from src.datastructures.array_list import ArrayList

def test_vehicle_hierarchy():
    """
    Test the vehicle hierarchy classes.
    """
    # Create a vehicle make
    honda = VehicleMake(1, "Honda")
    
    # Create vehicle models
    civic = VehicleModel(101, "Civic")
    accord = VehicleModel(102, "Accord")
    crv = VehicleModel(103, "CR-V")
    
    # Add models to make
    honda.add_model(civic)
    honda.add_model(accord)
    honda.add_model(crv)
    
    # Create years for models
    civic_2018 = VehicleYear(2018)
    civic_2019 = VehicleYear(2019)
    civic_2020 = VehicleYear(2020)
    
    accord_2018 = VehicleYear(2018)
    accord_2019 = VehicleYear(2019)
    
    crv_2020 = VehicleYear(2020)
    
    # Add years to models
    civic.add_year(civic_2018)
    civic.add_year(civic_2019)
    civic.add_year(civic_2020)
    
    accord.add_year(accord_2018)
    accord.add_year(accord_2019)
    
    crv.add_year(crv_2020)
    
    # Add compatible parts
    civic_2018.add_compatible_part(1001)  # Oil filter
    civic_2018.add_compatible_part(1002)  # Air filter
    civic_2019.add_compatible_part(1001)  # Oil filter
    civic_2019.add_compatible_part(1002)  # Air filter
    civic_2020.add_compatible_part(1001)  # Oil filter
    civic_2020.add_compatible_part(1003)  # New air filter
    
    # Test the structure
    assert len(honda.get_models()) == 3
    assert honda.get_model(101) == civic
    assert honda.get_model(102) == accord
    assert honda.get_model(103) == crv
    
    assert len(civic.get_years()) == 3
    assert civic.get_year(2018) == civic_2018
    assert civic.get_year(2019) == civic_2019
    assert civic.get_year(2020) == civic_2020
    
    assert civic_2018.is_part_compatible(1001)
    assert civic_2018.is_part_compatible(1002)
    assert not civic_2018.is_part_compatible(1003)
    
    assert civic_2020.is_part_compatible(1001)
    assert not civic_2020.is_part_compatible(1002)
    assert civic_2020.is_part_compatible(1003)
    
    print("All vehicle hierarchy tests passed!")


def test_part_catalog():
    """
    Test the part catalog classes.
    """
    # Create part categories
    filters = PartCategory(1, "Filters", "Air, oil, and fuel filters")
    brakes = PartCategory(2, "Brakes", "Brake pads, rotors, and calipers")
    engine = PartCategory(3, "Engine", "Engine components and parts")
    
    # Create parts
    oil_filter = Part(
        1001, 
        "Oil Filter", 
        "Filters", 
        12.99, 
        "Removes contaminants from engine oil"
    )
    
    air_filter = Part(
        1002, 
        "Air Filter", 
        "Filters", 
        15.99, 
        "Filters air entering the engine"
    )
    
    brake_pads = Part(
        1003, 
        "Brake Pads", 
        "Brakes", 
        45.99, 
        "Provides friction to stop the vehicle"
    )
    
    spark_plugs = Part(
        1004, 
        "Spark Plugs", 
        "Engine", 
        8.99, 
        "Delivers electric current to ignite fuel"
    )
    
    # Add compatible vehicles
    oil_filter.add_compatible_vehicle("Honda", "Civic", 2018)
    oil_filter.add_compatible_vehicle("Honda", "Civic", 2019)
    oil_filter.add_compatible_vehicle("Honda", "Civic", 2020)
    oil_filter.add_compatible_vehicle("Honda", "Accord", 2018)
    oil_filter.add_compatible_vehicle("Honda", "Accord", 2019)
    
    air_filter.add_compatible_vehicle("Honda", "Civic", 2018)
    air_filter.add_compatible_vehicle("Honda", "Civic", 2019)
    air_filter.add_compatible_vehicle("Honda", "Accord", 2018)
    
    brake_pads.add_compatible_vehicle("Honda", "Civic", 2018)
    brake_pads.add_compatible_vehicle("Honda", "Civic", 2019)
    brake_pads.add_compatible_vehicle("Honda", "Civic", 2020)
    
    spark_plugs.add_compatible_vehicle("Honda", "Civic", 2018)
    spark_plugs.add_compatible_vehicle("Honda", "Civic", 2019)
    
    # Create part catalog
    catalog = PartCatalog()
    
    # Add categories to catalog
    catalog.add_category(filters)
    catalog.add_category(brakes)
    catalog.add_category(engine)
    
    # Add parts to catalog
    catalog.add_part(oil_filter)
    catalog.add_part(air_filter)
    catalog.add_part(brake_pads)
    catalog.add_part(spark_plugs)
    
    # Test the structure
    assert len(catalog.get_categories()) == 3
    assert catalog.get_category(1) == filters
    assert catalog.get_category(2) == brakes
    assert catalog.get_category(3) == engine
    
    assert len(catalog.get_parts()) == 4
    assert catalog.get_part(1001) == oil_filter
    assert catalog.get_part(1002) == air_filter
    assert catalog.get_part(1003) == brake_pads
    assert catalog.get_part(1004) == spark_plugs
    
    # Test search
    search_results = catalog.search_parts("filter")
    assert len(search_results) == 2
    assert oil_filter in search_results
    assert air_filter in search_results
    
    # Test compatibility search
    compatible_parts = catalog.find_compatible_parts("Honda", "Civic", 2018)
    assert len(compatible_parts) == 4
    
    compatible_parts = catalog.find_compatible_parts("Honda", "Civic", 2020)
    assert len(compatible_parts) == 2
    assert oil_filter in compatible_parts
    assert brake_pads in compatible_parts
    assert air_filter not in compatible_parts
    
    compatible_parts = catalog.find_compatible_parts("Honda", "CR-V", 2020)
    assert len(compatible_parts) == 0
    
    # Test category search
    filter_parts = catalog.get_parts_by_category("Filters")
    assert len(filter_parts) == 2
    assert oil_filter in filter_parts
    assert air_filter in filter_parts
    
    print("All part catalog tests passed!")


def demonstrate_registry_and_catalog():
    """
    Demonstrate the use of VehicleRegistry and PartCatalog together.
    """
    # Create a vehicle registry
    registry = VehicleRegistry()
    
    # Create vehicle makes
    honda = VehicleMake(1, "Honda")
    toyota = VehicleMake(2, "Toyota")
    ford = VehicleMake(3, "Ford")
    
    # Add makes to registry
    registry.add_make(honda)
    registry.add_make(toyota)
    registry.add_make(ford)
    
    # Create vehicle models for Honda
    civic = VehicleModel(101, "Civic")
    accord = VehicleModel(102, "Accord")
    
    # Create vehicle models for Toyota
    camry = VehicleModel(201, "Camry")
    corolla = VehicleModel(202, "Corolla")
    
    # Create vehicle models for Ford
    f150 = VehicleModel(301, "F-150")
    
    # Add models to makes
    honda.add_model(civic)
    honda.add_model(accord)
    toyota.add_model(camry)
    toyota.add_model(corolla)
    ford.add_model(f150)
    
    # Create years
    for model, years in [
        (civic, [2018, 2019, 2020]),
        (accord, [2018, 2019]),
        (camry, [2018, 2019, 2020]),
        (corolla, [2019, 2020]),
        (f150, [2018, 2019, 2020])
    ]:
        for year in years:
            model.add_year(VehicleYear(year))
    
    # Create a part catalog
    catalog = PartCatalog()
    
    # Create categories
    filters = PartCategory(1, "Filters", "Air, oil, and fuel filters")
    brakes = PartCategory(2, "Brakes", "Brake pads, rotors, and calipers")
    engine = PartCategory(3, "Engine", "Engine components and parts")
    
    # Add categories to catalog
    catalog.add_category(filters)
    catalog.add_category(brakes)
    catalog.add_category(engine)
    
    # Create some parts
    parts_data = [
        (1001, "Oil Filter", "Filters", 12.99, "Removes contaminants from engine oil"),
        (1002, "Air Filter", "Filters", 15.99, "Filters air entering the engine"),
        (1003, "Fuel Filter", "Filters", 18.99, "Filters fuel before it enters the engine"),
        (1004, "Brake Pads", "Brakes", 45.99, "Provides friction to stop the vehicle"),
        (1005, "Brake Rotors", "Brakes", 89.99, "Rotating disc that brake pads clamp onto"),
        (1006, "Spark Plugs", "Engine", 8.99, "Delivers electric current to ignite fuel"),
        (1007, "Timing Belt", "Engine", 28.99, "Synchronizes engine valves with pistons")
    ]
    
    # Add parts to catalog with compatibility
    parts = {}
    for part_id, name, category, price, desc in parts_data:
        part = Part(part_id, name, category, price, desc)
        parts[part_id] = part
        catalog.add_part(part)
    
    # Define compatibility
    compatibility_data = [
        # Honda Civic
        (1001, "Honda", "Civic", [2018, 2019, 2020]),  # Oil Filter
        (1002, "Honda", "Civic", [2018, 2019]),        # Air Filter
        (1003, "Honda", "Civic", [2018, 2019, 2020]),  # Fuel Filter
        (1004, "Honda", "Civic", [2018, 2019, 2020]),  # Brake Pads
        (1005, "Honda", "Civic", [2018, 2019, 2020]),  # Brake Rotors
        (1006, "Honda", "Civic", [2018, 2019, 2020]),  # Spark Plugs
        
        # Honda Accord
        (1001, "Honda", "Accord", [2018, 2019]),       # Oil Filter
        (1002, "Honda", "Accord", [2018, 2019]),       # Air Filter
        (1003, "Honda", "Accord", [2018, 2019]),       # Fuel Filter
        (1004, "Honda", "Accord", [2018, 2019]),       # Brake Pads
        (1005, "Honda", "Accord", [2018, 2019]),       # Brake Rotors
        (1006, "Honda", "Accord", [2018, 2019]),       # Spark Plugs
        
        # Toyota Camry
        (1001, "Toyota", "Camry", [2018, 2019, 2020]), # Oil Filter
        (1002, "Toyota", "Camry", [2018, 2019, 2020]), # Air Filter
        (1003, "Toyota", "Camry", [2018, 2019, 2020]), # Fuel Filter
        (1004, "Toyota", "Camry", [2018, 2019, 2020]), # Brake Pads
        (1005, "Toyota", "Camry", [2018, 2019, 2020]), # Brake Rotors
        (1006, "Toyota", "Camry", [2018, 2019, 2020]), # Spark Plugs
        (1007, "Toyota", "Camry", [2018, 2019, 2020]), # Timing Belt
        
        # Toyota Corolla
        (1001, "Toyota", "Corolla", [2019, 2020]),     # Oil Filter
        (1002, "Toyota", "Corolla", [2019, 2020]),     # Air Filter
        (1003, "Toyota", "Corolla", [2019, 2020]),     # Fuel Filter
        (1004, "Toyota", "Corolla", [2019, 2020]),     # Brake Pads
        (1006, "Toyota", "Corolla", [2019, 2020]),     # Spark Plugs
        
        # Ford F-150
        (1001, "Ford", "F-150", [2018, 2019, 2020]),   # Oil Filter
        (1002, "Ford", "F-150", [2018, 2019, 2020]),   # Air Filter
        (1003, "Ford", "F-150", [2018, 2019, 2020]),   # Fuel Filter
        (1004, "Ford", "F-150", [2018, 2019, 2020]),   # Brake Pads
        (1005, "Ford", "F-150", [2018, 2019, 2020]),   # Brake Rotors
        (1007, "Ford", "F-150", [2018, 2019, 2020]),   # Timing Belt
    ]
    
    # Add compatibility data
    for part_id, make_name, model_name, years in compatibility_data:
        part = parts[part_id]
        for year in years:
            part.add_compatible_vehicle(make_name, model_name, year)
    
    # Demonstrate searching for parts
    print("Available vehicle makes:")
    for make in registry.get_makes():
        print(f"- {make.name}")
    
    print("\nHonda models:")
    for model in honda.get_models():
        print(f"- {model.name} ({', '.join(str(year.year) for year in model.get_years())})")
    
    print("\nAll available parts:")
    for part in catalog.get_parts():
        print(f"- {part}")
    
    # Demonstrate finding compatible parts for a specific vehicle
    make_name = "Honda"
    model_name = "Civic"
    year = 2019
    
    print(f"\nParts compatible with {year} {make_name} {model_name}:")
    compatible_parts = catalog.find_compatible_parts(make_name, model_name, year)
    
    for part in compatible_parts:
        print(f"- {part}")
    
    # Demonstrate searching by part name
    search_term = "filter"
    print(f"\nParts matching search term '{search_term}':")
    search_results = catalog.search_parts(search_term)
    
    for part in search_results:
        print(f"- {part}")
    
    # Demonstrate search history
    registry.add_search_to_history(f"Parts for {year} {make_name} {model_name}")
    registry.add_search_to_history(f"Search for '{search_term}'")
    
    print("\nSearch history:")
    for i, query in enumerate(registry.get_search_history()):
        print(f"{i+1}. {query}")


if __name__ == "__main__":
    test_vehicle_hierarchy()
    print("\n" + "-"*40 + "\n")
    test_part_catalog()
    print("\n" + "-"*40 + "\n")
    demonstrate_registry_and_catalog()
