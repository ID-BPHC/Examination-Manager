class Table:
    def __init__(self, header):
        self.rows = []
        self.rows.append(header)

    def add_row(self, row):
        self.rows.append(row)


class IC_Report_Table(Table):
    def __init__(self):
        super().__init__(
            [
                "Course Code",
                "Course Title",
                "Date",
                "Time",
                "Room",
                "Invigilator",
                "Email",
            ]
        )


class Invigilator_Report_Table(Table):
    def __init__(self):
        super().__init__(
            [
                "Course Code",
                "Course Title",
                "Date",
                "Time",
                "Room",
                "IC Name",
                "IC Chamber",
                "Email",
            ]
        )


class Room_Captain_Report_Table(Table):
    def __init__(self):
        super().__init__(
            [
                "Room",
                "Date",
                "Time",
                "Group Captain Name",
                "Group Captain Email",
                "Group Captain Mobile",
            ]
        )


class Group_Captain_Report_Table(Table):
    def __init__(self):
        super().__init__(
            [
                "Date",
                "Time",
                "Room",
                "Room Captain Name",
                "Email",
                "Mobile Number",
            ]
        )
