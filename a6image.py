"""
The main class for our imager application.

This modules contains a single class. Instances of this class support an image
that can be modified. This is the main class needed to display images in the
viewer.

Based on an original file by Dexter Kozen (dck10) and Walker White (wmw2)

YOUR NAME(S) AND NETID(S) HERE
DATE COMPLETED HERE
"""

def _is_pixel(item):
    """
    Returns True if item is a pixel, False otherwise.

    A pixel is a tuple of 3 ints in the range 0..255

    Parameter item: The item to check
    Precondition: NONE (item can be anything)
    """
    if not isinstance(item, tuple) or len(item) != 3:
        return False

    for ii in range(3):
        if not isinstance(item[ii], int) or item[ii] < 0 or item[ii] > 255:
            return False

    return True


# TASK 0: IMPLEMENT THIS HELPER
def _is_pixel_list(data):
    """
    Returns True if data is a pixel list, False otherwise.

    A pixel list is a 1-dimensional list of pixels where a pixel is a tuple
    of 3 ints in the range 0..255

    Parameter data: The data to check
    Precondition: NONE (data can be anything)
    """
    if not isinstance(data, list):
        return False

    for item in data:
        if not _is_pixel(item):
            return False

    return True


# TASK 1: IMPLEMENT THIS CLASS
class Image(object):
    """
    A class that allows flexible access to an image pixel list

    One of the things that we will see in this assignment is that sometimes
    you want to treat an image as a flat 1D list and other times you want to
    treat it as a 2D list. This class has methods that allow you to go back
    and forth between the two.

    If you want to treat the image like a 2D list, you use the methods
    `getPixel` and `setPixel`. As with the Pixels class, pixels are represented
    as 3-element tuples, with each element in the range 0..255.  For example,
    red is (255,0,0). These methods are used by many of the Instagram-style
    filter functions.

    If you want to treat the image like a 1D list you use the methods
    `getFlatPixel` and `setFlatPixel`. These methods are used by the greyscale
    and stenography methods.
    """
    # IMMUTABLE ATTRIBUTES (Fixed after initialization)
    # Attribute _data: The underlying list of pixels
    # Invariant: _data is a pixel list (see _is_pixel_list)
    #
    # MUTABLE ATTRIBUTES (Can be changed at any time, via the setters)
    # Attribute _width:  The image width, which is the number of columns
    # Invariant: _width is an int > 0, _width*_height = len(_data).
    # width = 0 only if len(_data) = 0
    #
    # Attribute _height:  The image height, which is the number of rows
    # Invariant: _height is an int > 0, _width*_height = len(_data)
    # height = 0 only if len(_data) = 0
    # Note that if you change width, you must change height (to satisfy the
    # invariant)

    # PART A
    # GETTERS AND SETTERS
    def getPixels(self):
        """
        Returns a COPY of the pixel list for this image

        Copying an image is incredibly expensive. You should ABSOLUTELY NEVER
        use this method as a helper in any of your other methods in this
        assignment. It is only used internally by the GUI.
        """
        return self._data[:]

    def getLength(self):
        """
        Returns the number of pixels in this image
        """
        return len(self._data)

    def getWidth(self):
        """
        Returns the image width

        A value width is an int evenly dividing the number of pixels in the
        image. Width can only be 0 if the image is empty.
        """
        return self._width

    def setWidth(self,value):
        """
        Sets the image width to value, assuming it is valid.

        If the width changes, then height must change to so that we preserve
        width*height == # of pixels. This can only happen if the value is valid.

        The value is valid if it is an int and it evenly divides the number of
        pixels in the image. If the pixel list has 10 pixels, a valid width is
        1, 2, 5, or 10. Width can only be 0 if the image is empty.

        Parameter value: the new width value
        Precondition: value is a valid width >= 0
        """
        assert isinstance(value, int), 'width is not an int'
        assert value >= 0, 'width is negative'
        if len(self._data) == 0:
            assert value == 0, 'width must be 0 for an empty image'
            self._width = 0
            self._height = 0
        else:
            assert value > 0, 'width must be positive for a non-empty image'
            assert len(self._data) % value == 0, 'width does not divide length'
            self._width = value
            self._height = len(self._data) // value

    def getHeight(self):
        """
        Returns the image height

        A value height is an int evenly dividing the number of pixels in the
        image. Height can only be 0 if the image is empty.
        """
        return self._height

    def setHeight(self,value):
        """
        Sets the image height to value, assuming it is valid.

        If the height changes, then width must change to so that we preserve
        width*height == # of pixels. This can only happen if the value is valid.

        The value is valid if it is an int and it evenly divides the number of
        pixels in the image. If the pixel list has 10 pixels, a valid height is
        1, 2, 5, or 10. Height can only be 0 if the image is empty.

        Parameter value: the new height value
        Precondition: value is a valid height >= 0
        """
        assert isinstance(value, int), 'height is not an int'
        assert value >= 0, 'height is negative'
        if len(self._data) == 0:
            assert value == 0, 'height must be 0 for an empty image'
            self._width = 0
            self._height = 0
        else:
            assert value > 0, 'height must be positive for a non-empty image'
            assert len(self._data) % value == 0, 'height does not divide length'
            self._height = value
            self._width = len(self._data) // value

    # INITIALIZER
    def __init__(self, data, width):
        """
        Initializes an Image from the given pixel list.

        A pixel list is a 1-dimensional list of pixels where a pixel is a
        tuple of 3 ints in the range 0..255. The pixel list contains the
        image data. You do not need to worry about loading an image file.
        That happens elsewhere in the application (in code that you did not
        write).

        Note that this initializer stores a reference to data in this object.
        It does NOT copy the data. So changes to the image will change the data
        parameter as well.

        In order to be valid, the width  must evenly divide the number of pixels
        in the image. So if the pixel list has 10 pixels, a valid width is
        1, 2, 5, or 10. The height is not given explicitly, but you must compute
        it from the width and pixel list length.

        Parameter data: The image data as a pixel list
        Precondition: data is a pixel list

        Parameter width: The image width
        Precondition: width is an int > 0 and evenly divides the length of pixels
        """
        assert _is_pixel_list(data), 'data is not a pixel list'
        assert isinstance(width, int), 'width is not an int'
        if len(data) == 0:
            assert width == 0 or width > 0, 'width is invalid'
            self._data = data
            self._width = 0
            self._height = 0
        else:
            assert width > 0, 'width must be positive'
            assert len(data) % width == 0, 'width does not divide length'
            self._data = data
            self._width = width
            self._height = len(data) // width

    # PART B
    # ONE-DIMENSIONAL ACCESS METHODS
    def getFlatPixel(self, n):
        """
        Returns pixel number n of the image (from the underlying pixel list)

        This method is used when you want to treat an image as a flat,
        one-dimensional list rather than a 2-dimensional image.  It is useful
        operations that do not depend on the pixel location.

        The value returned is a 3-element tuple (r,g,b).

        Parameter n: The pixel number to access
        Precondition: n is an int >= 0 and < length (of the pixel list)
        """
        assert isinstance(n, int), 'n is not an int'
        assert 0 <= n < len(self._data), 'n is out of range'
        return self._data[n]

    def setFlatPixel(self, n, pixel):
        """
        Sets pixel number n of the image (from the underlying pixel list) to pixel

        This method is used when you want to treat an image as a flat,
        one-dimensional list rather than a 2-dimensional image.  It is useful
        operations that do not depend on the pixel location.

        The value returned is a 3-element tuple (r,g,b).

        Parameter n: The pixel number to access
        Precondition: n is an int >= 0 and < length (of the pixel list)

        Parameter pixel: The pixel value
        Precondition: pixel is a 3-element tuple (r,g,b) where each value is 0..255
        """
        assert isinstance(n, int), 'n is not an int'
        assert 0 <= n < len(self._data), 'n is out of range'
        assert _is_pixel(pixel), 'pixel is not a valid pixel'
        self._data[n] = pixel

    # PART C
    # TWO-DIMENSIONAL ACCESS METHODS
    def getPixel(self, row, col):
        """
        Returns the pixel value at (row, col)

        Remember that this way of accessing a pixel is essentially (y,x) since
        height is the number of rows and width is the number of columns.

        The value returned is a 3-element tuple (r,g,b).

        Parameter row: The pixel row
        Precondition: row is an int >= 0 and < height

        Parameter col: The pixel column
        Precondition: col is an int >= 0 and < width
        """
        assert isinstance(row, int), 'row is not an int'
        assert isinstance(col, int), 'col is not an int'
        assert 0 <= row < self._height, 'row is out of range'
        assert 0 <= col < self._width, 'col is out of range'
        return self._data[row*self._width + col]

    def setPixel(self, row, col, pixel):
        """
        Sets the pixel value at (row, col) to (a copy of) pixel

        Remember that this way of setting a pixel is essentially (y,x) since
        height is the number of rows and width is the number of columns.

        Parameter row: The pixel row
        Precondition: row is an int >= 0 and < height

        Parameter col: The pixel column
        Precondition: col is an int >= 0 and < width

        Parameter pixel: The pixel value
        Precondition: pixel is a 3-element tuple (r,g,b) of ints in 0..255
        """
        assert isinstance(row, int), 'row is not an int'
        assert isinstance(col, int), 'col is not an int'
        assert 0 <= row < self._height, 'row is out of range'
        assert 0 <= col < self._width, 'col is out of range'
        assert _is_pixel(pixel), 'pixel is not a valid pixel'
        self._data[row*self._width + col] = pixel

    # PART D
    def __str__(self):
        """
        Returns: The string representation of this image.

        The string should be displayed as a 2D list of pixels in row-major
        order. For example, suppose the image data is

            [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 0, 0), (128, 0, 0), (0, 128, 0)]

        If the width (which is the number of columns) is two, the string
        should be

            '[[(255, 0, 0), (0, 255, 0)],\n[(0, 0, 255), (0, 0, 0)],\n[(128, 0, 0), (0, 128, 0)]]

        Note the newlines (\n) after each row. That is because when you print
        this string, it will look like this:

            [[(255, 0, 0), (0, 255, 0)],
            [(0, 0, 255), (0, 0, 0)],
            [(128, 0, 0), (0, 128, 0)]]

        This is useful for debugging, since it allows us to see each row of the
        image on its own line.

        There should be spaces after the commas but no where else. Tuples
        (the individual pixels) handle this  part for you automatically, but you
        need to handle the commas between pixels and the newlines between rows.
        """
        result = '['
        for row in range(self._height):
            if row > 0:
                result += ',\n'
            result += '['
            for col in range(self._width):
                if col > 0:
                    result += ', '
                result += str(self.getPixel(row, col))
            result += ']'
        result += ']'
        return result

    # ADDITIONAL METHODS (WE HAVE PROVIDED THESE FOR YOU)
    def swapPixels(self, row1, col1, row2, col2):
        """
        Swaps the pixel at (row1, col1) with the pixel at (row2, col2)

        Parameter row1: The pixel row to swap from
        Precondition: row1 is an int >= 0 and < height

        Parameter col1: The pixel column to swap from
        Precondition: col1 is an int >= 0 and < width

        Parameter row2: The pixel row to swap to
        Precondition: row1 is an int >= 0 and < height

        Parameter col2: The pixel column to swap to
        Precondition: col2 is an int >= 0 and < width
        """
        # NOTE: We DO NOT need to enforce any preconditions here.
        # They should be enforced already in getPixel and setPixel.
        temp = self.getPixel(row1, col1)
        self.setPixel(row1, col1, self.getPixel(row2, col2))
        self.setPixel(row2, col2, temp)

    def copy(self):
        """
        Returns a copy of this image object.

        The underlying pixel data must be copied (e.g. the copy cannot refer
        to the same list of pixels that this object does).
        """
        return Image(self.getPixels(),self.getWidth())
