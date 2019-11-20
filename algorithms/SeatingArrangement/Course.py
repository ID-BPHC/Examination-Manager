import os


class Course:
    def __init__(self, code, name, exam_start, exam_end):
        self.code = code
        self.name = name
        self.students = []
        # Array of tuples of format (Room Number, Student Count)
        self.rooms = []
        self.exam_start = exam_start
        self.exam_end = exam_end

    def get_exam_slices(self):

        slices = []
        start_index = 0

        for room in self.rooms:

            if start_index >= len(self.students):
                break

            end_index = start_index + \
                room[1] - 1 if start_index + room[1] - \
                1 < len(self.students) else -1
            slices.append(
                (room[0], room[1], self.students[start_index], self.students[end_index]))
            start_index += room[1]

        return slices

    def __repr__(self):
        return f"{self.code} | {self.name}"


class CourseList:
    def __init__(self):
        self.courses = []

    def add_course(self, code, name, exam_start, exam_end):
        self.courses.append(Course(code, name, exam_start, exam_end))

    def add_if_not_exists(self, code, name, exam_start, exam_end):
        if self.find_by_code(code) is None:
            self.add_course(code, name, exam_start, exam_end)

    def find_by_code(self, code):
        for course in self.courses:

            if course.code == code:
                return course

            splitted = course.code.split("/")

            for splitted_course in splitted:
                if code.strip() == splitted_course.strip():
                    return course

        return None

    def sort_entries(self):

        self.courses.sort(key=lambda x: x.code)

        for course in self.courses:
            course.rooms.sort()
            course.students.sort()

    def __repr__(self):
        return f"{len(self.courses)} courses"
