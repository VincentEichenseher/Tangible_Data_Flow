from datastructures.TuioDatastructures import *
from parsers.MessageTypes import MessageTypes
from datastructures.Trackables import *
from smath import smath
from interaction import Interaction
from util.Utility import InfiniteThread

import pyautogui
import Xlib.threaded
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
        #self.zombies = []
        self.mouse_pressed = False
        self.json = None
        with open("./node_data.json","r") as fh_in:
            self.json_data = json.load(fh_in)

        self.message_time = int(round(time.time() * 1000))
        self.current_time = int(round(time.time() * 1000))

    def parse(self, *args):
        self.bundle.append(args)

        if args[0] == MessageTypes.ALIVE.value:
            self.__handle_message_bundle()

            self.bundle = []

    def __handle_message_bundle(self):
        self.__track_objects()
        self.process_tracked_objects()

    def __get_frame(self):
        try:
            return {
                'num': self.bundle[0][1], 't': self.bundle[0][2][0], 's_fraction': self.bundle[0][2][1], 'dim': self.bundle[0][3], 'src': self.bundle[0][4]
            }

        except IndexError:
            return None

    def __get_alive(self):
        if len(self.bundle) != 0:
            return list(self.bundle[len(self.bundle) - 1][1:])
        else:
            return []

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

        if len(alive) > 0:
            self.__remove_dead_objects(alive)

    def __remove_dead_objects(self, alive):
        dead = []

        for key in self.alive_objects.keys():
            if key not in alive:
                #if key not in self.zombies:
                dead.append(key)

        for d in dead:
            #print(f"trying to pop dead object {d} from list {self.alive_objects.keys()}")
            if d in self.alive_objects.keys():
                #print(f"removing element {d}")
                dead_trackable = self.alive_objects.pop(d)
            else:
                #print(f"skipping element {d}")
                #self.zombies.append(d)
                continue
            try:
                trackable_type_id =  dead_trackable.get_token_component().type_id
                if trackable_type_id == TrackableTypes.TANGIBLE.value:
                    dead_trackable_type = dead_trackable.get_class_id()
                    self.json_data["nodes"][dead_trackable_type]["is_active"] = False
                else:
                    pass
            except RuntimeError:
                pass

        if len(dead) == 0 and self.mouse_pressed == True:
            pyautogui.mouseUp()
            self.mouse_pressed = False

    def get_tracked_objects(self):
        pass

    def process_tracked_objects(self):
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
                        # print(f"Detected Tangible of type {trackable_type} at position {position}") # this causes WAY too much lag
                        self.json_data["nodes"][trackable_type]["is_active"] = True
                        self.json_data["nodes"][trackable_type]["coord"] = [position[0]*0.5+self.x_offset,position[1]*0.5+self.y_offset]
                    elif trackable_type_id == TrackableTypes.TOUCH.value:
                        self.temp.append(position)
                        # print(f"Detected TOUCH at {position}") # this too

            with open("./node_data.json","w") as f_out:
                f_out.write(json.dumps(self.json_data))

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
        
