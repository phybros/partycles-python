class Point:
    def __init__(self, x=0.0, y=0.0, data=None):
        self.x = x
        self.y = y
        self.data = data


class AABB:
    def __init__(self, center=Point(), half=50.0):
        self.center = center
        self.half = half

    def contains(self, point):
        return self.center.x - self.half <= point.x <= self.center.x + self.half and \
            self.center.y - self.half <= point.y <= self.center.y + self.half

    def intersects(self, other):
        return not other.center.x - other.half > self.center.x + self.half or \
            other.center.y - other.half > self.center.y + self.half or \
            other.center.x + other.half < self.center.x - self.half or \
            other.center.y + other.half < self.center.y - self.half


class Quadtree:
    def __init__(self, capacity=10, boundary=AABB(), points=None):
        if points is None:
            points = []

        self.capacity = capacity
        self.boundary = boundary
        self.points = points

        self.ne = None
        self.nw = None
        self.se = None
        self.sw = None

        self.mypoints = [
            Point(self.boundary.center.x - self.boundary.half, self.boundary.center.y - self.boundary.half),
            Point(self.boundary.center.x + self.boundary.half, self.boundary.center.y - self.boundary.half),
            Point(self.boundary.center.x - self.boundary.half, self.boundary.center.y + self.boundary.half),
            Point(self.boundary.center.x + self.boundary.half, self.boundary.center.y + self.boundary.half),
        ]

    def insert(self, point):
        # Ignore objects that do not belong in this quad tree
        if not self.boundary.contains(point):
            return False

        # If there is space in this quad tree and if doesn't have subdivisions, add the object here
        if len(self.points) < self.capacity and self.nw is None:
            self.points.append(point)
            return True

        # Otherwise, subdivide and then add the point to whichever node will accept it
        if self.nw is None:
            self.subdivide()

        if self.nw.insert(point):
            return True
        if self.ne.insert(point):
            return True
        if self.sw.insert(point):
            return True
        if self.se.insert(point):
            return True

        # should never get here!
        return False

    def subdivide(self):
        x = self.boundary.center.x
        y = self.boundary.center.y
        ha = self.boundary.half / 2.0

        # get the point halfway between center and edge in all quadrants
        ul = Point(x - ha, y - ha)
        ur = Point(x + ha, y - ha)
        bl = Point(x - ha, y + ha)
        br = Point(x + ha, y + ha)

        self.ne = Quadtree(self.capacity, AABB(center=ur, half=ha))
        self.nw = Quadtree(self.capacity, AABB(center=ul, half=ha))
        self.se = Quadtree(self.capacity, AABB(center=br, half=ha))
        self.sw = Quadtree(self.capacity, AABB(center=bl, half=ha))

    def query(self, boundary):
        found = []

        # not in the thing, ignore
        if not self.boundary.intersects(boundary):
            return []

        skip = False
        for corner in self.mypoints:
            if not boundary.contains(corner):
                skip = False
                break

            skip = True

        if skip:
            found += self.points
        else:
            for point in self.points:
                if boundary.contains(point):
                    found.append(point)

        # if we are subdivided
        if self.nw is not None:
            found += self.nw.query(boundary)
            found += self.ne.query(boundary)
            found += self.sw.query(boundary)
            found += self.se.query(boundary)

        return found

    def clear(self):
        self.ne = None
        self.nw = None
        self.se = None
        self.sw = None
        self.points.clear()
