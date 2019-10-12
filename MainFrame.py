# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 10 2019)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.stc

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 1024,768 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		self.m_notebook2 = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panel3 = wx.Panel( self.m_notebook2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gbSizer2 = wx.GridBagSizer( 20, 20 )
		gbSizer2.SetFlexibleDirection( wx.BOTH )
		gbSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText1 = wx.StaticText( self.m_panel3, wx.ID_ANY, u"*Room CSV File*\n-room_num, capacity\n-No Duplicates\n-Sort by room number", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )

		gbSizer2.Add( self.m_staticText1, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.room_csv_picker = wx.FilePickerCtrl( self.m_panel3, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.csv", wx.DefaultPosition, wx.Size( -1,-1 ), wx.FLP_DEFAULT_STYLE )
		gbSizer2.Add( self.room_csv_picker, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText2 = wx.StaticText( self.m_panel3, wx.ID_ANY, u"*Exam CSV File*\n-course_code, course_title, Enrolment_Count, date (DD/MM/YY), start_time (HH:MM), end_time (HH:MM)\n-No Duplicates", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( 490 )

		gbSizer2.Add( self.m_staticText2, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 5 )

		self.room_exam_csv_picker = wx.FilePickerCtrl( self.m_panel3, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.csv", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		gbSizer2.Add( self.room_exam_csv_picker, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER|wx.EXPAND, 5 )

		room_algorithm_radioChoices = [ u"Single Course", u"Double Course" ]
		self.room_algorithm_radio = wx.RadioBox( self.m_panel3, wx.ID_ANY, u"Allotment Algorithm", wx.DefaultPosition, wx.Size( -1,-1 ), room_algorithm_radioChoices, 2, wx.RA_SPECIFY_COLS )
		self.room_algorithm_radio.SetSelection( 1 )
		gbSizer2.Add( self.room_algorithm_radio, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 5 )

		self.room_generate_btn = wx.Button( self.m_panel3, wx.ID_ANY, u"Generate", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer2.Add( self.room_generate_btn, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER|wx.ALL, 5 )

		self.room_error_log_box = wx.stc.StyledTextCtrl(self.m_panel3, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), 0)
		self.room_error_log_box.SetUseTabs ( True )
		self.room_error_log_box.SetTabWidth ( 4 )
		self.room_error_log_box.SetIndent ( 4 )
		self.room_error_log_box.SetTabIndents( True )
		self.room_error_log_box.SetBackSpaceUnIndents( True )
		self.room_error_log_box.SetViewEOL( False )
		self.room_error_log_box.SetViewWhiteSpace( False )
		self.room_error_log_box.SetMarginWidth( 2, 0 )
		self.room_error_log_box.SetIndentationGuides( True )
		self.room_error_log_box.SetMarginWidth( 1, 0 )
		self.room_error_log_box.SetMarginType( 0, wx.stc.STC_MARGIN_NUMBER );
		self.room_error_log_box.SetMarginWidth( 0, self.room_error_log_box.TextWidth( wx.stc.STC_STYLE_LINENUMBER, "_99999" ) )
		self.room_error_log_box.MarkerDefine( wx.stc.STC_MARKNUM_FOLDER, wx.stc.STC_MARK_BOXPLUS )
		self.room_error_log_box.MarkerSetBackground( wx.stc.STC_MARKNUM_FOLDER, wx.BLACK)
		self.room_error_log_box.MarkerSetForeground( wx.stc.STC_MARKNUM_FOLDER, wx.WHITE)
		self.room_error_log_box.MarkerDefine( wx.stc.STC_MARKNUM_FOLDEROPEN, wx.stc.STC_MARK_BOXMINUS )
		self.room_error_log_box.MarkerSetBackground( wx.stc.STC_MARKNUM_FOLDEROPEN, wx.BLACK )
		self.room_error_log_box.MarkerSetForeground( wx.stc.STC_MARKNUM_FOLDEROPEN, wx.WHITE )
		self.room_error_log_box.MarkerDefine( wx.stc.STC_MARKNUM_FOLDERSUB, wx.stc.STC_MARK_EMPTY )
		self.room_error_log_box.MarkerDefine( wx.stc.STC_MARKNUM_FOLDEREND, wx.stc.STC_MARK_BOXPLUS )
		self.room_error_log_box.MarkerSetBackground( wx.stc.STC_MARKNUM_FOLDEREND, wx.BLACK )
		self.room_error_log_box.MarkerSetForeground( wx.stc.STC_MARKNUM_FOLDEREND, wx.WHITE )
		self.room_error_log_box.MarkerDefine( wx.stc.STC_MARKNUM_FOLDEROPENMID, wx.stc.STC_MARK_BOXMINUS )
		self.room_error_log_box.MarkerSetBackground( wx.stc.STC_MARKNUM_FOLDEROPENMID, wx.BLACK)
		self.room_error_log_box.MarkerSetForeground( wx.stc.STC_MARKNUM_FOLDEROPENMID, wx.WHITE)
		self.room_error_log_box.MarkerDefine( wx.stc.STC_MARKNUM_FOLDERMIDTAIL, wx.stc.STC_MARK_EMPTY )
		self.room_error_log_box.MarkerDefine( wx.stc.STC_MARKNUM_FOLDERTAIL, wx.stc.STC_MARK_EMPTY )
		self.room_error_log_box.SetSelBackground( True, wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT ) )
		self.room_error_log_box.SetSelForeground( True, wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT ) )
		gbSizer2.Add( self.room_error_log_box, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 2 ), wx.EXPAND |wx.ALL, 5 )


		gbSizer2.AddGrowableCol( 0 )
		gbSizer2.AddGrowableCol( 1 )
		gbSizer2.AddGrowableRow( 3 )

		self.m_panel3.SetSizer( gbSizer2 )
		self.m_panel3.Layout()
		gbSizer2.Fit( self.m_panel3 )
		self.m_notebook2.AddPage( self.m_panel3, u"Room Allotment", True )
		self.m_panel4 = wx.Panel( self.m_notebook2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gbSizer21 = wx.GridBagSizer( 20, 20 )
		gbSizer21.SetFlexibleDirection( wx.BOTH )
		gbSizer21.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText11 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Room Allotment CSV File", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )

		gbSizer21.Add( self.m_staticText11, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.seating_room_csv_picker = wx.FilePickerCtrl( self.m_panel4, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.csv", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		gbSizer21.Add( self.seating_room_csv_picker, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText21 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Registered Students CSV File\n-student_id, course_code", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText21.Wrap( 350 )

		gbSizer21.Add( self.m_staticText21, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.seating_student_csv_picker = wx.FilePickerCtrl( self.m_panel4, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.csv", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		gbSizer21.Add( self.seating_student_csv_picker, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.seating_generate_btn = wx.Button( self.m_panel4, wx.ID_ANY, u"Generate", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer21.Add( self.seating_generate_btn, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 2 ), wx.ALIGN_CENTER|wx.ALL, 5 )

		self.seating_error_box = wx.stc.StyledTextCtrl(self.m_panel4, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), 0)
		self.seating_error_box.SetUseTabs ( True )
		self.seating_error_box.SetTabWidth ( 4 )
		self.seating_error_box.SetIndent ( 4 )
		self.seating_error_box.SetTabIndents( True )
		self.seating_error_box.SetBackSpaceUnIndents( True )
		self.seating_error_box.SetViewEOL( False )
		self.seating_error_box.SetViewWhiteSpace( False )
		self.seating_error_box.SetMarginWidth( 2, 0 )
		self.seating_error_box.SetIndentationGuides( True )
		self.seating_error_box.SetMarginWidth( 1, 0 )
		self.seating_error_box.SetMarginType( 0, wx.stc.STC_MARGIN_NUMBER );
		self.seating_error_box.SetMarginWidth( 0, self.seating_error_box.TextWidth( wx.stc.STC_STYLE_LINENUMBER, "_99999" ) )
		self.seating_error_box.MarkerDefine( wx.stc.STC_MARKNUM_FOLDER, wx.stc.STC_MARK_BOXPLUS )
		self.seating_error_box.MarkerSetBackground( wx.stc.STC_MARKNUM_FOLDER, wx.BLACK)
		self.seating_error_box.MarkerSetForeground( wx.stc.STC_MARKNUM_FOLDER, wx.WHITE)
		self.seating_error_box.MarkerDefine( wx.stc.STC_MARKNUM_FOLDEROPEN, wx.stc.STC_MARK_BOXMINUS )
		self.seating_error_box.MarkerSetBackground( wx.stc.STC_MARKNUM_FOLDEROPEN, wx.BLACK )
		self.seating_error_box.MarkerSetForeground( wx.stc.STC_MARKNUM_FOLDEROPEN, wx.WHITE )
		self.seating_error_box.MarkerDefine( wx.stc.STC_MARKNUM_FOLDERSUB, wx.stc.STC_MARK_EMPTY )
		self.seating_error_box.MarkerDefine( wx.stc.STC_MARKNUM_FOLDEREND, wx.stc.STC_MARK_BOXPLUS )
		self.seating_error_box.MarkerSetBackground( wx.stc.STC_MARKNUM_FOLDEREND, wx.BLACK )
		self.seating_error_box.MarkerSetForeground( wx.stc.STC_MARKNUM_FOLDEREND, wx.WHITE )
		self.seating_error_box.MarkerDefine( wx.stc.STC_MARKNUM_FOLDEROPENMID, wx.stc.STC_MARK_BOXMINUS )
		self.seating_error_box.MarkerSetBackground( wx.stc.STC_MARKNUM_FOLDEROPENMID, wx.BLACK)
		self.seating_error_box.MarkerSetForeground( wx.stc.STC_MARKNUM_FOLDEROPENMID, wx.WHITE)
		self.seating_error_box.MarkerDefine( wx.stc.STC_MARKNUM_FOLDERMIDTAIL, wx.stc.STC_MARK_EMPTY )
		self.seating_error_box.MarkerDefine( wx.stc.STC_MARKNUM_FOLDERTAIL, wx.stc.STC_MARK_EMPTY )
		self.seating_error_box.SetSelBackground( True, wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT ) )
		self.seating_error_box.SetSelForeground( True, wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT ) )
		gbSizer21.Add( self.seating_error_box, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 2 ), wx.EXPAND |wx.ALL, 5 )


		gbSizer21.AddGrowableCol( 0 )
		gbSizer21.AddGrowableCol( 1 )
		gbSizer21.AddGrowableRow( 3 )

		self.m_panel4.SetSizer( gbSizer21 )
		self.m_panel4.Layout()
		gbSizer21.Fit( self.m_panel4 )
		self.m_notebook2.AddPage( self.m_panel4, u"Seating Arrangement", False )
		self.m_panel5 = wx.Panel( self.m_notebook2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gbSizer211 = wx.GridBagSizer( 4, 8 )
		gbSizer211.SetFlexibleDirection( wx.BOTH )
		gbSizer211.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText111 = wx.StaticText( self.m_panel5, wx.ID_ANY, u"Room Allotment CSV File", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText111.Wrap( -1 )

		gbSizer211.Add( self.m_staticText111, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.invig_room_csv_picker = wx.FilePickerCtrl( self.m_panel5, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.csv", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		gbSizer211.Add( self.invig_room_csv_picker, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER|wx.EXPAND, 5 )

		self.m_staticText211 = wx.StaticText( self.m_panel5, wx.ID_ANY, u"Faculty List\n-psrn, name, department, email", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText211.Wrap( 350 )

		gbSizer211.Add( self.m_staticText211, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.invig_faculty_csv_picker = wx.FilePickerCtrl( self.m_panel5, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.csv", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		gbSizer211.Add( self.invig_faculty_csv_picker, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText19 = wx.StaticText( self.m_panel5, wx.ID_ANY, u"Scholar List\n-psrn, name, department, email", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText19.Wrap( -1 )

		gbSizer211.Add( self.m_staticText19, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.invig_scholar_csv_picker = wx.FilePickerCtrl( self.m_panel5, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.csv", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		gbSizer211.Add( self.invig_scholar_csv_picker, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText20 = wx.StaticText( self.m_panel5, wx.ID_ANY, u"Faculty Chamber CSV\n-psrn, chamber", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText20.Wrap( -1 )

		gbSizer211.Add( self.m_staticText20, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.invig_chamber_csv_picker = wx.FilePickerCtrl( self.m_panel5, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.csv", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		gbSizer211.Add( self.invig_chamber_csv_picker, wx.GBPosition( 3, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText212 = wx.StaticText( self.m_panel5, wx.ID_ANY, u"Timetable CSV\n-Course Code, Course Title, Class_Instructor, Course_admin", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText212.Wrap( -1 )

		gbSizer211.Add( self.m_staticText212, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.invig_timetable_csv_picker = wx.FilePickerCtrl( self.m_panel5, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.csv", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		gbSizer211.Add( self.invig_timetable_csv_picker, wx.GBPosition( 4, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText22 = wx.StaticText( self.m_panel5, wx.ID_ANY, u"Leaves CSV\n-PSRN, start_date_time, end_date_time (DD/MM/YYYY HH:MM)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText22.Wrap( -1 )

		gbSizer211.Add( self.m_staticText22, wx.GBPosition( 5, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.invig_leaves_csv_picker = wx.FilePickerCtrl( self.m_panel5, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.csv", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		gbSizer211.Add( self.invig_leaves_csv_picker, wx.GBPosition( 5, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText23 = wx.StaticText( self.m_panel5, wx.ID_ANY, u"Max Duties CSV\n-PSRN, max_duties", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText23.Wrap( -1 )

		gbSizer211.Add( self.m_staticText23, wx.GBPosition( 6, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.invig_duties_csv_picker = wx.FilePickerCtrl( self.m_panel5, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.csv", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		gbSizer211.Add( self.invig_duties_csv_picker, wx.GBPosition( 6, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText191 = wx.StaticText( self.m_panel5, wx.ID_ANY, u"Reserve duties per time slot", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText191.Wrap( -1 )

		gbSizer211.Add( self.m_staticText191, wx.GBPosition( 7, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.invig_reserve_duties_box = wx.SpinCtrl( self.m_panel5, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10, 0 )
		gbSizer211.Add( self.invig_reserve_duties_box, wx.GBPosition( 7, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText201 = wx.StaticText( self.m_panel5, wx.ID_ANY, u"Big Course Cutoffs", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText201.Wrap( -1 )

		gbSizer211.Add( self.m_staticText201, wx.GBPosition( 8, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.invig_big_course_cutoffs_box = wx.TextCtrl( self.m_panel5, wx.ID_ANY, u"150,300,500,1000", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer211.Add( self.invig_big_course_cutoffs_box, wx.GBPosition( 8, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.invig_generate_btn = wx.Button( self.m_panel5, wx.ID_ANY, u"Generate", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer211.Add( self.invig_generate_btn, wx.GBPosition( 9, 0 ), wx.GBSpan( 1, 2 ), wx.ALIGN_CENTER|wx.ALL, 5 )

		self.invig_error_box = wx.stc.StyledTextCtrl(self.m_panel5, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), 0)
		self.invig_error_box.SetUseTabs ( True )
		self.invig_error_box.SetTabWidth ( 4 )
		self.invig_error_box.SetIndent ( 4 )
		self.invig_error_box.SetTabIndents( True )
		self.invig_error_box.SetBackSpaceUnIndents( True )
		self.invig_error_box.SetViewEOL( False )
		self.invig_error_box.SetViewWhiteSpace( False )
		self.invig_error_box.SetMarginWidth( 2, 0 )
		self.invig_error_box.SetIndentationGuides( True )
		self.invig_error_box.SetMarginWidth( 1, 0 )
		self.invig_error_box.SetMarginType( 0, wx.stc.STC_MARGIN_NUMBER );
		self.invig_error_box.SetMarginWidth( 0, self.invig_error_box.TextWidth( wx.stc.STC_STYLE_LINENUMBER, "_99999" ) )
		self.invig_error_box.MarkerDefine( wx.stc.STC_MARKNUM_FOLDER, wx.stc.STC_MARK_BOXPLUS )
		self.invig_error_box.MarkerSetBackground( wx.stc.STC_MARKNUM_FOLDER, wx.BLACK)
		self.invig_error_box.MarkerSetForeground( wx.stc.STC_MARKNUM_FOLDER, wx.WHITE)
		self.invig_error_box.MarkerDefine( wx.stc.STC_MARKNUM_FOLDEROPEN, wx.stc.STC_MARK_BOXMINUS )
		self.invig_error_box.MarkerSetBackground( wx.stc.STC_MARKNUM_FOLDEROPEN, wx.BLACK )
		self.invig_error_box.MarkerSetForeground( wx.stc.STC_MARKNUM_FOLDEROPEN, wx.WHITE )
		self.invig_error_box.MarkerDefine( wx.stc.STC_MARKNUM_FOLDERSUB, wx.stc.STC_MARK_EMPTY )
		self.invig_error_box.MarkerDefine( wx.stc.STC_MARKNUM_FOLDEREND, wx.stc.STC_MARK_BOXPLUS )
		self.invig_error_box.MarkerSetBackground( wx.stc.STC_MARKNUM_FOLDEREND, wx.BLACK )
		self.invig_error_box.MarkerSetForeground( wx.stc.STC_MARKNUM_FOLDEREND, wx.WHITE )
		self.invig_error_box.MarkerDefine( wx.stc.STC_MARKNUM_FOLDEROPENMID, wx.stc.STC_MARK_BOXMINUS )
		self.invig_error_box.MarkerSetBackground( wx.stc.STC_MARKNUM_FOLDEROPENMID, wx.BLACK)
		self.invig_error_box.MarkerSetForeground( wx.stc.STC_MARKNUM_FOLDEROPENMID, wx.WHITE)
		self.invig_error_box.MarkerDefine( wx.stc.STC_MARKNUM_FOLDERMIDTAIL, wx.stc.STC_MARK_EMPTY )
		self.invig_error_box.MarkerDefine( wx.stc.STC_MARKNUM_FOLDERTAIL, wx.stc.STC_MARK_EMPTY )
		self.invig_error_box.SetSelBackground( True, wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT ) )
		self.invig_error_box.SetSelForeground( True, wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT ) )
		gbSizer211.Add( self.invig_error_box, wx.GBPosition( 10, 0 ), wx.GBSpan( 1, 2 ), wx.EXPAND |wx.ALL, 5 )


		gbSizer211.AddGrowableCol( 0 )
		gbSizer211.AddGrowableCol( 1 )
		gbSizer211.AddGrowableRow( 10 )

		self.m_panel5.SetSizer( gbSizer211 )
		self.m_panel5.Layout()
		gbSizer211.Fit( self.m_panel5 )
		self.m_notebook2.AddPage( self.m_panel5, u"Invigilation", False )
		self.m_panel6 = wx.Panel( self.m_notebook2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gbSizer212 = wx.GridBagSizer( 20, 20 )
		gbSizer212.SetFlexibleDirection( wx.BOTH )
		gbSizer212.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText112 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"Invigilation CSV File", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText112.Wrap( -1 )

		gbSizer212.Add( self.m_staticText112, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.report_invig_csv_picker = wx.FilePickerCtrl( self.m_panel6, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.csv", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		gbSizer212.Add( self.report_invig_csv_picker, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.report_invig_generate_btn = wx.Button( self.m_panel6, wx.ID_ANY, u"Generate Invigilation PDFs", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer212.Add( self.report_invig_generate_btn, wx.GBPosition( 0, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText213 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"Seating Arrangement XLSX", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText213.Wrap( 350 )

		gbSizer212.Add( self.m_staticText213, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.report_seating_xlsx_picker = wx.FilePickerCtrl( self.m_panel6, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.xlsx", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		gbSizer212.Add( self.report_seating_xlsx_picker, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText31 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"Registered Students CSV File\n-student_id, course_code", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText31.Wrap( -1 )

		gbSizer212.Add( self.m_staticText31, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.reprot_students_csv_picker = wx.FilePickerCtrl( self.m_panel6, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.csv", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		gbSizer212.Add( self.reprot_students_csv_picker, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText32 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"IC Email Course CSV\ncourse_code, ic_email", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText32.Wrap( -1 )

		gbSizer212.Add( self.m_staticText32, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.report_ic_csv_picker = wx.FilePickerCtrl( self.m_panel6, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.csv", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		gbSizer212.Add( self.report_ic_csv_picker, wx.GBPosition( 3, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.report_generate_seat_map_btn = wx.Button( self.m_panel6, wx.ID_ANY, u"Generate Seating Maps", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer212.Add( self.report_generate_seat_map_btn, wx.GBPosition( 1, 2 ), wx.GBSpan( 3, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.report_error_box = wx.stc.StyledTextCtrl(self.m_panel6, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), 0)
		self.report_error_box.SetUseTabs ( True )
		self.report_error_box.SetTabWidth ( 4 )
		self.report_error_box.SetIndent ( 4 )
		self.report_error_box.SetTabIndents( True )
		self.report_error_box.SetBackSpaceUnIndents( True )
		self.report_error_box.SetViewEOL( False )
		self.report_error_box.SetViewWhiteSpace( False )
		self.report_error_box.SetMarginWidth( 2, 0 )
		self.report_error_box.SetIndentationGuides( True )
		self.report_error_box.SetMarginWidth( 1, 0 )
		self.report_error_box.SetMarginType( 0, wx.stc.STC_MARGIN_NUMBER );
		self.report_error_box.SetMarginWidth( 0, self.report_error_box.TextWidth( wx.stc.STC_STYLE_LINENUMBER, "_99999" ) )
		self.report_error_box.MarkerDefine( wx.stc.STC_MARKNUM_FOLDER, wx.stc.STC_MARK_BOXPLUS )
		self.report_error_box.MarkerSetBackground( wx.stc.STC_MARKNUM_FOLDER, wx.BLACK)
		self.report_error_box.MarkerSetForeground( wx.stc.STC_MARKNUM_FOLDER, wx.WHITE)
		self.report_error_box.MarkerDefine( wx.stc.STC_MARKNUM_FOLDEROPEN, wx.stc.STC_MARK_BOXMINUS )
		self.report_error_box.MarkerSetBackground( wx.stc.STC_MARKNUM_FOLDEROPEN, wx.BLACK )
		self.report_error_box.MarkerSetForeground( wx.stc.STC_MARKNUM_FOLDEROPEN, wx.WHITE )
		self.report_error_box.MarkerDefine( wx.stc.STC_MARKNUM_FOLDERSUB, wx.stc.STC_MARK_EMPTY )
		self.report_error_box.MarkerDefine( wx.stc.STC_MARKNUM_FOLDEREND, wx.stc.STC_MARK_BOXPLUS )
		self.report_error_box.MarkerSetBackground( wx.stc.STC_MARKNUM_FOLDEREND, wx.BLACK )
		self.report_error_box.MarkerSetForeground( wx.stc.STC_MARKNUM_FOLDEREND, wx.WHITE )
		self.report_error_box.MarkerDefine( wx.stc.STC_MARKNUM_FOLDEROPENMID, wx.stc.STC_MARK_BOXMINUS )
		self.report_error_box.MarkerSetBackground( wx.stc.STC_MARKNUM_FOLDEROPENMID, wx.BLACK)
		self.report_error_box.MarkerSetForeground( wx.stc.STC_MARKNUM_FOLDEROPENMID, wx.WHITE)
		self.report_error_box.MarkerDefine( wx.stc.STC_MARKNUM_FOLDERMIDTAIL, wx.stc.STC_MARK_EMPTY )
		self.report_error_box.MarkerDefine( wx.stc.STC_MARKNUM_FOLDERTAIL, wx.stc.STC_MARK_EMPTY )
		self.report_error_box.SetSelBackground( True, wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT ) )
		self.report_error_box.SetSelForeground( True, wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT ) )
		gbSizer212.Add( self.report_error_box, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 3 ), wx.EXPAND |wx.ALL, 5 )


		gbSizer212.AddGrowableCol( 0 )
		gbSizer212.AddGrowableCol( 1 )
		gbSizer212.AddGrowableRow( 4 )

		self.m_panel6.SetSizer( gbSizer212 )
		self.m_panel6.Layout()
		gbSizer212.Fit( self.m_panel6 )
		self.m_notebook2.AddPage( self.m_panel6, u"Reports", False )
		self.m_panel7 = wx.Panel( self.m_notebook2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gbSizer15 = wx.GridBagSizer( 0, 0 )
		gbSizer15.SetFlexibleDirection( wx.BOTH )
		gbSizer15.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.mailer_login_btn = wx.Button( self.m_panel7, wx.ID_ANY, u"Login with Gmail", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer15.Add( self.mailer_login_btn, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 2 ), wx.ALIGN_CENTER|wx.ALL|wx.EXPAND, 5 )

		self.m_staticText28 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"Subject", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText28.Wrap( -1 )

		gbSizer15.Add( self.m_staticText28, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.mailer_subject_box = wx.TextCtrl( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer15.Add( self.mailer_subject_box, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText29 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"Body", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText29.Wrap( -1 )

		gbSizer15.Add( self.m_staticText29, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.mailer_body_box = wx.stc.StyledTextCtrl(self.m_panel7, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,225 ), 0)
		self.mailer_body_box.SetUseTabs ( True )
		self.mailer_body_box.SetTabWidth ( 4 )
		self.mailer_body_box.SetIndent ( 4 )
		self.mailer_body_box.SetTabIndents( True )
		self.mailer_body_box.SetBackSpaceUnIndents( True )
		self.mailer_body_box.SetViewEOL( False )
		self.mailer_body_box.SetViewWhiteSpace( False )
		self.mailer_body_box.SetMarginWidth( 2, 0 )
		self.mailer_body_box.SetIndentationGuides( True )
		self.mailer_body_box.SetMarginWidth( 1, 0 )
		self.mailer_body_box.SetMarginWidth ( 0, 0 )
		self.mailer_body_box.MarkerDefine( wx.stc.STC_MARKNUM_FOLDER, wx.stc.STC_MARK_BOXPLUS )
		self.mailer_body_box.MarkerSetBackground( wx.stc.STC_MARKNUM_FOLDER, wx.BLACK)
		self.mailer_body_box.MarkerSetForeground( wx.stc.STC_MARKNUM_FOLDER, wx.WHITE)
		self.mailer_body_box.MarkerDefine( wx.stc.STC_MARKNUM_FOLDEROPEN, wx.stc.STC_MARK_BOXMINUS )
		self.mailer_body_box.MarkerSetBackground( wx.stc.STC_MARKNUM_FOLDEROPEN, wx.BLACK )
		self.mailer_body_box.MarkerSetForeground( wx.stc.STC_MARKNUM_FOLDEROPEN, wx.WHITE )
		self.mailer_body_box.MarkerDefine( wx.stc.STC_MARKNUM_FOLDERSUB, wx.stc.STC_MARK_EMPTY )
		self.mailer_body_box.MarkerDefine( wx.stc.STC_MARKNUM_FOLDEREND, wx.stc.STC_MARK_BOXPLUS )
		self.mailer_body_box.MarkerSetBackground( wx.stc.STC_MARKNUM_FOLDEREND, wx.BLACK )
		self.mailer_body_box.MarkerSetForeground( wx.stc.STC_MARKNUM_FOLDEREND, wx.WHITE )
		self.mailer_body_box.MarkerDefine( wx.stc.STC_MARKNUM_FOLDEROPENMID, wx.stc.STC_MARK_BOXMINUS )
		self.mailer_body_box.MarkerSetBackground( wx.stc.STC_MARKNUM_FOLDEROPENMID, wx.BLACK)
		self.mailer_body_box.MarkerSetForeground( wx.stc.STC_MARKNUM_FOLDEROPENMID, wx.WHITE)
		self.mailer_body_box.MarkerDefine( wx.stc.STC_MARKNUM_FOLDERMIDTAIL, wx.stc.STC_MARK_EMPTY )
		self.mailer_body_box.MarkerDefine( wx.stc.STC_MARKNUM_FOLDERTAIL, wx.stc.STC_MARK_EMPTY )
		self.mailer_body_box.SetSelBackground( True, wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT ) )
		self.mailer_body_box.SetSelForeground( True, wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT ) )
		gbSizer15.Add( self.mailer_body_box, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.EXPAND |wx.ALL, 5 )

		self.m_staticText30 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"Directory", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText30.Wrap( -1 )

		gbSizer15.Add( self.m_staticText30, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.mailer_dir_picker = wx.DirPickerCtrl( self.m_panel7, wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE )
		gbSizer15.Add( self.mailer_dir_picker, wx.GBPosition( 3, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.mailer_send_btn = wx.Button( self.m_panel7, wx.ID_ANY, u"Send Mails", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer15.Add( self.mailer_send_btn, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		self.mailer_error_box = wx.stc.StyledTextCtrl(self.m_panel7, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
		self.mailer_error_box.SetUseTabs ( True )
		self.mailer_error_box.SetTabWidth ( 4 )
		self.mailer_error_box.SetIndent ( 4 )
		self.mailer_error_box.SetTabIndents( True )
		self.mailer_error_box.SetBackSpaceUnIndents( True )
		self.mailer_error_box.SetViewEOL( False )
		self.mailer_error_box.SetViewWhiteSpace( False )
		self.mailer_error_box.SetMarginWidth( 2, 0 )
		self.mailer_error_box.SetIndentationGuides( True )
		self.mailer_error_box.SetMarginType ( 1, wx.stc.STC_MARGIN_SYMBOL )
		self.mailer_error_box.SetMarginMask ( 1, wx.stc.STC_MASK_FOLDERS )
		self.mailer_error_box.SetMarginWidth ( 1, 16)
		self.mailer_error_box.SetMarginSensitive( 1, True )
		self.mailer_error_box.SetProperty ( "fold", "1" )
		self.mailer_error_box.SetFoldFlags ( wx.stc.STC_FOLDFLAG_LINEBEFORE_CONTRACTED | wx.stc.STC_FOLDFLAG_LINEAFTER_CONTRACTED );
		self.mailer_error_box.SetMarginType( 0, wx.stc.STC_MARGIN_NUMBER );
		self.mailer_error_box.SetMarginWidth( 0, self.mailer_error_box.TextWidth( wx.stc.STC_STYLE_LINENUMBER, "_99999" ) )
		self.mailer_error_box.MarkerDefine( wx.stc.STC_MARKNUM_FOLDER, wx.stc.STC_MARK_BOXPLUS )
		self.mailer_error_box.MarkerSetBackground( wx.stc.STC_MARKNUM_FOLDER, wx.BLACK)
		self.mailer_error_box.MarkerSetForeground( wx.stc.STC_MARKNUM_FOLDER, wx.WHITE)
		self.mailer_error_box.MarkerDefine( wx.stc.STC_MARKNUM_FOLDEROPEN, wx.stc.STC_MARK_BOXMINUS )
		self.mailer_error_box.MarkerSetBackground( wx.stc.STC_MARKNUM_FOLDEROPEN, wx.BLACK )
		self.mailer_error_box.MarkerSetForeground( wx.stc.STC_MARKNUM_FOLDEROPEN, wx.WHITE )
		self.mailer_error_box.MarkerDefine( wx.stc.STC_MARKNUM_FOLDERSUB, wx.stc.STC_MARK_EMPTY )
		self.mailer_error_box.MarkerDefine( wx.stc.STC_MARKNUM_FOLDEREND, wx.stc.STC_MARK_BOXPLUS )
		self.mailer_error_box.MarkerSetBackground( wx.stc.STC_MARKNUM_FOLDEREND, wx.BLACK )
		self.mailer_error_box.MarkerSetForeground( wx.stc.STC_MARKNUM_FOLDEREND, wx.WHITE )
		self.mailer_error_box.MarkerDefine( wx.stc.STC_MARKNUM_FOLDEROPENMID, wx.stc.STC_MARK_BOXMINUS )
		self.mailer_error_box.MarkerSetBackground( wx.stc.STC_MARKNUM_FOLDEROPENMID, wx.BLACK)
		self.mailer_error_box.MarkerSetForeground( wx.stc.STC_MARKNUM_FOLDEROPENMID, wx.WHITE)
		self.mailer_error_box.MarkerDefine( wx.stc.STC_MARKNUM_FOLDERMIDTAIL, wx.stc.STC_MARK_EMPTY )
		self.mailer_error_box.MarkerDefine( wx.stc.STC_MARKNUM_FOLDERTAIL, wx.stc.STC_MARK_EMPTY )
		self.mailer_error_box.SetSelBackground( True, wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT ) )
		self.mailer_error_box.SetSelForeground( True, wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT ) )
		gbSizer15.Add( self.mailer_error_box, wx.GBPosition( 5, 0 ), wx.GBSpan( 1, 2 ), wx.EXPAND |wx.ALL, 5 )


		gbSizer15.AddGrowableCol( 0 )
		gbSizer15.AddGrowableCol( 1 )
		gbSizer15.AddGrowableRow( 5 )

		self.m_panel7.SetSizer( gbSizer15 )
		self.m_panel7.Layout()
		gbSizer15.Fit( self.m_panel7 )
		self.m_notebook2.AddPage( self.m_panel7, u"Mailer", False )

		bSizer1.Add( self.m_notebook2, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

	def __del__( self ):
		pass


