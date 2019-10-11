from appJar import gui

# create a GUI variable called app
app = gui("Examination Manager", "1024x768")
app.setFont(18)

app.startTabbedFrame("TabbedFrame")
app.startTab("Room Allotment")
app.addLabel("l1", "Room Allotment")
app.stopTab()

app.startTab("Seating Arrangement")
app.addLabel("l2", "Seating Arrangement")
app.stopTab()

app.startTab("Invigilation")
app.addLabel("l3", "Invigilation")
app.stopTab()
app.stopTabbedFrame()

app.go()