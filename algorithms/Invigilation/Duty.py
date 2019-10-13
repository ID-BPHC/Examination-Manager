import datetime

class Duty:
    def __init__(self, room, course, start_time, end_time):
        self.room = room
        self.course = course
        self.start_time = start_time
        self.end_time = end_time

    def __repr__(self):
        return self.room + " - " + self.course.code + " - " + datetime.datetime.strftime(self.start_time, "%d/%m/%Y %H:%M") + " TO " + datetime.datetime.strftime(self.end_time, "%d/%m/%Y %H:%M")
