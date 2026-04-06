# import numpy as np

# arr = np.array([1, 2, 3, 4, 5])

# print(arr)
# print(type(arr))
# print(len(arr))

# import numpy as np
# a1D = np.array([1, 2, 3, 4])

# a2D = np.array([[1, 2], 
#                 [3, 4]])

# a3D = np.array([[[1, 2], 
#                   [3, 4]], 
#                   [[5, 6], 
#                   [7, 8]
#                       ]])

# print(a1D)
# print(a2D)
# print(a3D)

# Create an array with 5 dimensions and verify that it has 5 dimensions:


import numpy as np
import time
start = time.time()

arr = np.array([1, 2, 3, 4], ndmin=5)
print(arr)
print('number of dimensions :', arr.ndim)

end = time.time()
print("Execution time :", end - start)

