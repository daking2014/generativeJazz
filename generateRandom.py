import numpy as np
import random

for i in range(16):
    rand = [random.randint(0,36) for j in range(192)]
    np.save('simpleResults\\random_'+str(i), rand)