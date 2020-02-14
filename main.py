
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

from city import City
from peoplePool import PeoplePool
from hospital import Hospital


ORIGINAL_NUM = 50 #初始感染数量
BROAD_RATE = 0.7 #传播率
SHADOW_TIME = 24 #潜伏时间 最新数据潜伏期可长达24天
HOSPITAL_RECEIVE_TIME = 3 #医院收治响应时间
CURE_TIME = 14 #治疗时间
BED_NUM = 1000 #医院床位
SAFETY_DIST = 15 #安全距离
u = np.exp(-0.99) #流动意向平均值 几乎不动
PERSON_NUM = 5000 #城市内人数


city = City(0, 0)
# def __init__(self,city,u,people_num,BROAD_RATE,SHADOW_TIME,HOSPITAL_RECEIVE_TIME,CURE_TIME,SAFETY_DIST):
pool = PeoplePool(city, u, PERSON_NUM, BROAD_RATE, SHADOW_TIME, HOSPITAL_RECEIVE_TIME, CURE_TIME, SAFETY_DIST)

hospital = Hospital(BED_NUM)

# 随机选择初始感染者
for i in range(ORIGINAL_NUM):
    idx = np.random.randint(0, PERSON_NUM)
    pool.people[idx].status = 1
    pool.people[idx].infected_time = 0


color_person =['white', 'yellow', 'red', 'black']  # 正常, 潜伏, 确诊感染, 住院
color_bed =['red', 'black']  # 0 感染者入住 , 1空床位

fig = plt.figure(figsize=(20, 10))

plt.style.use('dark_background')
fig.patch.set_facecolor('black')

gs = plt.GridSpec(3, 5, wspace=0.5, hspace=0.5)
ax1 = plt.subplot(gs[:, 0:3])
ax2 = plt.subplot(gs[:, 3])
ax3 = plt.subplot(gs[0, 4])
ax4 = plt.subplot(gs[1, 4])
ax5 = plt.subplot(gs[2, 4])

Hx = hospital.getX()
Hy = hospital.getY()


# 只更新动态对象，而静态对象保存起来
ax1background = fig.canvas.copy_from_bbox(ax1.bbox)
ax2background = fig.canvas.copy_from_bbox(ax2.bbox)


def animate(time):
    status_of_pool = pool.getStatus()
    status_of_hospital = hospital.getStatus() # 空 = true 1 black
    # print(status_of_hospital)
    healthy = np.sum(status_of_pool == 0)
    infected = np.sum(status_of_pool == 1)
    confirmed = np.sum(status_of_pool == 2)
    hospitalized = np.sum(status_of_hospital == False)
    # print(hospitalized)

    fig.canvas.restore_region(ax1background)
    fig.canvas.restore_region(ax2background)

    ax1.clear()
    ax1.scatter(pool.getX(), pool.getY(), c=[color_person[i] for i in status_of_pool],marker='.',alpha=0.5,s=10)
    ax1.set_title(f'TIME:{time:<10}PERSON_NUM:{PERSON_NUM:<10}HEALTHY:{healthy}')
    ax1.set_xticks([])
    ax1.set_yticks([])

    ax1.set_xlim(-5000,5000)
    ax1.set_ylim(-5000,5000)

    ax2.clear()
    # ax2.scatter(hospital.getX(),hospital.getY(),c=[color_bed[i] for i in status_of_hospital],\
    #            marker='*',alpha=1,s=10)
    ax2.scatter(Hx,Hy,c=[color_bed[i] for i in status_of_hospital], marker='*',alpha=1,s=10)
    ax2.set_title(f'HOSPITALIZED:{hospitalized}/{BED_NUM}')
    ax2.set_xticks([])
    ax2.set_yticks([])

    ax3.bar(time,healthy,color = color_person[0],width=1)
    ax3.set_title(f'HEALTHY:{healthy}')

    ax4.bar(time,infected,color = color_person[1],width=1)
    ax4.set_title(f'INFECTED:{infected}')

    ax5.bar(time,confirmed,color = color_person[2],width=1)
    ax5.set_title(f'CONFIRMED:{confirmed}')

    pool.update(hospital,time)
    return 0


ani = animation.FuncAnimation(fig=fig, func=animate)
plt.show()

