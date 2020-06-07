import time
import numpy as np
import matplotlib.pyplot as plt
min_range = 1000
max_range = 2000

start_time = time.time()
for i in range(min_range,max_range):
    x=i
    for o in range(min_range,max_range):
        y=o
        for p in range(min_range,max_range):
            z=p
            if 230*x+230*y+224*z==851600:
                print('230*%s+230*%s+224*%s=851600' %(x,y,z))

end_time = time.time()
project_time = end_time - start_time
print('程序用时', project_time)

x, y = np.meshgrid(x,y)
plt.contour(x, y, 230*x + 224*y, [16])     #x**2 + y**2 = 9 的圆形
plt.plot(0,0,'r.')
plt.plot(x1,y1,'r-')