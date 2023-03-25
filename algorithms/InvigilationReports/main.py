from algorithms.InvigilationReports.Report import Invigilator_Report, IC_Report
from algorithms.InvigilationReports.Recipent import Recipent
from algorithms.InvigilationReports import styles

import os
import shutil
from reportlab.platypus import Paragraph, Table, Spacer, SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import landscape, A4


def get_invigilator_reports(file_name):
    report_map = {}
    f = open(file_name)

    for line in f.readlines():

        splitted = line.strip().split(",")
        invigilator_psrn = splitted[0]
        invigilator_name = splitted[1]
        room = splitted[4]
        course_code = splitted[5]
        course_name = splitted[6]
        date = splitted[7]
        time = splitted[8] + " to " + splitted[9]
        email = splitted[10]
        ic_name = splitted[13]
        ic_email = splitted[14]
        ic_chamber = splitted[15]

        if invigilator_psrn not in report_map:
            report_map[invigilator_psrn] = Invigilator_Report(
                Recipent(invigilator_name, email))

        report_map[invigilator_psrn].table.add_row(
            [course_code, course_name, date, time, room, ic_name, ic_chamber, ic_email])
                        


    f.close()

    return [report for report in report_map.values()]


def get_ic_reports(file_name):

    f = open(file_name)

    ic_map = {}

    for line in f.readlines():
        splitted = line.strip().split(",")
        invigilator_name = splitted[1]
        room = splitted[4]
        course_code = splitted[5]
        course_name = splitted[6]
        date = splitted[7]
        time = splitted[8] + " to " + splitted[9]
        invigilator_email = splitted[10]
        ic_psrn = splitted[12]
        ic_name = splitted[13]
        ic_email = splitted[14]

        if ic_psrn not in ic_map:
            ic_map[ic_psrn] = {"name": ic_name,
                               "email":  ic_email, "courses": {}}

        if course_code not in ic_map[ic_psrn]["courses"]:
            ic_map[ic_psrn]["courses"][course_code] = {
                "name": course_name,
                "date": date,
                "time": time,
                "invigilators": []
            }

        ic_map[ic_psrn]["courses"][course_code]["invigilators"].append(
            (room, invigilator_name, invigilator_email))
            # ic_map[ic_psrn].table.add_row(
            # [course_code, course_name, date, time, room, invigilator_name, invigilator_email])


    f.close()

    reports = []

    for ic in ic_map:

        report = IC_Report(Recipent(ic_map[ic]["name"], ic_map[ic]["email"]))

        for course_code in ic_map[ic]["courses"]:

            course = ic_map[ic]["courses"][course_code]
            invigilators = ic_map[ic]["courses"][course_code]["invigilators"]
            invigilators.sort()

            report.table.add_row(
                [course_code, course["name"], course["date"], course["time"], invigilators[0][0], invigilators[0][1], invigilators[0][2]])

            for invigilator in invigilators[1:]:
                report.table.add_row(
                    ["", "", "", "", invigilator[0], invigilator[1], invigilator[2]])

        reports.append(report)

    return reports


def generate_report_pdfs(reports, path):

    for report in reports:
        if(not(report.recipent.email)):
            print(report.recipent.name)
        doc = SimpleDocTemplate(os.path.join(
            path, report.recipent.email + ".pdf"))
        doc.pagesize = landscape(A4)

        flowables = []

        title = Paragraph(report.college_name, styles.get_title_style())
        flowables.append(title)

        office_name = Paragraph(report.office_name, styles.get_title_style())
        flowables.append(office_name)

        semester = Paragraph(report.semester, styles.get_semester_style())
        flowables.append(semester)

        date = Paragraph(report.date, styles.get_date_style())
        flowables.append(date)

        greeting = Paragraph(report.greeting, styles.get_greeting_style())
        flowables.append(greeting)

        intro = Paragraph(report.intro, styles.get_intro_style())
        flowables.append(intro)

        flowables.append(Spacer(1, 15))

        table = Table(report.table.rows, style=styles.get_table_style())
        flowables.append(table)

        flowables.append(Spacer(1, 20))

        signature_1 = Paragraph(report.signature, styles.get_signature_style())
        flowables.append(signature_1)

        signature_2 = Paragraph(
            report.office_name, styles.get_signature_style())
        flowables.append(signature_2)

        flowables.append(Spacer(1, 20))

        for index, note in enumerate(report.notes):
            item = Paragraph(f"{index + 1}. {note}", styles.get_intro_style())
            flowables.append(item)

        doc.build(flowables)


def start_invig_report_generation(invig_csv):

    print("***** Starting Report Generation *****")

    if os.path.exists("./Invigilation_Reports") and os.path.isdir("./Invigilation_Reports"):
        shutil.rmtree("./Invigilation_Reports")

    os.mkdir("./Invigilation_Reports")
    os.mkdir("./Invigilation_Reports/IC")
    os.mkdir("./Invigilation_Reports/Instructor")

    print("******** Generating Instructor PDFs ********")
    invigilator_reports = get_invigilator_reports(invig_csv)
    generate_report_pdfs(invigilator_reports,
                         "./Invigilation_Reports/Instructor")

    print("******** Generating IC PDFs ********")
    ic_reports = get_ic_reports(invig_csv)
    generate_report_pdfs(ic_reports, "./Invigilation_Reports/IC")

    print("******** Done ********")
