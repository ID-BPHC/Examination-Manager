import pandas as pd
import os

# Set Pandas to display all rows and columns
pd.set_option("display.max_rows", None)  # Show all rows
pd.set_option("display.max_columns", None)  # Show all columns


def get_room_data(staff_duties):
    try:
        room_data = pd.read_excel(staff_duties, sheet_name="ROOM", header=None)
        room_data.columns = ["Room", "Time"]
    except:
        print("Error: Sheet 'ROOM' not found in the excel file")

    # Cleaning the data
    room_data[["Date", "Start Time", "End Time"]] = room_data["Time"].str.split(
        "|", expand=True
    )
    room_data = room_data.drop(columns=["Time"])
    room_data["Period"] = room_data["End Time"].apply(
        lambda x: "FN" if x < "14:00" else "AN" if x >= "14:00" else ""
    )
    room_data["Floor"] = room_data["Room"].apply(get_floor)
    room_data["Block"] = room_data["Room"].str.strip().str[0]

    return room_data


def get_staff_data(staff_duties):
    try:
        staff_data = pd.read_excel(staff_duties, sheet_name="STAFF", header=None)
    except:
        print("Error: Sheet 'STAFF' not found in the excel file")

    # Cleaning the data
    staff_data.columns = [
        "ID",
        "Name",
        "Branch",
        "Role",
        "Mobile Number",
        "Email",
    ]

    return staff_data


def get_leave_data(staff_leave):
    leave_data = pd.read_excel(staff_leave, header=None)
    leave_data.columns = ["ID", "email", "start_date", "end_date"]
    return leave_data


def get_floor(room_name):
    if room_name[-3:].isdigit():
        floor_number = int(room_name[-3])
        return "Ground Floor" if floor_number == 1 else "First Floor"
    return "Reserved"


def get_duty_limits(max_duties):
    duty_limits_data = pd.read_excel(max_duties, header=None)
    duty_limits_data.columns = ["ID", "Max Duties"]
    duty_limits = dict(zip(duty_limits_data["ID"], duty_limits_data["Max Duties"]))

    return duty_limits


def main_allot(room_data, staff_data, leave_data, duty_limits):

    # Merging Data (staff data and leave data)
    merged_data = pd.merge(
        staff_data,
        leave_data[["ID", "end_date"]],
        on=["ID"],
        how="left",
    )

    # Assinging Group captains and Room Captains
    room_captains = merged_data[merged_data["Role"] == "ROOM CAPTAIN"]
    group_captains = merged_data[merged_data["Role"] == "GROUP CAPTAIN"]

    # Indexing Room and Group Captains according to their branch

    room_data = room_data.sort_values(by=["Room", "Date", "Period"])
    room_data = room_data.drop_duplicates()

    # Allotment Logic
    room_data["Date"] = pd.to_datetime(
        room_data["Date"], format="%d-%m-%y", errors="coerce", dayfirst=True
    )
    room_captains.loc[:, "end_date"] = pd.to_datetime(
        room_captains["end_date"], format="%d-%m-%y", errors="coerce"
    )
    group_captains.loc[:, "end_date"] = pd.to_datetime(
        group_captains["end_date"], format="%d-%m-%y", errors="coerce"
    )

    room_data["Room Captain Name"] = None
    room_data["Room Captain ID"] = None
    room_data["Group Captain Name"] = None
    room_data["Group Captain ID"] = None

    room_data = allot_room_captains(room_data, room_captains, duty_limits)
    room_data = allot_group_captains(room_data, group_captains, duty_limits)

    # Final Modifications to the data
    room_data["Group Captain Email ID"] = (
        room_data["Group Captain"].str.split("-").str[3]
    )
    room_data["Group Captain Mobile Number"] = (
        room_data["Group Captain"].str.split("-").str[2]
    )
    room_data["Group Captain Name"] = room_data["Group Captain"].str.split("-").str[1]
    room_data["Group Captain ID"] = room_data["Group Captain"].str.split("-").str[0]

    rows_to_duplicate = room_data[room_data["Room"].isin(["F102", "F105"])]
    duplicated_rows = rows_to_duplicate.copy()
    room_data.loc[rows_to_duplicate.index, "Room Captain"] = (
        rows_to_duplicate["Room Captain"].str.split(",").str[0]
    )
    duplicated_rows["Room Captain"] = (
        rows_to_duplicate["Room Captain"].str.split(",").str[1]
    )

    room_data_1 = pd.concat([room_data, duplicated_rows], ignore_index=True)

    room_data_1["Room Captain Email ID"] = (
        room_data_1["Room Captain"].str.split("-").str[3]
    )
    room_data_1["Room Captain Mobile Number"] = (
        room_data_1["Room Captain"].str.split("-").str[2]
    )
    room_data_1["Room Captain Name"] = room_data_1["Room Captain"].str.split("-").str[1]
    room_data_1["Room Captain ID"] = room_data_1["Room Captain"].str.split("-").str[0]

    room_captains = room_captains.rename(
        columns={
            "ID": "Room Captain ID",
            "Branch": "Room Captain Branch",
            "Name": "Room Captain Name",
        }
    )

    room_data_1["Room Captain ID"] = room_data_1["Room Captain ID"].astype(str)
    room_captains.loc[:, "Room Captain ID"] = room_captains["Room Captain ID"].astype(
        str
    )
    room_data_1["Room Captain ID"] = room_data_1["Room Captain ID"].str.strip()
    room_captains.loc[:, "Room Captain ID"] = room_captains[
        "Room Captain ID"
    ].str.strip()

    merged_df = room_data_1.merge(room_captains, on="Room Captain ID", how="inner")

    merged_df.drop(
        ["Room Captain Name_y", "Role", "Mobile Number", "Email", "end_date"],
        axis=1,
        inplace=True,
    )

    merged_df.rename(
        columns={
            "Room Captain Name_x": "Room Captain Name",
            "Room Captain Branch_y": "Room Captain Branch",
        },
        inplace=True,
    )

    merged_df.drop(["Room Captain", "Group Captain"], axis=1, inplace=True)

    cols = [
        "Room",
        "Date",
        "Start Time",
        "End Time",
        "Period",
        "Floor",
        "Room Captain ID",
        "Room Captain Name",
        "Room Captain Email ID",
        "Room Captain Mobile Number",
        "Room Captain Branch",
        "Group Captain ID",
        "Group Captain Name",
        "Group Captain Email ID",
        "Group Captain Mobile Number",
    ]
    merged_df = merged_df[cols]
    merged_df = merged_df.sort_values(by=["Date", "Start Time", "Room"])
    return merged_df


# Allotment of room captains
def allot_room_captains(room_data, room_captains, duty_limits):
    print("Allotting Room Captains....")
    room_data["Room Captain"] = None
    duties = {captain: [] for captain in room_captains["ID"]}
    branch_duty_count = {}

    for idx, row in room_data.iterrows():
        available_captains = room_captains[
            room_captains["end_date"].isna()
            | (room_captains["end_date"] != row["Date"])
        ]
        assigned_captains = []

        for _, captain_row in available_captains.iterrows():
            captain_id = captain_row["ID"]
            captain_name = captain_row["Name"]
            branch = captain_row["Branch"]
            mobile_number = captain_row["Mobile Number"]
            email_id = captain_row["Email"]
            max_duties = duty_limits.get(captain_id, 10)  # Default to 10 if not found

            # Initialize branch count for the date if not present
            if (row["Date"], branch) not in branch_duty_count:
                branch_duty_count[(row["Date"], branch)] = 0

            # Check branch constraint and max duties
            branch_total = len(room_captains[room_captains["Branch"] == branch])
            if (
                len(duties[captain_id]) < max_duties
                and room_data.loc[idx, "Room Captain"] is None
                and not any(
                    (duty_date == row["Date"] and duty_period == row["Period"])
                    for duty_date, duty_period in duties[captain_id]
                )
            ):

                assigned_captains.append(
                    f"{captain_id} - {captain_name} - {mobile_number} - {email_id}"
                )
                duties[captain_id].append((row["Date"], row["Period"]))
                branch_duty_count[(row["Date"], branch)] += 1

                if row["Room"] in ["F102", "F105"] and len(assigned_captains) < 2:
                    continue
                else:
                    break

        if len(assigned_captains) == 0:
            continue
        room_data.loc[
            (room_data["Date"] == row["Date"])
            & (room_data["Period"] == row["Period"])
            & (room_data["Room"] == row["Room"]),
            "Room Captain",
        ] = ", ".join(assigned_captains)

    # Convert date back to desired format for display
    room_data["Date"] = room_data["Date"].dt.strftime("%d-%m-%Y")
    return room_data


# Allotment of group captains
def allot_group_captains(room_data, group_captains, duty_limits):
    print("Allotting Group Captains....")
    room_data["Group Captain"] = None
    duties = {captain: [] for captain in group_captains["ID"]}
    allotted_duties = {}
    for floor in room_data["Floor"].unique():
        floor_rooms = room_data[room_data["Floor"] == floor]

        for idx, row in floor_rooms.iterrows():
            for _, captain_row in group_captains.iterrows():
                captain_id = captain_row["ID"]
                captain_name = captain_row["Name"]
                branch = captain_row["Branch"]
                mobile_number = captain_row["Mobile Number"]
                email_id = captain_row["Email"]
                max_duties = duty_limits.get(
                    captain_id, 10
                )  # Default to 10 if not found

                if (
                    len(duties[captain_id]) < max_duties
                    and not allotted_duties.get(
                        f"{row['Date']}|{row['Period']}|{row['Floor']}|{row['Block']}",
                        False,
                    )
                    and not any(
                        duty_date == row["Date"]
                        and (
                            duty_period != row["Period"]
                            or duty_floor != floor
                            or duty_block != row["Block"]
                        )
                        for duty_date, duty_period, duty_floor, duty_block in duties[
                            captain_id
                        ]
                    )
                ):

                    room_data.loc[
                        (room_data["Date"] == row["Date"])
                        & (room_data["Period"] == row["Period"])
                        & (room_data["Floor"] == row["Floor"])
                        & (room_data["Block"] == row["Block"]),
                        "Group Captain",
                    ] = f"{captain_id} - {captain_name} - {mobile_number} - {email_id}"
                    timeslots = len(
                        room_data.loc[
                            (room_data["Date"] == row["Date"])
                            & (room_data["Period"] == row["Period"])
                            & (room_data["Floor"] == row["Floor"])
                            & (room_data["Block"] == row["Block"]),
                            "Start Time",
                        ].unique()
                    )
                    allotted_duties[
                        f"{row['Date']}|{row['Period']}|{row['Floor']}|{row['Block']}"
                    ] = True
                    for i in range(timeslots):
                        duties[captain_id].append(
                            (row["Date"], row["Period"], floor, row["Block"])
                        )
                    break

    return room_data


def export_csv(room_data):
    # Save the final results
    output_file_path = "Staff Duties.csv"
    room_data.to_csv(output_file_path, index=False)

    print(f"Staff Duties exported to {output_file_path}")


def start_staff_duties_generation(staff_duties, staff_leave, max_duties):
    print("Starting...")
    room_data = get_room_data(staff_duties)
    staff_data = get_staff_data(staff_duties)
    leave_data = get_leave_data(staff_leave)
    duty_limits = get_duty_limits(max_duties)
    room_data = main_allot(room_data, staff_data, leave_data, duty_limits)
    export_csv(room_data)


if __name__ == "__main__":
    # staff_duties = r"C:\Users\Anirudh\Documents\staff duties.xlsx"

    staff_duties = r"C:\Users\Anirudh\Documents\ROOM STAFF.xlsx"
    staff_leave = r"C:\Users\Anirudh\Documents\LEAVES (2).xlsx"
    max_duties = r"C:\Users\Anirudh\Documents\MAX.xlsx"
    start_staff_duties_generation(staff_duties, staff_leave, max_duties)
