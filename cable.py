import numpy as np

class Cable:
    def __init__(self, length, cable_type="straight"):
        self.coords = np.empty(shape=[0, 3])
        self.generate_cable(length, cable_type)

    def generate_cable(self, length, cable_type):
        if cable_type == "straight":
            self._generate_straight(length)
        elif cable_type == "coil":
            self._generate_coil(length)
        elif cable_type == "sine":
            self._generate_sine(length)
        else:
            raise ValueError(f"Unknown cable type: {cable_type}")

    def _generate_straight(self, length):
        for i in range(length):
            self.coords = np.append(self.coords, [[i, 0, 0]], axis=0)

    def _generate_sine(self, length):
        for i in range(length):
            theta = i * (2 * np.pi) / 4
            new_x = i
            new_y = 0
            new_z = np.sin(theta / 8)
            self.coords = np.append(self.coords, [[new_x, new_y, new_z]], axis=0)

    def _generate_coil(self, length):
        for i in range(length):
            theta = i * (2 * np.pi) / 2
            new_x = i
            new_y = np.cos(theta / 8)
            new_z = np.sin(theta / 8)
            self.coords = np.append(self.coords, [[new_x, new_y, new_z]], axis=0)

    def get_coords_at_index(self, index):
        return self.coords[index]

    def get_cable_structure(self):
        return self.coords