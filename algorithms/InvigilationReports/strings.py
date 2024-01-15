from bs4 import BeautifulSoup
import os, sys


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


f = open(resource_path("invigilation_reports_config.xml"))
parsed = BeautifulSoup(f, "xml")

college_name = parsed.college.text
office_name = parsed.office.text
semester = parsed.semester.text
signature = parsed.signature.text

invigilator_greeting = parsed.invigilator.greeting.text
invigilator_intro = parsed.invigilator.intro.text
invigilator_notes = [x.text for x in parsed.invigilator.notes.findAll("note")]

ic_greeting = parsed.ic.greeting.text
ic_intro = parsed.ic.intro.text
ic_notes = [x.text for x in parsed.ic.notes.findAll("note")]
