import numpy as np

class Person:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.status = 0  # 0 正常 1 潜伏 2 感染 3 住院
        self.bed = None
        self.infected_time = None  # 被感染时间 从0 -> 1
        self.confirmed_time = None  # 被确诊时间 从1 -> 2
        self.hospitalized_time = None  # 被收治时间  2 ->3

    def move(self, u):
        self.x += u * 20 * np.random.normal(0,1)
        self.y += u * 20 * np.random.normal(0,1)


