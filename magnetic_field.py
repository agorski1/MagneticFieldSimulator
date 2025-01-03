import numpy as np

class MagneticField:
    MU_0 = 4 * np.pi * 1e-7  # Magnetic constant (permeability of free space)

    @classmethod
    def field_at_point_from_segment(cls, point, current, start_point, end_point):
        dl = end_point - start_point
        r = point - start_point
        norm_r = np.linalg.norm(r)
        dB = np.array([0.0, 0.0, 0.0])

        if norm_r != 0:
            dB = (cls.MU_0 / (4 * np.pi)) * current * (np.cross(dl, r) / (norm_r ** 3))
        return dB

    @classmethod
    def field_at_point_from_cable(cls, point, cable_coords):
        total_field = np.array([0.0, 0.0, 0.0])
        for i in range(cable_coords.shape[0] - 1):
            segment_field = cls.field_at_point_from_segment(point, 100, cable_coords[i], cable_coords[i + 1])
            total_field += segment_field
        return total_field