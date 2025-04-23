import numpy as np
dict = {
    "red" : 1,
}
x = np.array(list(dict.keys()))
y = np.random.choice(x, 2)
print(y)