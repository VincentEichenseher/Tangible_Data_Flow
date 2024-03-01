
from PyQt5 import QtCore, QtGui

import time


class InfiniteThread(QtCore.QThread):
    update_trigger = QtCore.pyqtSignal()

    def __init__(self, frequency, no_sleep=False):
        super(InfiniteThread, self).__init__()
        self.is_running = True
        self.frequency = frequency
        self.no_sleep = no_sleep

    def run(self):
        while self.is_running:
            if not self.no_sleep:
                time.sleep(1.0 / self.frequency)

            self.update_trigger.emit()


class TaskProgressThread(QtCore.QThread):
    update_trigger = QtCore.pyqtSignal(float, int, int)
    on_finished = QtCore.pyqtSignal(int, int, int)

    def __init__(self, idx, row, num):
        super(TaskProgressThread, self).__init__()
        self.is_running = True
        self.target_shape_index = idx
        self.thread_num = num
        self.row = row

    def run(self):
        timer = QtCore.QTime()

        timer.start()

        while timer.elapsed() < 1000:
            self.update_trigger.emit(timer.elapsed() / 49 * 5, self.target_shape_index, self.row)

            time.sleep(1.0 / 33.0)

        self.on_finished.emit(self.target_shape_index, self.row, self.thread_num)
        self.finished.emit()


class AnimationThread(QtCore.QThread):
    update_trigger = QtCore.pyqtSignal()
    animation_start = QtCore.pyqtSignal(QtCore.QPropertyAnimation)
    on_finished = QtCore.pyqtSignal(int, int)

    def __init__(self, file_index, num, file_icon_widget, path_index, full_path, animation_time, v, looped, is_composite_anim=False, composite_steps=3):
        super(AnimationThread, self).__init__()

        self.is_running = False
        self.is_paused = False

        self.file_index = file_index
        self.num = num

        self.file_icon_widget = file_icon_widget
        self.animation = QtCore.QPropertyAnimation(file_icon_widget, b'posi')
        self.animation.finished.connect(self.on_stop)
        self.animation.setDuration(animation_time)
        self.looped = looped

        self.is_composite_anim=is_composite_anim
        self.composite_steps = composite_steps

        qpath = QtGui.QPainterPath()

        if self.looped:
            self.animation.setLoopCount(-1)

            path = full_path[path_index:] + full_path[:path_index]

            qpath.moveTo(QtCore.QPointF(path[0][0], path[0][1]))

            for i in range(1, len(path)):
                qpath.lineTo(QtCore.QPointF(path[i][0], path[i][1]))

            for i in [p / 100 for p in range(0, 101)]:
                self.animation.setKeyValueAt(i, qpath.pointAtPercent(i))

            self.animation.setStartValue(QtCore.QPointF(path[0][0], path[0][1]))
            self.animation.setEndValue(QtCore.QPointF(path[-1][0], path[-1][1]))

        if self.is_composite_anim:
            qpath.moveTo(QtCore.QPointF(full_path[path_index:][0][0],
                                        full_path[path_index:][0][1]))
            # build original path

            keyframes = [
                QtCore.QPointF(full_path[24][0], full_path[24][1] - 150),
                QtCore.QPointF(full_path[49][0], full_path[49][1]),
                QtCore.QPointF(full_path[74][0], full_path[74][1] + 50),
            ]

            for i in range(1, len(full_path[path_index:])):
                qpath.lineTo(QtCore.QPointF(full_path[path_index:][i][0],
                                            full_path[path_index:][i][1]))

            self.animation.setKeyValueAt(0, qpath.pointAtPercent((0)))
            self.animation.setKeyValueAt(1, qpath.pointAtPercent((1)))


            for i in range(0, self.composite_steps):
                start_frame = (i * 1/composite_steps + .01)
                stop_frame =  ((i+1) * 1/composite_steps - .001)
                #point = qpath.pointAtPercent((i+1)*0.25)
                #point.setY(point.y() - 50)
                self.animation.setKeyValueAt(start_frame, keyframes[i])
                self.animation.setKeyValueAt(stop_frame, keyframes[i])
            print(self.animation.keyValues())

            #for i in [p / 100 for p in range(0, 101)]:
            #     self.animation.setKeyValueAt(i, qpath.pointAtPercent(i))

            self.animation.setStartValue(QtCore.QPointF(full_path[path_index:][0][0], full_path[path_index:][0][1]))
            self.animation.setEndValue(QtCore.QPointF(full_path[path_index:][-1][0] + v[0], full_path[path_index:][-1][1] + v[1]))

        else:
            qpath.moveTo(QtCore.QPointF(full_path[path_index:][0][0],
                                        full_path[path_index:][0][1]))

            for i in range(1, len(full_path[path_index:])):
                qpath.lineTo(QtCore.QPointF(full_path[path_index:][i][0],
                                            full_path[path_index:][i][1]))

            for i in [p / 100 for p in range(0, 101)]:
                self.animation.setKeyValueAt(i, qpath.pointAtPercent(i))

            self.animation.setStartValue(QtCore.QPointF(full_path[path_index:][0][0], full_path[path_index:][0][1]))
            self.animation.setEndValue(QtCore.QPointF(full_path[path_index:][-1][0] + v[0], full_path[path_index:][-1][1] + v[1]))

    def run(self):
        self.is_running = True
        self.is_paused = False

        self.animation_start.emit(self.animation)

        while self.is_running:
            self.update_trigger.emit()
            time.sleep(0.034)


        self.on_finished.emit(self.num, self.file_index)
        self.finished.emit()

    def pause(self):
        self.is_paused = True
        self.animation.pause()

    def resume(self):
        self.is_paused = False
        self.animation.resume()

    def stop(self):
        self.on_finished.emit(self.num, self.file_index)
        self.finished.emit()

    def on_stop(self):
        self.is_running = False

        self.animation.setEndValue(QtCore.QPointF(self.file_icon_widget.x() + self.file_icon_widget.width() / 2, self.file_icon_widget.y() + self.file_icon_widget.height() / 2))
        self.animation.setDuration(0)
        self.animation.stop()
