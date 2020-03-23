
import json
import os
import shutil
import openpyxl
import time

from openpyxl.styles.borders import Border, Side
from openpyxl.styles import Font, PatternFill


class Course:

    def __init__(self, code, title):
        self.code = code
        self.title = title
        self.ic_email = ""
        self.rooms = []
        self.time = None
        self.students = []
        self.allotment_index = 0

    def get_next_student(self):

        if self.allotment_index >= len(self.students):
            return None

        else:
            student = self.students[self.allotment_index]
            self.allotment_index += 1
            return student


class CourseList:
    def __init__(self):
        self.courses = []

    def add_course(self, code, name):
        self.courses.append(Course(code, name))

    def add_if_not_exists(self, code, name):
        if self.find_by_code(code) is None:
            self.add_course(code, name)

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

        for course in self.courses:
            course.rooms.sort()
            course.students.sort()

    def __repr__(self):
        return f"{len(self.courses)} courses"


def get_matched_rooms(room_map, number):

    keys = []

    for key in room_map.keys():

        if number in key:
            keys.append(key)

    return keys


def get_populated_maps(room_map_csv, room_allotment_csv, registered_students_csv, ic_csv):

    room_map = {}
    final_solution = {}
    course_list = CourseList()

    print("Reading Data")

    f = open(room_map_csv)

    for line in f.readlines():

        line = line.strip()
        splitted = line.split(",")
        room_number = splitted[0]
        no_of_cols = int(splitted[1])
        col_map = [int(x) for x in splitted[2: no_of_cols + 2]]

        room_map[room_number] = col_map

    f.close()

    f = open(room_allotment_csv)

    for line in f.readlines()[1:]:

        line = line.strip()
        splitted = line.split(",")

        room = splitted[0]
        code = splitted[1]
        title = splitted[2]
        student_count = int(splitted[4])
        time = splitted[6]
        flag = splitted[7]

        course_list.add_if_not_exists(code, title)
        course = course_list.find_by_code(code)

        if course is not None:
            course.rooms.append((room, flag, student_count))
            course.time = time

        if time not in final_solution:
            final_solution[time] = {}

        if room not in final_solution[time]:
            matched_room_keys = get_matched_rooms(room_map, room)

            for key in matched_room_keys:

                seating_map = []

                for i in range(0, max(room_map[key])):

                    seating_map.append([])

                    for j in range(0, len(room_map[key])):
                        seating_map[i].append("")

                final_solution[time][key] = seating_map

    f.close()

    f = open(registered_students_csv)

    for line in f.readlines():
        line = line.strip()
        splitted = line.split(",")

        id_number = splitted[0]
        course_code = splitted[1]

        course = course_list.find_by_code(course_code)

        if course is not None:
            course.students.append(id_number)

    f.close()

    course_list.sort_entries()

    f = open(ic_csv)

    for line in f.readlines():

        line = line.strip()
        splitted = line.split(",")

        course_code = splitted[0]
        email = splitted[1]

        course = course_list.find_by_code(course_code)

        if course is not None:
            # print(email)
            course.ic_email = email

    f.close()

    return room_map, final_solution, course_list


def generate_seating_charts(room_map_csv, room_allotment_csv, registered_students_csv, ic_csv):

    print("Generating Seating Charts")

    room_map, final_solution, course_list = get_populated_maps(room_map_csv, room_allotment_csv,
                  registered_students_csv, ic_csv)

    for course in course_list.courses:

        for room, remark, student_count in course.rooms:

            keys = get_matched_rooms(room_map, room)
            seated = 0

            for key in keys:

                chart = final_solution[course.time][key]
                limits = room_map[key]
                start_point = 1 if remark == "LEFT" else 0
                step_value = 1 if remark == "FULL" else 2

                for i in range(0, len(limits)):

                    for j in range(start_point, limits[i], step_value):

                        if seated >= student_count:
                            break

                        student = course.get_next_student()
                        chart[len(chart) - j -
                              1][i] = f"{course.code} - {student}"
                        seated += 1

                    if remark != "FULL":
                        start_point = start_point ^ 1

            for i in range(seated, student_count):
                print(
                    f"Could not assign a seat for {course.get_next_student()} in {room} for {course.code} - {course.ic_email}. Assign manually in the room.")

        if course.allotment_index < len(course.students):
            print(
                f"Seating Arrangement Discrepancy - {len(course.students) - course.allotment_index} students after {course.get_next_student()} for {course.code} - {course.title}")

    export_charts(room_map, course_list, final_solution)
    print("***** Done *****")


def export_charts(room_map, course_list, final_solution):

    print("***** Starting Chart Generation *****")

    thin_border = Border(left=Side(style='thin'),
                         right=Side(style='thin'),
                         top=Side(style='thin'),
                         bottom=Side(style='thin'))

    heading_font = Font(size=13, bold=True)
    sub_heading_font = Font(size=11, bold=True)

    if os.path.exists("./Seating_Charts") and os.path.isdir("./Seating_Charts"):
        shutil.rmtree("./Seating_Charts")
        time.sleep(0.5)

    os.mkdir("./Seating_Charts")

    for course in course_list.courses:

        if course.time is None:
            continue

        if not os.path.exists(f"./Seating_Charts/{course.ic_email}"):
            print("Folder created for ", course.ic_email)
            os.mkdir(f"./Seating_Charts/{course.ic_email}")

        wb = openpyxl.Workbook()

        for room, flag, student_count in course.rooms:

            keys = get_matched_rooms(room_map, room)

            for key in keys:

                print(f"Generating {course.code} - {key}")

                wb.create_sheet(key)
                ws = wb[key]
                ws.sheet_properties.pageSetUpPr.fitToPage = True
                ws.page_setup.fitToHeight = False
                openpyxl.worksheet.worksheet.Worksheet.set_printer_settings(
                    ws, paper_size=ws.PAPERSIZE_A4, orientation='landscape')

                total_cols = len(room_map[key])
                heading = f"{key} - {course.code} - {course.title}"

                end_char = chr(64 + total_cols)
                ws.merge_cells(f"A1:{end_char}1")
                ws.merge_cells(f"A2:{end_char}2")

                ws["A1"] = heading
                ws["A1"].font = heading_font

                ws["A2"] = "***** Blackboard Here *****"
                ws["A2"].font = sub_heading_font

                for row in final_solution[course.time][key]:
                    ws.append(row)

                for col in range(65, 90):
                    ws.column_dimensions[chr(col)].width = 15

                for row in ws.iter_rows():
                    for cell in row:
                        cell.alignment = openpyxl.styles.Alignment(
                            wrap_text=True, horizontal='center', vertical='center')
                        cell.border = thin_border

                        if cell.value is not None and cell.value.split("-")[0].strip() == course.code:
                            cell.fill = PatternFill(
                                start_color="E8E8E8", end_color="E8E8E8", fill_type="solid")

        del wb["Sheet"]
        try:
            path = os.path.join("Seating_Charts", course.ic_email,
                            course.code.split("/")[0] + ".xlsx")
            wb.save(path)
        except:
            print("Course could not be allotted ", course.code)
