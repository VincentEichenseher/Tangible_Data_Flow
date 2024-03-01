
from PyQt5 import QtCore, QtGui, QtWidgets
from style import style
from datastructures.TrackableTypes import FileType


# All status icons were retrieved from https://material.io/resources/icons/?icon=message&style=round, Google - Apache 2.0 licensed

def clickable(widget):
    class Filter(QtCore.QObject):
        press = QtCore.pyqtSignal(QtCore.QEvent)
        move = QtCore.pyqtSignal(QtCore.QEvent)
        release = QtCore.pyqtSignal(QtCore.QEvent)

        def eventFilter(self, obj, event):
            if obj == widget:
                if event.type() == QtCore.QEvent.MouseButtonPress:
                    if obj.rect().contains(event.pos()):
                        self.press.emit(event)

                        return True

                if event.type() == QtCore.QEvent.MouseButtonRelease:
                    if obj.rect().contains(event.pos()):
                        self.release.emit(event)

                        return True

                if event.type() == QtCore.QEvent.MouseMove:
                    if obj.rect().contains(event.pos()):
                        self.move.emit(event)

                        return True

            return False

    filter = Filter(widget)

    widget.installEventFilter(filter)

    return filter.press, filter.release, filter.move


class QFileIconWidget(QtWidgets.QLabel):
    on_mouse_move = QtCore.pyqtSignal()

    def __init__(self, width, height, parent, type_, path='res/img/file_icon.png', name='dummy', file=None):
        # http://www.clker.com/clipart-new-file-simple.html

        super(QFileIconWidget, self).__init__()

        self.default_width = width
        self.default_height = height
        self.name = name
        self.setCursor(QtCore.Qt.BlankCursor)

        self.setParent(parent)
        self.file = file
        self.type = type_

        self.is_affected_by_effect = False
        self.setObjectName("file")

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.setPixmap(QtGui.QPixmap(path).scaledToWidth(width))
        self.setScaledContents(False)
        self.is_over_icon = False

        self.name_widget = QtWidgets.QTextEdit()
        self.name_widget.setReadOnly(True)
        self.name_widget.setParent(self.parent())
        self.name_widget.setText(self.name)
        self.name_widget.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.name_widget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.name_widget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.name_widget.setAlignment(QtCore.Qt.AlignCenter)
        self.name_widget.setStyleSheet(style.WidgetStyle.QTEXTEDIT_STYLE.value)
        self.name_widget.setGeometry(self.x() - 15, self.y() + 5, self.width() + 30, 20)
        self.name_widget.setCursor(QtCore.Qt.BlankCursor)

        self.name_widget.press, self.name_widget.release, self.name_widget.move = clickable(self.name_widget)

        self.name_widget.press.connect(self.mousePressEvent)
        self.name_widget.release.connect(self.mouseReleaseEvent)
        self.name_widget.move.connect(self.mouseMoveEvent)

        self.name_widget.setCursor(QtCore.Qt.BlankCursor)

        self.name_widget.show()

        # 0:    no review requested
        # 1:    review pending
        # 2:    review received
        # 4:    review passed
        # 5:    review failed
        self.request_processing_states = 0
        self.request_processing_indicator = QtWidgets.QLabel()
        self.request_processing_indicator_image = QtGui.QPixmap(None)
        self.request_processing_indicator.setPixmap(self.request_processing_indicator_image)
        self.request_processing_indicator.setParent(self.parent())
        self.request_processing_indicator.setAlignment(QtCore.Qt.AlignCenter)

        self.request_processing_indicator.setGeometry(self.x() + self.width() / 2,
                                 self.y() + self.height() / 2,
                                 80,
                                 80)
        self.request_processing_indicator.show()

        if self.type == FileType.TEXT.value:
            width = 500
            height = 450

            self.preview_default_width = width
            self.preview_default_height = height

            self.preview = QtWidgets.QTextEdit()
            self.preview.setReadOnly(True)
            self.preview.setParent(self.parent())
            self.preview.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
            self.preview.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.preview.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.preview.setStyleSheet(style.WidgetStyle.QTEXTEDIT_STYLE.value)
            self.preview.setGeometry(self.x() + self.width() / 2, self.y() + self.height() / 2, self.preview_default_width, self.preview_default_height)
            self.preview.setCursor(QtCore.Qt.BlankCursor)
            self.preview.setAcceptRichText(True)
            self.preview.setHtml(self.file.content)

        elif self.type == FileType.IMAGE.value:

            self.preview = QtWidgets.QLabel()
            self.preview.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)

            if self.file.is_digital_twin:
                self.preview_default_width = 520 / 4
                self.preview_default_height = 695 / 4
                self.preview.setPixmap(QtGui.QPixmap(self.file.content).scaledToWidth(520 / 4))
            else:
                self.preview_default_width = 550
                self.preview_default_height = 695
                self.preview.setPixmap(QtGui.QPixmap(self.file.content).scaledToWidth(550))

            self.preview.setGeometry(self.x() + self.width() / 2, self.y() + self.height() / 2, self.preview_default_width, self.preview_default_height)
            self.preview.setCursor(QtCore.Qt.BlankCursor)

            self.preview.setParent(self.parent())

        self.preview.press, self.preview.release, self.preview.move = clickable(self.preview)

        self.preview.press.connect(self.mousePressEvent)
        self.preview.release.connect(self.mouseReleaseEvent)
        self.preview.move.connect(self.mouseMoveEvent)
        self.preview.hide()

        # define cr window
        self.change_requests = QtWidgets.QTextEdit()
        self.change_requests.setReadOnly(True)
        self.change_requests.setParent(self.parent())
        # self.change_requests.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.change_requests.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.change_requests.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.change_requests.setGeometry(self.x() + self.width() / 2,
                                 self.y() + self.height() / 2,
                                 600,
                                 590)

        # self.change_requests.setStyleSheet("margin:0px;padding:0px!important;border:0px;")
        self.change_requests.setCursor(QtCore.Qt.BlankCursor)
        self.change_requests.setAcceptRichText(True)





        change_request_msg = \
        """
            <div style='margin:0px; padding: 0px;width=100%;'> 
            <p style='font-weight:bold; margin-bottom:0px; font-size:24px; color:black;'>{}</p> 
            <hr> 
            <p style='color:dimgray; font-size: 12px;'>{}</p> <hr> 
  
            <table width='100%'>
            <tbody>
            
            <tr>
            <td>
                <h2>Purchase Request</h2>
                <h3>Hardware Procurement</h3>
                <h3>Request ID: <span style="color:green;">491230</span></h3>
                <h3>Requester: John Doe</h3>
            </td>
            
            <td>
            <b>HARDWIRE Electrical</b>
            <p>542 Hardwire Drive</p>
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
                <td style="color:green;font-weight: bold;">10</td>
                <td>9.90$</td>
                <td style="color:green;font-weight: bold;">99.00$</td>
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
                <td style="color:green;font-weight: bold;">10</td>
                <td>2.30$</td>
                <td style="color:green;font-weight: bold;">23.00$</td>
            </tr>
            </tbody>
            </table>           
            <br>
            <hr> 
            <p>
            <i style='color: dimgray;'>Hey Sarah, I have entered the request ID as well as the missing quantities. If you are okay with it, the request is ready for submission.  - Karl</i> 
            </p>
            </div>
        """

        text = change_request_msg.format("purchase_152342.docx", "5 changes by Karl")

        self.change_requests.setHtml(text)

        self.change_requests.hide()

        self.change_requests_btn_confirm = QtWidgets.QPushButton()
        self.change_requests_btn_confirm.setParent(self.parent())
        self.change_requests_btn_confirm.setGeometry(self.x() + self.width() / 2,
                                 self.y() + self.height() / 2,
                                 120,
                                 80)
        self.change_requests_btn_confirm.setText("Confirm")
        self.change_requests_btn_confirm.hide()
        self.change_requests_btn_confirm.setStyleSheet("background-color: springgreen; color: darkgreen;")
        # self.change_requests_btn_confirm.clicked.connect(self.printOk)
        self.change_requests_btn_confirm.setCursor(QtCore.Qt.BlankCursor)


        self.change_requests_btn_decline = QtWidgets.QPushButton()
        self.change_requests_btn_decline.setParent(self.parent())
        self.change_requests_btn_decline.setGeometry(
            self.change_requests.x() + self.change_requests.width() -120,
            self.change_requests.y() + self.change_requests.height()-80,
            120, 80)
        self.change_requests_btn_decline.setText("Decline")
        self.change_requests_btn_decline.setStyleSheet("background-color: lightsalmon; color: darkred;")
        self.change_requests_btn_decline.hide()
        # self.change_requests_btn_confirm.clicked.connect(self.printOk)
        self.change_requests_btn_decline.setCursor(QtCore.Qt.BlankCursor)

        self.__mousePressPos = None
        self.__mouseMovePos = None

    def update(self):
        self.preview.setHtml(self.file.content)


    def mousePressEvent(self, event):
        self.is_over_icon = True
        self.file.mouse_used = True

        if self.file.is_on_conveyor_belt:
            self.file.grabbed = True

        if event.buttons() == QtCore.Qt.LeftButton:
            self.__mousePressPos = event.globalPos()
            self.__mouseMovePos = event.globalPos()

        super(QFileIconWidget, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.is_over_icon = True
            self.file.mouse_used = True

            if self.file.is_on_conveyor_belt:
                self.file.grabbed = True

            current_position = self.mapToGlobal(self.pos())
            global_position = event.globalPos()

            new_position = self.mapFromGlobal(current_position + global_position - self.__mouseMovePos)

            self.file.set_position((new_position.x(), new_position.y()))

            self.move(new_position)

            self.__mouseMovePos = global_position
            self.on_mouse_move.emit()

        super(QFileIconWidget, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.is_over_icon = False
        self.file.grabbed = False
        self.file.mouse_used = False

        if self.__mousePressPos is not None:
            moved = event.globalPos() - self.__mousePressPos
            if moved.manhattanLength() > 3:
                event.ignore()
                return

        super(QFileIconWidget, self).mouseReleaseEvent(event)

    #
    #
    #

    def set_processing_state(self, state):
        if state == 0:
            self.request_processing_indicator_image = QtGui.QPixmap(None)
        elif state == 1:
            self.request_processing_indicator_image = QtGui.QPixmap("res/img/status/pending.png")
        elif state == 2:
            self.request_processing_indicator_image = QtGui.QPixmap("res/img/status/processed.png")
        elif state == 3:
            self.request_processing_indicator_image = QtGui.QPixmap("res/img/status/accepted.png")
        elif state == 4:
            self.request_processing_indicator_image = QtGui.QPixmap("res/img/status/declined.png")

        self.request_processing_indicator.setPixmap(self.request_processing_indicator_image)

    def set_pos(self, pos):
        self.file.previously_touched = True
        self.move(pos.x() - self.width() / 2, pos.y() - self.height() / 2)
        self.on_mouse_move.emit()

    posi = QtCore.pyqtProperty(QtCore.QPointF, fset=set_pos)
