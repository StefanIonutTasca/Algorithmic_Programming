# Algorithmic_Programming
## Automotive Parts Catalog System

An application for searching and managing automotive parts using custom data structures and algorithms.

### Features
- Search for car parts by make, model, and year
- Multiple data structure implementations (ArrayList, LinkedList, BinarySearchTree)
- Custom search and sort algorithms
- Performance metrics for comparing algorithm efficiency
- Robust error handling and data validation

### Project Structure
- `/src` - Source code
  - `/datastructures` - Custom data structure implementations
  - `/algorithms` - Search and sort algorithm implementations
  - `/models` - Data models for vehicles and parts
  - `/utils` - Utility functions and data loading
  - `/gui` - Graphical user interface
- `/data` - Sample datasets
- `/docs` - Documentation

## Installation

### Prerequisites
- Python 3.7 or higher
- Tkinter (usually comes with Python installation)
- Required Python packages:
  - matplotlib
  - numpy

### Setup Instructions

1. **Clone the repository**
   ```
   git clone https://github.com/StefanIonutTasca/Algorithmic_Programming.git
   cd Algorithmic_Programming
   ```

2. **Install required packages**
   ```
   pip install -r requirements.txt
   ```
   If requirements.txt is not available, install the required packages manually:
   ```
   pip install matplotlib numpy
   ```

3. **Verify data files**
   Ensure that the following data files exist in the `/data` directory:
   - `car_makes.json` - Contains information about car makes, models, and years
   - `parts.json` - Contains information about automotive parts

## Running the Application

The application is started using the run_application.py script:
```
python run_application.py
```
This script is optimized for both regular use and provides helpful error messages if issues arise.

### Troubleshooting
If you encounter any issues running the application:

1. **Import Errors**
   - Ensure your Python path is set correctly
   - Make sure all files have the correct case sensitivity (especially important on Unix systems)

2. **Data Loading Issues**
   - Verify that the data files exist in the `/data` directory
   - Check for proper JSON format in the data files

3. **GUI Issues**
   - Ensure Tkinter is properly installed with your Python distribution
   - On Linux, you may need to install additional packages: `sudo apt-get install python3-tk`

## Using the Application

1. **Search for Parts**
   - Select a car make from the dropdown
   - Optionally select a model and year
   - Choose a part category if desired
   - Click the "Search" button to find compatible parts
   - Results will appear in the results panel

2. **View Performance Metrics**
   - Navigate to the Performance Metrics tab
   - Select an algorithm to benchmark
   - Click the "Run Algorithm Demo" button
   - View the performance statistics and comparison charts

3. **Data Structures**
   - The application demonstrates the use of various data structures:
     - Binary Search Tree for efficient search operations
     - Lists for storing and managing collections of objects
   - Performance comparisons between different implementations are available

## Project Requirements

- Python 3.7+
- Tkinter for GUI components
- Matplotlib for performance visualization
- JSON files for data storage


## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
