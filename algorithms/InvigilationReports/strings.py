from bs4 import BeautifulSoup
import os, sys

f = open("./invigilation_reports_config.xml")
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

room_captain_greeting = parsed.room_captain.greeting.text
room_captain_intro = parsed.room_captain.intro.text
room_captain_notes = [x.text for x in parsed.room_captain.notes.findAll("note")]

group_captain_greeting = parsed.group_captain.greeting.text
group_captain_intro = parsed.group_captain.intro.text
group_captain_notes = [x.text for x in parsed.group_captain.notes.findAll("note")]
