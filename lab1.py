import time
# finland_flag_split.py
COL, ROW = 36,10
off   = 10          # 竖条左边距
thick_h = 2        # 横条厚度（行数）
thick_w = 6        # 竖条厚度（列数）

for r in range(ROW):
    line = ""
    for c in range(COL):
        in_h = (ROW - thick_h) // 2 <= r < (ROW + thick_h) // 2   # 横条
        in_v = off <= c < off + thick_w                           # 竖条
        line += "\033[44m \033[0m" if in_h or in_v else "\033[107m \033[0m"
    print(line)
    time.sleep(0.2)





r = 10
# 遍历y轴（垂直方向覆盖单个圆的范围）
for y in range(-r, r + 1):
    # 遍历x轴（水平方向覆盖两个圆：从-2r到2r）
    for x in range(-2 * r, 2 * r + 1):
        # 第一个圆：圆心(-r, 0)，判断点是否在圆内（含边缘）
        in_circle1 = (x + r)**2 + y**2 <= r**2
        # 第二个圆：圆心(r, 0)，判断点是否在圆内（含边缘）
        in_circle2 = (x - r)** 2 + y**2 <= r**2
        # 只要在任意一个圆内，就打印*，否则打印空格
        if in_circle1 or in_circle2:
            print("*", end="")
        else:
            print(" ", end="")
    # 每行结束后换行
    print()



print("          function: y=x/2")
def simple_function_graph():
    # 确定x的取值范围（第一象限，0到16）
    x_values = list(range(0, 11))

    # 生成y坐标（从8.0到0.0，共11行）
    y_coord = [i * 0.5 for i in range(10, -1, -1)]

    # 绘制图形
    for y in y_coord:
        print(f"{y:7.1f} |", end="")
        for x in x_values:
            if abs(y - x / 2) < 0.4:  # 容差判断
                print(" *", end="")
            else:
                print("  ", end="")
        print()

# 打印分隔线
    print("-" * (15 + len(x_values) * 2))

 # 打印表头
    print("function  0 1 2 3 4 5 6 7 8 9 10", end="")

# 运行
simple_function_graph()




# 读取文件中的数字
numbers = []
with open(r'C:\Users\zyp92\OneDrive\桌面\linux\sequence.txt', 'r') as file:
    for line in file:
        numbers.append(float(line.strip()))

# 统计两个区间的数字数量
count_5_to_10 = 0
count_neg5_to_neg10 = 0

for num in numbers:
    if 5 <= num <= 10:
        count_5_to_10 += 1
    elif -10 <= num <= -5:
        count_neg5_to_neg10 += 1

# 计算总数和百分比
total = count_5_to_10 + count_neg5_to_neg10
percent_5_to_10 = (count_5_to_10 / total) * 100
percent_neg5_to_neg10 = (count_neg5_to_neg10 / total) * 100

# 在控制台绘制条形图
print("\n        диаграмму процентного соотношения")
print("=" * 50)

# 5到10的条形
bar_5_to_10 = "█" * int(percent_5_to_10 / 2)
print(f" 5 ~  10: {bar_5_to_10} {percent_5_to_10:.1f}%")

# -5到-10的条形
bar_neg5_to_neg10 = "█" * int(percent_neg5_to_neg10 / 2)
print(f"-5 ~ -10: {bar_neg5_to_neg10} {percent_neg5_to_neg10:.1f}%")

print("=" * 50)
print(f"Всего: {total} номеров")

import os
import time

# 定义3个动画帧
frames = ["(*_*)","(-_-)","(o_o)"]

# 播放动画
try:
    while True:
        for frame in frames:
            # 清空控制台 - Windows专用命令
            os.system('cls')

            # 显示当前帧
            print(frame)

            # 等待0.5秒
            time.sleep(0.5)
except KeyboardInterrupt:
    # 当用户按下Ctrl+C时退出
    os.system('cls')
