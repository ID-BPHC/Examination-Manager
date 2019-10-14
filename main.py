import wx
import sys
import threading

from MainFrame import MainFrame
from algorithms import RoomAllotment
from algorithms.SeatingArrangement.main import start_seating_arrangement_process
from algorithms.Invigilation.main import start_invigilation_process
from algorithms.InvigilationReports.main import start_invig_report_generation
from xmlEditor import start_xml_editor

frame: MainFrame = None
app = None


def room_generate_btn_clicked(event):
    is_double = frame.room_algorithm_radio.GetSelection() == 1
    sys.stdout = frame.room_error_log_box
    sys.stderr = frame.room_error_log_box
    frame.room_error_log_box.ClearAll()
    thread = threading.Thread(target=RoomAllotment.start_process, args=(
        frame.room_csv_picker.GetPath(), frame.room_exam_csv_picker.GetPath(), is_double))
    thread.start()


def seating_generate_btn_clicked(event):
    sys.stdout = frame.seating_error_box
    sys.stderr = frame.seating_error_box
    frame.seating_error_box.ClearAll()
    thread = threading.Thread(target=start_seating_arrangement_process, args=(
        frame.seating_room_csv_picker.GetPath(), frame.seating_student_csv_picker.GetPath()))
    thread.start()


def invig_generate_btn_clicked(event):
    sys.stdout = frame.invig_error_box
    sys.stderr = frame.invig_error_box
    frame.invig_error_box.ClearAll()
    reserve_duties = int(frame.invig_reserve_duties_box.GetValue())
    cutoffs = [int(x)
               for x in frame.invig_big_course_cutoffs_box.GetValue().split(",")]
    thread = threading.Thread(target=start_invigilation_process, args=(
        frame.invig_faculty_csv_picker.GetPath(),
        frame.invig_scholar_csv_picker.GetPath(),
        frame.invig_chamber_csv_picker.GetPath(),
        frame.invig_timetable_csv_picker.GetPath(),
        frame.invig_leaves_csv_picker.GetPath(),
        frame.invig_duties_csv_picker.GetPath(),
        frame.invig_room_csv_picker.GetPath(),
        reserve_duties,
        cutoffs
    ))
    thread.start()


def report_config_clicked(event):
    start_xml_editor()


def report_invig_generate_btn_clicked(event):
    sys.stdout = frame.report_error_box
    sys.stderr = frame.report_error_box
    frame.report_error_box.ClearAll()
    thread = threading.Thread(target=start_invig_report_generation, args=(
        frame.report_invig_csv_picker.GetPath(),))
    thread.start()


if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame(None)
    frame.room_generate_btn.Bind(wx.EVT_BUTTON, room_generate_btn_clicked)
    frame.seating_generate_btn.Bind(
        wx.EVT_BUTTON, seating_generate_btn_clicked)
    frame.invig_generate_btn.Bind(wx.EVT_BUTTON, invig_generate_btn_clicked)
    frame.report_config_btn.Bind(wx.EVT_BUTTON, report_config_clicked)
    frame.report_invig_generate_btn.Bind(
        wx.EVT_BUTTON, report_invig_generate_btn_clicked)
    frame.Show()
    app.MainLoop()
