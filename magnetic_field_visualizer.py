import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
import csv
from magnetic_field import MagneticField

class MagneticFieldVisualizer:
    def __init__(self, cable_coords, points_per_circle=20, num_circles=10, radii=[1.0, 1.1, 1.2]):
        self.cable_coords = cable_coords
        self.fig = px.line_3d(x=cable_coords[:, 0], y=cable_coords[:, 1], z=cable_coords[:, 2])
        self.field_points = []
        self.field_vectors = []
        self.points_per_circle = points_per_circle  # Domyślna liczba punktów w okręgu
        self.num_circles = num_circles  # Domyślna liczba okręgów
        self.radii = radii  # Domyślna lista promieni

    def _rotation_matrix_around_vector(self, rotation_vector, theta):
        v = rotation_vector / np.linalg.norm(rotation_vector)
        m1 = np.array([v[0]**2 * (1 - np.cos(theta)) + np.cos(theta),
                       v[0] * v[1] * (1 - np.cos(theta)) - v[2] * np.sin(theta),
                       v[0] * v[2] * (1 - np.cos(theta)) + v[1] * np.sin(theta)])
        m2 = np.array([v[0] * v[1] * (1 - np.cos(theta)) + v[2] * np.sin(theta),
                       v[1]**2 * (1 - np.cos(theta)) + np.cos(theta),
                       v[1] * v[2] * (1 - np.cos(theta)) - v[0] * np.sin(theta)])
        m3 = np.array([v[0] * v[2] * (1 - np.cos(theta)) - v[1] * np.sin(theta),
                       v[1] * v[2] * (1 - np.cos(theta)) + v[0] * np.sin(theta),
                       v[2]**2 * (1 - np.cos(theta)) + np.cos(theta)])
        return np.array([m1, m2, m3])

    def _find_perpendicular_vector(self, vector):
        perp_vector = np.cross(vector, np.array([1, 1, 1]))
        return perp_vector / np.linalg.norm(perp_vector) if np.linalg.norm(perp_vector) != 0 else perp_vector

    def _generate_points_around_segment(self, start, end, points_per_circle, num_circles, radius):
        direction = end - start
        perp_vector = self._find_perpendicular_vector(direction) * radius
        rotation_matrix = self._rotation_matrix_around_vector(direction, (2 * np.pi) / (points_per_circle - 1))

        for j in range(num_circles + 1):
            point = perp_vector + (j / num_circles * direction)
            self.field_points.append(point + start)
            field = MagneticField.field_at_point_from_cable(point + start, self.cable_coords)
            self.field_vectors.append(field)

            next_point = point
            for i in range(1, points_per_circle):
                next_point = np.dot(rotation_matrix, next_point)
                self.field_points.append(next_point + start)
                self.field_vectors.append(MagneticField.field_at_point_from_cable(next_point + start, self.cable_coords))

    def generate_points_around_cable(self, points_per_circle, num_circles, radius):
        for i in range(self.cable_coords.shape[0] - 1):
            self._generate_points_around_segment(self.cable_coords[i], self.cable_coords[i + 1],
                                                 points_per_circle, num_circles, radius)

    def _save_coords_vectors_to_file(self, start, end, points_per_circle, num_circles, radius, coords_file, vectors_file):
        direction = end - start
        perp_vector = self._find_perpendicular_vector(direction) * radius
        rotation_matrix = self._rotation_matrix_around_vector(direction, (2 * np.pi) / (points_per_circle - 1))

        for j in range(num_circles + 1):
            point = perp_vector + (j / num_circles * direction)
            self._save_coords(coords_file, point + start)
            field = MagneticField.field_at_point_from_cable(point + start, self.cable_coords)
            self._save_vectors(vectors_file, field)

            next_point = point
            for i in range(1, points_per_circle):
                next_point = np.dot(rotation_matrix, next_point)
                self._save_coords(coords_file, next_point + start)
                self._save_vectors(vectors_file, MagneticField.field_at_point_from_cable(next_point + start, self.cable_coords))

    def save_coords_vectors_to_files(self, points_per_circle, num_circles, radius, coords_file, vectors_file):
        for i in range(self.cable_coords.shape[0] - 1):
            self._save_coords_vectors_to_file(self.cable_coords[i], self.cable_coords[i + 1],
                                              points_per_circle, num_circles, radius, coords_file, vectors_file)

    def _save_coords(self, coords_file, coords):
        with open(coords_file, 'a', newline='') as csvfile:
            csv.writer(csvfile).writerow(coords)

    def _save_vectors(self, vectors_file, vectors):
        with open(vectors_file, 'a', newline='') as csvfile:
            csv.writer(csvfile).writerow(vectors)

    def add_cones(self, points_per_circle=None, num_circles=None, radii=None):
        # Użyj wartości domyślnych z konstruktora, jeśli nie podano nowych
        points_per_circle = points_per_circle if points_per_circle is not None else self.points_per_circle
        num_circles = num_circles if num_circles is not None else self.num_circles
        radii = radii if radii is not None else self.radii

        # Generuj punkty dla każdego promienia
        for radius in radii:
            self.generate_points_around_cable(points_per_circle, num_circles, radius)

        cone_coords = np.array(self.field_points)
        cone_vectors = np.array(self.field_vectors)

        cones = go.Cone(x=cone_coords[:, 0], y=cone_coords[:, 1], z=cone_coords[:, 2],
                        u=cone_vectors[:, 0], v=cone_vectors[:, 1], w=cone_vectors[:, 2],
                        sizemode="scaled", sizeref=1)
        self.fig.add_trace(cones)

    def add_cones_from_file(self, coords_file, vectors_file):
        coords = pd.read_csv(coords_file, names=['x', 'y', 'z'])
        vectors = pd.read_csv(vectors_file, names=['u', 'v', 'w'])

        cones = go.Cone(x=coords['x'], y=coords['y'], z=coords['z'],
                        u=vectors['u'], v=vectors['v'], w=vectors['w'],
                        sizemode="scaled", sizeref=3)
        self.fig.add_trace(cones)

    def draw(self):
        self.fig.show()