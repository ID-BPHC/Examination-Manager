import csv
import datetime
import pprint
from research_scholar_extract import find_research_scholar_by_date
pp = pprint.PrettyPrinter(width=82, compact=True)
def find_course_details_by_course_code(code):
    f=open('./InvigilationDuties.csv')
    for line in f.readlines():
        line=line.strip()
        splitted=line.split(",")
        #print(splitted[5])
        if(code==splitted[5]):
            course=[]
            course.append([splitted[5],splitted[6],splitted[7],splitted[8],splitted[9],splitted[12],splitted[13],splitted[14],splitted[15]])

            return course
def get_research_scholars(input_date, check):
    # input_date=datetime.datetime.strptime(input_date, "%d-%m-%y")
    print(input_date)
    research_scholars_to_be_alloted=find_research_scholar_by_date(input_date, check)
    return research_scholars_to_be_alloted
def increase_invigilation_duties(psrn_number):
    f=open('./InvigilationDuties.csv','w')
    for line in f.readlines():
        line=line.strip()
        splitted=line.split(",")

def main():
    f_course_error=open("./Room_Course_Error.csv")
    check = 0
    for line in f_course_error.readlines():
        line=line.strip()
        splitted=line.split(",")
        room=splitted[0]
        course_to_be_searched=splitted[1]
        course=find_course_details_by_course_code(course_to_be_searched)
        exam_date_to_be_alloted=datetime.datetime.strptime(course[0][2], "%d-%m-%y")
        research_scholar_by_date=get_research_scholars(exam_date_to_be_alloted, check)
        check = 1
        f=open('./InvigilationDuties.csv','a')
        scholar="SCHOLAR"
        Invigilation_count="3"
        # print(research_scholar_by_date[0])
        f.write(f"{research_scholar_by_date[0][0]},{research_scholar_by_date[0][1]}, {scholar}, {research_scholar_by_date[0][2]},{room}, {course[0][0]},{course[0][1]},{course[0][2]},{course[0][3]},{course[0][4]},{research_scholar_by_date[0][3]},{Invigilation_count}, {course[0][5]},{course[0][6]},{course[0][7]},{course[0][8]}\n")
        f.write(f"{research_scholar_by_date[1][0]},{research_scholar_by_date[1][1]}, {scholar}, {research_scholar_by_date[1][2]},{room}, {course[0][0]},{course[0][1]},{course[0][2]},{course[0][3]},{course[0][4]},{research_scholar_by_date[1][3]},{Invigilation_count}, {course[0][5]},{course[0][6]},{course[0][7]},{course[0][8]}\n")
main()
