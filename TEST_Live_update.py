import matplotlib.pyplot as plt
import numpy as np
import time

plt.ion()  # Interactive mode on
fig, ax = plt.subplots()
x = []
y = []

for i in range(50):
    x.append(i)
    y.append(np.random.random())
    ax.clear()
    ax.plot(x, y)
    plt.draw()
    plt.pause(0.1)  # Pause briefly to update plot

plt.ioff()
plt.show()
