import math

class Point(object):
    def __init__(self, x, y):
        self.x, self.y = x, y

player = Point(10.0, 25.0)
mouse = Point(30.0, 70.0)
speed = math.sqrt(2)

distance = [mouse.x - player.x, mouse.y - player.y]
norm = math.sqrt(distance[0]**2 + distance[1]**2)
direction = [distance[0]/norm, distance[1]/norm]
bullet_vector = [direction[0]*speed, direction[1]*speed]

#print(bullet_vector)
###############################################


init_pos = (0.0, 0.0)
x1, y1 = init_pos

click_pos = (2.0, 0.0)
x2, y2 = click_pos

def vector_calculator(init_point, second_point):
    distance = [second_point[0] - init_point[0], second_point[1] - init_point[1]]
    norm = math.sqrt(distance[0]**2 + distance[1]**2)
    direction = [distance[0]/norm, distance[1]/norm]
    print direction
    bullet_vector = [direction[0]*speed, direction[1]*speed]

    return(bullet_vector)

print(vector_calculator(init_pos, click_pos))

################################################
    def calculate_initial_compass_bearing(self, pointA, pointB):
        """https://gist.github.com/jeromer/2005586"""
        if (type(pointA) != tuple) or (type(pointB) != tuple):
            raise TypeError("Only tuples are supported as arguments")

        lat1 = math.radians(pointA[0])
        lat2 = math.radians(pointB[0])

        diffLong = math.radians(pointB[1] - pointA[1])

        x = math.sin(diffLong) * math.cos(lat2)
        y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
                * math.cos(lat2) * math.cos(diffLong))

        initial_bearing = math.atan2(x, y)

        initial_bearing = math.degrees(initial_bearing)
        compass_bearing = (initial_bearing + 360) % 360

        return compass_bearing