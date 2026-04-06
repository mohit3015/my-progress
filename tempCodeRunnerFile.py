# import numpy as np

# a = np.array([[2,5],[7,8]])
# print(a*7)

import numpy as np

import pandas as pd

# # Arrays
# a = np.array([[2,3,4,1],
#               [4,2,3,1]])
# b = np.array([[2,1,3,2],
#               [3,2,4,1]])

# # Square matrix
# c = np.array([[2,3],
#               [4,1]])

# print("Dot Product:\n",      np.dot(a, b.T))
# print("Matrix Multiply:\n",  np.matmul(a, b.T))
# print("Inverse:\n",          np.linalg.inv(c))
# print("Determinant:\n",      np.linalg.det(c))

# val, vec = np.linalg.eig(c)
# print("Eigenvalues:\n",      val)
# print("Eigenvectors:\n",     vec)

students_details = {"Name" : ['Mohit', 'Munna', 'Amit', 'Manoj', 'Roshan'],
                    "Age" : [21,19,20,22,12],
                    "City" : ['Delhi', 'Mumbai', 'jharkhand', 'Giridih', 'Pindatand']}
print(students_details)

d1 = pd.DataFrame(students_details)
print(d1)