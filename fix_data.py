"""
Fix data for the Automotive Parts Catalog System.
This script fixes the JSON data to match the expected format for the application.
"""
import json
import os
import random
from datetime import datetime
from typing import List, Dict, Any

def fix_car_makes_json():
    """Fix the car_makes.json file to use integer make_id values."""
    # Get the base directory for data files
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    car_makes_path = os.path.join(data_dir, 'car_makes.json')
    
    try:
        # Load existing data
        with open(car_makes_path, 'r') as f:
            makes_data = json.load(f)
        
        # Fix the make_id format to be integers
        for i, make in enumerate(makes_data):
            make['make_id'] = i + 1  # Convert to integer ID
            
            # Fix model IDs as well
            for j, model in enumerate(make.get('models', [])):
                model['model_id'] = j + 1  # Convert to integer ID
                
                # Ensure years are integers
                for year_data in model.get('years', []):
                    if 'year' in year_data:
                        year_data['year'] = int(year_data['year'])
        
        # Save the fixed data
        with open(car_makes_path, 'w') as f:
            json.dump(makes_data, f, indent=2)
        
        print(f"Fixed make_id format in {car_makes_path}")
        return True
    except Exception as e:
        print(f"Error fixing car makes data: {e}")
        return False

def fix_parts_json():
    """Fix the parts.json file to match the expected format."""
    # Get the base directory for data files
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    parts_path = os.path.join(data_dir, 'parts.json')
    
    try:
        # Load existing data
        with open(parts_path, 'r') as f:
            parts_data = json.load(f)
        
        # Fix the parts to ensure they have the correct format for compatible vehicles
        for part in parts_data:
            # Fix the id format if needed
            if not part['id'].startswith('P'):
                part['id'] = f"P{part['id']}"
            
            # Fix the compatible vehicles format to use integers for make_id and model_id
            compatible_vehicles = []
            for vehicle_str in part.get('compatibleVehicles', []):
                parts = vehicle_str.split(':')
                if len(parts) == 3:
                    make_id, model_id, year = parts
                    # Extract numeric parts from make_id and model_id
                    make_num = ''.join(filter(str.isdigit, make_id))
                    model_num = ''.join(filter(str.isdigit, model_id))
                    
                    if make_num and model_num:
                        # Format with integers
                        compatible_vehicles.append(f"{int(make_num)}:{int(model_num)}:{year}")
            
            # Update the compatible vehicles
            part['compatibleVehicles'] = compatible_vehicles
        
        # Save the fixed data
        with open(parts_path, 'w') as f:
            json.dump(parts_data, f, indent=2)
        
        print(f"Fixed parts format in {parts_path}")
        return True
    except Exception as e:
        print(f"Error fixing parts data: {e}")
        return False

def create_minimal_test_data():
    """Create minimal test data to ensure the application works."""
    # Get the base directory for data files
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    car_makes_path = os.path.join(data_dir, 'car_makes.json')
    parts_path = os.path.join(data_dir, 'parts.json')
    
    # Create minimal car makes data
    makes_data = [
        {
            "make_id": 1,
            "name": "Toyota",
            "country": "Japan",
            "models": [
                {
                    "model_id": 1,
                    "name": "Camry",
                    "years": [
                        {"year": 2020, "generation": "XV70"},
                        {"year": 2021, "generation": "XV70"},
                        {"year": 2022, "generation": "XV70"}
                    ]
                },
                {
                    "model_id": 2,
                    "name": "Corolla",
                    "years": [
                        {"year": 2020, "generation": "E210"},
                        {"year": 2021, "generation": "E210"},
                        {"year": 2022, "generation": "E210"}
                    ]
                }
            ]
        },
        {
            "make_id": 2,
            "name": "Honda",
            "country": "Japan",
            "models": [
                {
                    "model_id": 1,
                    "name": "Civic",
                    "years": [
                        {"year": 2020, "generation": "10th"},
                        {"year": 2021, "generation": "10th"},
                        {"year": 2022, "generation": "11th"}
                    ]
                },
                {
                    "model_id": 2,
                    "name": "Accord",
                    "years": [
                        {"year": 2020, "generation": "10th"},
                        {"year": 2021, "generation": "10th"},
                        {"year": 2022, "generation": "10th"}
                    ]
                }
            ]
        }
    ]
    
    # Create minimal parts data
    parts_data = [
        {
            "id": "P001",
            "name": "Oil Filter",
            "category": "Engine",
            "price": 12.99,
            "manufacturer": "Bosch",
            "description": "High-quality oil filter that removes contaminants from engine oil.",
            "specifications": {
                "filterType": "Spin-on",
                "height": "3.5 inches",
                "diameter": "2.75 inches",
                "threadSize": "3/4-16 UNF",
                "mediaType": "Synthetic blend"
            },
            "compatibleVehicles": [
                "1:1:2020",
                "1:1:2021",
                "1:2:2020",
                "2:1:2021"
            ]
        },
        {
            "id": "P002",
            "name": "Air Filter",
            "category": "Engine",
            "price": 15.99,
            "manufacturer": "K&N",
            "description": "Premium air filter for enhanced engine performance and protection.",
            "specifications": {
                "filterType": "Panel",
                "height": "1.5 inches",
                "length": "10 inches",
                "width": "8 inches",
                "material": "Cotton gauze"
            },
            "compatibleVehicles": [
                "1:1:2020",
                "1:1:2021",
                "1:2:2021",
                "2:1:2020"
            ]
        }
    ]
    
    # Save the data
    with open(car_makes_path, 'w') as f:
        json.dump(makes_data, f, indent=2)
    
    with open(parts_path, 'w') as f:
        json.dump(parts_data, f, indent=2)
    
    print(f"Created minimal test data in {data_dir}")
    return True

def main():
    """Fix or create data files to ensure the application works."""
    print("Checking and fixing data files for the Automotive Parts Catalog System...")
    
    # Try to fix existing files first
    fixed_makes = fix_car_makes_json()
    fixed_parts = fix_parts_json()
    
    # If fixing didn't work, create minimal test data
    if not (fixed_makes and fixed_parts):
        print("Creating minimal test data instead...")
        create_minimal_test_data()
    
    print("Data fixing complete! Try running the application now.")

if __name__ == "__main__":
    main()
