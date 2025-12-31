from algorithms.InvigilationReports import strings
from algorithms.InvigilationReports.Table import (
    Invigilator_Report_Table,
    IC_Report_Table,
    Room_Captain_Report_Table,
    Group_Captain_Report_Table,
)
import datetime


class Report:
    college_name = strings.college_name
    office_name = strings.office_name
    semester = strings.semester
    date = datetime.datetime.now().strftime("%d %B %Y")
    signature = strings.signature
    intro = ""
    notes = []

    def __init__(self, recipent):
        self.recipent = recipent
        self.table = None
        self.greeting = ""


class Invigilator_Report(Report):

    intro = strings.invigilator_intro
    notes = strings.invigilator_notes

    def __init__(self, recipent):
        super().__init__(recipent)
        self.table = Invigilator_Report_Table()
        self.greeting = f"{strings.invigilator_greeting} {recipent.name}"


class IC_Report(Report):

    intro = strings.ic_intro
    notes = strings.ic_notes

    def __init__(self, recipent):
        super().__init__(recipent)
        self.table = IC_Report_Table()
        self.greeting = f"{strings.ic_greeting} {recipent.name}"


class Room_Captain_Report(Report):

    intro = strings.room_captain_intro
    notes = strings.room_captain_notes

    def __init__(self, recipent):
        super().__init__(recipent)
        self.table = Room_Captain_Report_Table()
        self.greeting = f"{strings.room_captain_greeting} {recipent.name}"


class Group_Captain_Report(Report):

    intro = strings.group_captain_intro
    notes = strings.group_captain_notes

    def __init__(self, recipent):
        super().__init__(recipent)
        self.table = Group_Captain_Report_Table()
        self.greeting = f"{strings.group_captain_greeting} {recipent.name}"
