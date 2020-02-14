import numpy as np
from people import Person
from scipy.spatial.distance import cdist


class PeoplePool:
    def __init__(self,city,u,people_num,BROAD_RATE,SHADOW_TIME,HOSPITAL_RECEIVE_TIME,CURE_TIME,SAFETY_DIST):
        self.u = u
        self.people = np.array([])
        self.BROAD_RATE = BROAD_RATE
        self.SHADOW_TIME = SHADOW_TIME
        self.HOSPITAL_RECEIVE_TIME = HOSPITAL_RECEIVE_TIME
        self.CURE_TIME = CURE_TIME
        self.SAFETY_DIST = SAFETY_DIST

        for i in range(people_num):
            x = 1000 * np.random.normal(0,1) + city.x
            y = 1000 * np.random.normal(0,1) + city.y
            person = Person(x, y)
            self.people = np.append(self.people, person)

    # 不包括已入院的人
    def getX(self):
        return np.array([person.x for person in self.people if person.status != 3])

    def getY(self):
        return np.array([person.y for person in self.people if person.status != 3])

    def getStatus(self):
        return np.array([person.status for person in self.people if person.status != 3])

    def getCoordinates(self):
        return np.array([(i.x,i.y) for i in self.people])

    def update(self, hospital, time):
        # people = self.people
        coord = self.getCoordinates()
        dist = cdist(coord,coord) # 欧氏距离

        for idx, person in enumerate(self.people):
            # 潜伏 -> 确认感染
            if person.status == 1:
                if (time - person.infected_time) > self.SHADOW_TIME:
                    person.status = 2
                    person.confirmed_time = time

            # 确诊感染 -> 住院
            elif person.status == 2:
                if(time - person.confirmed_time) > self.HOSPITAL_RECEIVE_TIME:
                    bed = hospital.pickBed()
                    if bed is None:
                        print(f"TIME={time:<5}医院床位不足")
                    else:
                        person.bed = bed
                        person.status = 3
                        person.hospitalized_time = time

            # 住院 -> 治愈
            elif person.status == 3:
                if(time - person.hospitalized_time) > self.CURE_TIME:
                    person.status = 0
                    person.infected_time = None
                    person.confirmed_time = None
                    person.hospitalized_time = None
                    # bed = people.bed
                    # bed.isEmpty = True
                    person.bed.isEmpty = True
                    person.bed = None

            # 正常 -> 被感染(潜伏)
            elif person.status == 0:
                # 这个人的所有邻居
                i_neighbors = np.where(dist[idx] < self.SAFETY_DIST)[0]
                for i in i_neighbors:
                    if i != idx:
                        if self.people[i].status == 1 or self.people[i].status == 2:
                            # 传播率
                            if np.random.rand() < self.BROAD_RATE:
                                person.status = 1
                                person.infected_time = time
                                break

            person.move(self.u)