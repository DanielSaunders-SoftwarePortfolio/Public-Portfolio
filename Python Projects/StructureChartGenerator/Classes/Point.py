def sqrt(value):
    return value**(1/2)

class Point:
    def __init__(self, x:float=0, y:float=0) -> None:
        self._x = x
        self._y = y
    
    def __add__(self, value:'Point') -> 'Point':
        x = value.get_x()
        y = value.get_y()
        return Point(x, y)

    def __add__(self, value:float) -> float:
        '''
        When adding a number to a point, take the distance between the point 
        and the origin and add the value, then find the new x and y components.
        '''
        slope = self._y/self._x
        # Using the pythagorean theorum the following line finds the x 
        # component of the new length 
        x = sqrt(value**2/(1+slope**2)) 
        # The y component is just the x component times the slope.
        y = slope * x
        # Add the original x and y values to get the new x and y values
        x += self._x
        y += self._y
        return Point(x, y)
    
    def __sub__(point1, point2:'Point') -> 'Point':
        x = point1._x - point2._x
        y = point1._y - point2._y
        return Point(x, y)
    
    def __sub__(self, value:float) -> float:
        # subtracting a value is the same as adding the negative value
        return self + (-1*value)
    
    def __rsub__(self, value:float) -> float:
        '''
        When subtracting a point from a number, we use the magnitude of the 
        point (a float) so that we return the same data type as the left side
        of the opperator used.
        '''
        return value - self.get_magnitude()
    
    def __radd__(self, value:float) -> float:
        '''
        When adding a point to a number in this order, we use the magnitude 
        of the point (a float) so that we return the same data type as the 
        left side of the opperator used.
        '''
        return value + self.get_magnitude()
    
    def __mul__(point1, point2:'Point') -> 'Point':
        x = point1._x * point2._x
        y = point1._y * point2._y
        return Point(x, y)
    
    def __rmul__(self, value:float) -> float:
        return self.get_magnitude() * value

    def copy(self) -> 'Point':
        return Point(self._x, self._y)

    def get_x(self) -> float:
        '''Return x of self'''
        return self._x
    
    def set_x(self, new_x) -> None:
        '''Change value of x'''
        self._x = new_x
    
    def get_y(self) -> float:
        '''Return y of self'''
        return self._y
    
    def set_y(self, new_y) -> None:
        '''Change value of y'''
        self._y = new_y
    
    def get_magnitude(self) -> float:
        '''Return the distance between this point and the origin'''
        magnitude = (self._x**2 + self._y**2)**(1/2) # sqrt(x^2 + y^2)
        return magnitude
    
    def __str__(self) -> str:
        return(f'({self._x:.2f}, {self._y:.2f})')
    
    def __int__(self) -> int:
        return int(self.get_magnitude())
    
    def __float__(self) -> float:
        return float(self.get_magnitude())
    
    def to_list(self):
        return int(self._x), int(self._y)
    
    def __iter__(self) -> tuple:
        yield from self.to_list()

    def __repr__(self):
        return str(self)
