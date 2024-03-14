import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.animation as animation

"""
 1.參數設定
"""
L, N, k, cut = 6, 200, 5*2, 1.5 # 0.5倍寬度, 每邊分割數量, 角波數, z軸範圍
fps, frn = 12, 25         # 每秒影格數量, 影格總數
x = np.linspace(-2*L, 2*L, N)   # x軸
y = np.linspace(-L, L, N)   # y軸
X, Y = np.meshgrid(x, y)    # 組成2維陣列
j = complex(0, 1)        # 根號 -1

"""
 2.設定計算振幅的函數, 計算每個位置的振幅並存入陣列
"""
# 自訂函式, 計算每個位置對應的振幅


def func(x, y, t, n, a, b):
 
    for i in range(n):
        r = np.sqrt((x-a[i])**2 + (y-b[i])**2)
        if(i == 0):
            z = np.exp(j*k*r)*np.exp(-r/100)
        else:
            z += np.exp(j*k*r)*np.exp(-r/100)
    z=np.round(z,5)
    return np.real(z*np.exp(-j*t))    # 回傳實部


Z = np.zeros((N, N, frn))   # 儲存振幅用的2維陣列
T = np.linspace(0, 2*np.pi, frn)   # 儲存時間用的1維陣列

# user input
n=int(input("輸入波源數量:"))
print('點波源位置輸入格式: x , y')
a=[]
b=[]
for i in range(n):
  temp=input(f"位置{i}:").split(',')
  a.append(int(temp[0]))
  b.append(int(temp[1]))

# 計算每個時刻每個位置對應的振幅
for i in range(frn):
    Z[:, :, i] = func(X, Y, T[i], n,a,b).clip(-cut, cut)

"""
 3.繪圖
"""

fig = plt.figure(figsize=(7, 6), dpi=100)   # 開啟繪圖視窗
ax = fig.gca()
ax.set_aspect(1.0)   # 使圖片長寬變成1:1

# 以某個預設的colormap為基底, 修改成對應到 -cut ~ +cut 的colormap
mappable = plt.cm.ScalarMappable(cmap=plt.cm.jet)
mappable.set_array(np.arange(-cut, cut, 0.1))

# 在圖片右側加上color bar, 高度與圖片相同
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1)
plt.colorbar(mappable, cax=cax)

# 自訂函式, 先移除前一張圖, 再畫出下一張圖
def update(frame_number):
    plot[0] = ax.contourf(X, Y, Z[:, :, frame_number], cmap=mappable.cmap, norm=mappable.norm)

# t = 0 的圖片
plot = [ax.contourf(X, Y, Z[:, :, 0], cmap=mappable.cmap, norm=mappable.norm)]

# 產生動畫, 目標為繪圖物件fig, 使用自訂函式update更新圖片, 圖片總數為frn, 時間間隔為interal, 單位為ms
ani = animation.FuncAnimation(fig, update, frn, interval=1000/fps)

plt.show()   # 顯示圖片
