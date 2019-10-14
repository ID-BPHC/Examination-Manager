from bs4 import BeautifulSoup

f = open("./invigilation_reports_config.xml")
parsed = BeautifulSoup(f, 'xml')

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
