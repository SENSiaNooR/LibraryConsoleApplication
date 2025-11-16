
from xml.sax.handler import property_declaration_handler


class SizeAndPosition:
    """
    Represents a rectangular region defined by its position (left, top)
    and size (width, height).

    Provides properties for convenient access to `right` and `bottom` edges,
    while automatically keeping consistency between position and size.

    Attributes
    ----------
    left : int
        The x-coordinate of the left edge (non-negative).
    top : int
        The y-coordinate of the top edge (non-negative).
    width : int
        The width of the rectangle (must be >= 1).
    height : int
        The height of the rectangle (must be >= 1).
    right : int
        The x-coordinate of the right edge (derived).
    bottom : int
        The y-coordinate of the bottom edge (derived).
    """

    def __init__(self, left: int = 0, top: int = 0, height: int = 1, width: int = 1):
        self.left = left
        self.top = top
        self.height = height
        self.width = width

    @property
    def top(self):
        return self._y

    @top.setter
    def top(self, top):
        if not isinstance(top, int):
            raise TypeError("top must be an integer")
        if top < 0:
            raise ValueError("top cannot be negative")
        self._y = top

    @property
    def left(self):
        return self._x

    @left.setter
    def left(self, left):
        if not isinstance(left, int):
            raise TypeError("left must be an integer")
        if left < 0:
            raise ValueError("left cannot be negative")
        self._x = left

    @property
    def width(self):
        return self._w

    @width.setter
    def width(self, width):
        if not isinstance(width, int):
            raise TypeError("width must be an integer")
        if width < 1:
            raise ValueError("width cannot be zero or negative")
        self._w = width

    @property
    def height(self):
        return self._h

    @height.setter
    def height(self, height):
        if not isinstance(height, int):
            raise TypeError("height must be an integer")
        if height < 1:
            raise ValueError("height cannot be zero or negative")
        self._h = height

    @property
    def right(self):
        return self._x + self._w

    @right.setter
    def right(self, right):
        if not isinstance(right, int):
            raise TypeError("right must be an integer")
        if right <= self._x:
            raise ValueError("right cannot be less than or equal to left")
        self._w = right - self._x

    @property
    def bottom(self):
        return self._y + self._h

    @bottom.setter
    def bottom(self, bottom):
        if not isinstance(bottom, int):
            raise TypeError("bottom must be an integer")
        if bottom <= self._y:
            raise ValueError("bottom cannot be less than or equal to top")
        self._h = bottom - self._y
        
    @property
    def x_center(self):
        return self._x + self._w / 2
    
    @property
    def y_center(self):
        return self._y + self._h / 2

    def __repr__(self):
        return f"{self.__class__.__name__}(left={self._x}, top={self._y}, height={self._h}, width={self._w})"

    def __str__(self):
        return f"SizeAndPosition: left={self._x}, top={self._y}, width={self._w}, height={self._h}"

    def __eq__(self, other):
        if not isinstance(other, SizeAndPosition):
            return NotImplemented
        return (self._x, self._y, self._w, self._h) == (other._x, other._y, other._w, other._h)

