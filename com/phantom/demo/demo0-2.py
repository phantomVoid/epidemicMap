# 功能：绘制z=x^2 + y^2 三维图像
# 时间：2019/10/1
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D   #1
import numpy as np

def do_plt():
    plt.figure()
    ax = plt.axes(projection="3d")

    x_rang_max = 1000
    x_rang_min = -10

    y_rang_max = 1000
    y_rang_min = -10

    x = np.arange(x_rang_min,x_rang_max,0.1)
    y = np.arange(y_rang_min,y_rang_max,0.1)
    X,Y = np.meshgrid(x,y)    # 2生成绘制3D图形所需的网络数据
    # Z = X**2+Y**2
    Z = (851600 - 230 * (X + Y)) / 224

    ax.plot_surface(X,Y,Z,alpha=0.5,cmap="winter") #生成表面，alpha用于控制透明度
    ax.contour(X,Y,Z,zdir="x",offset=-6,cmap="rainbow")   #x轴投影
    ax.contour(X,Y,Z,zdir="y",offset=6,cmap="rainbow")    #y轴投影
    ax.contour(X,Y,Z,zdir="z",offset=-3,cmap="rainbow")   #z轴投影
    ax.set_xlabel("X")  #设置X、Y、Z 坐标范围
    # ax.set_xlim(x_rang_min,x_rang_max)   #设置X、Y、Z 轴
    ax.set_ylabel("Y")
    # ax.set_ylim(y_rang_min,y_rang_max)
    ax.set_zlabel("Z")
    plt.show()

if __name__ == '__main__':
    do_plt()
