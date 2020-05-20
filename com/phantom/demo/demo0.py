import numpy as np
import matplotlib.pyplot as plt

x = y = np.arange(-5, 5, 0.1)


x1=[-3.064177772475912,0,3.6252311481465997,-3.064177772475912]
y1=[-2.571150438746157,4,-1.6904730469627978,-2.571150438746157]

x, y = np.meshgrid(x,y)
plt.contour(x, y, 230*x + 224*y, [16])     #x**2 + y**2 = 9 的圆形
plt.plot(0,0,'r.')
plt.plot(x1,y1,'r-')

plt.axis('scaled')
plt.show()