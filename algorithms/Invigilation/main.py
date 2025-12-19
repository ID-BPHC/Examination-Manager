import os
import datetime
from functools import partial
from algorithms.Invigilation.Course import *
from algorithms.Invigilation.Duty import *
from algorithms.Invigilation.Invigilator import Invigilator, InvigilatorList
from algorithms.Invigilation.Leave import *


def get_invigilator_list(faculty_file_name, scholar_file_name):
    invigilator_list = InvigilatorList()

    f = open(faculty_file_name, "r")

    for line in f.readlines():
        splitted = line.split(",")
        splitted = list(map(str.strip, splitted))
        invigilator_list.add(splitted[0], splitted[1], splitted[2], splitted[3], False)

    f.close()

    f = open(scholar_file_name, "r")

    for line in f.readlines():
        splitted = line.split(",")
        splitted = list(map(str.strip, splitted))
        invigilator_list.add(splitted[0], splitted[1], splitted[2], splitted[3], True)

    f.close()

    return invigilator_list


def update_chamber_numbers(invigilator_list, file_name):
    f = open(file_name)

    for line in f.readlines():
        splitted = line.strip().split(",")
        psrn = splitted[0]
        chamber = splitted[1]

        faculty = invigilator_list.find_by_psrn(psrn)

        if len(chamber) > 0 and faculty is not None:
            faculty.chamber = chamber

    f.close()


def update_invigilator_leaves(invigilator_list, leaves_file_name):
    f = open(leaves_file_name)

    for line in f.readlines():
        line = line.strip()
        splitted = line.split(",")
        psrn = splitted[0]

        faculty = invigilator_list.find_by_psrn(psrn)

        if faculty is not None:
            try:
                start_time = datetime.datetime.strptime(splitted[1].strip(), "%d-%m-%y")
                end_time = datetime.datetime.strptime(splitted[2].strip(), "%d-%m-%y")
                faculty.leaves.append(Leave(start_time, end_time))
            except:
                print(
                    f"****** ERROR: Invalid leave date for faculty {faculty.psrn} {splitted[1]}******"
                )
                print("Leave will not be considered" + os.linesep)

    f.close()


def update_invigilator_max_duties(invigilator_list, max_duties_filename):
    f = open(max_duties_filename)

    for line in f.readlines():
        line = line.strip()
        splitted = line.split(",")

        invigilator = invigilator_list.find_by_psrn(splitted[0])
        if invigilator is not None:
            invigilator.max_duties = int(splitted[1])

    f.close()


def get_course_list(file_name, invigilator_list):
    f = open(file_name, "r")
    course_list = CourseList()

    lines = f.readlines()

    for line in lines:
        splitted = line.split(",")
        splitted = list(map(str.strip, splitted))
        code = splitted[0]
        name = splitted[1]
        faculty = invigilator_list.find_by_psrn(splitted[2])
        ic = invigilator_list.find_by_psrn(splitted[3])

        if faculty is None:
            print(
                f"****** ERROR: Faculty not found '{splitted[2]}' - Course: '{code}' ******"
            )
            print("This faculty will not be used during invigilation", os.linesep)
            continue

        course = course_list.find_by_code(code)

        if course is None:
            course_list.add(code, name, ic, [faculty])

        else:
            course.faculty.append(faculty)

    f.close()
    return course_list


def get_master_map(course_list, file_name):
    # rooms -> time_slot -> courses
    master_map = {}

    f = open(file_name)

    for line in f.readlines():
        line = line.strip()
        splitted = line.split(",")

        room = splitted[0]
        course = course_list.find_by_code(splitted[1].strip())
        time_slot_key = splitted[6]
        lr = splitted[7].strip()

        if course is None:
            print(f"****** ERROR: Course not found '{splitted[2]}' ******")
            print(
                "No invigilators will be alloted for this course. Check Room Allotments or Course CSV file",
                os.linesep,
            )
            continue

        try:
            enrolment_count = int(splitted[5])
            course.enrolment_count = enrolment_count
        except:
            pass

        if room not in master_map:
            master_map[room] = {}

        if time_slot_key not in master_map[room]:
            master_map[room][time_slot_key] = {
                "left_course": None,
                "right_course": None,
                "left_invigilator": None,
                "right_invigilator": None,
            }

        if lr == "LEFT":
            if master_map[room][time_slot_key]["left_course"] is not None:
                print(
                    f"****** ERROR: Duplicate Entry in Room Allotment for {room} @ {time_slot_key} ******"
                )

            master_map[room][time_slot_key]["left_course"] = course

        elif lr == "RIGHT":
            if master_map[room][time_slot_key]["right_course"] is not None:
                print(
                    f"****** ERROR: Duplicate Entry in Room Allotment for {room} @ {time_slot_key} ******"
                )

            master_map[room][time_slot_key]["right_course"] = course

        else:
            if (
                master_map[room][time_slot_key]["left_course"] is not None
                or master_map[room][time_slot_key]["right_course"] is not None
            ):
                print(
                    f"****** ERROR: Duplicate Entry in Room Allotment for {room} @ {time_slot_key} ******"
                )

            master_map[room][time_slot_key]["left_course"] = course
            master_map[room][time_slot_key]["right_course"] = course

    f.close()

    # Make left and right course same in half filled rooms
    for room in master_map:
        for time_slot_key in master_map[room]:
            left_course = master_map[room][time_slot_key]["left_course"]
            right_course = master_map[room][time_slot_key]["right_course"]

            if left_course is None:
                master_map[room][time_slot_key]["left_course"] = right_course

            if right_course is None:
                master_map[room][time_slot_key]["right_course"] = left_course

    return master_map


def get_dates_from_key(key):
    splitted = key.split("|")

    start = datetime.datetime.strptime(
        splitted[0].strip() + " " + splitted[1].strip(), "%d-%m-%y %H:%M"
    )
    end = datetime.datetime.strptime(
        splitted[0].strip() + " " + splitted[2].strip(), "%d-%m-%y %H:%M"
    )
    return (start, end)


def get_primary_invigilator(course, invigilator_list, start, end):
    # Get other invigilator after one faculty has been assigned
    if course.ic != None:
        fns = [
            partial(course.get_available_faculty, start, end),
            partial(invigilator_list.get_available_faculty, start, end),
        ]

    else:
        fns = [
            partial(course.get_available_faculty, start, end),
            # partial(invigilator_list.get_available_department_faculty,
            # course.ic.department, start, end),
            partial(invigilator_list.get_available_faculty, start, end),
        ]
    for fn in fns:
        invigilator = fn()

        if invigilator is not None:
            return invigilator

    return None


def get_secondary_invigilator(course, invigilator_list, start, end):
    # Get other invigilator after one faculty has been assigned
    try:
        fns = [
            partial(course.get_available_scholar, start, end),
            partial(
                invigilator_list.get_available_department_scholar,
                course.ic.department,
                start,
                end,
            ),
            partial(invigilator_list.get_available_scholar, start, end),
        ]

        for fn in fns:
            invigilator = fn()

            if invigilator is not None:
                return invigilator
    except:
        print("Could not get secondary invigilator", course)
        return None

def get_big_course_extra_invigilator(course, invigilator_list, start, end):
    # Get invigilator for big courses. course scholar > department scholar > course faculty > department faculty > other dept
    try:
        fns = [
            partial(course.get_available_scholar, start, end),
            partial(
                invigilator_list.get_available_department_scholar,
                course.ic.department,
                start,
                end,
            ),
            partial(course.get_available_faculty, start, end),
            partial(
                invigilator_list.get_available_department_faculty,
                course.ic.department,
                start,
                end,
            ),
            partial(invigilator_list.get_available_faculty, start, end),
            partial(invigilator_list.get_available_scholar, start, end),
        ]

        for fn in fns:
            invigilator = fn()

            if invigilator is not None:
                return invigilator
    except:
        print("Could not get big course extra invigilator", course)
        return None

def get_reserved_invigilator(invigilator_list, start, end):
    fns = [
        partial(invigilator_list.get_available_scholar, start, end),
        partial(invigilator_list.get_available_faculty, start, end),
    ]

    for fn in fns:
        invigilator = fn()

        if invigilator is not None:
            return invigilator

    return None


def assign_invigilators(master_map, invigilator_list):
    flag = True
    for room in master_map:
        for time_slot_key in master_map[room]:
            start = None
            end = None

            try:
                start, end = get_dates_from_key(time_slot_key)

            except:
                continue

            left_course = master_map[room][time_slot_key]["left_course"]
            right_course = master_map[room][time_slot_key]["right_course"]
            left_invigilator = master_map[room][time_slot_key]["left_invigilator"]
            right_invigilator = master_map[room][time_slot_key]["right_invigilator"]

            if (left_invigilator is not None) and (right_invigilator is not None):
                continue

            elif (left_invigilator is None) and (right_invigilator is None):
                if flag:
                    left_primary = get_primary_invigilator(
                        left_course, invigilator_list, start, end
                    )
                    right_primary = get_secondary_invigilator(
                        right_course, invigilator_list, start, end
                    )
                else:
                    left_primary = get_secondary_invigilator(
                        left_course, invigilator_list, start, end
                    )
                    right_primary = get_primary_invigilator(
                        right_course, invigilator_list, start, end
                    )

                if (left_primary is None) and (right_primary is None):
                    print(
                        f"****** ERROR: Could not allot primary invigilator at '{room}' for '{right_course.code}'  Alloting secondary invigilators ******"
                    )
                    if flag:
                        left_invigilator = get_secondary_invigilator(
                            left_course, invigilator_list, start, end
                        )
                        left_invigilator.duties.append(
                            Duty(room, left_course, start, end)
                        )
                        right_invigilator = get_primary_invigilator(
                            right_course, invigilator_list, start, end
                        )
                        right_invigilator.duties.append(
                            Duty(room, right_course, start, end)
                        )
                    else:
                        left_invigilator = get_primary_invigilator(
                            left_course, invigilator_list, start, end
                        )
                        left_invigilator.duties.append(
                            Duty(room, left_course, start, end)
                        )
                        right_invigilator = get_secondary_invigilator(
                            right_course, invigilator_list, start, end
                        )
                        right_invigilator.duties.append(
                            Duty(room, right_course, start, end)
                        )
                    if left_invigilator is None:
                        print(
                            f"Could not find primary and secondary invigilator at '{room}' for {left_course.code} "
                        )
                        continue
                    if right_invigilator is None:
                        print(
                            f"Could not find primary and secondary invigilator at '{room}' for {right_course.code} "
                        )
                        continue
                    master_map[room][time_slot_key][
                        "left_invigilator"
                    ] = left_invigilator
                    master_map[room][time_slot_key][
                        "right_invigilator"
                    ] = right_invigilator
                    continue

                elif left_primary is right_primary:
                    left_invigilator = left_primary
                    left_invigilator.duties.append(Duty(room, left_course, start, end))

                    if not left_primary.is_research_scholar:
                        right_invigilator = get_secondary_invigilator(
                            right_course, invigilator_list, start, end
                        )
                    else:
                        right_invigilator = get_primary_invigilator(
                            right_course, invigilator_list, start, end
                        )

                    if right_invigilator is None:
                        right_invigilator = get_primary_invigilator(
                            right_course, invigilator_list, start, end
                        )
                        if right_invigilator is None:
                            right_invigilator = get_secondary_invigilator(
                                right_course, invigilator_list, start, end
                            )
                    right_invigilator.duties.append(
                        Duty(room, right_course, start, end)
                    )

                    master_map[room][time_slot_key][
                        "left_invigilator"
                    ] = left_invigilator
                    master_map[room][time_slot_key][
                        "right_invigilator"
                    ] = right_invigilator

                else:
                    if len(left_course.faculty) > len(right_course.faculty):
                        left_invigilator = left_primary

                        left_invigilator.duties.append(
                            Duty(room, left_course, start, end)
                        )

                        if not left_invigilator.is_research_scholar:
                            right_invigilator = get_secondary_invigilator(
                                right_course, invigilator_list, start, end
                            )
                        else:
                            right_invigilator = get_primary_invigilator(
                                right_course, invigilator_list, start, end
                            )
                        if right_invigilator == None:
                            right_invigilator = get_primary_invigilator(
                                right_course, invigilator_list, start, end
                            )
                            if right_invigilator is None:
                                right_invigilator = get_secondary_invigilator(
                                    right_course, invigilator_list, start, end
                                )
                        right_invigilator.duties.append(
                            Duty(room, right_course, start, end)
                        )

                        master_map[room][time_slot_key][
                            "left_invigilator"
                        ] = left_invigilator
                        master_map[room][time_slot_key][
                            "right_invigilator"
                        ] = right_invigilator

                    else:
                        right_invigilator = right_primary

                        right_invigilator.duties.append(
                            Duty(room, right_course, start, end)
                        )

                        if right_invigilator.is_research_scholar:
                            left_invigilator = get_primary_invigilator(
                                left_course, invigilator_list, start, end
                            )
                        else:
                            left_invigilator = get_secondary_invigilator(
                                left_course, invigilator_list, start, end
                            )
                        if left_invigilator != None:
                            left_invigilator.duties.append(
                                Duty(room, left_course, start, end)
                            )

                            master_map[room][time_slot_key][
                                "left_invigilator"
                            ] = left_invigilator
                        master_map[room][time_slot_key][
                            "right_invigilator"
                        ] = right_invigilator

            elif left_invigilator is None:
                if not right_invigilator.is_research_scholar:
                    left_invigilator = get_secondary_invigilator(
                        left_course, invigilator_list, start, end
                    )
                else:
                    left_invigilator = get_primary_invigilator(
                        left_course, invigilator_list, start, end
                    )

                if left_invigilator is None:
                    print(
                        f"****** ERROR: Could not allot secondary invigilator at '{room}' for '{left_course.code}'  ******"
                    )
                    continue
                if hasattr(left_invigilator, "duties"):
                    left_invigilator.duties.append(Duty(room, left_course, start, end))
                    master_map[room][time_slot_key][
                        "left_invigilator"
                    ] = left_invigilator

            elif right_invigilator is None:
                if left_invigilator.is_research_scholar:
                    right_invigilator = get_primary_invigilator(
                        right_course, invigilator_list, start, end
                    )
                else:
                    right_invigilator = get_secondary_invigilator(
                        right_course, invigilator_list, start, end
                    )

                if right_invigilator is None:
                    print(
                        f"****** ERROR: Could not allot secondary invigilator at '{room}' for '{right_course.code}'  ******"
                    )
                    continue
                if hasattr(right_invigilator, "duties"):
                    right_invigilator.duties.append(
                        Duty(room, right_course, start, end)
                    )
                    master_map[room][time_slot_key][
                        "right_invigilator"
                    ] = right_invigilator
        flag = not flag


def assign_ics(master_map):
    ic_assigned_set = set()

    for room in master_map:
        for time_slot_key in master_map[room]:
            start = None
            end = None

            try:
                start, end = get_dates_from_key(time_slot_key)
            except:
                print(
                    f"****** ERROR: Invalid time slot key '{time_slot_key}' in room {room} ******"
                )
                print("Invigilation will not be done for this slot", os.linesep)
                continue

            left_course = master_map[room][time_slot_key]["left_course"]
            right_course = master_map[room][time_slot_key]["right_course"]

            if (left_course is not None) and (left_course.code not in ic_assigned_set):
                ic_assigned_set.add(left_course.code)

                if left_course.ic is not None:
                    master_map[room][time_slot_key]["left_invigilator"] = left_course.ic
                    left_course.ic.duties.append(Duty(room, left_course, start, end))

                else:
                    print(f"****** ERROR: IC is None for {left_course.code} ******")

            if (right_course is not None) and (
                right_course.code not in ic_assigned_set
            ):
                ic_assigned_set.add(right_course.code)

                if right_course.ic is not None:
                    master_map[room][time_slot_key][
                        "right_invigilator"
                    ] = right_course.ic
                    right_course.ic.duties.append(Duty(room, right_course, start, end))

                else:
                    print(f"****** ERROR: IC is None for {right_course.code} ******")


def assign_course_faculty(master_map):
    flag = True
    for room in master_map:
        for time_slot_key in master_map[room]:
            start = None
            end = None

            try:
                start, end = get_dates_from_key(time_slot_key)

            except:
                print(
                    f"****** ERROR: Invalid time slot key '{time_slot_key}' in room {room} ******"
                )
                print("Invigilation will not be done for this slot", os.linesep)
                continue

            left_course = master_map[room][time_slot_key]["left_course"]
            right_course = master_map[room][time_slot_key]["right_course"]

            no_invigilator = (
                master_map[room][time_slot_key]["left_invigilator"] is None
                and master_map[room][time_slot_key]["right_invigilator"] is None
            )

            if left_course is right_course and no_invigilator:
                faculty = left_course.get_available_faculty(start, end)

                if faculty is None:
                    continue

                master_map[room][time_slot_key]["left_invigilator"] = faculty
                faculty.duties.append(Duty(room, left_course, start, end))
                continue

            # Alternate assignment order based on flag
            if flag:
                # Flag = True: Try left course first, then right course
                if master_map[room][time_slot_key]["left_invigilator"] is None:
                    faculty = left_course.get_available_faculty(start, end)

                    if faculty is not None:
                        master_map[room][time_slot_key]["left_invigilator"] = faculty
                        faculty.duties.append(Duty(room, left_course, start, end))
                        continue

                if master_map[room][time_slot_key]["right_invigilator"] is None:
                    faculty = right_course.get_available_faculty(start, end)

                    if faculty is not None:
                        master_map[room][time_slot_key]["right_invigilator"] = faculty
                        faculty.duties.append(Duty(room, right_course, start, end))
                        continue
            else:
                # Flag = False: Try right course first, then left course
                if master_map[room][time_slot_key]["right_invigilator"] is None:
                    faculty = right_course.get_available_faculty(start, end)

                    if faculty is not None:
                        master_map[room][time_slot_key]["right_invigilator"] = faculty
                        faculty.duties.append(Duty(room, right_course, start, end))
                        continue

                if master_map[room][time_slot_key]["left_invigilator"] is None:
                    faculty = left_course.get_available_faculty(start, end)

                    if faculty is not None:
                        master_map[room][time_slot_key]["left_invigilator"] = faculty
                        faculty.duties.append(Duty(room, left_course, start, end))
                        continue

        flag = not flag


def assign_big_course_invigilators(master_map, invigilator_list, big_course_cutoffs):
    extra_assigned_set = set()

    for room in master_map:
        for time_slot_key in master_map[room]:
            start = None
            end = None

            try:
                start, end = get_dates_from_key(time_slot_key)
            except:
                continue

            left_course = master_map[room][time_slot_key]["left_course"]
            right_course = master_map[room][time_slot_key]["right_course"]
            left_invigilator = master_map[room][time_slot_key]["left_invigilator"]
            right_invigilator = master_map[room][time_slot_key]["right_invigilator"]

            intervals = big_course_cutoffs

            if left_course.code not in extra_assigned_set:
                for value in intervals:
                    if left_course.enrolment_count >= value:
                        # extra_invigilator = get_secondary_invigilator(
                        #     left_course, invigilator_list, start, end
                        # )

                        for duty in left_course.ic.duties:
                            if duty.course == left_course:
                                if duty.room!="TBA" and right_invigilator is not None and right_invigilator.is_research_scholar:
                                    extra_invigilator=get_primary_invigilator(left_course, invigilator_list, start, end)
                                elif duty.room!="TBA" and right_invigilator is not None and not right_invigilator.is_research_scholar:
                                    extra_invigilator=get_secondary_invigilator(left_course, invigilator_list, start, end)
                                else:
                                    extra_invigilator = get_big_course_extra_invigilator(
                                        left_course, invigilator_list, start, end
                                    )
                                if extra_invigilator is None:
                                    print(
                                        f"****** ERROR: No EXTRA Invigilators left for {left_course.code} @ {time_slot_key} ******"
                                    )
                                    continue
                                left_invigilator = extra_invigilator

                                extra_invigilator.duties.append(
                                    Duty(duty.room, left_course, start, end)
                                )
                                if duty.room!="TBA":
                                    master_map[room][time_slot_key][
                                        "left_invigilator"
                                    ] = extra_invigilator
                                duty.room = "TBA"
                                break

                extra_assigned_set.add(left_course.code)

            if right_course.code not in extra_assigned_set:
                for value in intervals:
                    if right_course.enrolment_count >= value:
                        # extra_invigilator = get_secondary_invigilator(
                        #     right_course, invigilator_list, start, end
                        # )

                        # if extra_invigilator is None:
                        #     print(
                        #         f"****** ERROR: No EXTRA Invigilators left for {right_course.code} @ {time_slot_key} ******"
                        #     )
                        #     continue

                        for duty in right_course.ic.duties:
                            if duty.course == right_course:
                                if duty.room!="TBA" and left_invigilator is not None and left_invigilator.is_research_scholar:
                                    extra_invigilator=get_primary_invigilator(right_course, invigilator_list, start, end)
                                elif duty.room!="TBA" and left_invigilator is not None and not left_invigilator.is_research_scholar:
                                    extra_invigilator=get_secondary_invigilator(right_course, invigilator_list, start, end)
                                else:
                                    extra_invigilator = get_big_course_extra_invigilator(
                                        right_course, invigilator_list, start, end
                                    )
                                if extra_invigilator is None:
                                    print(
                                        f"****** ERROR: No EXTRA Invigilators left for {right_course.code} @ {time_slot_key} ******"
                                    )
                                    continue
                                if duty.room!="TBA":
                                    master_map[room][time_slot_key][
                                        "right_invigilator"
                                    ] = extra_invigilator
                                extra_invigilator.duties.append(
                                    Duty(duty.room, right_course, start, end)
                                )
                                duty.room = "TBA"
                                break

                extra_assigned_set.add(right_course.code)


def assign_big_room_4_invigilators(master_map, invigilator_list, big_rooms):
    for room in master_map:
        if room not in big_rooms:
            continue

        for time_slot_key in master_map[room]:
            start = None
            end = None

            try:
                start, end = get_dates_from_key(time_slot_key)
            except:
                continue

            left_course = master_map[room][time_slot_key]["left_course"]
            right_course = master_map[room][time_slot_key]["right_course"]
            left_invigilator = master_map[room][time_slot_key]["left_invigilator"]
            right_invigilator = master_map[room][time_slot_key]["right_invigilator"]
            invigilator = None
            if left_invigilator.is_research_scholar:
                invigilator = get_primary_invigilator(
                    left_course, invigilator_list, start, end
                )
            if not left_invigilator.is_research_scholar or invigilator is None:
                invigilator = get_secondary_invigilator(
                    left_course, invigilator_list, start, end
                )
            invigilator.duties.append(Duty(room, left_course, start, end))

            invigilator = None
            if right_invigilator.is_research_scholar:
                invigilator = get_primary_invigilator(
                    right_course, invigilator_list, start, end
                )
            if not right_invigilator.is_research_scholar or invigilator is None:
                invigilator = get_secondary_invigilator(
                    right_course, invigilator_list, start, end
                )
            invigilator.duties.append(Duty(room, right_course, start, end))


def assign_big_room_3_invigilators(master_map, invigilator_list, big_rooms_3):
    for room in master_map:
        if room not in big_rooms_3:
            continue

        for time_slot_key in master_map[room]:
            start = None
            end = None

            try:
                start, end = get_dates_from_key(time_slot_key)
            except:
                continue

            left_course = master_map[room][time_slot_key]["left_course"]
            right_course = master_map[room][time_slot_key]["right_course"]
            left_invigilator = master_map[room][time_slot_key]["left_invigilator"]
            right_invigilator = master_map[room][time_slot_key]["right_invigilator"]
            invigilator = None

            if left_invigilator.is_research_scholar:
                invigilator = get_secondary_invigilator(
                    left_course, invigilator_list, start, end
                )
                invigilator.duties.append(Duty(room, left_course, start, end))
            else:
                invigilator = get_secondary_invigilator(
                    left_course, invigilator_list, start, end
                )
                invigilator.duties.append(Duty(room, right_course, start, end))


def assign_reserved_duties(master_map, invigilator_list, reserve_duties):
    assigned_set = set()
    dummy_course = Course("NA", "RESERVED DUTY")
    dummy_ic = Invigilator("NA", "NA", "NA", "NA", False)
    dummy_course.ic = dummy_ic

    for room in master_map:
        for time_slot_key in master_map[room]:
            start = None
            end = None

            try:
                start, end = get_dates_from_key(time_slot_key)
            except:
                continue

            if time_slot_key not in assigned_set:
                assigned_set.add(time_slot_key)

                for i in range(0, reserve_duties):
                    invigilator = get_reserved_invigilator(invigilator_list, start, end)

                    if invigilator is None:
                        print(
                            f"****** ERROR: No reserve invigilator for {time_slot_key} ******"
                        )
                        continue

                    invigilator.duties.append(Duty("C317", dummy_course, start, end))


def export_csv(invigilator_list, file_name):
    f = open(file_name, "w")

    f.write(
        f"invigilator_psrn,invigilator_name,invigilator_type,invigilator_dept,room,course_code,course_name,date,start_time,end_time,invigilator_email,total_invigilator_duties,ic_psrn,ic_name,ic_email,ic_chamber\n"
    )

    for invigilator in invigilator_list:
        try:
            invigilator_type = (
                "SCHOLAR" if invigilator.is_research_scholar else "FACULTY"
            )

            for duty in invigilator.duties:
                date = duty.start_time.strftime("%d %B %Y")
                start_time = duty.start_time.strftime("%H:%M:%S")
                end_time = duty.end_time.strftime("%H:%M:%S")

                f.write(
                    f"{invigilator.psrn},{invigilator.name},{invigilator_type},{invigilator.department},{duty.room},{duty.course.code},{duty.course.name},{date},{start_time},{end_time},{invigilator.email},{len(invigilator.duties)},{duty.course.ic.psrn},{duty.course.ic.name},{duty.course.ic.email},{duty.course.ic.chamber}\n"
                )
        except:
            print("Could not assign", invigilator)

    f.close()


def start_invigilation_process(
    faculty_csv,
    scholar_csv,
    chamber_csv,
    course_teacher_csv,
    leaves_csv,
    max_duties_csv,
    room_allotment_csv,
    reserve_duties,
    big_course_cutoffs,
    big_rooms_3,
):
    print("Starting....")

    # ENSURE UNIQUE ROWS IN EACH CSV

    # psrn, name, dept, email
    # Ensure UTF-8 WITHOUT BOM and WITHOUT commas
    invigilator_list = get_invigilator_list(faculty_csv, scholar_csv)

    # psrn, chamber
    # Ensure UTF-8 WITHOUT BOM and WITHOUT commas
    update_chamber_numbers(invigilator_list, chamber_csv)

    # Course Code, Course Title, Class_Instructor, Course_admin
    # Ensure UTF-8 WITHOUT BOM and WITHOUT commas
    # SORTED according to the course code
    course_list = get_course_list(course_teacher_csv, invigilator_list)

    # PSRN, start_date_time (DD/MM/YYYY HH:MM), end_date_time (DD/MM/YYYY HH:MM)
    # Example: H0008,16/12/2019 17:00,32/12/2019 22:00
    # Ensure UTF-8 WITHOUT BOM and WITHOUT commas
    update_invigilator_leaves(invigilator_list, leaves_csv)

    # PSRN, max_duties
    # Ensure UTF-8 WITHOUT BOM and WITHOUT commas
    update_invigilator_max_duties(invigilator_list, max_duties_csv)

    master_map = get_master_map(course_list, room_allotment_csv)

    assign_ics(master_map)

    assign_course_faculty(master_map)

    assign_invigilators(master_map, invigilator_list)

    assign_big_course_invigilators(master_map, invigilator_list, big_course_cutoffs)

    assign_big_room_4_invigilators(master_map, invigilator_list, ["F102", "F105"])

    assign_big_room_3_invigilators(master_map, invigilator_list, big_rooms_3)

    assign_reserved_duties(master_map, invigilator_list, reserve_duties)

    export_csv(invigilator_list.get_all(), "./InvigilationDuties.csv")


if __name__ == "__main__":
    start_invigilation_process(
        r"C:\Users\Anirudh\Desktop\New folder\TTDdata\24-25 sem2\compre\FACULTY.csv",
        r"C:\Users\Anirudh\Desktop\New folder\TTDdata\24-25 sem2\compre\PHD.csv",
        r"C:\Users\Anirudh\Desktop\New folder\TTDdata\24-25 sem2\compre\chamber.csv",
        r"C:\Users\Anirudh\Desktop\New folder\TTDdata\24-25 sem2\compre\For TT.csv",
        r"C:\Users\Anirudh\Desktop\New folder\TTDdata\24-25 sem2\compre\PhD_Leave_Data (2).csv",
        r"C:\Users\Anirudh\Desktop\New folder\TTDdata\24-25 sem2\compre\MAX.csv",
        r"C:\Users\Anirudh\Desktop\New folder\TTDdata\24-25 sem2\compre\RoomAllotment.csv",
        6,
        [40, 150, 300, 500, 1000],
        ["F103", "F104", "F106"],
    )
