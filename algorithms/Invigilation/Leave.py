import datetime

class Leave:
    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time

    def __repr__(self):
        return datetime.datetime.strftime(self.start_time, "%d-%m-%y") + " TO " + datetime.datetime.strftime(self.end_time, "%d-%m-%y")
