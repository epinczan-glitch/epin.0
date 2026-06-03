import pygame
import sys
import random
import numpy as np
import matplotlib
# 指定 Matplotlib 使用 PyQt5 作为渲染后端
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QSpinBox, 
                             QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QFrame)
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPainter


class Particle:
    def __init__(self, radius, velocity, r, mass):
        self.radius = radius
        self.v = np.array(velocity)
        self.r = np.array(r)
        self.x = r[0]
        self.y = r[1]
        self.mass = mass
        
        # 扩散功能：根据初始位置划分左右两类气体
        if self.x < 250:
            self.color = (255, 60, 60)    # 鲜红色
            self.gas_type = "left"
        else:
            self.color = (60, 180, 255)   # 亮蓝色
            self.gas_type = "right"

    def move(self):
        self.r = self.r + self.v


class Game:
    def __init__(self, amount=100, temperature=300):
        pygame.display.init()
        self.screen_size = 500
        self.screen = pygame.display.set_mode((self.screen_size, self.screen_size), pygame.HIDDEN)
        self.amount_balls = amount
        self.screen.fill((0, 0, 0))
        self.press_momentum = 0
        self.vels = [0.0] * self.amount_balls
        self.list_balls = []
        self.k = 1.38e-23
        self.N = self.amount_balls
        
        # 统计数据列表
        self.list_press = []
        self.list_diffusion = []
        
        self.v_quad = 0
        self.energy = 0
        self.t = 0
        self.T = temperature
        self.dt = 0.2e-11  
        self.dl = 0.2e-9   
        self.tree = [[], [], [], []]
        self.mass = 6.63e-26

    def spawn_particles(self):
        v0 = (2 * self.k * self.T / self.mass) ** 0.5 / (100 * 2 ** 0.5)
        for _ in range(self.amount_balls):
            # 留出边界防止卡墙
            ball = Particle(2, (random.choice([-v0, v0]), random.choice([-v0, v0])), 
                            (random.randint(10, self.screen_size - 10),
                             random.randint(10, self.screen_size - 10)), self.mass)
            self.list_balls.append(ball)

    def particle_collision(self, ball_1, ball_2):
        if ((ball_1.r[0] - ball_2.r[0]) ** 2 + (ball_1.r[1] - ball_2.r[1]) ** 2) <= 16:
            if ball_1.r[0] != ball_2.r[0]:
                v1, v2 = ball_1.v, ball_2.v
                r1, r2 = ball_1.r, ball_2.r
                d_r1 = r1 - r2
                d_v1 = v1 - v2
                d_r2 = r2 - r1
                d_v2 = v2 - v1
                ball_1.v = v1 - d_r1 * (d_v1 @ d_r1) / (d_r1[0] ** 2 + d_r1[1] ** 2)
                ball_2.v = v2 - d_r2 * (d_v2 @ d_r2) / (d_r2[0] ** 2 + d_r2[1] ** 2)

    def total_energy(self):
        if len(self.list_balls) == 0: return
        self.energy = sum([self.list_balls[i].mass / 2 * ((100 * self.list_balls[i].v[0]) ** 2 + (100 * self.list_balls[i].v[1]) ** 2)
             for i in range(len(self.list_balls))]) / self.N

    def temperature(self):
        self.total_energy()
        self.T = self.energy / (self.k * len(self.list_balls))

    def loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        self.screen.fill((15, 15, 15)) # 深灰色背景，更有质感
        self.t += 1
        
        for ball in self.list_balls:
            pygame.draw.circle(self.screen, ball.color, (int(ball.r[0]), int(ball.r[1])), ball.radius)
            ball.move()
            
            # 边界碰撞与压强动量积累
            if ball.r[0] <= ball.radius:
                ball.v[0] *= -1
                ball.r[0] = ball.radius
                self.press_momentum += ball.mass * abs(100 * ball.v[0]) * 2
            elif ball.r[0] >= self.screen_size - ball.radius:
                ball.v[0] *= -1
                ball.r[0] = self.screen_size - ball.radius
                self.press_momentum += ball.mass * abs(100 * ball.v[0]) * 2
                
            if ball.r[1] <= ball.radius:
                ball.v[1] *= -1
                ball.r[1] = ball.radius
                self.press_momentum += ball.mass * abs(100 * ball.v[1]) * 2
            elif ball.r[1] >= self.screen_size - ball.radius:
                ball.v[1] *= -1
                ball.r[1] = self.screen_size - ball.radius
                self.press_momentum += ball.mass * abs(100 * ball.v[1]) * 2

        # 空间四分树网格划分
        for i in range(4): self.tree[i].clear()
        for ball in self.list_balls:
            if ball.r[0] > 250:
                if ball.r[1] <= 250: self.tree[0].append(ball)
                else: self.tree[3].append(ball)
            else:
                if ball.r[1] <= 250: self.tree[1].append(ball)
                else: self.tree[2].append(ball)

        for k in range(4):
            for i in range(len(self.tree[k])):
                for j in range(i + 1, len(self.tree[k])):
                    self.particle_collision(self.tree[k][i], self.tree[k][j])
                    
        self.vels = [((ball.v[0] ** 2 + ball.v[1] ** 2) ** 0.5) * 100 for ball in self.list_balls]
        
        sum_v2 = sum([b.v[0] ** 2 + b.v[1] ** 2 for b in self.list_balls])
        self.v_quad = (sum_v2 / self.N) ** 0.5 if self.N > 0 else 0

        # 定时统计宏观量
        if self.t >= 50:
            cur_press = self.press_momentum / (4 * 500 * 0.2e-9 * 50 * self.dt)
            self.list_press.append(cur_press)
            
            # 计算扩散混合度
            mixed = sum(1 for b in self.list_balls if (b.gas_type == "left" and b.r[0] >= 250) or (b.gas_type == "right" and b.r[0] < 250))
            self.list_diffusion.append(mixed / self.amount_balls)
            
            self.total_energy()
            self.temperature()
            self.t = 0
            self.press_momentum = 0


# 💥 新增的第二个窗口类：专门用于实时绘制并刷新图表
class RealTimeGraphWindow(QWidget):
    def __init__(self, game_instance):
        super().__init__()
        self.game = game_instance
        self.setWindowTitle("Мониторинг графиков в реальном времени (实时图表监控)")
        self.resize(900, 450)
        
        # 创建 Matplotlib 画布
        self.figure = Figure(figsize=(9, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        
        # 分割成左右两个子图：左边压强和扩散，右边麦克斯韦速度分布
        self.ax_press = self.figure.add_subplot(121)
        self.ax_speed = self.figure.add_subplot(122)
        
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def update_charts(self):
        if not self.game.list_balls:
            return
            
        # --- 1. 绘制左图（压强与扩散历史） ---
        self.ax_press.clear()
        time_steps = [i * 50 for i in range(1, len(self.game.list_press) + 1)]
        
        if time_steps:
            self.ax_press.plot(time_steps, self.game.list_press, 'r-', label="Давление (压强)")
            # 同步绘制扩散程度
            ax2 = self.ax_press.twinx()
            ax2.clear()
            ax2.plot(time_steps, self.game.list_diffusion, 'g-', label="Смешивание (扩散度)", alpha=0.6)
            ax2.set_ylabel('Доля смешивания', color='g')
            ax2.tick_params(axis='y', labelcolor='g')
            
        self.ax_press.set_xlabel('Время (时间步)')
        self.ax_press.set_ylabel('Давление (压强)')
        self.ax_press.set_title('Давление и Диффузия')
        self.ax_press.grid(True, linestyle='--', alpha=0.5)

        # --- 2. 绘制右图（速度分布直方图对比理论曲线） ---
        self.ax_speed.clear()
        if self.game.vels:
            self.ax_speed.hist(self.game.game_instance_vels if hasattr(self, 'game_instance_vels') else self.game.vels, 
                               bins=15, density=True, color='gray', alpha=0.6, label="Моделирование")
            
            # 绘制麦克斯韦理论红虚线
            v_axis = np.arange(0., 1500, 5)
            v_q = self.game.v_quad * 100
            if v_q > 0:
                f_v = (2 * v_axis / (v_q ** 2)) * np.exp(-v_axis ** 2 / (v_q ** 2))
                self.ax_speed.plot(v_axis, f_v, 'r--', linewidth=2, label="Максвелл-Больцман")
                
        self.ax_speed.set_xlabel('Скорость, м/с')
        self.ax_speed.set_ylabel('Доля молекул')
        self.ax_speed.set_title('Распределение скоростей')
        self.ax_speed.legend(loc='upper right', fontsize=8)
        self.ax_speed.grid(True, linestyle='--', alpha=0.5)
        
        self.figure.tight_layout()
        self.canvas.draw()


class GameWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.game = Game(amount=400, temperature=400)
        self.graph_window = None  # 第二窗口实例句柄
        self.initUI()

    def initUI(self):
        # 整体采用水平主布局：左边是Pygame物理沙盒，右边是清爽通透的控制面板
        main_layout = QHBoxLayout()
        
        # 1. 左侧：Pygame显示区域容器
        self.pygame_label = QLabel()
        self.pygame_label.setFixedSize(500, 500)
        self.pygame_label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        main_layout.addWidget(self.pygame_label)
        
        # 2. 右侧：全自动网格化的参数控制区
        right_panel = QVBoxLayout()
        control_grid = QGridLayout()
        
        font_title = QtGui.QFont("Times", 11)
        font_data = QtGui.QFont("Arial", 10)
        
        # 输入控件添加
        lbl1 = QLabel('Количество частиц (粒子数):')
        lbl1.setFont(font_title)
        self.put_amount = QSpinBox()
        self.put_amount.setRange(10, 1000)
        self.put_amount.setValue(400)
        control_grid.addWidget(lbl1, 0, 0)
        control_grid.addWidget(self.put_amount, 0, 1)

        lbl2 = QLabel('Температура (温度):')
        lbl2.setFont(font_title)
        self.put_temp = QSpinBox()
        self.put_temp.setRange(10, 10000)
        self.put_temp.setValue(400)
        control_grid.addWidget(lbl2, 1, 0)
        control_grid.addWidget(self.put_temp, 1, 1)
        
        right_panel.addLayout(control_grid)
        right_panel.addSpacing(15)
        
        # 状态文本数据显示区
        self.label_gas = QLabel('Газ модели: Аргон (左右两色扩散)')
        self.label_press = QLabel('Давление: 计算中... Н/м')
        self.label_v_quad = QLabel('Средняя квадр. скорость: 0 м/с')
        self.label_scale = QLabel('Масштаб: 1 пикс = 0.2 нм')
        
        for lbl in [self.label_gas, self.label_press, self.label_v_quad, self.label_scale]:
            lbl.setFont(font_data)
            right_panel.addWidget(lbl)
            
        right_panel.addStretch()
        
        # 开始大按钮
        self.btn_start = QPushButton('Начать моделирование\n(开始模拟并打开图表)')
        self.btn_start.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        self.btn_start.setMinimumHeight(60)
        self.btn_start.setStyleSheet("background-color: #2a82da; color: white; border-radius: 5px;")
        self.btn_start.clicked.connect(self.start_simulation)
        right_panel.addWidget(self.btn_start)
        
        main_layout.addLayout(right_panel)
        self.setLayout(main_layout)

    def start_simulation(self):
        # 初始化沙盒数据
        self.game = Game(amount=self.put_amount.value(), temperature=self.put_temp.value())
        self.game.spawn_particles()
        
        # 💥 核心点：创建并显示独立的第二图表窗口
        if self.graph_window is not None:
            self.graph_window.close()
        self.graph_window = RealTimeGraphWindow(self.game)
        self.graph_window.show()
        
        # 定时器高频刷新逻辑
        self.timer = QTimer()
        self.timer.timeout.connect(self.pygame_loop)
        self.timer.start(30)

    def pygame_loop(self):
        self.game.loop()
        
        # 实时更新右侧状态面板文本
        self.label_v_quad.setText(f'Средняя квадратичная скорость:\n{round(self.game.v_quad * 100)} м/с')
        if len(self.game.list_press) > 0:
            self.label_press.setText(f'Давление: {round(self.game.list_press[-1], 2)} Н/м')
            
        # 💥 核心点：驱动第二窗口的图表进行无缝刷新
        if self.graph_window and self.graph_window.isVisible():
            # 每隔几个计算周期刷新一次图表，防止数据量太大导致频繁UI重绘卡顿
            if random.random() < 0.15 or self.game.t == 49:
                self.graph_window.update_charts()
                
        self.update()

    def paintEvent(self, e):
        # 将 Pygame 缓存内的像素帧安全投射渲染到 PyQt5 的 QLabel 载体上
        if self.game and hasattr(self.game, 'screen'):
            buf = self.game.screen.get_buffer()
            img = QImage(buf, 500, 500, QImage.Format_RGB32)
            pix = QtGui.QPixmap.fromImage(img)
            self.pygame_label.setPixmap(pix)


if __name__ == "__main__":
    # 针对 Windows 高分屏缩放自动模糊修复
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    app = QApplication(sys.argv)
    w = GameWidget()
    w.setWindowTitle('Симулятор идеального газа v2.0')
    w.resize(850, 550)
    w.show()
    sys.exit(app.exec_())