import line_profiler


class SpatialHash:
    def __init__(self, cell_size, numcells):
        self.cell_size = cell_size
        self.hash_map = {}
        self.numcells = numcells

    @line_profiler.profile
    def hashcoords(self, xi, yi):
        # this is so dumb
        return str(xi) + str(yi)

    @line_profiler.profile
    def add_object(self, obj, position):
        cell_x = int(position[0] / self.cell_size)
        cell_y = int(position[1] / self.cell_size)
        cell = self.hashcoords(cell_x, cell_y)
        if cell in self.hash_map:
            self.hash_map[cell].append(obj)
        else:
            self.hash_map[cell] = [obj]

    @line_profiler.profile
    def get_objects_in_range(self, position, radius):
        objects = []
        min_cell_x = int((position[0] - radius) / self.cell_size)
        max_cell_x = int((position[0] + radius) / self.cell_size)
        min_cell_y = int((position[1] - radius) / self.cell_size)
        max_cell_y = int((position[1] + radius) / self.cell_size)

        for cell_x in range(min_cell_x, max_cell_x + 1):
            for cell_y in range(min_cell_y, max_cell_y + 1):
                cell = self.hashcoords(cell_x, cell_y)
                if cell in self.hash_map:
                    objects.extend(self.hash_map[cell])

        return objects
