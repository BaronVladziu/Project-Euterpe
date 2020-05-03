#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets


class PictureLabel(QtWidgets.QLabel):
    def __init__(self, picture_path:str, parent=None):
        super(PictureLabel, self).__init__(parent)
        self.act_pixmap = QtGui.QPixmap(picture_path)
        self.pixmap_path = picture_path
        self.setPixmap(self.act_pixmap)
        self.setMouseTracking(True)

        self.if_active = False
        self.press_event = None
        self.move_event = None

    def set_move_event(self, method):
        self.move_event = method

    def set_press_event(self, method):
        self.press_event = method

    def mouseMoveEvent(self, event):
        if self.if_active:
            # Get original picture
            self.act_pixmap = QtGui.QPixmap(self.pixmap_path)

            # Draw main cursor
            x = event.x()
            painter = QtGui.QPainter(self.act_pixmap)
            painter.setPen(
                QtGui.QPen(QtCore.Qt.blue, 1, QtCore.Qt.SolidLine)
            )
            painter.drawLine(
                QtCore.QPoint(x, 0),
                QtCore.QPoint(x, self.act_pixmap.height())
            )

            # Update picture
            self.setPixmap(self.act_pixmap)
            del painter

            # Actvate move_event
            if self.move_event is not None:
                self.move_event(event.x(), event.y())

    def mark_max_error(self, x:float, max_error:float):
        # Draw secondary cursors
        painter = QtGui.QPainter(self.act_pixmap)
        painter.setPen(
            QtGui.QPen(QtCore.Qt.cyan, 1, QtCore.Qt.SolidLine)
        )
        painter.drawLine(
            QtCore.QPoint(x-max_error, 0),
            QtCore.QPoint(x-max_error, self.act_pixmap.height())
        )
        painter.drawLine(
            QtCore.QPoint(x+max_error, 0),
            QtCore.QPoint(x+max_error, self.act_pixmap.height())
        )

        # Update picture
        self.setPixmap(self.act_pixmap)


    def mousePressEvent(self, event):
        if self.if_active:
            # Actvate press_event
            if self.press_event is not None:
                self.press_event(event.x(), event.y())

    def mark_answer(self, if_correct:bool, x:float):
        painter = QtGui.QPainter(self.act_pixmap)
        if if_correct:
            painter.setPen(
                QtGui.QPen(QtCore.Qt.green, 1, QtCore.Qt.SolidLine)
            )
        else:
            painter.setPen(
                QtGui.QPen(QtCore.Qt.red, 1, QtCore.Qt.SolidLine)
            )
        painter.drawLine(
            QtCore.QPoint(x, 0),
            QtCore.QPoint(x, self.act_pixmap.height())
        )
        self.setPixmap(self.act_pixmap)
        self.if_active = False
