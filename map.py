from points import *
from items import *


__all__ = ['Room', 'Coridor', 'Map', 'Point', 'ShadedPoint']

class Node:

    def __init__(self, content, previous = None, g = 0, h = 0):
        self.content = content
        self.previous = previous
        self.g = g
        self.h = h
    
    @property
    def f(self):
        return self.g + self.h

def _h_calculate(current: Point, end: Point):
    return abs(current.x-end.x) + abs(current.y - end.y)


class Room:
    
    view: str = "█"
    point: Point
    width: int
    height: int

    @property
    def coordinates(self) -> list[Point]:
        cord = []

        for x in range(1 + self.point.x, self.point.x + self.width + 1):
            for y in range(1 + self.point.y, self.point.y + self.height + 1):
                cord.append(ShadedPoint(x, y, self.view))

        return cord
    
    @property
    def board(self) -> list[Point]:
        return [point for point in self.coordinates
                if point.x == self.point.x + 1 or point.x == self.point.x + self.width
                or point.y == self.point.y + 1 or point.y == self.point.y + self.height]

    def __init__(self, point, width, height):
        self.point = point
        self.width = width
        self.height = height


class Coridor:

    view: str = "▒"
    connected_points: list[Point]
    path: list[ShadedPoint]

    def __init__(self, connected_points, path):
        self.connected_points = connected_points
        self.path = path


class Map:
    view: str = " "
    exit_view: str = "𐌢"
    width: int
    height: int 
    room_count: int
    rooms: list[Room]
    coridors: list[Coridor]
    items: list[Item]
    map: list[ShadedPoint]

    def __init__(self, room_count, width, height, room_width, room_height):
        self.width = width
        self.height = height
        self.room_count = room_count
        self.rooms = []
        self.coridors = []
        self.items = []
        self.map = []

        for y in range(1, self.height+1):
            for x in range(1, self.width+1):
                self.map.append(ShadedPoint(x, y, self.view))

        self.__generate_rooms(room_width, room_height)
        self.__generate_corridors()
        self.__generate_exit()
        self.__spawn_items()
        
        
    def __generate_rooms(self, room_width, room_height):
        while len(self.rooms) < self.room_count:
            point = randPoint(self.width, self.height)
            width = random.randint(room_width, room_height)
            height = random.randint(room_width, room_height)
            
            
            if point.x + width > self.width or point.y + height > self.height:
                continue
                
            
            new_room = Room(point, width, height)

            if not self.__has_collision(new_room):
                self.rooms.append(new_room)
                for p in new_room.coordinates:
                    index = self.map.index(p)
                    self.map[index] = p
            

    def __generate_corridors(self):
        
        rooms = self.rooms

        for i in range(len(rooms) - 1):
            first_room = rooms[i]
            second_room = rooms[i+1]
            

            valid_points = [p for p in first_room.board 
                        if 2 < p.x < self.width-1 and 2 < p.y < self.height-1]
            if not valid_points:
                continue
            rand_point_first = random.choice(valid_points)

            valid_points = [p for p in second_room.board 
                        if 2 < p.x < self.width-1 and 2 < p.y < self.height-1]
            if not valid_points:
                continue
            rand_point_second = random.choice(valid_points)

            index = self.map.index(rand_point_first)
            self.map[index] = ShadedPoint(rand_point_first.x, rand_point_first.y, Coridor.view)
            index = self.map.index(rand_point_second)
            self.map[index] = ShadedPoint(rand_point_second.x, rand_point_second.y, Coridor.view)


            path = self.__find_path(rand_point_first, rand_point_second)
            if not path:
                print(f"Не удалось соединить комнаты {i} и {i+1}")
                continue

            coridor = Coridor([rand_point_first, rand_point_second], path)
            self.coridors.append(coridor)

            for point in path:
                index = self.map.index(point)
                self.map[index] = ShadedPoint(point.x, point.y, Coridor.view)

   
    def __has_collision(self, new_room):
        for room in self.rooms:

            if ((new_room.point.x - 3 < room.point.x + room.width and
                new_room.point.x + new_room.width + 3 > room.point.x - 3 and
                new_room.point.y - 3 < room.point.y + room.height and
                new_room.point.y + new_room.height + 3 > room.point.y - 3) or
                (new_room.point.y + new_room.height -1 >= self.height) or
                (new_room.point.x + new_room.width -1 >= self.width)):
                
                return True
        return False


    def __find_path(self, start: Point, end: Point):
        visited = []
        open = [Node(start, h=_h_calculate(start, end))]

        while len(open) != 0:
            current_node = min(open, key=lambda node: node.f)

            if current_node.content == end:
                path = []
                while current_node:
                    path.append(current_node.content)
                    current_node = current_node.previous
                path.reverse()
                return path
            

            open = [node for node in open if node.content != current_node.content]
            visited.append(current_node)
            

            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:

                x = current_node.content.x + dx
                y = current_node.content.y + dy
                
                
                if any(node.content.x == x and node.content.y == y for node in visited):
                    continue
                    
                
                if 1 <= x <= self.width and 1 <= y <= self.height:
                    
                    point = next((p for p in self.map if p.x == x and p.y == y), None)
                    
                    if point is None or (point.symbol == Room.view and (point.x, point.y) != (end.x, end.y)):
                        continue
                    
                    too_close = False
                    if (point.x, point.y) != (end.x , end.y):
                        for dx2, dy2 in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                            x2, y2 = point.x + dx2, point.y + dy2
                            point2 = next((p for p in self.map if p.x == x2 and p.y == y2), None)
                            if point2 and point2.symbol == Room.view:
                                too_close = True
                                break
                        
                    if too_close:
                        continue

                    new_node = Node(
                        point,
                        current_node,
                        current_node.g + 1,
                        _h_calculate(point, end)
                    )
                    
                    existing_node = next((node for node in open if node.content == point), None)
                    
                    if existing_node is None or existing_node.f > new_node.f:
                        if existing_node:
                            open.remove(existing_node)
                        open.append(new_node)

        print("Путь не найден!")
        return []

    def __generate_exit(self):
        possible_points = []
        for room in self.rooms:
            for point in room.board:
                possible_points.append(point)

        exit_point = random.choice(possible_points)
        index = self.map.index(exit_point)
        self.map[index] = ShadedPoint(exit_point.x, exit_point.y, self.exit_view)

    def __spawn_items(self):
        possible_points = []
        for room in self.rooms:
            for point in room.coordinates:
                possible_points.append(point)

        while len(self.items) < 3:
            point = random.choice(possible_points)
            item = Part_Weapon()
            index = self.map.index(point)
            if self.map[index].shaded is None:
                self.map[index] = ShadedPoint(point.x, point.y, point.symbol, item.view)
                item.position = self.map[index]
                self.items.append(item)
    
    def spawn_key(self, point):
        key = Key()
        point.shaded = "K"
        key.position = point
        self.items.append(key)