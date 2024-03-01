from datastructures.TuioDatastructures import *
from parsers.MessageTypes import MessageTypes
from datastructures.Trackables import *
from smath import smath
from interaction import Interaction
from util.Utility import InfiniteThread

import pyautogui
import json
import time


class MessageParser:
    def __init__(self):
        self.bundle = []
        self.x_offset = -235
        self.y_offset = -320
        self.alive_objects = {}
        self.interaction_manager = Interaction.Interaction()
        self.temp = []
        self.mouse_pressed = False

        self.message_time = int(round(time.time() * 1000))
        self.current_time = int(round(time.time() * 1000))

    def parse(self, *args):
        self.bundle.append(args)

        if args[0] == MessageTypes.ALIVE.value:
            self.__handle_message_bundle()

            self.bundle = []

    def __handle_message_bundle(self):
        self.__track_objects()
        self.get_tracked_objects()

    def __get_frame(self):
        try:
            return {
                'num': self.bundle[0][1], 't': self.bundle[0][2][0], 's_fraction': self.bundle[0][2][1], 'dim': self.bundle[0][3], 'src': self.bundle[0][4]
            }

        except IndexError:
            return None

    def __get_alive(self):
        return list(self.bundle[len(self.bundle) - 1][1:])

    def __track_objects(self):
        frame = self.__get_frame()
        alive = self.__get_alive()
        data = self.bundle[1:-1]
        sub_bundle = []

        for i in alive:
            for elem in data:
                try:
                    if elem[1] == i:
                        sub_bundle.append(elem)
                except:
                    pass

            if len(sub_bundle) > 0:
                self.alive_objects[i] = TUIOObject.create_tuio_object(i, sub_bundle, frame)

            sub_bundle = []

        self.__remove_dead_objects(alive)

    def __remove_dead_objects(self, alive):
        dead = []

        for key in self.alive_objects.keys():
            if key not in alive:
                dead.append(key)
                        
        for d in dead:
            dead_trackable = self.alive_objects.pop(d)
            try:
                trackable_type_id =  dead_trackable.get_token_component().type_id
                if trackable_type_id == TrackableTypes.TANGIBLE.value:
                    dead_trackable_type = dead_trackable.get_class_id()
                    json_data = {}
                    with open("./node_data.json","r") as fh:
                        json_data = json.load(fh)
                    json_data["nodes"][dead_trackable_type]["is_active"] = False
                    with open("./node_data.json","w") as fh:
                        fh.write(json.dumps(json_data))
                else:
                    pass
            except RuntimeError:
                pass

        if len(dead) == 0 and self.mouse_pressed == True:
            pyautogui.mouseUp()
            self.mouse_pressed = False

    def get_tracked_objects(self):
        return self.generate_trackables_json()

    def generate_trackables_json(self):
        try:
            for key in self.alive_objects.keys():
                o = self.alive_objects[key]

                if o.get_token_component():
                    trackable_type_id = o.get_token_component().type_id
                    trackable_type = o.get_class_id()
                    position = list(o.get_bounds_component().get_position())
                    angle = o.get_bounds_component().angle
                    width = o.get_bounds_component().width
                    height = o.get_bounds_component().height

                    roi = list(smath.Math.create_rectangle(position[0],position[1],width,height,angle))
                    
                    if trackable_type_id == TrackableTypes.TANGIBLE.value:    
                        print(f"Detected Tangible of type {trackable_type} at position {position}")
                        json_data = {}
                        with open("./node_data.json","r") as fh:
                            json_data = json.load(fh)
                        json_data["nodes"][trackable_type]["is_active"] = True
                        json_data["nodes"][trackable_type]["coord"] = [position[0]*0.5+self.x_offset,position[1]*0.5+self.y_offset]
                        with open("./node_data.json","w") as fh:
                            fh.write(json.dumps(json_data))
                        #self.tangible_positions.append(roi)
                    elif trackable_type_id == TrackableTypes.TOUCH.value:
                        #finger = True
                        #for item in self.tangible_positions:
                        #    bool_inside = smath.Math.aabb_in_aabb(roi,item)
                        #    if bool_inside == True:
                        #        finger = False
                        #if finger == True:
                        self.temp.append(position)
                        print(f"Detected TOUCH at {position}")

            if len(self.temp)>=3:
                start = self.temp[0]
                end = self.temp[-1]
                self.temp = [] 
                pyautogui.moveTo(start[0],start[1])
                if self.mouse_pressed == False:
                    pyautogui.mouseDown()
                    self.mouse_pressed = True

        except RuntimeError:
            pass
        
