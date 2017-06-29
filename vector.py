"""
@author: Stefan Karan Singh Marwah
@Date: 03/06/2017

"""
import math
from decimal import Decimal, getcontext

class Vector(object):

    CANNOT_NORMALIZE_ZERO_VECTOR_MSG = "Cannot normalize the zero vector"
    NO_UNIQUE_ORTHOGONAL_MSG = "There is no unique orthogonal vector"
    NO_UNIQUE_PARALLEL_COMPONENT_MSG = "There is no unique parallel component"
    ONLY_DEFINEDIN_TWO_THREE_DIMS_MSG = "Can only carry out action on two or three dimension vector"

    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(x) for x in coordinates])
            self.dimension = len(self.coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')

    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)

    def __eq__(self, v):
        return self.coordinates == v.coordinates

    def add_(self,v):
      return Vector([x + y for x,y in zip(self.coordinates,v.coordinates)])

    def sub_(self,v):
        return Vector([x-y for x,y in zip(self.coordinates,v.coordinates)])

    def times_scalar(self,c):
        return Vector([Decimal(c)*x for x in self.coordinates])

    def magnitude_(self):
        return math.sqrt(sum(x**2 for x in self.coordinates))

    def normalize_(self):
        try:
            return(self.times_scalar(Decimal('1.0')/self.magnitude_()))
        except ZeroDivisionError:
            raise(self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG)

    def dot_(self,v):
         return sum([x*y for x,y in zip(self.coordinates,v.coordinates)])

    def angle_with_(self,v,in_degrees=False):
        try:
            if in_degrees:
                return math.degrees(math.acos(self.dot_(v)/(Decimal(self.magnitude_())*Decimal(v.magnitude_()))))
            else:
                return math.acos(self.dot_(v)/(Decimal(self.magnitude_())*Decimal(v.magnitude_())))

        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception('Cannot compute an angle with a zero vector')
            else:
                raise e

    def is_orthogonal_to(self,v,tolerance=1e-10):
        return abs(self.dot_(v)) < tolerance

    def is_parallel_to(self,v):
        return ( self.is_zero()
                 or v.is_zero()
                 or self.angle_with_(v) == 0
                 or self.angle_with_(v) == math.pi)

    def is_zero(self,tolerance=1e-10):
        return self.magnitude_() < tolerance

    def component_orthogonal_to(self,basis):
        try:
            return self.sub_(self.component_parallel_to(basis))
        except Exception as e:
            if str(e) == self.NO_UNIQUE_PARALLEL_COMPONENT_MSG:
                raise Exception(self.NO_UNIQUE_ORTHOGONAL_MSG)
            else:
                e

    def component_parallel_to(self,basis):
        try:
            u = basis.normalize_()
            weight = self.dot(u)
            return u.times_scalar(weight)
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception(self.NO_UNIQUE_PARALLEL_COMPONENT_MSG)
            else:
                e

    def cross_(self,v):
        try:
            x_1,y_1,z_1 = self.coordinates
            x_2,y_2,z_2 = v.coordinates
            return Vector([ y_1*z_2 - y_2*z_1,
                            -(x_1*z_2 - x_2*z_1),
                             x_1*y_2 - x_2*y_1
                            ])
        except ValueError as e:
            msg = str(e)
            if msg == 'need more than 2 values to unpack':
                self_embedded_in_R3 = Vector(self.coordinates + ('0',))
                v_embedded_in_R3 = Vector(v.coordinates + ('0',))
                return self_embedded_in_R3.cross_(v_embedded_in_R3)
            elif (msg == "too many values to unpack" or msg == "need more than 1 value to unpack"):
                raise Exception(self.ONLY_DEFINEDIN_TWO_THREE_DIMS_MSG)
            else:
                raise e

    def area_parallelogram(self,v):
        return self.cross_(v).magnitude_()

    def area_triangle(self,v):
        return 0.5* self.area_parallelogram(v)


#v = Vector([8.462,7.893,-8.187])
#w = Vector([6.984,-5.975,4.778])
#print(v.cross_product_(w))

#v = Vector([-8.987,-9.838,5.031])
#w = Vector([-4.268,-1.861,-8.866])
#c = v.cross_product_(w)
#print(c.area_parallelogram())



v = Vector([1.5,9.547,3.691])
w = Vector([-6.007,0.124,5.772])
print(v.area_triangle(w))
