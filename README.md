# MagneticFieldSimulator

A Python-based tool for simulating and visualizing magnetic fields around cables. This project allows you to generate 3D cable structures (straight, sine, or coil) and visualize the magnetic field around them using interactive 3D plots with Plotly.

## Features
- Generate cable structures with different shapes: straight, sine, or coil.
- Calculate magnetic field vectors around the cable using the Biot-Savart law.
- Visualize the cable and magnetic field with customizable point density and radius.
- Save field coordinates and vectors to CSV files for further analysis.

## Prerequisites
To run this project, you need:
- Python 3.8 or higher
- Required Python packages:
  - `numpy`
  - `plotly`
  - `pandas`

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/MagneticFieldSimulator.git
   cd MagneticFieldSimulator
   pip install numpy plotly pandas
   ```

## Usage
1. Run the main script to see a default visualization:
```bash
python main.py
```
This will generate a coil-shaped cable and display its magnetic field with default settings.

2. Customize the visualization by editing main.py. For example:
```bash
from cable import Cable
from magnetic_field_visualizer import MagneticFieldVisualizer

# Create a sine-shaped cable with 50 points
cable = Cable(50, "sine")
# Customize point density and radii
visualizer = MagneticFieldVisualizer(cable.get_cable_structure(), points_per_circle=15, num_circles=8, radii=[0.5, 1.0, 1.5])
visualizer.add_cones()
visualizer.draw()
```
Parameters
 - cable_type: "straight", "sine", or "coil" – shape of the cable.
 - points_per_circle: Number of points per circle around the cable (affects density in the perpendicular plane).
 - num_circles: Number of circles along the cable (affects density along the length).
 - radii: List of distances from the cable where field points are calculated (e.g., [0.5, 1.0]).

## Project Structure
```MagneticFieldSimulator/
├── cable.py              # Cable structure generation
├── magnetic_field.py     # Magnetic field calculations
├── magnetic_field_visualizer.py  # Visualization logic
├── main.py               # Example usage
└── README.md             # This file
```

## Example Output
The visualization shows a 3D cable with cones representing the magnetic field vectors. You can interact with the plot (rotate, zoom) in your browser.
![Magnetic Field Visualization](https://github.com/agorski1/MagneticFieldSimulator/blob/master/output.png)
## Contributing 
Feel free to submit issues or pull requests if you have ideas for improvements!

## License
This project is licensed under the MIT License - see the  file for details.

## Acknowledgments
Built with ❤️ using Python, NumPy, and Plotly.