#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets


class PictureLabel(QtWidgets.QLabel):
    def __init__(self, picture_path:str, parent=None, max_markers=1):
        super(PictureLabel, self).__init__(parent)
        self.act_pixmap = QtGui.QPixmap(picture_path)
        self.pixmap_path = picture_path
        self.setPixmap(self.act_pixmap)
        self.setMouseTracking(True)

        self.if_active = False
        self.left_click_event = None
        self.right_click_event = None
        self.move_event = None
        self.unerasable_markers = list()
        self.markers = list()
        self.max_markers = max_markers
        self.label_id = None

    def set_move_event(self, method, label_id=None):
        self.move_event = method
        self.label_id = label_id

    def set_left_click_event(self, method, label_id=None):
        self.left_click_event = method
        self.label_id = label_id

    def set_right_click_event(self, method, label_id=None):
        self.right_click_event = method
        self.label_id = label_id

    def reset(self):
        # Remove markers
        self.unerasable_markers = list()
        self.markers = list()

        # Reset picture
        self.act_pixmap = QtGui.QPixmap(self.pixmap_path)
        self.setPixmap(self.act_pixmap)
        
        # Enable interaction
        self.if_active = True
            
    def mouseMoveEvent(self, event):
        if self.if_active:
            # Prepare pixmap
            self.act_pixmap = QtGui.QPixmap(self.pixmap_path)

            # Draw markers
            painter = QtGui.QPainter(self.act_pixmap)
            for marker in self.markers:
                painter.setPen(
                    QtGui.QPen(QtCore.Qt.yellow, 1, QtCore.Qt.SolidLine)
                )
                painter.drawLine(
                    QtCore.QPoint(marker, 0),
                    QtCore.QPoint(marker, self.act_pixmap.height())
                )
            for marker in self.unerasable_markers:
                painter.setPen(
                    QtGui.QPen(QtCore.Qt.yellow, 1, QtCore.Qt.SolidLine)
                )
                painter.drawLine(
                    QtCore.QPoint(marker, 0),
                    QtCore.QPoint(marker, self.act_pixmap.height())
                )

            # Draw main cursor
            x = event.x()
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
                if self.label_id is not None:
                    self.move_event(event.x(), event.y(), self.label_id)
                else:
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

    def leaveEvent(self, event):
        if self.if_active:
            # Prepare pixmap
            self.act_pixmap = QtGui.QPixmap(self.pixmap_path)

            # Draw markers
            painter = QtGui.QPainter(self.act_pixmap)
            for marker in self.markers:
                painter.setPen(
                    QtGui.QPen(QtCore.Qt.yellow, 1, QtCore.Qt.SolidLine)
                )
                painter.drawLine(
                    QtCore.QPoint(marker, 0),
                    QtCore.QPoint(marker, self.act_pixmap.height())
                )
            for marker in self.unerasable_markers:
                painter.setPen(
                    QtGui.QPen(QtCore.Qt.yellow, 1, QtCore.Qt.SolidLine)
                )
                painter.drawLine(
                    QtCore.QPoint(marker, 0),
                    QtCore.QPoint(marker, self.act_pixmap.height())
                )

            # Update picture
            self.setPixmap(self.act_pixmap)
            del painter

    def mousePressEvent(self, event):
        if self.if_active:
            # Left click
            if event.button() == QtCore.Qt.LeftButton:
                # Actvate left_click_event
                if self.left_click_event is not None:
                    if self.label_id is not None:
                        self.left_click_event(event.x(), event.y(), self.label_id)
                    else:
                        self.left_click_event(event.x(), event.y())

            # Right click
            elif event.button() == QtCore.Qt.RightButton:
                # Actvate right_click_event
                if self.right_click_event is not None:
                    if self.label_id is not None:
                        self.right_click_event(event.x(), event.y(), self.label_id)
                    else:
                        self.right_click_event(event.x(), event.y())

    def add_unerasable_marker(self, x:float):
        # Add marker
        self.unerasable_markers.append(x)

        # Prepare pixmap
        self.act_pixmap = QtGui.QPixmap(self.pixmap_path)

        # Draw markers
        painter = QtGui.QPainter(self.act_pixmap)
        for marker in self.markers:
            painter.setPen(
                QtGui.QPen(QtCore.Qt.yellow, 1, QtCore.Qt.SolidLine)
            )
            painter.drawLine(
                QtCore.QPoint(marker, 0),
                QtCore.QPoint(marker, self.act_pixmap.height())
            )
        for marker in self.unerasable_markers:
            painter.setPen(
                QtGui.QPen(QtCore.Qt.yellow, 1, QtCore.Qt.SolidLine)
            )
            painter.drawLine(
                QtCore.QPoint(marker, 0),
                QtCore.QPoint(marker, self.act_pixmap.height())
            )

        # Update picture
        self.setPixmap(self.act_pixmap)
        del painter

    def mark_user_answer(self, x:float):
        if len(self.markers) + len(self.unerasable_markers) < self.max_markers:
            self.markers.append(x)

            # Prepare pixmap
            self.act_pixmap = QtGui.QPixmap(self.pixmap_path)

            # Draw markers
            painter = QtGui.QPainter(self.act_pixmap)
            for marker in self.markers:
                painter.setPen(
                    QtGui.QPen(QtCore.Qt.yellow, 1, QtCore.Qt.SolidLine)
                )
                painter.drawLine(
                    QtCore.QPoint(marker, 0),
                    QtCore.QPoint(marker, self.act_pixmap.height())
                )
            for marker in self.unerasable_markers:
                painter.setPen(
                    QtGui.QPen(QtCore.Qt.yellow, 1, QtCore.Qt.SolidLine)
                )
                painter.drawLine(
                    QtCore.QPoint(marker, 0),
                    QtCore.QPoint(marker, self.act_pixmap.height())
                )

            # Update picture
            self.setPixmap(self.act_pixmap)
            del painter

    def erase_user_answer(self, x:float, margin:float):
        # Erase all markers close to pressed point
        new_markers = list()
        for marker in self.markers:
            if x - margin > marker or marker > x + margin:
                new_markers.append(marker)
        self.markers = new_markers

        # Prepare pixmap
        self.act_pixmap = QtGui.QPixmap(self.pixmap_path)

        # Draw markers
        painter = QtGui.QPainter(self.act_pixmap)
        for marker in self.markers:
            painter.setPen(
                QtGui.QPen(QtCore.Qt.yellow, 1, QtCore.Qt.SolidLine)
            )
            painter.drawLine(
                QtCore.QPoint(marker, 0),
                QtCore.QPoint(marker, self.act_pixmap.height())
            )
        for marker in self.unerasable_markers:
            painter.setPen(
                QtGui.QPen(QtCore.Qt.yellow, 1, QtCore.Qt.SolidLine)
            )
            painter.drawLine(
                QtCore.QPoint(marker, 0),
                QtCore.QPoint(marker, self.act_pixmap.height())
            )

        # Update picture
        self.setPixmap(self.act_pixmap)
        del painter

    def mark_correct_answer(self, if_correct:bool, x:float):
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
