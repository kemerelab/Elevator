import xml.etree.cElementTree as ET
from datetime import datetime
import time

# create tree root 
maze_events = ET.Element("MazeEvents")

# Level 1
level1 = ET.SubElement(maze_events, "Level", name="Level 1")

reward_well_visited_level1 = ET.SubElement(level1, "RewardWellVisited")

rw1_level1 = ET.SubElement(reward_well_visited_level1, "RW1")
rw1_event_trigger_level1 = ET.SubElement(rw1_level1, "EventTrigger")

rw2_level1 = ET.SubElement(reward_well_visited_level1, "RW2")
rw2_event_trigger_level1 = ET.SubElement(rw2_level1, "EventTrigger")

elevator1_detected = ET.SubElement(level1, "ElevatorDetected")
elevator1_event_trigger = ET.SubElement(elevator1_detected, "EventTrigger")

door1_opened = ET.SubElement(level1, "DoorOpened")
opendoor1_event_trigger = ET.SubElement(door1_opened, "EventTrigger")

door1_closed = ET.SubElement(level1, "DoorClosed")
closedoor1_event_trigger = ET.SubElement(door1_closed, "EventTrigger")

# Level 2
level2 = ET.SubElement(maze_events, "Level", name="Level 2")

reward_well_visited_level2 = ET.SubElement(level2, "RewardWellVisited")

rw2_level2 = ET.SubElement(reward_well_visited_level2, "RW2")
rw2_event_trigger_level2 = ET.SubElement(rw2_level2, "EventTrigger")

rw2_level2 = ET.SubElement(reward_well_visited_level2, "RW2")
rw2_event_trigger_level2 = ET.SubElement(rw2_level2, "EventTrigger")

elevator2_detected = ET.SubElement(level2, "ElevatorDetected")
elevator2_event_trigger = ET.SubElement(elevator2_detected, "EventTrigger")

door2_opened = ET.SubElement(level2, "DoorOpened")
opendoor2_event_trigger = ET.SubElement(door2_opened, "EventTrigger")

door2_closed = ET.SubElement(level2, "DoorClosed")
closedoor2_event_trigger = ET.SubElement(door2_closed, "EventTrigger")

#level 3
level3 = ET.SubElement(maze_events, "Level", name="Level 3")

reward_well_visited_level3 = ET.SubElement(level3, "RewardWellVisited")

rw3_level3 = ET.SubElement(reward_well_visited_level3, "RW3")
rw3_event_trigger_level3 = ET.SubElement(rw3_level3, "EventTrigger")

rw3_level3 = ET.SubElement(reward_well_visited_level3, "RW3")
rw3_event_trigger_level3 = ET.SubElement(rw3_level3, "EventTrigger")

elevator3_detected = ET.SubElement(level3, "ElevatorDetected")
elevator3_event_trigger = ET.SubElement(elevator3_detected, "EventTrigger")

door3_opened = ET.SubElement(level3, "DoorOpened")
opendoor3_event_trigger = ET.SubElement(door3_opened, "EventTrigger")

door3_closed = ET.SubElement(level3, "DoorClosed")
closedoor3_event_trigger = ET.SubElement(door3_closed, "EventTrigger")

# build tree and write to xml file
tree = ET.ElementTree(maze_events)

year = "01"
month = "01"
day = "01"

now = datetime.now()
year = str(now.year)[2:4]

if len(str(now.month)) == 1:
	month = month.replace("1", str(now.month), 1)
else: 
	month = month.replace(month, str(now.month), 1)

if len(str(now.day)) == 1:
	day = day.replace("1", str(now.day))
else: 
	day = day.replace(day, str(now.day), 1)

filename = "ElevatorData_" + year + month + day + ".xml"
tree.write(filename)