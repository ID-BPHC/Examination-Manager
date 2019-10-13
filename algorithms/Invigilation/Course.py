
class Course:

    def __init__(self, code, name):
        self.code = code
        self.name = name
        self.ic = None
        self.faculty = []
        self.enrolment_count = 0

    def set_ic(self, invigilator):
        self.ic = invigilator

    def add_faculty(self, invigilator):
        self.faculty.append(invigilator)

    def set_faculty_list(self, faculty_list):
        self.faculty = faculty_list

    def get_available_scholar(self, start_time, end_time):

        free_invigilator = None
        remaining_duties_max = 0

        for invigilator in self.faculty:
            if invigilator.is_research_scholar and invigilator.is_available(start_time, end_time) and invigilator.get_reamining_duty_count() > remaining_duties_max:
                free_invigilator = invigilator
                remaining_duties_max = invigilator.get_reamining_duty_count()

        return free_invigilator

    def get_available_faculty(self, start_time, end_time):

        free_invigilator = None
        remaining_duties_max = 0

        for invigilator in self.faculty:
            if (not invigilator.is_research_scholar) and invigilator.is_available(start_time, end_time) and invigilator.get_reamining_duty_count() > remaining_duties_max:
                free_invigilator = invigilator
                remaining_duties_max = invigilator.get_reamining_duty_count()

        return free_invigilator

    def __repr__(self):
        return str(self.__dict__)


class CourseList:

    def __init__(self):
        self.courses = []

    def add(self, code, name, ic, faculty_list):

        if code is None:
            return
        
        if self.find_by_code(code) is not None:
            return

        course = Course(code, name)
        course.set_ic(ic)
        course.set_faculty_list(faculty_list)
        self.courses.append(course)

    def find_by_name(self, name):
        for i in self.courses:
            if i.name == name:
                return i
        return None
    
    def find_by_code(self, code):
        for i in self.courses:
            if i.code == code:
                return i
        return None

    def __repr__(self):
        return str(self.courses)
