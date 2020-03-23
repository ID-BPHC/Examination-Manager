import datetime
def do_dates_intersect(date_1_start, date_1_end, date_2_start, date_2_end):

    return date_1_start <= date_2_end and date_1_end >= date_2_start


class Invigilator:
    def __init__(self, psrn, name, department, email, is_research_scholar):
        self.psrn = psrn
        self.name = name
        self.department = department
        self.email = email
        self.is_research_scholar = is_research_scholar
        self.duties = []
        self.leaves = []
        self.chamber = "NA"

        if is_research_scholar:
            self.max_duties = 3
        else:
            self.max_duties = 4

    def get_reamining_duty_count(self):
        return self.max_duties - len(self.duties)

    def is_available(self, start, end):

        if len(self.duties) >= self.max_duties:
            return False

        for leave in self.leaves:
            if do_dates_intersect(start, end, leave.start_time, leave.end_time):
                return False

        for duty in self.duties:
            if do_dates_intersect(start, end, duty.start_time, duty.end_time):
                return False

            if duty.start_time.date() == start.date():
                return False

        return True

    def __repr__(self):
        return self.psrn + " " + self.name


class InvigilatorList:

    def __init__(self):
        self.invigilators = []

    def add(self, psrn, name, dept, email, is_research_scholar):
        if self.find_by_psrn(psrn) is None:
            self.invigilators.append(Invigilator(
                psrn,
                name,
                dept,
                email,
                is_research_scholar
            ))

    def find_by_psrn(self, psrn):
        for i in self.invigilators:
            if i.psrn == psrn:
                return i
        return None

    def get_all(self):
        return self.invigilators

    def get_available_department_scholar(self, department, start_time, end_time):

        free_invigilator = None
        remaining_duties_max = 0

        for invigilator in self.invigilators:
            if invigilator.department == department and invigilator.is_research_scholar and invigilator.is_available(start_time, end_time) and invigilator.get_reamining_duty_count() > remaining_duties_max:
                free_invigilator = invigilator
                remaining_duties_max = invigilator.get_reamining_duty_count()

        return free_invigilator

    def get_available_scholar(self, start_time, end_time):

        free_invigilator = None
        remaining_duties_max = 0

        for invigilator in self.invigilators:
            if invigilator.is_research_scholar and invigilator.is_available(start_time, end_time) and invigilator.get_reamining_duty_count() > remaining_duties_max:
                free_invigilator = invigilator
                remaining_duties_max = invigilator.get_reamining_duty_count()

        return free_invigilator

    def get_available_department_faculty(self, department, start_time, end_time):

        free_invigilator = None
        remaining_duties_max = 0

        for invigilator in self.invigilators:
            if invigilator.department == department and (not invigilator.is_research_scholar) and invigilator.is_available(start_time, end_time) and invigilator.get_reamining_duty_count() > remaining_duties_max:
                free_invigilator = invigilator
                remaining_duties_max = invigilator.get_reamining_duty_count()

        return free_invigilator

    def get_available_faculty(self, start_time, end_time):

        free_invigilator = None
        remaining_duties_max = 0

        for invigilator in self.invigilators:
            if (not invigilator.is_research_scholar) and invigilator.is_available(start_time, end_time) and invigilator.get_reamining_duty_count() > remaining_duties_max:
                #Considering no hrs and minutes in date therefore added a day to endtime
                free_invigilator = invigilator
                remaining_duties_max = invigilator.get_reamining_duty_count()

        return free_invigilator

    def __repr__(self):
        return str(self.invigilators)
