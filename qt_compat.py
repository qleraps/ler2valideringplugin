# -*- coding: utf-8 -*-
"""
Qt5/Qt6 Compatibility Layer for QGIS plugins

This module provides compatibility between Qt5 (QGIS 3.4x) and Qt6 (QGIS 3.99+).
Import Qt classes and enums from this module instead of directly from PyQt.
"""

from qgis.PyQt.QtCore import Qt, QT_VERSION_STR
from qgis.PyQt.QtWidgets import QFrame, QTableWidget, QAbstractItemView

# Detect Qt version
QT_VERSION_MAJOR = int(QT_VERSION_STR.split('.')[0])
IS_QT6 = QT_VERSION_MAJOR >= 6


def get_qt_enum(enum_class, enum_name):
    """
    Get Qt enum value compatible with both Qt5 and Qt6.
    
    In Qt6, enums are scoped (e.g., Qt.AlignmentFlag.AlignCenter)
    In Qt5, enums are not scoped (e.g., Qt.AlignCenter)
    
    Args:
        enum_class: The enum class (e.g., Qt, QFrame)
        enum_name: The enum value name as string (e.g., 'AlignCenter')
    
    Returns:
        The enum value
    """
    # First try direct access (Qt5 style)
    if hasattr(enum_class, enum_name):
        return getattr(enum_class, enum_name)
    
    # For Qt6, we need to search in nested enum classes
    for attr_name in dir(enum_class):
        attr = getattr(enum_class, attr_name)
        if isinstance(attr, type) and hasattr(attr, enum_name):
            return getattr(attr, enum_name)
    
    raise AttributeError(f"Cannot find enum {enum_name} in {enum_class}")


# Qt.ItemDataRole enums
try:
    # Qt6 style
    Qt_UserRole = Qt.ItemDataRole.UserRole
except AttributeError:
    # Qt5 style
    Qt_UserRole = Qt.UserRole

# Qt.AlignmentFlag enums
try:
    # Qt6 style
    Qt_AlignRight = Qt.AlignmentFlag.AlignRight
    Qt_AlignLeft = Qt.AlignmentFlag.AlignLeft
    Qt_AlignCenter = Qt.AlignmentFlag.AlignCenter
    Qt_AlignVCenter = Qt.AlignmentFlag.AlignVCenter
    Qt_AlignHCenter = Qt.AlignmentFlag.AlignHCenter
    Qt_AlignTop = Qt.AlignmentFlag.AlignTop
    Qt_AlignBottom = Qt.AlignmentFlag.AlignBottom
except AttributeError:
    # Qt5 style
    Qt_AlignRight = Qt.AlignRight
    Qt_AlignLeft = Qt.AlignLeft
    Qt_AlignCenter = Qt.AlignCenter
    Qt_AlignVCenter = Qt.AlignVCenter
    Qt_AlignHCenter = Qt.AlignHCenter
    Qt_AlignTop = Qt.AlignTop
    Qt_AlignBottom = Qt.AlignBottom

# Qt.DockWidgetArea enums
try:
    # Qt6 style
    Qt_TopDockWidgetArea = Qt.DockWidgetArea.TopDockWidgetArea
    Qt_BottomDockWidgetArea = Qt.DockWidgetArea.BottomDockWidgetArea
    Qt_LeftDockWidgetArea = Qt.DockWidgetArea.LeftDockWidgetArea
    Qt_RightDockWidgetArea = Qt.DockWidgetArea.RightDockWidgetArea
except AttributeError:
    # Qt5 style
    Qt_TopDockWidgetArea = Qt.TopDockWidgetArea
    Qt_BottomDockWidgetArea = Qt.BottomDockWidgetArea
    Qt_LeftDockWidgetArea = Qt.LeftDockWidgetArea
    Qt_RightDockWidgetArea = Qt.RightDockWidgetArea

# Qt.GlobalColor enums
try:
    # Qt6 style
    Qt_white = Qt.GlobalColor.white
    Qt_black = Qt.GlobalColor.black
    Qt_red = Qt.GlobalColor.red
    Qt_green = Qt.GlobalColor.green
    Qt_blue = Qt.GlobalColor.blue
except AttributeError:
    # Qt5 style
    Qt_white = Qt.white
    Qt_black = Qt.black
    Qt_red = Qt.red
    Qt_green = Qt.green
    Qt_blue = Qt.blue

# QFrame.Shape enums
try:
    # Qt6 style
    QFrame_StyledPanel = QFrame.Shape.StyledPanel
    QFrame_NoFrame = QFrame.Shape.NoFrame
    QFrame_Box = QFrame.Shape.Box
    QFrame_Panel = QFrame.Shape.Panel
except AttributeError:
    # Qt5 style
    QFrame_StyledPanel = QFrame.StyledPanel
    QFrame_NoFrame = QFrame.NoFrame
    QFrame_Box = QFrame.Box
    QFrame_Panel = QFrame.Panel

# QFrame.Shadow enums
try:
    # Qt6 style
    QFrame_Raised = QFrame.Shadow.Raised
    QFrame_Sunken = QFrame.Shadow.Sunken
    QFrame_Plain = QFrame.Shadow.Plain
except AttributeError:
    # Qt5 style
    QFrame_Raised = QFrame.Raised
    QFrame_Sunken = QFrame.Sunken
    QFrame_Plain = QFrame.Plain

# QTableWidget/QAbstractItemView SelectionBehavior enums
try:
    # Qt6 style
    QTableWidget_SelectRows = QAbstractItemView.SelectionBehavior.SelectRows
    QTableWidget_SelectColumns = QAbstractItemView.SelectionBehavior.SelectColumns
    QTableWidget_SelectItems = QAbstractItemView.SelectionBehavior.SelectItems
except AttributeError:
    # Qt5 style
    QTableWidget_SelectRows = QAbstractItemView.SelectRows
    QTableWidget_SelectColumns = QAbstractItemView.SelectColumns
    QTableWidget_SelectItems = QAbstractItemView.SelectItems

# QTableWidget/QAbstractItemView EditTriggers enums
try:
    # Qt6 style
    QTableWidget_NoEditTriggers = QAbstractItemView.EditTrigger.NoEditTriggers
    QTableWidget_DoubleClicked = QAbstractItemView.EditTrigger.DoubleClicked
    QTableWidget_AllEditTriggers = QAbstractItemView.EditTrigger.AllEditTriggers
except AttributeError:
    # Qt5 style
    QTableWidget_NoEditTriggers = QAbstractItemView.NoEditTriggers
    QTableWidget_DoubleClicked = QAbstractItemView.DoubleClicked
    QTableWidget_AllEditTriggers = QAbstractItemView.AllEditTriggers

# QAction compatibility - moved from QtWidgets to QtGui in Qt6
try:
    from qgis.PyQt.QtGui import QAction
except ImportError:
    from qgis.PyQt.QtWidgets import QAction
