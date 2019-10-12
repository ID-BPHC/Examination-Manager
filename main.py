import wx
import sys
from MainFrame import MainFrame
from algorithms import RoomAllotment

frame: MainFrame = None
app = None


def room_generate_btn_clicked(event):
    is_double = frame.room_algorithm_radio.GetSelection() == 1
    sys.stdout = frame.room_error_log_box
    sys.stderr = frame.room_error_log_box
    RoomAllotment.start_process(
        frame.room_csv_picker.GetPath(), frame.room_exam_csv_picker.GetPath(), is_double)


if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame(None)
    frame.room_generate_btn.Bind(wx.EVT_BUTTON, room_generate_btn_clicked)
    frame.Show()
    app.MainLoop()
