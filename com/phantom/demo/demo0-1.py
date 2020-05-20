from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  #此模块并非不用，如果缺少了会引起三维坐标的创建ValueError: Unknown projection '3d
import numpy as np

fig = plt.figure()
ax1 = plt.axes(projection="3d")

x = np.arange(0,851600,0.1)
y = np.arange(0,851600,0.1)
Z = (851600-230*(x+y))/224

ax1.plot3D(x,y,Z,"red")
plt.show()
