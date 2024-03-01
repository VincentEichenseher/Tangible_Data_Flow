"""
Based on Raphael Wimmer's implementation for the course ITT
See Computational Geometry for Gesture Recognition jupyter notebook
"""

from datastructures.Shape import Shape
from datastructures import Brush
from widgets import QMenuWidget
from style import style
from datastructures.Trackables import *
from datastructures.TrackableTypes import *
from datastructures import Mask
from interaction import Effect

from util.Utility import TaskProgressThread, AnimationThread, InfiniteThread
from interaction import Interaction
from evaluation import Evaluation
from random import randint

import time



CREATE_PALETTE_ON_INIT = True
CREATE_COMPOSITE_ON_INIT = False

CODE = """<html>
<pre>
<code>
# This is a small code snippet for getting started with Python!

def fizzbuzz(n):
    if n % 4 == 0: 
        print("Buzz")
    elif n % 3 == 0:
        print("Fizz") 

def main(): 
    for i in range(1, 101):
        fizzbuzz(i)
            
main()
</code>
</pre>
        </html>"""

CODE_2 = """<html>
<pre>
<code>
# This is a small code snippet for getting started with Python!

def fizzbuzz(n):
    if n % 15 == 0:
        print("FizzBuzz")
    elif n % 5 == 0: 
        print("Buzz")
    elif n % 3 == 0:
        print("Fizz") 

def main(): 
    for i in range(1, 101):
        fizzbuzz(i)
            
main()
</code>
</pre>
        </html>"""

MAIL_1 = """<html><h1>Re: Work</h1> <br/>
                <b>From: </b> Max &lt;max@mustermann.de&gt; <br/>
                <b>To: </b> Me <br/>
                <p>Hi, could we meet later today to discuss the new project?</p>
</html>"""

MAIL_2 = """<html><h1>Re: Lunch</h1> <br/>
                <b>From: </b> Tina &lt;tina@anita.de&gt;<br/>
                <b>To: </b> Me <br/>
                <p>Hi, let's have lunch some time? :) </p>
</html>"""

PURCHASE_REQUEST_1 = """
<html>
<div style='margin:0px; padding: 0px;width=100%;'>

<table width='100%'>
<tbody>

<tr>
<td>
    <h2>Purchase Request</h2>
    <h3>Hardware Procurement</h3>
    <h3>Request ID: ?</h3>
    <h3>Requester: John Doe</h3>
</td>

<td>
<b>HARDWIRE Electrical</b>
<p>123 Hardwire Drive</p>
<p>Anytown, AT 12345</p>
<p>
<i>+1-202-867-5301</i>
</p>
<p>
<i>info@hardwire-electrical.com</i>
</p>
<p>Request Date: 23.10.2019</p>
</td>
</tr>
</tbody>
</table>

<hr>

<table width='100%'>
<tbody>

<tr>
    <td><b>No</b></td>
    <td><b>ID</b></td>
    <td><b>Descr</b></td>
    <td><b>Qty</b></td>
    <td><b>Price/unit</b></td>
    <td><b>Price total</b></td>
</tr>
<tr>
    <td>1</td>
    <td>481523</td>
    <td>FullHD Beamer</td>
    <td>1</td>
    <td>499.90$</td>
    <td>499.90$</td>
</tr>
<tr>
    <td>2</td>
    <td>492213</td>
    <td>4K Monitor</td>
    <td>4</td>
    <td>283.90$</td>
    <td>851.70$</td>
</tr>
<tr>
    <td>3</td>
    <td>493141</td>
    <td>Optical Mouse</td>
    <td>10</td>
    <td>19.90$</td>
    <td>199.00$</td>
</tr>
<tr>
    <td>4</td>
    <td>493244</td>
    <td>USB Keyboard</td>
    <td>?</td>
    <td>9.90$</td>
    <td>?</td>
</tr>
<tr>
    <td>5</td>
    <td>493474</td>
    <td>Coffee Mug "Happy Monday"</td>
    <td>1</td>
    <td>5.40$</td>
    <td>5.40$</td>
</tr>
<tr>
    <td>6</td>
    <td>493779</td>
    <td>Cat 5.e Cable</td>
    <td>?</td>
    <td>2.30$</td>
    <td>?</td>
</tr>
</tbody>
</table>
</div>
</html>
"""

PURCHASE_REQUEST_2 = """
<html>
<div style='margin:0px; padding: 0px;width=100%;'>

<table width='100%'>
<tbody>

<tr>
<td>
    <h2>Purchase Request</h2>
    <h3>Hardware Procurement</h3>
    <h3>Request ID: 491230</h3>
    <h3>Requester: John Doe</h3>
</td>

<td>
<b>HARDWIRE Electrical</b>
<p>542 N. Marlborough Ave.</p>
<p>Kernersville, NC 27284</p>
<p>
<i>+1-202-867-5301</i>
</p>
<p>
<i>info@hardwire-electrical.com</i>
</p>
<p>Request Date: 23.10.2019</p>
</td>
</tr>
</tbody>
</table>

<hr>

<table width='100%'>
<tbody>

<tr>
    <td><b>No</b></td>
    <td><b>ID</b></td>
    <td><b>Descr</b></td>
    <td><b>Qty</b></td>
    <td><b>Price/unit</b></td>
    <td><b>Price total</b></td>
</tr>
<tr>
    <td>1</td>
    <td>481523</td>
    <td>FullHD Beamer</td>
    <td>1</td>
    <td>499.90$</td>
    <td>499.90$</td>
</tr>
<tr>
    <td>2</td>
    <td>492213</td>
    <td>4K Monitor</td>
    <td>4</td>
    <td>283.90$</td>
    <td>851.70$</td>
</tr>
<tr>
    <td>3</td>
    <td>493141</td>
    <td>Optical Mouse</td>
    <td>10</td>
    <td>19.90$</td>
    <td>199.00$</td>
</tr>
<tr>
    <td>4</td>
    <td>493244</td>
    <td>USB Keyboard</td>
    <td>10</td>
    <td>9.90$</td>
    <td>99.00$</td>
</tr>
<tr>
    <td>5</td>
    <td>493474</td>
    <td>Coffee Mug "Happy Monday"</td>
    <td>1</td>
    <td>5.40$</td>
    <td>5.40$</td>
</tr>
<tr>
    <td>6</td>
    <td>493779</td>
    <td>Cat 5.e Cable</td>
    <td>10</td>
    <td>2.30$</td>
    <td>23.00$</td>
</tr>
</tbody>
</table>
</div>
</html>
"""

MAIL_URGENT = """<html><h1>URGENT: Flight Delayed until tomorrow</h1> <br/>
                       <b>From: </b> Airline &lt;airline@major_airline.com&gt;<br/>
                       <b>To: </b> Me <br/>
                       <p>Dear Guest, <br/>unfortunately we had to delay your flight home until tomorrow. Sorry for the inconvenience. <br/><br/>Best,<br/> Airline</p>
                 </html>
"""

NOTES = """<html><h2>Phone Call, Tom, 4.6. 12:30</h2>
                 <ul>
                    <li>application granted</li>
                    <li>porject start on July 1st</li>
                 </ul>
                 <p>&#8658; send scan of app. docs to him!</p>
</html>"""

IMAGES_ON_PHONE = [
    "res/img/photos/architecture-buildings-business-1134166-13481529604398hqweqdom7s.jpg",
    "res/img/photos/bridge-city-czech-republic-229958-11251527786959atcm2lustc.jpg",
    "res/img/photos/cheese-cherry-tomatos-food-14251532670903czgorcitug.jpg",
    "res/img/photos/PHOTO-2018-03-28-19-38-27.jpg",
    "res/img/photos/PHOTO-2018-04-03-16-11-31.jpg",
    "res/img/photos/PHOTO-2018-09-02-19-29-42.jpg",
    "res/img/photos/sushi-asia-eat-fish-japanese-14051531977866shq8qvjmev.jpg",
    "res/img/photos/vienna-2989756-95415257937514n274synns.jpg",
    "res/img/photos/pizza-2000614-14871534318958fcshonvgmm.jpg",
]


class QDrawWidget(QtWidgets.QWidget):
    on_close = QtCore.pyqtSignal()
    on_context_menu_open = QtCore.pyqtSignal(float, float, float, float, int, list)
    on_context_menu_selection = QtCore.pyqtSignal(float, float)
    on_context_menu_close = QtCore.pyqtSignal(float)
    on_new_file_append_requested = QtCore.pyqtSignal(float, float, str, int)
    on_delete_digital_twin = QtCore.pyqtSignal(int)
    on_delete_solo_file = QtCore.pyqtSignal(tuple)
    on_conveyor_move_requested = QtCore.pyqtSignal(float, float, int, list, float, bool, bool, int)
    # effect requests
    on_pd_magnification_requested = QtCore.pyqtSignal(int, float)
    on_file_magnification_requested = QtCore.pyqtSignal(int, float)
    on_halt_file_for_review = QtCore.pyqtSignal(int)
    on_file_halted_for_review = QtCore.pyqtSignal(int)

    on_touch_tap = QtCore.pyqtSignal(int, int)

    on_shape_deletion = QtCore.pyqtSignal(list)
    on_file_click = QtCore.pyqtSignal(int, int)
    on_thread_visualization_requested = QtCore.pyqtSignal(list, int)
    on_region_move_change_requested = QtCore.pyqtSignal(int, bool, bool)
    on_region_movement_requested = QtCore.pyqtSignal(int, int)
    on_region_collision_deletion = QtCore.pyqtSignal(int)
    on_button_clicked = QtCore.pyqtSignal(int)
    on_evaluation = QtCore.pyqtSignal(dict)
    on_palette_selection = QtCore.pyqtSignal(int)
    on_region_effect_storage_requested = QtCore.pyqtSignal(int, int)
    on_region_effect_transfer_requested = QtCore.pyqtSignal(int, int)
    on_file_effect_transfer_requested = QtCore.pyqtSignal(int, int)

    # only needed for logging as of now
    on_magnification_toggled = QtCore.pyqtSignal(bool, int)
    on_email_delegate_storage_doAtOnce_left = QtCore.pyqtSignal(int)
    on_do_at_once_requested = QtCore.pyqtSignal(list, int, str)
    on_file_drag = QtCore.pyqtSignal(int)

    def __init__(self, app, mp, width=1920, height=1080):
        super().__init__()

        self.image_spawn_index = 0

        self.dict_file_ids_to_thread_num = dict()

        self.DEBUG = False
        self.EVAL_SPECIFICATION_ID = Evaluation.Experiment.ExperimentType.COLLABORATION.value

        self.app = app
        self.mp = mp

        self.notification_widget = QtWidgets.QLabel()
        self.notification_widget.setWordWrap(True)
        self.notification_widget.setGeometry(self.x() + 20, 1020, int(self.width() / 2), 20)
        self.notification_widget.setText("Current Brush: Region Palette")
        self.notification_widget.fontMetrics().width(self.notification_widget.text())
        self.notification_widget.setMinimumWidth(1920 / 2)

        self.notification_widget.setStyleSheet(style.WidgetStyle.QLABEL_STYLE.value)
        self.notification_widget.setParent(self)

        font = self.notification_widget.font()
        font.setPointSize(14)

        self.notification_widget.setFont(font)
        self.notification_widget.show()

        """
        self.notification_widget2 = QtWidgets.QLabel()
        self.notification_widget2.setGeometry(self.x() + 20, 1050, int(self.width() / 2), 20)
        self.notification_widget2.setText("Current Transfer Effect: None")
        self.notification_widget2.setStyleSheet(style.WidgetStyle.QLABEL_STYLE.value)
        self.notification_widget2.setParent(self)
        self.notification_widget2.setMinimumWidth(1920 / 2)

        font = self.notification_widget2.font()
        font.setPointSize(14)

        self.notification_widget2.setFont(font)
        self.notification_widget2.show()
        """

        self.resize(width, height)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.drawing = False
        self.is_released = False
        self.grid = False
        self.is_logging = False
        self.has_transfer_effect_stored = False
        self.transfer_effect = None
        self.messaged_data = {}
        self.processed_trackables = []
        self.previous_processed_trackables = []
        self.drawn_shapes = []
        self.current_drawn_points = []
        self.setMouseTracking(True)  # do not only get events when button is pressed
        self.current_brush = Brush.Brush(Brush.BrushTypes.NONE.value, None)

        self.phys_tag = False

        self.current_brush.set_brush_type(Brush.BrushTypes.PALETTE.value)
        # TODO: disable
        self.setCursor(QtCore.Qt.BlankCursor)

        self.shapes_to_assign = []

        # settings = Evaluation.Experiment.get_experiment_specification(self.EVAL_SPECIFICATION_ID)

        settings = None

        if settings is not None:
            self.evaluation_categories = []
            self.pid = -1
            self.apply_evaluation_settings(settings)
            self.eval_csv_path = 'res/eval/review/out/'
            self.last_timestamp = None

            if self.EVAL_SPECIFICATION_ID == Evaluation.Experiment.ExperimentType.COLLABORATION.value:
                self.log_for_experiment('pid', 'timestamp', 'action', 'time_since_last_action', 'file_id', 'categorization_correct', 'categorization_correction')

        else:
            self.file_icons = {
                1: File(1, 50, 50, self, "main.py", CODE, FileType.TEXT.value, self.DEBUG),
                2: File(2, 50, 200, self, "accounting.mail", MAIL_1, FileType.MAIL.value, self.DEBUG),
                3: File(3, 50, 350, self, "karl.mail", MAIL_2, FileType.MAIL.value, self.DEBUG),
                4: File(4, 50, 500, self, "airline.mail", MAIL_URGENT, FileType.MAIL.value, self.DEBUG),
                5: File(5, 50, 800, self, "charly_cat.jpg", """res/img/kare.JPG""", FileType.IMAGE.value, self.DEBUG),
                6: File(6, 200, 50, self, "draft.docx", NOTES, FileType.TEXT.value, self.DEBUG),
                7: File(7, 200, 200, self, "purchase_152342.docx", PURCHASE_REQUEST_1, FileType.TEXT.value, self.DEBUG),
                8: File(8, 200, 350, self, "purchase_152413.docx", PURCHASE_REQUEST_1, FileType.TEXT.value, self.DEBUG),
                9: File(9, 200, 500, self, "purchase_152417.docx", PURCHASE_REQUEST_1, FileType.TEXT.value, self.DEBUG)
            }

        self.file_icon_count = len(self.file_icons)

        self.active_menus = []

        self.concurrent_touches = []
        self.concurrent_hands = []

        self.previous_concurrent_touches_1 = []
        self.previous_concurrent_touches_2 = []
        self.previous_concurrent_touches_3 = []
        self.previous_concurrent_touches_4 = []
        self.previous_concurrent_touches_5 = []
        self.previous_concurrent_touches_6 = []
        self.previous_concurrent_touches_7 = []
        self.previous_concurrent_touches_8 = []

        self.previous_concurrent_hands = []

        self.on_touch_tap.connect(self.perform_tap_click)

        self.on_context_menu_open.connect(self.show_context_menu)
        self.on_context_menu_selection.connect(self.perform_context_menu_selection)
        self.on_context_menu_close.connect(self.hide_context_menu)
        self.on_new_file_append_requested.connect(self.append_new_file_icon)
        self.on_delete_digital_twin.connect(self.delete_digital_twin_by_physical_id)
        self.on_conveyor_move_requested.connect(self.move_item_on_conveyor_belt)
        self.on_delete_solo_file.connect(self.delete_file)
        self.on_pd_magnification_requested.connect(self.magnify_physical_document)
        self.on_file_magnification_requested.connect(self.magnify_file)

        self.on_halt_file_for_review.connect(self.halt_item_on_request)
        self.on_file_halted_for_review.connect(self.halting_item)
        self.on_shape_deletion.connect(self.delete_regions)
        self.on_file_click.connect(self.click_file)
        self.on_thread_visualization_requested.connect(self.sending_visualization)
        self.on_region_move_change_requested.connect(self.set_region_moveable)
        self.on_region_movement_requested.connect(self.move_region)
        self.on_region_collision_deletion.connect(self.delete_region_by_collision)
        self.on_button_clicked.connect(self.on_button_click)
        self.on_magnification_toggled.connect(self.magnification_toggled)
        self.on_email_delegate_storage_doAtOnce_left.connect(self.pb_regions_left)
        self.on_file_drag.connect(self.file_drag_started)
        self.on_palette_selection.connect(self.on_palette_effect_selected)
        self.on_do_at_once_requested.connect(self.on_do_at_once)
        self.on_region_effect_storage_requested.connect(self.store_region_effect)
        self.on_region_effect_transfer_requested.connect(self.transfer_region_effect)
        self.on_file_effect_transfer_requested.connect(self.transfer_file_effect)

        self.interaction_manager = Interaction.Interaction()

        self.update_thread = InfiniteThread(33.0)
        self.update_thread.update_trigger.connect(self.update_all)
        self.update_thread.start()

        self.threads = {}
        self.num_threads = 0

        self.is_context_menu_open = False

        self.masks = []

        self.initUI()

        self.current_brush.set_effect(Effect.Palette())
        self.previous_palette_selection_index = -1
        self.currently_dragged_file = None

        self.test_p = []

        self.is_tangible_active = False
        self.tangible = None
        self.initial_tangible_collision = False
        self.tangible_effect = None

        if CREATE_PALETTE_ON_INIT:
            self.__create_palette_on_init__()
        if CREATE_COMPOSITE_ON_INIT:
            self.__create_composition_on_init__()

    def __create_palette_on_init__(self):
        palette_size = 250
        padding = 250
        image_dimensions = (1920, 1080)
        palette_shape = Shape(effect=Effect.Palette())
        palette_shape.set_roi([
            (image_dimensions[0] - palette_size - padding, image_dimensions[1] - palette_size - padding),
            (image_dimensions[0] - palette_size - padding, image_dimensions[1] - padding),
            (image_dimensions[0] - padding, image_dimensions[1] - palette_size - padding),
            (image_dimensions[0] - padding, image_dimensions[1] - padding)])
        self.drawn_shapes.append(palette_shape)
        palette_shape.parent = self
        palette_shape.is_palette_parent = False
        self.masks.append(Mask.Mask(palette_shape.roi, len(self.drawn_shapes) - 1))

        # Calculate Radius
        radius = int(sum(smath.Math.vector_norm((p[0] -
                                                 self.drawn_shapes[-1].center[
                                                     0], p[1] -
                                                 self.drawn_shapes[-1].center[
                                                     1])) for p in
                         self.drawn_shapes[-1].roi) / len(
            self.drawn_shapes[-1].roi))

        # Create circle ROI for last shape
        new_roi = smath.Math.compute_circle(self.drawn_shapes[-1].center[0],
                                            self.drawn_shapes[-1].center[1],
                                            radius)

        # Set shape to palette parent
        self.drawn_shapes[-1].is_palette_parent = True

        # Add circle ROI to shape
        # 90 controls spacing of sub area ROIs
        self.drawn_shapes[-1].set_roi(smath.Math.resample_points(new_roi, 100))

        # Set index to the parent
        parent_shape_index = len(self.drawn_shapes) - 1
        parent_shape_index = len(self.drawn_shapes) - 1

        # Create Sub-Area Rois
        # ! At this point, new menu items are spawned !
        for i, roi in enumerate(
                self.drawn_shapes[parent_shape_index].sub_area_rois):
            self.drawn_shapes.append(Shape())
            self.drawn_shapes[-1].set_effect(self.current_brush.get_effect())
            # at this point, we set the effect used in palette
            self.drawn_shapes[-1].set_palette_effect(i+1)
            self.drawn_shapes[-1].set_roi(roi)
            self.drawn_shapes[-1].parent = self
            self.drawn_shapes[-1].is_palette_parent = False
            self.drawn_shapes[-1].palette_parent = parent_shape_index
            self.drawn_shapes[-1].set_image()
            self.drawn_shapes[
                parent_shape_index].palette_children_indices.append(
                len(self.drawn_shapes) - 1)

            self.masks.append(Mask.Mask(self.drawn_shapes[-1].roi,
                                        len(self.drawn_shapes) - 1))

    # TODO: method stub
    def __create_composition_on_init__(self):
        pos_x = 700
        pos_y = 200
        width = 400
        height = 700
        num_effects = 3

        single_height = height  / num_effects

        effects = [
            Effect.Magnification([15]),
            Effect.Tag("Done"),
            Effect.SendMail("Karl")
        ]
        composite_padding = 0

        # Add base ROI
        base_shape = Shape()
        base_shape.set_effect(Effect.CompositeBase())
        base_shape.set_roi([
            (pos_x - composite_padding, pos_y - composite_padding),
            (pos_x - composite_padding, pos_y + height + composite_padding),
            (pos_x + width + composite_padding, pos_y + height - composite_padding),
            (pos_x + width + composite_padding, pos_y - composite_padding)
        ])
        base_shape.parent = self
        base_shape.set_image()
        self.drawn_shapes.append(base_shape)
        self.masks.append(
            Mask.Mask(base_shape.roi, len(self.drawn_shapes) - 1))

        # Add conveyor belt
        path = []
        for i in range(0, 100):
            point = (
                pos_x + width/2,
                pos_y + i*(height)/100 + 10)
            quantity = 1
            points_per_roi = 100/num_effects
            # TODO: this may be obsolete
            #if (int)(i % points_per_roi  ) is (int) (points_per_roi/2):
            #    quantity = 25
            for i in range(0, quantity):
                path.append(point)
        conveyor_belt = Shape()
        conveyor_belt.set_effect(Effect.ConveyorBelt([], False, True, 4))
        conveyor_belt.set_middle_line(path)
        shape, shape_part_one, shape_part_two = smath.Math.shapify(
            conveyor_belt.middle_line)
        conveyor_belt.shape_part_one = shape_part_one
        conveyor_belt.shape_part_two = shape_part_two
        conveyor_belt.set_roi(shape)
        conveyor_belt.effect.looped = False
        conveyor_belt.is_looped = False
        conveyor_belt.parent = self
        conveyor_belt.set_image()
        self.drawn_shapes.append(conveyor_belt)
        self.masks.append(
            Mask.Mask(conveyor_belt.roi, len(self.drawn_shapes) - 1))

        base_shape.effect.my_conveyor_belt = conveyor_belt

        # Add regions of composite
        #"""
        for i in range(0, num_effects):
            shape = Shape(effect=effects[i])
            shape.set_roi([
                (pos_x, pos_y + single_height * (1 + i)),
                (pos_x, pos_y  + single_height * i),
                (pos_x + width, pos_y  + single_height * i),
                (pos_x + width, pos_y + single_height * (1 + i))
            ])
            self.drawn_shapes.append(shape)
            shape.parent = self
            shape.set_image()
            self.masks.append(
                Mask.Mask(shape.roi, len(self.drawn_shapes) - 1))
        #"""

        pass

    #
    #
    #

    # <3 heartbeat of everything <3
    def update_all(self):
        self.previous_processed_trackables = self.processed_trackables
        self.processed_trackables = self.mp.get_tracked_objects()

        for icon in self.file_icons.keys():
            self.processed_trackables.append(self.file_icons[icon])

        self.track_touches(self.processed_trackables)
        self.track_tangible()

        self.interaction_manager.process(self)
        self.update()
        self.app.processEvents()

        if self.currently_dragged_file is not None:
            k = -1

            for i, w in enumerate(self.findChildren(QtWidgets.QLabel, "file")):
                if self.currently_dragged_file.widget == w:
                    k = i

            if k > -1:
                for n in range(len(self.findChildren(QtWidgets.QLabel, "file")) - k):
                    self.currently_dragged_file.widget.raise_()
                    self.currently_dragged_file.widget.name_widget.raise_()

    #
    #
    #

    def track_tangible(self):
        tangible_index = -1

        for i, t in enumerate(self.processed_trackables):
            if t.type_id == TrackableTypes.TANGIBLE.value:
                tangible_index = i

                break

        if tangible_index > -1:
            if self.processed_trackables[tangible_index].id not in [t.id for t in self.previous_processed_trackables]: # potential problem with PhysDoc
                self.is_tangible_active = True
                self.tangible = self.processed_trackables[i]
            else:
                self.tangible = self.processed_trackables[i]
                self.tangible.set_effect(self.tangible_effect)
        else:
            self.is_tangible_active = False
            self.tangible = None
            self.tangible_effect = None

    def on_do_at_once(self, roi, target_id, tagging):
        if self.is_logging:
            if self.EVAL_SPECIFICATION_ID == Evaluation.Experiment.ExperimentType.COLLABORATION.value:
                timestamp = int(time.time() * 1000)

                if self.last_timestamp is None:
                    duration = 'NA'
                else:
                    duration = timestamp - self.last_timestamp

                self.last_timestamp = timestamp

                action = "Entered Tag Region " + tagging

                self.log_for_experiment(self.pid, timestamp, action, duration, target_id, 'NA', 'NA')


    #
    #
    # FUNCTIONS FOR PALETTE MENU

    # Called, when an extension in the palette menu is opened
    def generate_palette_extension_shapes(self, shape_index, effect_type, data):
        m, temp = smath.Math.palette_circle_extension(self.drawn_shapes[shape_index].roi[1:-1], self.drawn_shapes[self.drawn_shapes[shape_index].palette_parent])

        n = 0

        for i, p in enumerate(self.drawn_shapes[self.drawn_shapes[shape_index].palette_parent].roi):
            if p == m:
                n = i

        k = 0

        temp1 = temp[n:] + temp[:n]
        temp2 = self.drawn_shapes[self.drawn_shapes[shape_index].palette_parent].roi[n:] + self.drawn_shapes[self.drawn_shapes[shape_index].palette_parent].roi[:n]

        upper = []
        lower = []

        upper.append(temp1[0])
        lower.append(temp2[0])

        # At this point we draw the palette extensions
        for i, s in enumerate(temp1[1:]):
            upper.append(s)
            lower.append(temp2[i])

            if i > 0 and i % 10 == 0:
                roi = [upper[0]] + lower + list(reversed(upper))

                self.drawn_shapes.append(Shape())

                self.drawn_shapes[-1].is_palette_extended = True
                self.drawn_shapes[-1].set_effect(Effect.Palette())

                if k < len(data):
                    self.drawn_shapes[-1].set_palette_effect(self.drawn_shapes[shape_index].palette_effect, effect_type, data[k])

                self.drawn_shapes[-1].set_roi(roi)
                self.drawn_shapes[-1].parent = self
                self.drawn_shapes[-1].is_palette_parent = False
                self.drawn_shapes[-1].palette_parent = self.drawn_shapes[shape_index].palette_parent
                self.drawn_shapes[-1].set_image()

                self.masks.append(Mask.Mask(self.drawn_shapes[-1].roi, len(self.drawn_shapes) - 1))

                upper = [s]
                lower = [temp2[i]]

                k += 1

    # Called, when a second level palette item is clicked
    def on_palette_extension_selected(self, shape_index):
        data = self.drawn_shapes[shape_index].palette_additional_info

        action = ''

        if self.drawn_shapes[shape_index].palette_effect == Effect.EffectType.MAGNIFICATION.value:
            self.current_brush.set_effect(Effect.Magnification([data], False))
            self.current_brush.set_brush_type(Brush.BrushTypes.MAGNIFY.value)
            self.brush_name = "Magnify by {}%".format(str(data) + '%')

            self.notification_widget.setText("Current Brush: Magnification by {0}".format(str(data) + "%"))
            self.notification_widget.fontMetrics().width(self.notification_widget.text())

            if self.is_logging:
                action = "Selected Magnify with factor " + str(data) + '%'

        elif self.drawn_shapes[shape_index].palette_effect == Effect.EffectType.SEND_EMAIL.value:
            self.current_brush.set_effect(Effect.SendMail(data))
            self.current_brush.set_brush_type(Brush.BrushTypes.SEND_MAIL.value)
            self.brush_name = "Send Email To {0}".format(data)

            self.notification_widget.setText("Current Brush: Send Email to {0}".format(data))
            self.notification_widget.fontMetrics().width(self.notification_widget.text())

            if self.is_logging:
                action = "Selected Send_Email with receiver" + str(data)

        elif self.drawn_shapes[shape_index].palette_effect == Effect.EffectType.DELEGATE.value:
            self.current_brush.set_effect(Effect.Delegate(data))
            self.current_brush.set_brush_type(Brush.BrushTypes.DELEGATE.value)
            self.brush_name = "Delegate To {0}".format(data)

            self.notification_widget.setText("Current Brush: Delegate to {0}".format(data))
            self.notification_widget.fontMetrics().width(self.notification_widget.text())

            if self.is_logging:
                action = "Selected Delegate with receiver " + str(data)

        elif self.drawn_shapes[shape_index].palette_effect == Effect.EffectType.TAG.value:
            self.current_brush.set_effect(Effect.Tag(data))
            self.current_brush.set_brush_type(Brush.BrushTypes.TAG.value)
            self.brush_name = "Tag with {0}".format(data)

            self.notification_widget.setText("Current Brush: Tag with {0}".format(data))
            self.notification_widget.fontMetrics().width(self.notification_widget.text())

            if self.is_logging:
                action = "Selected Tag with name: " + str(data)

        elif self.drawn_shapes[shape_index].palette_effect == Effect.EffectType.COLLABORATION.value:
            effect = Effect.RequestCollaboration(data)
            self.current_brush.set_effect(effect)
            self.current_brush.set_brush_type(Brush.BrushTypes.COLLABORATION.value)
            self.brush_name = "Request collaboration with {}".format(data)
            self.notification_widget.setText("Current Brush: {}".format(self.brush_name))
            self.notification_widget.fontMetrics().width(self.notification_widget.text())

        self.previous_palette_selection_index = self.drawn_shapes[shape_index].palette_parent

        self.previous_palette_selection_index = self.drawn_shapes[shape_index].palette_parent

        for i in range(len(self.drawn_shapes) - 1, -1, -1):
            if self.drawn_shapes[i].is_palette_extended:
                self.drawn_shapes[i].text.close()
                self.drawn_shapes.pop(i)
                self.masks.pop(i)

        if self.is_logging:
            if self.EVAL_SPECIFICATION_ID == Evaluation.Experiment.ExperimentType.COLLABORATION.value:
                timestamp = int(time.time() * 1000)

                if self.last_timestamp is None:
                    duration = 'NA'
                else:
                    duration = timestamp - self.last_timestamp

                self.last_timestamp = timestamp

                self.log_for_experiment(self.pid, timestamp, action, duration, 'NA', 'NA', 'NA')

    # Called, when an effect in the palette menu is selected
    def on_palette_effect_selected(self, shape_index):
        self.drawn_shapes[self.previous_palette_selection_index].palette_effect_selected = False
        self.drawn_shapes[shape_index].palette_effect_selected = True
        self.has_transfer_effect_stored = False
        self.transfer_effect = None

        if not self.drawn_shapes[shape_index].is_palette_extended:
            for i in range(len(self.drawn_shapes) - 1, -1, -1):
                if self.drawn_shapes[i].is_palette_extended:

                    if self.drawn_shapes[i].img is not None:
                        self.drawn_shapes[i].img.close()

                    if self.drawn_shapes[i].text is not None:
                        self.drawn_shapes[i].text.close()

                    self.drawn_shapes.pop(i)
                    self.masks.pop(i)

        if self.drawn_shapes[shape_index].palette_effect == Effect.EffectType.MAGNIFICATION.value:
            if not self.drawn_shapes[shape_index].is_palette_extended:
                magnifying_factors = [15, 25, 50, 75]

                self.generate_palette_extension_shapes(shape_index, Effect.EffectType.MAGNIFICATION.value, magnifying_factors)
            else:
                self.on_palette_extension_selected(shape_index)
                return

        # Review Submenu
        elif self.drawn_shapes[shape_index].palette_effect == Effect.EffectType.COLLABORATION.value:
            if not self.drawn_shapes[shape_index].is_palette_extended:
                users = ['Jill', 'Frank', 'Philipp', "Joseph", "Karl"]
                self.generate_palette_extension_shapes(shape_index, Effect.EffectType.COLLABORATION.value, users)
            else:
                self.on_palette_extension_selected(shape_index)
                return

        elif self.drawn_shapes[shape_index].palette_effect == Effect.EffectType.DELETION.value:
            self.current_brush.set_effect(Effect.Deletion())
            self.current_brush.set_brush_type(Brush.BrushTypes.DELETION.value)
            self.notification_widget.setText("Current Brush: Region Deletion")
            self.notification_widget.fontMetrics().width(self.notification_widget.text())

            if self.is_logging:
                if self.EVAL_SPECIFICATION_ID == Evaluation.Experiment.ExperimentType.COLLABORATION.value:
                    timestamp = int(time.time() * 1000)

                    if self.last_timestamp is None:
                        duration = 'NA'
                    else:
                        duration = timestamp - self.last_timestamp

                    self.last_timestamp = timestamp

                    action = "Selected Deletion Effect"

                    self.log_for_experiment(self.pid, timestamp, action, duration, 'NA', 'NA', 'NA')
        elif self.drawn_shapes[shape_index].palette_effect == Effect.EffectType.SEND_EMAIL.value:
            if not self.drawn_shapes[shape_index].is_palette_extended:
                receivers = ['Jill', 'Frank', 'Philipp', "Joseph", "Karl"]

                self.generate_palette_extension_shapes(shape_index, Effect.EffectType.SEND_EMAIL.value, receivers)
            else:
                self.on_palette_extension_selected(shape_index)
                return
        elif self.drawn_shapes[shape_index].palette_effect == Effect.EffectType.STORAGE.value:
            self.current_brush.set_effect(Effect.Storage())
            self.current_brush.set_brush_type(Brush.BrushTypes.STORAGE.value)
            self.brush_name = "Storage"
            self.notification_widget.setText("Current Brush: Region Storage")
            self.notification_widget.fontMetrics().width(self.notification_widget.text())

            if self.is_logging:
                if self.EVAL_SPECIFICATION_ID == Evaluation.Experiment.ExperimentType.COLLABORATION.value:
                    timestamp = int(time.time() * 1000)

                    if self.last_timestamp is None:
                        duration = 'NA'
                    else:
                        duration = timestamp - self.last_timestamp

                    self.last_timestamp = timestamp

                    action = "Selected Storage Effect"

                    self.log_for_experiment(self.pid, timestamp, action, duration, 'NA', 'NA', 'NA')
                    
        elif self.drawn_shapes[shape_index].palette_effect == Effect.EffectType.PORTAL.value:
            self.current_brush.set_effect(Effect.Portal())
            self.current_brush.set_brush_type(Brush.BrushTypes.PORTAL.value)
            self.brush_name = "Portal"
            self.notification_widget.setText("Current Brush: Portal Region")
            self.notification_widget.fontMetrics().width(self.notification_widget.text())

        elif self.drawn_shapes[shape_index].palette_effect == Effect.EffectType.CONVEYOR_BELT.value:
            self.current_brush.set_effect(Effect.ConveyorBelt())
            self.current_brush.set_brush_type(Brush.BrushTypes.CONVEYOR_BELT.value)
            self.brush_name = "Conveyor Belt"
            self.notification_widget.setText("Current Brush: Region Conveyor Belt")
            self.notification_widget.fontMetrics().width(self.notification_widget.text())

            if self.is_logging:
                if self.EVAL_SPECIFICATION_ID == Evaluation.Experiment.ExperimentType.COLLABORATION.value:
                    timestamp = int(time.time() * 1000)

                    if self.last_timestamp is None:
                        duration = 'NA'
                    else:
                        duration = timestamp - self.last_timestamp

                    self.last_timestamp = timestamp

                    action = "Selected Conveyor Belt Effect"

                    self.log_for_experiment(self.pid, timestamp, action, duration, 'NA', 'NA', 'NA')
        elif self.drawn_shapes[shape_index].palette_effect == Effect.EffectType.DELEGATE.value:
            if not self.drawn_shapes[shape_index].is_palette_extended:
                receivers = ['Jill', 'Frank', 'Philipp', "Joseph", "Karl"]

                self.generate_palette_extension_shapes(shape_index, Effect.EffectType.DELEGATE.value, receivers)
            else:
                self.on_palette_extension_selected(shape_index)

                return

        elif self.drawn_shapes[shape_index].palette_effect == Effect.EffectType.TAG.value:
            if not self.drawn_shapes[shape_index].is_palette_extended:
                tags = [
                    "To Do",
                    "Done",
                    "Holidays",
                    "Food",
                    "Pet"
                ]

                self.generate_palette_extension_shapes(shape_index, Effect.EffectType.TAG.value, tags)

            else:
                self.on_palette_extension_selected(shape_index)

                return 

            if self.is_logging:
                if self.EVAL_SPECIFICATION_ID == Evaluation.Experiment.ExperimentType.COLLABORATION.value:
                    timestamp = int(time.time() * 1000)

                    if self.last_timestamp is None:
                        duration = 'NA'
                    else:
                        duration = timestamp - self.last_timestamp

                    self.last_timestamp = timestamp

                    action = "Selected Tag Effect"

                    self.log_for_experiment(self.pid, timestamp, action, duration, 'NA', 'NA', 'NA')

        self.previous_palette_selection_index = shape_index

    #
    #
    #

    def store_region_effect(self, touch_id, shape_index):
        self.transfer_effect = self.drawn_shapes[shape_index].effect
        self.has_transfer_effect_stored = True

        # check which kind of effect and store name, values, etc.

        #if self.transfer_effect.effect_type ==

        #self.notification_widget2.setText("Current Transfer Effect: {0}".format()

    def transfer_region_effect(self, touch_id, shape_index):
        if self.drawn_shapes[shape_index].img is not None:
            self.drawn_shapes[shape_index].img.close()

        if self.drawn_shapes[shape_index].text is not None:
            self.drawn_shapes[shape_index].text.setText("")
            self.drawn_shapes[shape_index].text.close()

        self.drawn_shapes[shape_index].effect = self.transfer_effect
        self.drawn_shapes[shape_index].set_image()

    def transfer_file_effect(self, touch_id, file_id):
        if self.transfer_effect.effect_type == Effect.EffectType.DELETION.value:
            self.delete_file(self.file_icons[file_id].center)
        elif self.transfer_effect.effect_type == Effect.EffectType.MAGNIFICATION.value:
            if not self.file_icons[file_id].is_transfer_magnified:
                self.file_icons[file_id].is_transfer_magnified = True
                self.magnify_file(file_id, self.transfer_effect.factor)
            else:
                self.file_icons[file_id].is_transfer_magnified = False
        elif self.transfer_effect.effect_type == Effect.EffectType.TAG.value:
            pass

        # and so on for other effect types

    def magnification_toggled(self, toggle, file_id):
        if toggle:
            action = "Entered Seamless Preview"
        else:
            action = "Left Seamless Preview"

        if self.is_logging:
            if self.EVAL_SPECIFICATION_ID == Evaluation.Experiment.ExperimentType.COLLABORATION.value:
                timestamp = int(time.time() * 1000)

                if self.last_timestamp is None:
                    duration = 'NA'
                else:
                    duration = timestamp - self.last_timestamp

                self.last_timestamp = timestamp

                self.log_for_experiment(self.pid, timestamp, action, duration, file_id, 'NA', 'NA')

    def pb_regions_left(self, file_index):
        if len(self.file_icons) > 0:
            if self.is_logging:
                if self.EVAL_SPECIFICATION_ID == Evaluation.Experiment.ExperimentType.COLLABORATION.value:
                    action = ''

                    if self.file_icons[file_index].emailed:
                        action = 'Left Send-via-Email Region'
                    elif self.file_icons[file_index].stored:
                        action = 'Left Storage Region'
                    elif self.file_icons[file_index].delegated:
                        action = 'Left Delegate Region'
                    elif self.file_icons[file_index].done_at_once:
                        action = 'Left Tag Region'

                    if action != '':
                        timestamp = int(time.time() * 1000)

                        if self.last_timestamp is None:
                            duration = 'NA'
                        else:
                            duration = timestamp - self.last_timestamp

                        self.last_timestamp = timestamp

                        self.log_for_experiment(self.pid, timestamp, action, duration, file_index, 'NA', 'NA')

    def file_drag_started(self, _id):
        if self.is_logging and not self.file_icons[_id].grabbed:
            if self.EVAL_SPECIFICATION_ID == Evaluation.Experiment.ExperimentType.COLLABORATION.value:
                timestamp = int(time.time() * 1000)

                if self.last_timestamp is None:
                    duration = 'NA'
                else:
                    duration = timestamp - self.last_timestamp

                action = 'Dragging of File Started'

                self.last_timestamp = timestamp

                self.log_for_experiment(self.pid, timestamp, action, duration, str(_id), 'NA', 'NA')

    def on_button_click(self, _id):
        self.show_context_menu(self.button.x, self.button.y - 150, 50, 50, _id)

    def set_region_moveable(self, idx, toggle, is_attached):
        if toggle:
            for i in range(len(self.drawn_shapes) - 1, -1, -1):
                if self.drawn_shapes[i].is_palette_extended:
                    self.drawn_shapes[i].text.close()
                    self.drawn_shapes.pop(i)
                    self.masks.pop(i)

        self.drawn_shapes[idx].moveable = toggle
        self.drawn_shapes[idx].attached = is_attached

        if self.is_logging:
            if self.EVAL_SPECIFICATION_ID == Evaluation.Experiment.ExperimentType.COLLABORATION.value:
                timestamp = int(time.time() * 1000)

                if self.last_timestamp is None:
                    duration = 'NA'
                else:
                    duration = timestamp - self.last_timestamp

                action = 'Movement of ' + ('None' if self.drawn_shapes[idx].effect is None else self.drawn_shapes[idx].effect.name) + ' Region started'

                self.last_timestamp = timestamp

                self.log_for_experiment(self.pid, timestamp, action, duration, 'NA', 'NA', 'NA')

    def move_region(self, touch_id, shape_index):
        self.drawing = False
        self.current_drawn_points = []

        for t1 in self.concurrent_touches:
            for t2 in self.previous_concurrent_touches_1:
                if touch_id == t1.id == t2.id:
                    self.drawn_shapes[shape_index].touch_id = touch_id
                    self.drawn_shapes[shape_index].push(t1.center[0] - t2.center[0], t1.center[1] - t2.center[1])

                    if self.drawn_shapes[shape_index].attached:
                        self.masks[shape_index] = Mask.Mask(self.drawn_shapes[shape_index].roi, shape_index)

                    return

    def sending_visualization(self, roi, file_index):
        target_shape_index = -1

        for i in range(len(self.drawn_shapes)):
            if self.drawn_shapes[i].roi == roi:
                target_shape_index = i

        self.num_threads = self.num_threads + 1 if self.num_threads < 1000 else 1

        num = self.num_threads

        self.threads[num] = TaskProgressThread(target_shape_index, self.drawn_shapes[target_shape_index].list_view.item_rows[self.drawn_shapes[target_shape_index].list_view.model().rowCount() - 1], num)
        self.threads[num].update_trigger.connect(self.visualize_progressbar)
        self.threads[num].on_finished.connect(self.stop_visualize_progressbar)

        self.threads[num].start()

        if self.is_logging:
            if self.EVAL_SPECIFICATION_ID == Evaluation.Experiment.ExperimentType.COLLABORATION.value:
                timestamp = int(time.time() * 1000)

                if self.last_timestamp is None:
                    duration = 'NA'
                else:
                    duration = timestamp - self.last_timestamp

                self.last_timestamp = timestamp

                action = ''
                correct_category = False

                if self.drawn_shapes[target_shape_index].effect.effect_type == Effect.EffectType.STORAGE.value:
                    action = 'Entered Storage Region'
                elif self.drawn_shapes[target_shape_index].effect.effect_type == Effect.EffectType.DELEGATE.value:
                    action = 'Entered Delegate Region for ' + self.drawn_shapes[target_shape_index].effect.receiver
                    correct_category = self.evaluation_categories[file_index] == 'delegate'
                elif self.drawn_shapes[target_shape_index].effect.effect_type == Effect.EffectType.SEND_EMAIL.value:
                    action = 'Entered Send-via-Email Region for ' + self.drawn_shapes[target_shape_index].effect.receiver
                    correct_category = self.evaluation_categories[file_index] == 'send'

                if action != '':
                    self.log_for_experiment(self.pid, timestamp, action, duration, file_index, correct_category, 'NA')

    def visualize_progressbar(self, progress, target_shape_index, target_shape_list_view_row_index):
        if not self.drawn_shapes[target_shape_index].moveable:
            self.drawn_shapes[target_shape_index].update_progress(progress, target_shape_list_view_row_index)

    def stop_visualize_progressbar(self, target_shape_index, target_shape_list_view_row_index, thread_num):
        if not self.drawn_shapes[target_shape_index].moveable:
            self.threads.pop(thread_num)
            self.drawn_shapes[target_shape_index].remove_completed_item(target_shape_list_view_row_index)

    def track_touches(self, trackables):
        temp = []

        for i in range(len(trackables)):
            if trackables[i].type_id == TrackableTypes.TOUCH.value:
                for k in range(len(self.concurrent_touches)):
                    if trackables[i].id == self.concurrent_touches[k].id:

                        self.concurrent_touches[k].successive_detection_increments += 1

                        trackables[i].successive_detection_increments = self.concurrent_touches[k].successive_detection_increments
                        break

                temp.append(trackables[i])

        for k, f in self.file_icons.items():
            if f.touch_id not in [i.id for i in self.concurrent_touches]:
                self.currently_dragged_file = None

                if self.is_logging and f.grabbed:
                    if self.EVAL_SPECIFICATION_ID == Evaluation.Experiment.ExperimentType.COLLABORATION.value:
                        timestamp = int(time.time() * 1000)

                        if self.last_timestamp is None:
                            duration = 'NA'
                        else:
                            duration = timestamp - self.last_timestamp

                        action = 'Dragging of File Stopped'

                        self.last_timestamp = timestamp

                        self.log_for_experiment(self.pid, timestamp, action, duration, str(f.id), 'NA', 'NA')

                f.grabbed = False
                f.conveyable = True

        self.previous_concurrent_touches_8 = self.previous_concurrent_touches_7
        self.previous_concurrent_touches_7 = self.previous_concurrent_touches_6
        self.previous_concurrent_touches_6 = self.previous_concurrent_touches_5
        self.previous_concurrent_touches_5 = self.previous_concurrent_touches_4
        self.previous_concurrent_touches_4 = self.previous_concurrent_touches_3
        self.previous_concurrent_touches_3 = self.previous_concurrent_touches_2
        self.previous_concurrent_touches_2 = self.previous_concurrent_touches_1
        self.previous_concurrent_touches_1 = self.concurrent_touches
        self.concurrent_touches = temp

        for pct in self.previous_concurrent_touches_1 \
                   + self.previous_concurrent_touches_2 \
                   + self.previous_concurrent_touches_3 \
                   + self.previous_concurrent_touches_4 \
                   + self.previous_concurrent_touches_5\
                   + self.previous_concurrent_touches_6 \
                   + self.previous_concurrent_touches_7 \
                   + self.previous_concurrent_touches_8:

            last_ct_id = -1

            for ct in self.concurrent_touches:
                if pct.id != ct.id and last_ct_id != pct.id:
                    v = (ct.position[0] - pct.position[0], ct.position[1] - pct.position[1])

                    distance = smath.Math.vector_norm(v)

                    if distance < 350:
                        ct.id = pct.id
                        last_ct_id = ct.id

                        break

        for pct in self.previous_concurrent_touches_1:
            if pct.id not in [i.id for i in self.concurrent_touches]:
                self.app.postEvent(self, QtGui.QMouseEvent(QtGui.QMouseEvent.MouseButtonRelease, QtCore.QPoint(pct.position[0], pct.position[1]), QtCore.Qt.LeftButton, QtCore.Qt.NoButton, QtCore.Qt.NoModifier))

        for ct in self.concurrent_touches:
            self.cursor().setPos(self.mapToGlobal(QtCore.QPoint(ct.position[0], ct.position[1])))

            for roi in [self.file_icons[f].roi for f in self.file_icons.keys()]:
                if smath.Math.aabb_in_aabb(Shape(ct.roi).aabb, Shape(roi).aabb):
                    return

            if ct.is_holding():
                self.app.postEvent(self, QtGui.QMouseEvent(QtGui.QMouseEvent.MouseMove, QtCore.QPoint(ct.position[0], ct.position[1]), QtCore.Qt.LeftButton, QtCore.Qt.NoButton, QtCore.Qt.NoModifier))
            elif ct.id not in [i.id for i in self.previous_concurrent_touches_1]:
                self.app.postEvent(self, QtGui.QMouseEvent(QtGui.QMouseEvent.MouseButtonPress, QtCore.QPoint(ct.position[0], ct.position[1]), QtCore.Qt.LeftButton, QtCore.Qt.NoButton, QtCore.Qt.NoModifier))

        for i, s in enumerate(self.drawn_shapes):
            if s.touch_id != -1:
                if s.touch_id not in [ct.id for ct in self.concurrent_touches]:
                    self.drawn_shapes[i].touch_id = -1
                    self.interaction_manager.is_carrying_entity = False
                    self.drawn_shapes[i].moveable = False
                    self.drawn_shapes[i].attached = False
                    self.drawn_shapes[i].dropped = True

                    self.masks[i] = Mask.Mask(self.drawn_shapes[i].roi, i)

                    if self.drawn_shapes[i].effect.effect_type == Effect.EffectType.PALETTE.value:
                        for k in self.drawn_shapes[i].palette_children_indices:
                            self.drawn_shapes[k].touch_id = -1
                            self.interaction_manager.is_carrying_entity = False
                            self.drawn_shapes[k].moveable = False
                            self.drawn_shapes[k].attached = False
                            self.drawn_shapes[k].dropped = True

                            self.masks[k] = Mask.Mask(self.drawn_shapes[k].roi, k)

                    if self.is_logging:
                        if self.EVAL_SPECIFICATION_ID == Evaluation.Experiment.ExperimentType.COLLABORATION.value:
                            timestamp = int(time.time() * 1000)

                            if self.last_timestamp is None:
                                duration = 'NA'
                            else:
                                duration = timestamp - self.last_timestamp

                            action = 'Movement of ' + ('None' if self.drawn_shapes[i].effect is None else self.drawn_shapes[i].effect.name) + ' Region stopped'

                            self.last_timestamp = timestamp

                            self.log_for_experiment(self.pid, timestamp, action, duration, 'NA', 'NA', 'NA')

    def track_hands(self, trackables, target_widget):
        temp = []

        for i in range(len(trackables)):
            if trackables[i].type_id == TrackableTypes.HAND.value:
                temp.append(trackables[i])

        self.previous_concurrent_hands = self.concurrent_hands
        self.concurrent_hands = temp

    def show_context_menu(self, x, y, width, height, _id, shapes=[]):
        self.drawing = False

        action = ''

        if not self.is_context_menu_open:
            k = -1

            if len(shapes) > 0:
                for i in range(len(self.drawn_shapes)):
                    k += 1

                    if shapes[0].roi == self.drawn_shapes[i].roi:
                        break

            self.is_context_menu_open = True

            if k > -1:
                if not self.drawn_shapes[k].is_active:
                    menu = QMenuWidget.QMenuWidget(x, y, width, height, _id, self, self.drawn_shapes[k])
                    menu.add_top_level_menu()

                    self.active_menus.append(menu)
                    self.active_menus[-1].show()

                    if self.is_logging:
                        if self.EVAL_SPECIFICATION_ID == Evaluation.Experiment.ExperimentType.COLLABORATION.value:
                            action = 'Context Menu Requested for Region Reassignment'
            else:
                menu = QMenuWidget.QMenuWidget(x, y, width, height, _id, self)
                menu.add_top_level_menu()

                self.active_menus.append(menu)
                self.active_menus[-1].show()

                if self.is_logging:
                    if self.EVAL_SPECIFICATION_ID == Evaluation.Experiment.ExperimentType.COLLABORATION.value:
                        action = 'Context Menu Requested for Brush Assignment'

        if self.is_logging:
            if self.EVAL_SPECIFICATION_ID == Evaluation.Experiment.ExperimentType.COLLABORATION.value and action is not '':

                pid = self.pid
                timestamp = int(time.time() * 1000)

                if self.last_timestamp is None:
                    duration = 'NA'
                else:
                    duration = timestamp - self.last_timestamp

                self.last_timestamp = timestamp

                self.log_for_experiment(self.pid, timestamp, action, duration, 'NA', 'NA', 'NA')

    def hide_context_menu(self, id_to_close):
        self.drawing = False

        caller_ids = [i.caller_id for i in self.active_menus]

        idx = -1

        for i in range(len(caller_ids)):
            caller_id = caller_ids[i]

            if id_to_close == caller_id:
                if self.active_menus[i].sub_menu is not None:
                    self.active_menus[i].sub_menu.close()

                self.active_menus[i].close()

                idx = i

        if idx != -1:
            self.is_context_menu_open = False
            self.active_menus.pop(idx)

    def perform_tap_click(self, x, y):
        widget = self.app.widgetAt(x,y)
        if type(widget) is QtWidgets.QPushButton:
            widget.click()

    def perform_context_menu_selection(self, x, y):
        self.drawing = False

        self.cursor().setPos(self.mapToGlobal(QtCore.QPoint(x, y)))

        if self.is_logging:
            if self.EVAL_SPECIFICATION_ID == Evaluation.Experiment.ExperimentType.COLLABORATION.value:
                performed_action = ''

        for menu in self.active_menus:
            action = menu.activeAction()

            if action is not None:
                action.trigger()

                if self.is_logging:
                    if self.EVAL_SPECIFICATION_ID == Evaluation.Experiment.ExperimentType.COLLABORATION.value:
                        performed_action = "Selected " + action.text()[1:]

                menu.close()

            sub_menu = menu.sub_menu

            if sub_menu is not None:
                sub_menu_action = sub_menu.activeAction()

                if sub_menu_action is not None:
                    if self.is_logging:
                        if self.EVAL_SPECIFICATION_ID == Evaluation.Experiment.ExperimentType.COLLABORATION.value:
                            performed_action += ("with " + sub_menu_action.text()[1:])

                    sub_menu_action.trigger()
                    sub_menu.close()

        if self.is_logging:
            if self.EVAL_SPECIFICATION_ID == Evaluation.Experiment.ExperimentType.COLLABORATION.value and performed_action != '':

                timestamp = int(time.time() * 1000)

                if self.last_timestamp is None:
                    duration = 'NA'
                else:
                    duration = timestamp - self.last_timestamp

                self.last_timestamp = timestamp

                self.log_for_experiment(self.pid, timestamp, performed_action, duration, 'NA', 'NA', 'NA')

    def delete_file(self, center):
        idx = -1

        for key in self.file_icons.keys():
            if center == self.file_icons[key].center:
                idx = key
                self.file_icons[key].clear()
                break

        if idx != -1:
            self.file_icons.pop(idx, None)

            if self.is_logging:
                if self.EVAL_SPECIFICATION_ID == Evaluation.Experiment.ExperimentType.COLLABORATION.value:
                    timestamp = int(time.time() * 1000)
                    action = 'Deletion of File'
                    if self.last_timestamp is None:
                        duration = 'NA'
                    else:
                        duration = timestamp - self.last_timestamp
                    self.last_timestamp = timestamp
                    file_id = idx
                    categorization = self.evaluation_categories[idx] == 'delete'
                    self.log_for_experiment(self.pid, timestamp, action, duration, str(file_id), str(categorization), 'NA')

    def append_new_file_icon(self, x, y, name, physical_representation_id):
        if physical_representation_id not in [self.file_icons[i].physical_representation_id for i in self.file_icons.keys()]:

            self.file_icon_count = self.file_icon_count + 1 if self.file_icon_count < 1000 else 1

            if physical_representation_id == 1:
                self.file_icons[self.file_icon_count] = File(self.file_icon_count, x, y, self, name, """""" + str(name) + "\n-------------------"
                                                                                                                          """The ACM Conference on Human Factors in Computing Systems (CHI) series of academic conferences is generally considered the most prestigious in the field of human–computer interaction and is one of the top ranked conferences in computer science.[1] It is hosted by ACM SIGCHI, the Special Interest Group on computer–human interaction. CHI has been held annually since 1982 and attracts thousands of...""", FileType.TEXT.value, True, physical_representation_id, self.DEBUG)
                self.file_icons[self.file_icon_count].widget.show()
                self.file_icons[self.file_icon_count].stored = True
                self.file_icons[self.file_icon_count].magnified = True
                self.file_icons[self.file_icon_count].emailed = True
                self.file_icons[self.file_icon_count].delegated = True
            elif physical_representation_id == 0:
                self.file_icons[self.file_icon_count] = File(self.file_icon_count, x, y, self, """notes.txt""", NOTES, FileType.TEXT.value, True, physical_representation_id, self.DEBUG)

                self.file_icons[self.file_icon_count].widget.show()
                self.file_icons[self.file_icon_count].stored = True
                self.file_icons[self.file_icon_count].magnified = True
                self.file_icons[self.file_icon_count].emailed = True
                self.file_icons[self.file_icon_count].delegated = True

    def delete_digital_twin_by_physical_id(self, _id):
        idx = -1

        for key in self.file_icons.keys():
            p = self.file_icons[key]

            if p.type_id == TrackableTypes.FILE.value:
                if p.physical_representation_id == _id:
                    idx = key
                    break

        if idx > -1:
            self.file_icons[idx].set_digital_twin(-1)
            self.file_icons[idx].clear()
            self.file_icons.pop(idx, None)


    # If an item is placed on the conveyor belt, start its animation
    def move_item_on_conveyor_belt(self, x1, y1, idx, full_path, animation_time, looped, is_composite, n_composite_regions):
        for key in self.file_icons.keys():
            if not self.file_icons[key].grabbed:
                if not self.file_icons[key].is_on_conveyor_belt:
                    if self.file_icons[key].center[0] == x1 and self.file_icons[key].center[1] == y1:
                        self.file_icons[key].is_on_conveyor_belt = True

                        if len(full_path[idx:]) > 1:
                            if not looped:
                                p, q = full_path[idx:][-1], full_path[idx:][-2]
                                v = smath.Math.normalize_vector((p[0] - q[0], p[1] - q[1]))
                            else:
                                p, q = full_path[idx:][0], full_path[idx:][-1]

                                v = smath.Math.normalize_vector((p[0] - q[0], p[1] - q[1]))

                            v[0] *= 50
                            v[1] *= 50

                            if self.file_icons[key].anim_id == -1:
                                intersect_points = self.contains_intersect(full_path)
                                if intersect_points is not None:
                                    self.build_loop_in_path(full_path, intersect_points[0], intersect_points[1], 4)
                                if is_composite is True:
                                    temp_path = []
                                    points_per_section = len(full_path)/n_composite_regions
                                    for i, item in enumerate(full_path):
                                        quantity = 1
                                        for i in range(0, quantity):
                                            temp_path.append([item[0], item[1] + i*0.25])
                                    full_path = temp_path

                                self.animate(key, idx, full_path, animation_time, v, looped, is_composite, n_composite_regions)

                                if self.is_logging:
                                    timestamp = int(time.time() * 1000)
                                    action = 'Entered Conveyor Belt'
                                    if self.last_timestamp is None:
                                        duration = 'NA'
                                    else:
                                        duration = timestamp - self.last_timestamp

                                    self.last_timestamp = timestamp

                                    self.log_for_experiment(self.pid, timestamp, action, duration, self.file_icons[key].id, 'NA', 'NA')

            # called if file is currently held
            else:
                if self.file_icons[key].anim_id != -1:
                    if self.file_icons[key].anim_id in self.threads.keys():
                        self.threads[self.file_icons[key].anim_id].on_stop()

                    self.file_icons[key].anim_id = -1

                    if self.is_logging:
                        if self.EVAL_SPECIFICATION_ID == Evaluation.Experiment.ExperimentType.COLLABORATION.value:
                            timestamp = int(time.time() * 1000)
                            action = 'Exited Conveyor Belt via User'
                            if self.last_timestamp is None:
                                duration = 'NA'
                            else:
                                duration = timestamp - self.last_timestamp

                            self.last_timestamp = timestamp

                            self.log_for_experiment(self.pid, timestamp, action, duration, key, 'NA', 'NA')

    def build_loop_in_path(self, path, region_start, region_stop, multiplier):
        section = path[region_start:region_stop]*multiplier
        n_path = path[region_start:region_start] = section
        return n_path

    #
    #
    # Animation

    # Animate an item along the path
    def animate(self, idx, path_index, full_path, animation_time, v, looped, is_composite=False, n_composite_steps=3):
        if is_composite:
            animation_time = 4000
        num_thread = self.num_threads = self.num_threads + 1 if self.num_threads < 1000 else 1
        self.file_icons[idx].anim_id = num_thread
        thread = AnimationThread(idx, num_thread, self.file_icons[idx].widget, path_index, full_path, animation_time, v, looped, is_composite, n_composite_steps)

        self.threads[num_thread] = thread
        self.threads[num_thread].animation_start.connect(self.on_animation_requested)
        self.threads[num_thread].update_trigger.connect(self.on_animation_update)
        self.threads[num_thread].on_finished.connect(self.on_animation_stop_requested)

        self.threads[num_thread].start()

        self.dict_file_ids_to_thread_num[idx] = num_thread

    def on_animation_requested(self, animation):
        animation.start()

    def on_animation_update(self):
        self.app.processEvents()

    def on_animation_stop_requested(self, thread_num, file_index):
        self.threads.pop(thread_num)

        if self.is_logging:
            if self.EVAL_SPECIFICATION_ID == Evaluation.Experiment.ExperimentType.COLLABORATION.value:
                timestamp = int(time.time() * 1000)

                if timestamp - self.last_timestamp > 30:  # one frame
                    action = 'Exited Conveyor Belt via Ending'
                    if self.last_timestamp is None:
                        duration = 'NA'
                    else:
                        duration = timestamp - self.last_timestamp

                    self.last_timestamp = timestamp

                    self.log_for_experiment(self.pid, timestamp, action, duration, str(file_index), 'NA', 'NA')

    #
    #
    #


    def halt_item_on_request(self, _id):
        thread_num = self.dict_file_ids_to_thread_num.get(_id)

        if thread_num in self.threads:
            thread = self.threads[thread_num]
            thread.pause()
            thread.file_icon_widget.set_processing_state(1)

        return

    def stop_conveyor_belt_animation(self, _id):
        for key in self.file_icons.keys():
            if self.file_icons[key].id == _id:
                if self.file_icons[key].anim_id != -1:
                    if self.file_icons[key].anim_id in self.threads.keys():
                        self.threads[self.file_icons[key].anim_id].on_stop()
                self.file_icons[key].anim_id = -1

    # called each frame, when an item is halted, TODO: may be deprecated
    def halting_item(self, _id):
        pass
        # self.show_review_request_overlay(_id)

    def answer_item_on_request(self):
        has_released_item = False
        for thread in self.threads:
            if has_released_item is False and self.threads[thread].is_paused is True:
                self.threads[thread].file_icon_widget.set_processing_state(2)
                self.show_review_request_overlay(self.threads[thread].file_index)


    def release_item_on_request(self):
        has_released_item = False
        for thread in self.threads:
            if has_released_item is False and self.threads[thread].is_paused is True:
                self.threads[thread].resume()
                self.threads[thread].file_icon_widget.set_processing_state(3)
                has_released_item = True
                self.hide_review_request_overlay(self.threads[thread].file_index)
                # This is hardcoded and only works for purchase.docx
                self.threads[thread].file_icon_widget.file.review_accepted = True
                self.file_icons[7].content = PURCHASE_REQUEST_2
                self.file_icons[7].update()


    def decline_item_from_request(self):
        has_released_item = False
        for thread in self.threads:
            if has_released_item is False and self.threads[thread].is_paused is True:
                thread = self.threads[thread]
                curr_pos = [thread.file_icon_widget.x(), thread.file_icon_widget.y()]
                # target_pos = [thread.file_icon_widget.x(), thread.file_icon_widget.y() +400 ]
                thread.resume()
                self.hide_review_request_overlay(thread.file_index)
                thread.file_icon_widget.set_processing_state(4)
                thread.file_icon_widget.file.review_accepted = False
                # self.__animate_leave_conveyor(thread.file_index, curr_pos, target_pos)
                return

    def show_review_request_overlay(self, id):
        self.file_icons[id].show_change_request(0)
        self.file_icons[id].widget.change_requests_btn_confirm.clicked.connect(self.on_review_request_accepted)
        self.file_icons[id].widget.change_requests_btn_decline.clicked.connect(self.on_review_request_declined)

    def hide_review_request_overlay(self, id):
        self.file_icons[id].hide_change_requests()

    def on_review_request_accepted(self):
        self.release_item_on_request()
        pass

    def on_review_request_declined(self):
        self.decline_item_from_request()
        pass


    #
    #
    #

    def __animate_leave_conveyor(self, idx, from_point, to_point):
        y_offset = -200
        self.animate(idx, 0, [from_point, to_point], 1000,  smath.Math.normalize_vector((0, y_offset)), False)



    #
    #
    #

    def magnify_physical_document(self, _id, factor):
        for t in self.processed_trackables:
            if t.type_id == TrackableTypes.PHYSICAL_DOCUMENT.value:
                if t.id == _id:
                    pass

    def magnify_file(self, _id, factor):
        self.file_icons[_id].show_preview()

    def delete_regions(self, region):
        if region[0] is not None:
            for i in range(len(self.drawn_shapes) - 1, -1, -1):
                if region[0].roi == self.drawn_shapes[i].roi:
                    self.drawn_shapes[i].set_roi([])

                    if self.drawn_shapes[i].img is not None:
                        self.drawn_shapes[i].img.close()

                    if self.drawn_shapes[i].text is not None:
                        self.drawn_shapes[i].text.setText('')
                        self.drawn_shapes[i].text.close()

                    if self.is_logging:
                        if self.EVAL_SPECIFICATION_ID == Evaluation.Experiment.ExperimentType.COLLABORATION.value:
                            timestamp = int(time.time() * 1000)

                            if self.last_timestamp is None:
                                duration = 'NA'
                            else:
                                duration = timestamp - self.last_timestamp

                            self.last_timestamp = timestamp

                            action = 'Deletion of ' + ('None' if self.drawn_shapes[i].effect is None else self.drawn_shapes[i].effect.name)

                            self.log_for_experiment(self.pid, timestamp, action, duration, 'NA', 'NA', 'NA')

                    self.drawn_shapes.pop(i)
                    self.masks.pop(i)

                    if self.previous_palette_selection_index > i:
                        self.previous_palette_selection_index -= 1

    def delete_region_by_collision(self, region_index):
        self.delete_regions([self.drawn_shapes[region_index]])

    def click_file(self, _id, touch_id):
        for k, f in self.file_icons.items():
            if f.id == _id:
                f.grabbed = True

    def initUI(self):
        self.setWindowTitle('Canvas')

        if not self.DEBUG:
            self.showFullScreen()

        for icon in self.file_icons.keys():
            self.file_icons[icon].widget.setParent(self)
            self.file_icons[icon].widget.show()

        self.show()

        # self.__create_default_delete_region()

    def apply_evaluation_settings(self, settings):
        self.is_logging = True
        self.file_icons = {}

        for d in settings:
            _id = d['id']
            content = d['content']

            self.evaluation_categories.append(d['category'])
            self.file_icons[_id] = File(_id, 1920 / 2 + randint(0, 50), 800 + randint(0, 50), self, "doc" + str(_id), content, FileType.TEXT.value if content[0] != 'r' else FileType.IMAGE.value, self.DEBUG)

        self.pid = settings[0]['pid']

    def log_for_experiment(self, *args):
        Evaluation.Experiment.Logging.log(self.eval_csv_path + "review_p_" + str(self.pid) + '.csv', list(args))

    def __create_default_delete_region(self):
        self.drawn_shapes.append(Shape(effect=Effect.Deletion()))

        self.drawn_shapes[-1].set_roi([(1650, 760), (1650, 1060), (1900, 1060), (1900, 760)])
        self.drawn_shapes[-1].set_effect(Effect.Deletion())
        self.drawn_shapes[-1].parent = self
        self.drawn_shapes[-1].set_image()

        self.masks.append(Mask.Mask(self.drawn_shapes[-1].roi, len(self.drawn_shapes) - 1))

    def get_file_dictionary(self):
        return self.file_icons

    def get_drawn_shapes(self):
        return self.drawn_shapes

    def is_over_icon(self):
        for icon in self.file_icons:
            if self.file_icons[icon].widget.is_over_icon:
                return True

        return False

    def keyPressEvent(self, ev):
        if ev.key() == QtCore.Qt.Key_Return:
            self.handle_return_key()
        elif ev.key() == QtCore.Qt.Key_Delete:
            self.handle_delete_key()

            for key, value in self.animations.items():
                value.pause()
                value.stop()

            for f in self.file_icons.keys():
                self.file_icons[f].is_on_conveyor_belt = False

        elif ev.key() == QtCore.Qt.Key_Q or ev.key() == QtCore.Qt.Key_Escape:
            self.handle_exit_key()

        elif ev.key() == QtCore.Qt.Key_Y:
            self.handle_confirm_key()
        elif ev.key() == QtCore.Qt.Key_N:
            self.handle_reject_key()
        elif ev.key() == QtCore.Qt.Key_A:
            self.handle_answer_request_key()
        elif ev.key() == QtCore.Qt.Key_T:
            self.handle_transfer_files_key()
        elif ev.key() == QtCore.Qt.Key_Z:
            self.handle_transfer_files_key(True)
        elif ev.key() == QtCore.Qt.Key_W:
            self.__create_composition_on_init__()

    def handle_confirm_key(self):
        self.release_item_on_request()

    def handle_reject_key(self):
        self.decline_item_from_request()

    def handle_answer_request_key(self):
        self.answer_item_on_request()

    def handle_transfer_files_key(self, fixed_pos=False):
        print("Spawn index", self.image_spawn_index)
        portal_region = list(filter(lambda x: x.effect.effect_type == Effect.EffectType.PORTAL, self.drawn_shapes))
        if len(portal_region) > 0:
            region = portal_region[0]
            center = region.center
            num_files = len(self.file_icons.keys())

            num_files += 1

            if fixed_pos == True:
                self.file_icons[num_files] = File(
                    num_files,
                    center[0],
                    region.aabb[0][1],
                    self,
                    "DSC_" + str(512 + self.image_spawn_index) + ".jpg",
                    IMAGES_ON_PHONE[self.image_spawn_index%len(IMAGES_ON_PHONE)],
                    FileType.IMAGE.value,
                    self.DEBUG)
            else:
                self.file_icons[num_files] = File(
                    num_files,
                    center[0] + self.image_spawn_index % 2 * 110,
                    region.aabb[0][1] + 110 * (int)(self.image_spawn_index / 2),
                    self,
                    "DSC_" + str(512 + self.image_spawn_index) + ".jpg",
                    IMAGES_ON_PHONE[self.image_spawn_index%len(IMAGES_ON_PHONE)],
                    FileType.IMAGE.value,
                    self.DEBUG)
            self.image_spawn_index += 1
        pass

    def handle_return_key(self):
        pass

    def handle_exit_key(self):
        self.close()
        self.on_close.emit()

    def handle_delete_key(self):
        for s in self.drawn_shapes:
            if s.img is not None:
                s.img.setPixmap(QtGui.QPixmap())
                s.img.close()

            if s.text is not None:
                s.text.close()

            if s.effect is not None:
                if s.effect.effect_type == Effect.EffectType.SEND_EMAIL.value:
                    if s.progress is not None:
                        s.progress.close()

                    if s.sending_text is not None:
                        s.sending_text.setText("")
                        s.sending_text.close()

        self.drawn_shapes = []
        self.current_drawn_points = []

    def mousePressEvent(self, ev):
        if ev.button() == QtCore.Qt.LeftButton and not self.is_over_icon():
            self.is_released = False
            self.drawing = True

            for s in self.drawn_shapes:
                s.dropped = False

            self.current_drawn_points = []

            if self.is_logging and len(self.active_menus) == 0:
                if self.EVAL_SPECIFICATION_ID == Evaluation.Experiment.ExperimentType.COLLABORATION.value:
                    timestamp = int(time.time() * 1000)

                    action = 'Started Drawing'

                    if self.last_timestamp is None:
                        duration = 'NA'
                    else:
                        duration = timestamp - self.last_timestamp

                    self.last_timestamp = timestamp

                    self.log_for_experiment(self.pid, timestamp, action, duration, 'NA', 'NA', 'NA')

    def mouseReleaseEvent(self, ev):
        if ev.button() == QtCore.Qt.LeftButton:
            if not self.is_over_icon():

                self.drawing = False
                self.is_released = True

                if len(self.current_drawn_points) > 0:
                    if self.is_logging:
                        if self.EVAL_SPECIFICATION_ID == Evaluation.Experiment.ExperimentType.COLLABORATION.value:
                            timestamp = int(time.time() * 1000)

                            action = 'Stopped Drawing'

                            if self.last_timestamp is None:
                                duration = 'NA'
                            else:
                                duration = timestamp - self.last_timestamp

                            self.last_timestamp = timestamp

                            self.log_for_experiment(self.pid, timestamp, action, duration, 'NA', 'NA', 'NA')

                    # At this point, a new shape is generated
                    self.drawn_shapes.append(Shape(effect=self.current_brush.get_effect(), parent=self))

                    if self.current_brush.effect is None:
                        self.brush_name = "None"
                    else:
                        self.brush_name = self.current_brush.effect.name

                    # Handle all shapes except for conveyor belt
                    if self.current_brush.brush_tpye != Brush.BrushTypes.CONVEYOR_BELT.value:
                        if smath.Math.sufficient_shape_area(self.current_drawn_points):
                            self.current_drawn_points.append(self.current_drawn_points[0])

                            self.drawn_shapes[-1].set_roi(self.current_drawn_points)
                            self.drawn_shapes[-1].set_effect(self.current_brush.get_effect())
                            self.drawn_shapes[-1].parent = self
                            self.drawn_shapes[-1].is_palette_parent = False

                            self.masks.append(Mask.Mask(self.drawn_shapes[-1].roi, len(self.drawn_shapes) - 1))

                            #
                            #
                            # Generate Palette Shape
                            if self.current_brush.get_brush_type() == Brush.BrushTypes.PALETTE.value:
                                # Calculate Radius
                                radius = int(sum(smath.Math.vector_norm((p[0] - self.drawn_shapes[-1].center[0], p[1] - self.drawn_shapes[-1].center[1])) for p in self.drawn_shapes[-1].roi) / len(self.drawn_shapes[-1].roi))

                                # Create circle ROI for last shape
                                new_roi = smath.Math.compute_circle(self.drawn_shapes[-1].center[0], self.drawn_shapes[-1].center[1], radius)

                                # Set shape to palette parent
                                self.drawn_shapes[-1].is_palette_parent = True

                                # Add circle ROI to shape
                                # 90 controls spacing of sub area ROIs
                                self.drawn_shapes[-1].set_roi(smath.Math.resample_points(new_roi, 100))

                                # Set index to the parent
                                parent_shape_index = len(self.drawn_shapes) - 1

                                # Create Sub-Area Rois
                                # ! At this point, new menu items are spawned !
                                for i, roi in enumerate(self.drawn_shapes[parent_shape_index].sub_area_rois):
                                    self.drawn_shapes.append(Shape())
                                    self.drawn_shapes[-1].set_effect(self.current_brush.get_effect())
                                    self.drawn_shapes[-1].set_palette_effect(i + 1)
                                    self.drawn_shapes[-1].set_roi(roi)
                                    self.drawn_shapes[-1].parent = self
                                    self.drawn_shapes[-1].is_palette_parent = False
                                    self.drawn_shapes[-1].palette_parent = parent_shape_index
                                    self.drawn_shapes[-1].set_image()
                                    self.drawn_shapes[parent_shape_index].palette_children_indices.append(len(self.drawn_shapes) - 1)

                                    self.masks.append(Mask.Mask(self.drawn_shapes[-1].roi, len(self.drawn_shapes) - 1))

                            #
                            #
                            #


                            if self.is_logging:
                                if self.EVAL_SPECIFICATION_ID == Evaluation.Experiment.ExperimentType.COLLABORATION.value:
                                    timestamp = int(time.time() * 1000)

                                    action = ""

                                    if self.drawn_shapes[-1].effect is None:
                                        action = "None"
                                    else:
                                        action = self.drawn_shapes[-1].effect.name

                                        if self.drawn_shapes[-1].effect.effect_type == Effect.EffectType.TAG.value:
                                            action += " with " + self.drawn_shapes[-1].effect.effect_text
                                        if self.drawn_shapes[-1].effect.effect_type == Effect.EffectType.DELEGATE.value:
                                            action += " " + self.drawn_shapes[-1].effect.effect_text
                                        if self.drawn_shapes[-1].effect.effect_type == Effect.EffectType.SEND_EMAIL.value:
                                            action += " " + self.drawn_shapes[-1].effect.effect_text
                                        if self.drawn_shapes[-1].effect.effect_type == Effect.EffectType.MAGNIFICATION.value:
                                            action += " with " + self.drawn_shapes[-1].effect.effect_text

                                    action += ' Region Drawn Successfully'

                                    if self.last_timestamp is None:
                                        duration = 'NA'
                                    else:
                                        duration = timestamp - self.last_timestamp

                                    self.last_timestamp = timestamp

                                    self.log_for_experiment(self.pid, timestamp, action, duration, 'NA', 'NA', 'NA')
                        else:
                            if self.is_logging:
                                if self.EVAL_SPECIFICATION_ID == Evaluation.Experiment.ExperimentType.COLLABORATION.value:
                                    timestamp = int(time.time() * 1000)

                                    action = ("None" if self.drawn_shapes[-1].effect is None else self.drawn_shapes[-1].effect.name) + ' Region was rejected because of its size'
                                    if self.last_timestamp is None:
                                        duration = 'NA'
                                    else:
                                        duration = timestamp - self.last_timestamp

                                    self.last_timestamp = timestamp

                                    self.log_for_experiment(self.pid, timestamp, action, duration, 'NA', 'NA', 'NA')

                            self.drawn_shapes.pop(-1)


                    #
                    #
                    #
                    # Create conveyor belt
                    else:
                        if smath.Math.sufficient_shape_area(self.current_drawn_points, 1000):

                            # Handle, whether the shape is a loop

                            # v "may" handle the angle between the first and the last item, so that it can be infered, whether the shape is closed or it is not
                            v = (self.current_drawn_points[0][0] - self.current_drawn_points[-1][0], self.current_drawn_points[0][1] - self.current_drawn_points[-1][1])
                            looped = False
                            contains_loop = False
                            if smath.Math.vector_norm(v) < 75:
                                self.current_drawn_points.append(self.current_drawn_points[0])
                                looped = True

                            self.drawn_shapes[-1].set_middle_line(self.current_drawn_points)
                            shape, shape_part_one, shape_part_two = smath.Math.shapify(self.drawn_shapes[-1].middle_line)
                            self.drawn_shapes[-1].shape_part_one = shape_part_one
                            self.drawn_shapes[-1].shape_part_two = shape_part_two
                            self.drawn_shapes[-1].set_roi(shape)
                            self.drawn_shapes[-1].set_effect(self.current_brush.get_effect())
                            self.drawn_shapes[-1].effect.looped = looped
                            self.drawn_shapes[-1].is_looped = looped
                            self.drawn_shapes[-1].parent = self
                            self.drawn_shapes[-1].set_image()
                            self.masks.append(Mask.Mask(self.drawn_shapes[-1].roi, len(self.drawn_shapes) - 1))


                            # if has intersect, draw loop label
                            intersect_points = self.contains_intersect(self.current_drawn_points)
                            if intersect_points is not None and looped is False:
                                self.drawn_shapes[-1].set_loop_text(self.current_drawn_points[intersect_points[0]:intersect_points[1]], "5X")
                                pass

                            conveyor_belts = list(filter(lambda x: x.effect.effect_type == Effect.EffectType.CONVEYOR_BELT.value, self.drawn_shapes))
                            if len(conveyor_belts) > 1:
                                for belt in conveyor_belts[0:-1]:
                                    result = self.intersects_other_path(self.current_drawn_points, belt.roi)
                                    if result == True:
                                        self.drawn_shapes[-1].set_condition_text(self.current_drawn_points, "if changes accepted")



                            if self.is_logging:
                                if self.EVAL_SPECIFICATION_ID == Evaluation.Experiment.ExperimentType.COLLABORATION.value:
                                    timestamp = int(time.time() * 1000)

                                    action = ("None" if self.drawn_shapes[-1].effect is None else self.drawn_shapes[-1].effect.name) + ' Shape Drawn Successfully'
                                    if self.last_timestamp is None:
                                        duration = 'NA'
                                    else:
                                        duration = timestamp - self.last_timestamp

                                    self.last_timestamp = timestamp

                                    self.log_for_experiment(self.pid, timestamp, action, duration, 'NA', 'NA', 'NA')
                        else:
                            if self.is_logging:
                                if self.EVAL_SPECIFICATION_ID == Evaluation.Experiment.ExperimentType.COLLABORATION.value:
                                    timestamp = int(time.time() * 1000)

                                    action = ("None" if self.drawn_shapes[-1].effect is None else self.drawn_shapes[-1].effect.name) + ' Region was rejected because of its size'
                                    if self.last_timestamp is None:
                                        duration = 'NA'
                                    else:
                                        duration = timestamp - self.last_timestamp

                                    self.last_timestamp = timestamp

                                    self.log_for_experiment(self.pid, timestamp, action, duration, 'NA', 'NA', 'NA')

                            self.drawn_shapes.pop(-1)

                if len(self.drawn_shapes) > 0:
                    for w in (self.findChildren(QtWidgets.QLabel, "shape_img") + self.findChildren(QtWidgets.QLabel, "shape_text")):
                        w.lower()

                self.current_drawn_points = []

    #
    # using the intersect algorithm as proposed by BryceBoe (bryceboe.com/2006/10/23/line-segment-inersection-algorithm/)
    def ccw(self, A, B, C):
        return (C[1]-  A[1]) * (B[0] - A[0]) > (B[1] -A[1]) * (C[0] -A[0])

    def intersect(self, A, B, C, D):
        return (self.ccw(A, C, D) != self.ccw(B, C, D) and self.ccw(A,B,C) != self.ccw(A,B,D))

    def intersects_other_path(self, path_a, path_b):
        result = False
        for i in range(1, len(path_a)):
            for j in range(1, len(path_b)):
                couple1_point1 = path_a[i -1]
                couple1_point2 = path_a[i]
                couple2_point1 = path_b[j -1]
                couple2_point2 = path_b[j]

                if self.intersect(couple1_point1, couple1_point2,
                                  couple2_point1, couple2_point2):
                    result = True
        return result



    def contains_intersect(self, points):
        result = None
        len_path = -1
        for i in range(1, len(points)):
            for j in range(i + 2, len(points)):
                couple1_point1 = points[i - 1]
                couple1_point2 = points[i]
                couple2_point1 = points[j - 1]
                couple2_point2 = points[j]

                if self.intersect(couple1_point1, couple1_point2,
                                  couple2_point1, couple2_point2):
                    if self.is_identical_vector(couple2_point1, couple1_point2) is False:
                        # try to find biggest loops!
                        m_len_path = j-i
                        if m_len_path > len_path:
                            len_path = m_len_path
                            # the result will be the "welding" point of the loop
                            result = [i, j-1]

        return result

    def is_identical_vector(self, v1, v2):
        return v1[0]==v2[0] and v1[1]==v2[1]

    #
    #


    def mouseMoveEvent(self, ev):
        if self.drawing:
            self.current_drawn_points.append((ev.x(), ev.y()))

    def poly(self, pts):
        return QtGui.QPolygonF(map(lambda p: QtCore.QPointF(*p), pts))


    # Draws the line, that the user has previously drawn
    def paintActiveLine(self, qp):
        if self.current_brush.effect is not None:
            if self.current_brush.effect.effect_color is not None:
                qp.setPen(QtGui.QPen(self.current_brush.effect.effect_color, 5))
            else:
                qp.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255), 5))
        else:
            qp.setPen(QtGui.QPen(Effect.EffectColor.CONVEYOR_BELT, 5))

        qp.drawPolyline(self.poly(self.current_drawn_points))

    # Draws Trackable points (e.g. fingers of user)
    def paintTrackables(self, qp):
        for i, t in enumerate(self.processed_trackables):
            if t.type_id == TrackableTypes.TOUCH.value:
                qp.drawEllipse(t.center[0] - 8, t.center[1] - 8, 16, 16)

    # Whatever this does...
    def paintTest(self, qp):
        for p in self.test_p:
            qp.drawEllipse(p[0] - 7.5, p[1] - 7.5, 15, 15)

    def paintEvent(self, ev):
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing, True)
        qp.setRenderHint(QtGui.QPainter.SmoothPixmapTransform, True)
        qp.setBrush(QtGui.QColor(style.WidgetStyle.BACKGROUND_COLOR.value))
        qp.drawRect(ev.rect())
        qp.setBrush(QtGui.QColor(20, 255, 190))

        self.paintActiveLine(qp)

        self.paintTrackables(qp)

        self.paintTest(qp)



        for index, shape in enumerate(self.drawn_shapes):
            path = QtGui.QPainterPath()

            if shape.effect is None:
                qp.drawPolyline(self.poly(shape.roi))

            if len(shape.roi) > 0:
                first_point = shape.roi[0]
                path.moveTo(first_point[0], first_point[1])

            i = 0

            for point in shape.roi:
                if i > 0:
                    path.lineTo(point[0], point[1])

                i += 1

            if len(shape.roi) > 0:
                path.lineTo(first_point[0], first_point[1])

            if shape.moveable:
                for arrow in shape.moveable_highlighting:
                    qp.drawPolyline(self.poly(arrow['upper']))
                    qp.drawPolyline(self.poly(arrow['lower']))
                    qp.drawPolyline(self.poly(arrow['angle_one']))
                    qp.drawPolyline(self.poly(arrow['angle_two']))

            if shape.effect is not None:

                # Draw "Common" ROI
                if shape.effect.effect_type is not Effect.EffectType.CONVEYOR_BELT.value and shape.effect.effect_type is not Effect.EffectType.PALETTE.value:
                    qp.fillPath(path, shape.effect.effect_color)

                # Draw Palette
                elif shape.effect.effect_type is Effect.EffectType.PALETTE.value:
                    qp.setPen(QtGui.QPen(QtGui.QColor(style.WidgetStyle.PALETTE_OUTLINE_COLOR.value), 5))

                    if not shape.palette_parent:
                        qp.drawPolyline(self.poly(shape.roi))

                        if shape.palette_effect_selected:
                            qp.fillPath(path, shape.effect.effect_colors[shape.effect_color_index])
                        else:
                            qp.fillPath(path, QtGui.QColor(style.WidgetStyle.PALETTE_BACKGROUND_COLOR.value))
                else:
                    qp.setPen(QtGui.QPen(Effect.EffectColor.CONVEYOR_BELT.value, 5))
                    if len(shape.middle_line) > 0:
                        if not shape.is_looped:
                            qp.drawPolyline(self.poly(shape.roi))
                        else:
                            qp.drawPolyline(self.poly(shape.shape_part_one))
                            qp.drawPolyline(self.poly(shape.shape_part_two))

                        for arrow in shape.direction_visualization_arrows:
                            qp.drawPolyline(self.poly(arrow['arrow_part1']))
                            qp.drawPolyline(self.poly(arrow['arrow_part2']))
                            qp.drawPolyline(self.poly(arrow['arrow_base']))

        # Paint trackables
        for i, t in enumerate(self.processed_trackables):
            if t.type_id == TrackableTypes.FILE.value:
                if t.is_digital_twin:
                    for k, p in enumerate(self.processed_trackables):
                        if i == k:
                            continue

                        if p.type_id == TrackableTypes.PHYSICAL_DOCUMENT.value:
                            if t.physical_representation_id == p.id:
                                qp.drawLine(t.center[0], t.center[1], p.center[0], p.center[1])

                if t.grabbed:
                    qp.drawPolyline(self.poly(t.roi + [t.roi[0]]))

                if t.tagged:
                    qp.setPen(QtGui.QPen(Effect.EffectColor.TAG.value, 16))
                    qp.drawEllipse(QtCore.QPoint(t.roi[2][0], t.roi[2][1]), 8, 8)
                    qp.setPen(QtGui.QPen(QtGui.QColor(0, 155, 0), 5))

            if t.type_id == TrackableTypes.PHYSICAL_DOCUMENT.value:
                if t.tagged or self.phys_tag:
                    qp.setPen(QtGui.QPen(Effect.EffectColor.TAG.value, 48))
                    qp.drawEllipse(QtCore.QPoint(t.roi[3][0], t.roi[3][1]), 24, 24)
                    qp.setPen(QtGui.QPen(QtGui.QColor(0, 155, 0), 5))

            if t.type_id == TrackableTypes.TANGIBLE.value:
                if self.tangible.effect is None:
                    qp.drawPolyline(self.poly(t.roi))
                else:
                    path = QtGui.QPainterPath()

                    if len(t.roi) > 0:
                        first_point = t.roi[0]
                        path.moveTo(first_point[0], first_point[1])

                    i = 0

                    for point in t.roi:
                        if i > 0:
                            path.lineTo(point[0], point[1])

                        i += 1

                    if len(t.roi) > 0:
                        path.lineTo(first_point[0], first_point[1])

                    qp.fillPath(path, self.tangible.effect.effect_color)

        if self.DEBUG:
            if len(self.processed_trackables) > 0:
                qp.setPen(QtGui.QColor(0, 255, 0))

                for trackable in self.processed_trackables:
                    if trackable.type_id == TrackableTypes.FILE.value:
                        tlc, blc, brc, trc = trackable.collision_roi[0], trackable.collision_roi[1], trackable.collision_roi[2], trackable.collision_roi[3]
                    else:
                        tlc, blc, brc, trc = trackable.roi[0], trackable.roi[1], trackable.roi[2], trackable.roi[3]

                    center = trackable.center

                    qp.drawLine(tlc[0], tlc[1], trc[0], trc[1])
                    qp.drawLine(tlc[0], tlc[1], blc[0], blc[1])
                    qp.drawLine(blc[0], blc[1], brc[0], brc[1])
                    qp.drawLine(trc[0], trc[1], brc[0], brc[1])

                    qp.drawEllipse(center[0] - 7.5, center[1] - 7.5, 15, 15)

        if len(self.processed_trackables) > 0:
            qp.setPen(QtGui.QPen(QtGui.QColor(Effect.EffectColor.CONVEYOR_BELT.value), 5))

            for trackable in self.processed_trackables:
                if trackable.type_id == TrackableTypes.FILE.value:
                    if trackable.is_digital_twin:
                        for p in self.processed_trackables:
                            if p.type_id == TrackableTypes.PHYSICAL_DOCUMENT.value:
                                if trackable.physical_representation_id == p.id:
                                    qp.drawLine(trackable.center[0], trackable.center[1], p.center[0], p.center[1])
        qp.end()
