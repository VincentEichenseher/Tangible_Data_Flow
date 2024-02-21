#Based on the pyqtgraph Flowchart example that can be accessed with the command "pythom -m pyqtgraph.examples"
import pandas as pd
import pyqtgraph as pg
import json
import cv2
import signal

from pyqtgraph.flowchart.NodeLibrary import NodeLibrary
from pyqtgraph.flowchart import Flowchart
from pyqtgraph.Qt import QtWidgets
from pyqtgraph.Qt.QtCore import QTimer

from CustomNodes import SelectColumnNode, JoinDataNode, ThresholdDataNode, GroupByNode, MathOperationNode, MissingDataNode, LinePlotWidgetNode, HistogramWidgetNode
from sklearn import datasets

# important params:
# modify as needed
camera_id = 0 # opencv videocapture index parameter
camera_prefered_api = cv2.CAP_DSHOW # for Linux cv2.CAP_V4L2; Window CAP_DSHOW
offset_x = 0 # node offset in x direction
offset_y = 0 # node offset in y direction
update_interval = 250 # update interval in ms
marker_dict = cv2.aruco.DICT_4X4_250 # Arcuco dictionary

# temp storeage variables
json_data = None #json data cache 
elements_added = {} # dict to cache references to currently active elements (so these can be removed and to avoid duplication of elements on update)
json_changed = False # var keeping track of changes to the json so we can only change the flowchart when changes occur

# create Qt app
signal.signal(signal.SIGINT, signal.SIG_DFL) # SIGINT = Ctrl + C; this line lets us kill the Qt app and timer with te rest of this script
app = pg.mkQApp("Data Flow Visualization")

## Create main window and layout
win = QtWidgets.QMainWindow()
win.setWindowTitle('pyqtgraph: Data-Flow graph')
cw = QtWidgets.QWidget()
win.setCentralWidget(cw)
layout = QtWidgets.QGridLayout()
cw.setLayout(layout)

## Create flowchart object, set input/output Nodes (these are the input and output of the entire data-flow process)
fc = Flowchart(terminals={
    'dataIn': {'io': 'in'},
    'dataOut': {'io': 'out'}    
})
w = fc.widget()

## Add flowchart pannel
layout.addWidget(w.chartWidget.viewDock, 0, 0, 2, 1)

## init two plot widgets (areas for displaying plots) to main screen
pw1 = pg.PlotWidget()
pw2 = pg.PlotWidget()
layout.addWidget(pw1, 0, 1, 1, 1)
layout.addWidget(pw2, 1, 1, 1, 1)

layout.setColumnStretch(0, 27)
layout.setColumnStretch(1, 15)

win.showMaximized()

# load data
iris = datasets.load_iris()
iris_df=pd.DataFrame(iris.data)
iris_df['class']=iris.target

iris_df.columns=['sepal_len', 'sepal_wid', 'petal_len', 'petal_wid', 'class']
data = iris_df.to_dict()

## set Input Node data
fc.setInput(dataIn=data)
                        
# add custom Nodes

nodeLibrary = NodeLibrary()
nodeLibrary.addNodeType(SelectColumnNode, [('Filter',)])
nodeLibrary.addNodeType(JoinDataNode, [('Filter',)])
nodeLibrary.addNodeType(ThresholdDataNode, [('Filter',)])
nodeLibrary.addNodeType(GroupByNode, [('Filter',)])
nodeLibrary.addNodeType(MathOperationNode, [('Operations',)])
nodeLibrary.addNodeType(MissingDataNode, [('Operations',)])
nodeLibrary.addNodeType(LinePlotWidgetNode, [('Display',)])
nodeLibrary.addNodeType(HistogramWidgetNode, [('Display',)])
fc.setLibrary(nodeLibrary)

# set PlotWidget Nodes (Nodes for showing plots in the plotwidgets we created earlier)

pw1Node = fc.createNode('LinePlotWidget', pos=(300, -100))
pw1Node.setPlot(pw1)

pw2Node = fc.createNode('HistogramWidget', pos=(300, -50))
pw2Node.setPlot(pw2)

# get predefined marker dictionary for detecting aruco markers
aruco_dict = cv2.aruco.getPredefinedDictionary(marker_dict)

# load json for the first time
if json_data is None:
    with open("./node_data.json","r") as fh:
        json_data = json.load(fh)

# define functions
# create nodes based on aruco markers detected
def create_nodes_with_cv():
    global json_data
    detect_node_markers()
    with open("./node_data.json","r") as fh:
      json_data = json.load(fh)
    for element in json_data["nodes"]:
        id_as_string = str(element["aruco_id"])
        if element["is_active"] is True and id_as_string not in list(elements_added):
            nodename = element["node_type"]
            nodecoords = element["coord"]
            node = fc.createNode(nodename, pos=[nodecoords[0]+offset_x, nodecoords[1]+offset_y])
            elements_added.update({id_as_string:node})
        elif element["is_active"] is True and id_as_string in list(elements_added):
            # change crtl-widget values
            ui = elements_added[id_as_string].ctrls
            values = element["values"]
            for key in values.keys():
                ui[key].setValue(values[key])
        elif element["is_active"] is False and id_as_string in list(elements_added):
            fc.removeNode(elements_added[id_as_string])
            elements_added.pop(id_as_string)
    fc.outputChanged()

# Aruco marker detection
def detect_node_markers():
    camera = cv2.VideoCapture(camera_id, camera_prefered_api)
    #camera = cv2.VideoCapture("./Aruco_Test.mp4")
    
    while(camera.isOpened()):
        global json_changed
        ret, img = camera.read()
        if ret == True:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            corners, ids, rejected = cv2.aruco.detectMarkers(gray, aruco_dict)
            if ids is not None:
                for element in json_data["nodes"]:
                    if element["aruco_id"] in ids:
                        element["is_active"] = True
                        id_index = ids.flatten().tolist().index(element["aruco_id"])
                        element_corners = corners[id_index]
                        element["coord"] = [int(element_corners[0][0][0]),int(element_corners[0][0][1])]
                    else:
                        element["is_active"] = False
            else:
                for element in json_data["nodes"]:
                    element["is_active"] = False
                    
            with open("./node_data.json","w") as fh:
                fh.write(json.dumps(json_data))
                print(f"json updated; elements {ids} are currently active")
            break
        else:
            break

    camera.release()

# timer to perform additional process (computer vision and node creation) during main qt eventloop
timer = QTimer()
timer.timeout.connect(create_nodes_with_cv)
timer.start(update_interval)

# main
if __name__ == '__main__':
    pg.exec() # execute main qt event loop

