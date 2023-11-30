import numpy as np
from numpy import poly1d


fu = poly1d([4.525,-68.16666667,388.54166667,-1035.33333333,1268.43333333,-553])
fv = poly1d([-7.53333333,136.33333333,-920.33333333,2831.66666667,-3844.13333333,1809])
fw = poly1d([-13.30833333,254.83333333,-1791.625,5651.66666667,-7723.56666667,3647])

t = poly1d([1, -1])*poly1d([1, -2])*poly1d([1, -3])*poly1d([1, -4])*poly1d([1, -5])*poly1d([1, -6])

(h, reste) = ((fu * fv)-fw)/t

print("h \n", h)
print("reste \n", reste)
