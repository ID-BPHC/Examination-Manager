import os
import sys
import datetime


class Room:
    def __init__(self, number, capacity):
        self.number = number
        self.capacity = capacity
        self.allotments = []

    def get_half_capacity(self):
        return int(int(self.capacity/2))

    def __repr__(self):
        return self.number + " - " + str(self.capacity)

    def __lt__(self, value):
        return self.capacity < value.capacity


class Course:
    def __init__(self, code, name, strength):
        self.code = code
        self.name = name
        self.strength = strength

    def __repr__(self):
        return self.code + " - " + str(self.strength)

    def __lt__(self, value):
        return self.strength < value.strength


class Allotment:
    def __init__(self, course, time_slot, seats_alloted, remarks):
        self.course = course
        self.time_slot = time_slot
        self.seats_alloted = seats_alloted
        self.remarks = remarks


def get_rooms(file_name):

    rooms = []

    f = open(file_name)

    for line in f.readlines():
        line = line.strip()
        splitted = line.split(",")
        rooms.append(Room(splitted[0], int(splitted[1])))

    f.close()
    return rooms


def generate_map_key(time_slot):
    try:
        datetime.datetime.strptime(
            time_slot[0] + " " + time_slot[1], "%d-%m-%y %H:%M")
        datetime.datetime.strptime(
            time_slot[0] + " " + time_slot[2], "%d-%m-%y %H:%M")

    except Exception as e:
        print(e)
        raise e

    return "|".join(time_slot)


def get_date_course_map(file_name):

    date_course_map = {}

    f = open(file_name)

    for line in f.readlines():

        line = line.strip()
        splitted = line.split(",")
        code = splitted[0]
        name = splitted[1]
        strength = int(splitted[2])
        time_slot_key = None

        try:
            time_slot_key = generate_map_key(splitted[3:])
        except:
            print(f"Invalid date format for course {code}")
            print(
                "Ensure that the format is Date (DD/MM/YY), Start time (HH:MM), End time")
            print("Example: 29/08/19,15:00,18:00")
            return

        if strength <= 0:
            continue

        if time_slot_key not in date_course_map:
            date_course_map[time_slot_key] = [Course(code, name, strength)]
        else:
            date_course_map[time_slot_key].append(Course(code, name, strength))

    f.close()

    for time_slot in date_course_map:
        date_course_map[time_slot].sort()
        date_course_map[time_slot].reverse()

    return date_course_map


def allot_rooms_single(rooms, date_course_map):

    for time_slot in date_course_map:

        room_pointer = 0

        for course in date_course_map[time_slot]:

            total_seats_alloted = 0

            while total_seats_alloted < course.strength:

                if room_pointer == len(rooms):
                    print(f"ERROR: Could not allot {course.code}")
                    break

                room = rooms[room_pointer]

                seats_alloted = min(room.capacity,
                                    course.strength - total_seats_alloted)

                total_seats_alloted += seats_alloted

                room.allotments.append(Allotment(
                    course, time_slot, seats_alloted, "FULL"))

                room_pointer += 1


def allot_rooms_double(rooms, date_course_map):

    for time_slot in date_course_map:

        pointer = [0, 0]

        for course in date_course_map[time_slot]:

            total_seats_alloted = 0

            # 0 - left and 1 - right
            active_pointer = 0 if pointer[0] < pointer[1] else 1

            while total_seats_alloted < course.strength:

                if pointer[0] == len(rooms) - 1 and pointer[1] == len(rooms) - 1:
                    print(f"ERROR: Could not allot {course.code}")
                    break

                elif pointer[active_pointer] == len(rooms) - 1:
                    active_pointer = 0 if pointer[0] < pointer[1] else 1

                room = rooms[pointer[active_pointer]]

                seats_alloted = min(room.get_half_capacity(),
                                    course.strength - total_seats_alloted)

                total_seats_alloted += seats_alloted

                room.allotments.append(Allotment(
                    course, time_slot, seats_alloted, "LEFT" if active_pointer == 0 else "RIGHT"))

                pointer[active_pointer] += 1

        if pointer[0] != pointer[1]:

            active_pointer = 0 if pointer[0] > pointer[1] else 1

            remaining_total = 0
            allotments = rooms[pointer[active_pointer]-1].allotments
            course = allotments[-1].course

            for i in range(min(pointer[0], pointer[1]), max(pointer[0], pointer[1])):
                remaining_total += rooms[i].allotments[-1].seats_alloted
                rooms[i].allotments.pop()

            active_pointer = active_pointer ^ 1
            total_seats_alloted = 0

            while total_seats_alloted < remaining_total:
                room = rooms[pointer[active_pointer]]
                seats_alloted = min(room.capacity,
                                    remaining_total - total_seats_alloted)
                total_seats_alloted += seats_alloted
                room.allotments.append(Allotment(
                    course, time_slot, seats_alloted, "FULL"))
                pointer[active_pointer] += 1

def post_process(rooms):

    for room in rooms:
        for allotment_1 in room.allotments:
            for allotment_2 in room.allotments:

                if allotment_1 is allotment_2:
                    continue

                if allotment_1.course is allotment_2.course:

                    allotment_1.seats_alloted += allotment_2.seats_alloted
                    allotment_1.remarks = "FULL"
                    room.allotments.remove(allotment_2)

def export_csv(rooms, file_name):

    f = open(file_name, "w")
    f.write(
        "Room,Course Code,Course Name,Room Capacity,Student Count,Course Strength,Time,Remarks\n")

    for room in rooms:
        for allotment in room.allotments:
            f.write(
                f"{room.number},{allotment.course.code},{allotment.course.name},{room.capacity},{allotment.seats_alloted},{allotment.course.strength},{allotment.time_slot},{allotment.remarks}\n")

    f.close()


def start_process(rooms_csv, exams_csv, is_double):

    print("Starting....")

    # room, capacity
    # Ensure no commas, DUPLICATES and BOM
    rooms = get_rooms(rooms_csv)

    # course_code, course_title, Enrolment_Count, time_slot (multiple cols)
    # Ensure no commas, DUPLICATES and BOM
    date_course_map = get_date_course_map(exams_csv)

    if is_double:
        allot_rooms_double(rooms, date_course_map)

    else:
        allot_rooms_single(rooms, date_course_map)

    post_process(rooms)
    export_csv(rooms, "./RoomAllotment.csv")
    print("Room Allotment file exported to ./RoomAllotment.csv")
