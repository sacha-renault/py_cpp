from cumulative.cumulative import cumsum
import numpy as np

array = np.random.randint(0,10,10)
print("CUM SUM INT")
print(cumsum(array))

array = np.random.rand(10)
print("CUM SUM FLOAT")
print(cumsum(array))