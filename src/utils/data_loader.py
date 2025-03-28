"""
Data loader utility for the Automotive Parts Catalog System.
"""
import os
import csv
import random
from typing import List, Dict, Tuple, Any, Optional

from src.models.part import Part, PartCategory, PartCatalog
from src.models.vehicle import VehicleMake, VehicleModel, VehicleYear, VehicleRegistry


class DataLoader:
    """
    Utility class for loading and generating sample data for the Automotive Parts Catalog System.
    """
    
    @staticmethod
    def load_parts_from_csv(file_path: str, catalog: PartCatalog) -> List[Part]:
        """
        Load parts from a CSV file into the catalog.
        
        The CSV file should have the following columns:
        - part_id: Unique ID for the part
        - name: Name of the part
        - category: Category name of the part
        - price: Price of the part
        - description: Description of the part
        
        Args:
            file_path: Path to the CSV file
            catalog: PartCatalog to load parts into
            
        Returns:
            List of Part objects loaded from the CSV file
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        parts = []
        
        with open(file_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    part_id = int(row['part_id'])
                    name = row['name']
                    category_name = row['category']
                    price = float(row['price'])
                    description = row.get('description', '')
                    
                    # Create the part
                    part = Part(part_id, name, category_name, price, description)
                    parts.append(part)
                    
                    # Add to catalog
                    catalog.add_part(part)
                except (KeyError, ValueError) as e:
                    print(f"Error loading part from CSV: {e}")
                    print(f"Row: {row}")
        
        return parts
    
    @staticmethod
    def load_vehicles_from_csv(file_path: str, registry: VehicleRegistry) -> List[VehicleMake]:
        """
        Load vehicles from a CSV file into the registry.
        
        The CSV file should have the following columns:
        - make_id: Unique ID for the make
        - make_name: Name of the make
        - model_id: Unique ID for the model
        - model_name: Name of the model
        - year: Year of the vehicle
        
        Args:
            file_path: Path to the CSV file
            registry: VehicleRegistry to load vehicles into
            
        Returns:
            List of VehicleMake objects loaded from the CSV file
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        makes = {}
        
        with open(file_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    make_id = int(row['make_id'])
                    make_name = row['make_name']
                    model_id = int(row['model_id'])
                    model_name = row['model_name']
                    year = int(row['year'])
                    
                    # Get or create make
                    if make_id not in makes:
                        make = VehicleMake(make_id, make_name)
                        makes[make_id] = make
                        registry.add_make(make)
                    else:
                        make = makes[make_id]
                    
                    # Get or create model
                    model = make.get_model(model_id)
                    if not model:
                        model = VehicleModel(model_id, model_name)
                        make.add_model(model)
                    
                    # Get or create year
                    year_obj = model.get_year(year)
                    if not year_obj:
                        year_obj = VehicleYear(year)
                        model.add_year(year_obj)
                except (KeyError, ValueError) as e:
                    print(f"Error loading vehicle from CSV: {e}")
                    print(f"Row: {row}")
        
        return list(makes.values())
    
    @staticmethod
    def load_compatibility_from_csv(file_path: str, catalog: PartCatalog, registry: VehicleRegistry) -> None:
        """
        Load part-vehicle compatibility data from a CSV file.
        
        The CSV file should have the following columns:
        - part_id: ID of the part
        - make_id: ID of the vehicle make
        - model_id: ID of the vehicle model
        - year: Year of the vehicle
        
        Args:
            file_path: Path to the CSV file
            catalog: PartCatalog containing the parts
            registry: VehicleRegistry containing the vehicles
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with open(file_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    part_id = int(row['part_id'])
                    make_id = int(row['make_id'])
                    model_id = int(row['model_id'])
                    year = int(row['year'])
                    
                    # Get the part
                    part = catalog.get_part(part_id)
                    if not part:
                        print(f"Part not found: {part_id}")
                        continue
                    
                    # Get the make
                    make = registry.get_make(make_id)
                    if not make:
                        print(f"Make not found: {make_id}")
                        continue
                    
                    # Get the model
                    model = make.get_model(model_id)
                    if not model:
                        print(f"Model not found: {model_id}")
                        continue
                    
                    # Check if the year exists
                    year_obj = model.get_year(year)
                    if not year_obj:
                        print(f"Year not found: {year} for {make.name} {model.name}")
                        continue
                    
                    # Add compatibility
                    part.add_compatible_vehicle(make.name, model.name, year)
                    year_obj.add_compatible_part(part_id)
                except (KeyError, ValueError) as e:
                    print(f"Error loading compatibility from CSV: {e}")
                    print(f"Row: {row}")
    
    @staticmethod
    def generate_sample_data(catalog: PartCatalog, registry: VehicleRegistry, num_parts: int = 100) -> None:
        """
        Generate sample data for the Automotive Parts Catalog System.
        
        Args:
            catalog: PartCatalog to add parts to
            registry: VehicleRegistry to add vehicles to
            num_parts: Number of parts to generate
        """
        # Create categories
        categories = [
            PartCategory(1, "Filters", "Air, oil, and fuel filters"),
            PartCategory(2, "Brakes", "Brake pads, rotors, and calipers"),
            PartCategory(3, "Engine", "Engine components and parts"),
            PartCategory(4, "Suspension", "Suspension and steering components"),
            PartCategory(5, "Electrical", "Electrical components and wiring"),
            PartCategory(6, "Transmission", "Transmission components and fluids"),
            PartCategory(7, "Cooling", "Cooling system components"),
            PartCategory(8, "Body", "Body panels and parts")
        ]
        
        for category in categories:
            catalog.add_category(category)
        
        # Create makes
        makes = [
            VehicleMake(1, "Honda"),
            VehicleMake(2, "Toyota"),
            VehicleMake(3, "Ford"),
            VehicleMake(4, "Chevrolet"),
            VehicleMake(5, "BMW"),
            VehicleMake(6, "Mercedes-Benz"),
            VehicleMake(7, "Audi"),
            VehicleMake(8, "Volkswagen")
        ]
        
        for make in makes:
            registry.add_make(make)
        
        # Create models
        models_data = [
            # Honda models
            (1, 101, "Civic"),
            (1, 102, "Accord"),
            (1, 103, "CR-V"),
            # Toyota models
            (2, 201, "Camry"),
            (2, 202, "Corolla"),
            (2, 203, "RAV4"),
            # Ford models
            (3, 301, "F-150"),
            (3, 302, "Mustang"),
            (3, 303, "Explorer"),
            # Chevrolet models
            (4, 401, "Silverado"),
            (4, 402, "Camaro"),
            (4, 403, "Equinox"),
            # BMW models
            (5, 501, "3 Series"),
            (5, 502, "5 Series"),
            (5, 503, "X5"),
            # Mercedes-Benz models
            (6, 601, "C-Class"),
            (6, 602, "E-Class"),
            (6, 603, "GLE"),
            # Audi models
            (7, 701, "A4"),
            (7, 702, "A6"),
            (7, 703, "Q5"),
            # Volkswagen models
            (8, 801, "Golf"),
            (8, 802, "Passat"),
            (8, 803, "Tiguan")
        ]
        
        for make_id, model_id, model_name in models_data:
            make = registry.get_make(make_id)
            if make:
                model = VehicleModel(model_id, model_name)
                make.add_model(model)
                
                # Add years for each model (2015-2023)
                for year in range(2015, 2024):
                    model.add_year(VehicleYear(year))
        
        # Create parts
        part_names = [
            # Filters
            "Oil Filter", "Air Filter", "Fuel Filter", "Cabin Air Filter", "Transmission Filter",
            # Brakes
            "Front Brake Pads", "Rear Brake Pads", "Front Brake Rotors", "Rear Brake Rotors",
            "Brake Calipers", "Brake Fluid", "Brake Lines", "Brake Master Cylinder",
            # Engine
            "Spark Plugs", "Ignition Coils", "Timing Belt", "Timing Chain", "Alternator",
            "Starter Motor", "Engine Oil", "Oil Pan", "Head Gasket", "Valve Cover", "Turbocharger",
            # Suspension
            "Struts", "Shocks", "Control Arms", "Tie Rods", "Ball Joints", "Wheel Bearings",
            "Sway Bar Links", "Coil Springs", "Leaf Springs", "Strut Mounts",
            # Electrical
            "Battery", "Alternator", "Starter", "Headlights", "Tail Lights", "Turn Signals",
            "Ignition Switch", "Sensors", "Fuses", "Relays", "Wiring Harness",
            # Transmission
            "Transmission Fluid", "Clutch Kit", "Flywheel", "Torque Converter", "Transmission Mount",
            "Shift Cable", "Transmission Solenoid", "Transmission Control Module",
            # Cooling
            "Radiator", "Thermostat", "Water Pump", "Coolant", "Radiator Hoses", "Radiator Cap",
            "Cooling Fan", "Fan Clutch",
            # Body
            "Hood", "Fenders", "Doors", "Trunk Lid", "Bumper Cover", "Grille", "Side Mirrors",
            "Wiper Blades", "Windshield", "Weather Stripping"
        ]
        
        # Generate parts
        part_id = 1001
        parts = []
        
        for i in range(num_parts):
            # Pick a random category
            category = random.choice(categories)
            
            # Pick a related part name or random if none related
            related_parts = [p for p in part_names if any(
                keyword in p.lower() for keyword in category.name.lower().split())]
            
            if not related_parts:
                related_parts = part_names
            
            name = random.choice(related_parts)
            price = round(random.uniform(5.99, 299.99), 2)
            description = f"High quality {name.lower()} for optimal performance."
            
            # Create the part
            part = Part(part_id, name, category.name, price, description)
            catalog.add_part(part)
            parts.append(part)
            
            # Randomly assign compatibility with vehicles
            for make in makes:
                # Each part is compatible with 30% of makes
                if random.random() < 0.3:
                    for model in make.get_models():
                        # Compatible with 40% of models for each compatible make
                        if random.random() < 0.4:
                            for year_obj in model.get_years():
                                # Compatible with 60% of years for each compatible model
                                if random.random() < 0.6:
                                    part.add_compatible_vehicle(
                                        make.name, 
                                        model.name, 
                                        year_obj.year
                                    )
                                    year_obj.add_compatible_part(part_id)
            
            part_id += 1
        
        return parts
    
    @staticmethod
    def export_to_csv(catalog: PartCatalog, registry: VehicleRegistry, output_dir: str) -> None:
        """
        Export the catalog and registry data to CSV files.
        
        Args:
            catalog: PartCatalog to export
            registry: VehicleRegistry to export
            output_dir: Directory to write CSV files to
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Export parts
        parts_file = os.path.join(output_dir, "parts.csv")
        with open(parts_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["part_id", "name", "category", "price", "description"])
            
            for part in catalog.get_parts():
                writer.writerow([
                    part.part_id,
                    part.name,
                    part.category,
                    part.price,
                    part.description
                ])
        
        # Export categories
        categories_file = os.path.join(output_dir, "categories.csv")
        with open(categories_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["category_id", "name", "description"])
            
            for category in catalog.get_categories():
                writer.writerow([
                    category.category_id,
                    category.name,
                    category.description
                ])
        
        # Export vehicles
        vehicles_file = os.path.join(output_dir, "vehicles.csv")
        with open(vehicles_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["make_id", "make_name", "model_id", "model_name", "year"])
            
            for make in registry.get_makes():
                for model in make.get_models():
                    for year_obj in model.get_years():
                        writer.writerow([
                            make.make_id,
                            make.name,
                            model.model_id,
                            model.name,
                            year_obj.year
                        ])
        
        # Export compatibility
        compatibility_file = os.path.join(output_dir, "compatibility.csv")
        with open(compatibility_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["part_id", "make_name", "model_name", "year"])
            
            for part in catalog.get_parts():
                for compat in part.compatible_vehicles:
                    make_name, model_name, year_str = compat.split(":")
                    writer.writerow([
                        part.part_id,
                        make_name,
                        model_name,
                        year_str
                    ])
