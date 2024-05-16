import numpy as np


class SpatialHash2:
    def __init__(self, cell_size):
        self.cell_size = cell_size
        self.hash_map = {}

    def add_point(self, point, obj):
        cell_x = int(point[0] / self.cell_size)
        cell_y = int(point[1] / self.cell_size)
        cell = (cell_x, cell_y)
        if cell in self.hash_map:
            self.hash_map[cell].append((point, obj))
        else:
            self.hash_map[cell] = [(point, obj)]

    def get_points_in_range(self, query_point, radius):
        cell_x = int(query_point[0] / self.cell_size)
        cell_y = int(query_point[1] / self.cell_size)
        result = []
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                cell = (cell_x + dx, cell_y + dy)
                if cell in self.hash_map:
                    for point, obj in self.hash_map[cell]:
                        if (point[0] - query_point[0]) ** 2 + (point[1] - query_point[1]) ** 2 <= radius ** 2:
                            result.append((point, obj))
        return result

    def get_points_in_range2(self, query_point, radius):
        cell_x = int(query_point[0] / self.cell_size)
        cell_y = int(query_point[1] / self.cell_size)
        result = []
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                cell = (cell_x + dx, cell_y + dy)
                if cell in self.hash_map:
                    points, objs = zip(*self.hash_map[cell])
                    points = np.array(points)
                    distances_squared = np.sum((points - query_point)**2, axis=1)
                    indices = np.where(distances_squared <= radius**2)[0]
                    for i in indices:
                        result.append((points[i], objs[i]))
        return result