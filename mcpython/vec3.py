class Vec3:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, rhs):
        c = self.clone()
        c += rhs
        return c

    def __iadd__(self, rhs):
        self.x += rhs.x
        self.y += rhs.y
        self.z += rhs.z
        return self

    def length(self):
        return self.lengthSqr() ** .5

    def lengthSqr(self):
        return self.x * self.x + self.y * self.y  + self.z * self.z

    def __mul__(self, k):
        c = self.clone()
        c *= k
        return c

    def __imul__(self, k):
        self.x *= k
        self.y *= k
        self.z *= k
        return self

    def clone(self):
        return Vec3(self.x, self.y, self.z)

    def __neg__(self):
        return Vec3(-self.x, -self.y, -self.z)

    def __sub__(self, rhs):
        return self.__add__(-rhs)

    def __isub__(self, rhs):
        return self.__iadd__(-rhs)

    def __truediv__(self, k):
        return self.__mul__(1/k)

    def __itruediv__(self, k):
        return self.__imul__(1/k)

    def __repr__(self):
        return "Vec3(%s,%s,%s)"%(self.x,self.y,self.z)

    def __iter__(self):
        return iter((self.x, self.y, self.z))

    def _map(self, func):
        self.x = func(self.x)
        self.y = func(self.y)
        self.z = func(self.z)

    def __cmp__(self, rhs):
        dx = self.x - rhs.x
        if dx != 0: return dx
        dy = self.y - rhs.y
        if dy != 0: return dy
        dz = self.z - rhs.z
        if dz != 0: return dz
        return 0

    def __eq__(self, rhs):
        if self.x == rhs.x and self.y == rhs.y and self.z == rhs.z:
            return True

        return False

    def iround(self): self._map(lambda v:int(v+0.5))
    def ifloor(self): self._map(int)

    def unit(self):
        c = self.clone()
        c  = c/c.length()
        return c
    
    def isclose(self, rhs, rel_tol=1e-09, abs_tol = 0.0):
        """
        Determine if two Vec3s are close.  Adapted from math.isclose

        :param rhs: right hand side vector
        :type rhs: Vec3
        :param rel_tol: the relative tolerance – it is the maximum allowed difference between 
            self.? and rhs.?, relative to the larger absolute value of self.? or rhs.?. 
            For example, to set a tolerance of 5%, pass rel_tol=0.05. The default tolerance 
            is 1e-09, which assures that the two values are the same within about 9 decimal digits. 
            rel_tol must be greater than zero.
        :type rel_tol: float
        :param abs_tol: is the minimum absolute tolerance – useful for comparisons near zero. 
            abs_tol must be at least zero.
        :type abs_tol: float

        :return: False if any instance of abs(self.?-rhs.?) <= max(rel_tol * max(abs(self.?), abs(rhs.?)), abs_tol) is False
        :retype: bool
        """
        if abs(self.x-rhs.x) > max(rel_tol * max(abs(self.x), abs(rhs.x)), abs_tol):
            return False
        elif abs(self.y-rhs.y) > max(rel_tol * max(abs(self.y), abs(rhs.y)), abs_tol):
            return False
        elif abs(self.z-rhs.z) > max(rel_tol * max(abs(self.z), abs(rhs.z)), abs_tol):
            return False
        return True

    def rotateLeft(self):  self.x, self.z = self.z, -self.x
    def rotateRight(self): self.x, self.z = -self.z, self.x

def testVec3():
    # Note: It's not testing everything

    # 1.1 Test initialization
    it = Vec3(1, -2, 3)
    assert it.x == 1
    assert it.y == -2
    assert it.z == 3

    assert it.x != -1
    assert it.y != +2
    assert it.z != -3

    # 2.1 Test cloning and equality
    clone = it.clone()
    assert it == clone
    it.x += 1
    assert it != clone

    # 3.1 Arithmetic
    a = Vec3(10, -3, 4)
    b = Vec3(-7, 1, 2)
    c = a + b
    assert c - a == b
    assert c - b == a
    assert a + a == a * 2

    assert a - a == Vec3(0,0,0)
    assert a + (-a) == Vec3(0,0,0)

    # Test repr
    e = eval(repr(it))
    assert e == it

if __name__ == "__main__":
    testVec3()
