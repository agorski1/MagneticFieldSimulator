from cable import Cable
from magnetic_field_visualizer import MagneticFieldVisualizer

# Tworzymy kabel i wizualizator z domyślnymi parametrami
cable = Cable(30, "coil")
visualizer = MagneticFieldVisualizer(cable.get_cable_structure(), points_per_circle=10, num_circles=5, radii=[0.5, 1.0])

# Możemy zmienić gęstość punktów podczas dodawania stożków
visualizer.add_cones(points_per_circle=20, num_circles=20, radii=[1.2, 1.3])
visualizer.draw()