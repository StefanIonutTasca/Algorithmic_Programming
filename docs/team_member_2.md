# Team Member 2 Documentation
## Automotive Parts Catalog System

### Components Implemented
This documentation covers the implementation details for the components developed by Team Member 2 for the Automotive Parts Catalog System project.

#### 1. Data Structures
- **Node Class**: Generic implementation of a node for tree-based data structures
- **BinarySearchTree Class**: Complete implementation of a binary search tree data structure with:
  - Insertion, deletion, and search operations
  - Multiple traversal methods (inorder, preorder, postorder)
  - Height calculation and balanced tree operations

#### 2. Search Algorithms
- **Linear Search**: Implementation with performance tracking
- **Binary Search**: Implementation with performance tracking
- Performance comparison utilities for algorithm efficiency demonstration

#### 3. GUI Components
- **MainWindow**: Central application window that coordinates all GUI components
- **SearchPanel**: Interface for searching parts by vehicle make, model, year, and category
- **ResultsPanel**: Display panel for showing search results in a tabular format
- **PartDetailPanel**: Detailed view of a selected part with specifications and compatibility
- **PerformancePanel**: Visualization of search algorithm performance with comparative metrics

### User Interface Design
The GUI is designed using Tkinter to provide a clean, functional interface with:
- Hierarchical navigation through vehicle make, model, and year
- Part category filtering
- Results displayed in a sortable table
- Detailed part information with compatibility lists
- Visual performance metrics for algorithm comparison

### Usage Instructions
1. Launch the application using the main entry point
2. Select a vehicle make, model, and year from the dropdown menus
3. Optionally select a part category
4. Click "Search" to find compatible parts
5. Select a part from the results to view detailed information
6. Use the Performance tab to run algorithm demos and view comparisons

### Technical Details
- All implementations use Python's type hints for improved code quality
- The BinarySearchTree implementation is generic and can work with any comparable type
- The search algorithms include performance metrics to demonstrate algorithmic efficiency
- The GUI components are modular and follow a consistent design pattern
