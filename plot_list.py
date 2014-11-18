"""Argand Diagram Plotter

plot_list_delegate.py - Implements view and model classes
                        for the list in the plots dialog.

Written by Sam Hubbard - samlhub@gmail.com
"""

from PyQt4.QtGui import *
from PyQt4.QtCore import *


ICON_ROLE = Qt.UserRole
HEADER_ROLE = Qt.UserRole + 1
FOOTER_ROLE = Qt.UserRole + 2


class PlotListModel(QStandardItemModel):
    def __init__(self):
        super(PlotListModel, self).__init__()
        item = QStandardItem()
        icon = QIcon("img/logo16.png")
        item.setData(icon, ICON_ROLE)
        item.setData("Inbox", HEADER_ROLE)
        item.setData("BLOB", FOOTER_ROLE)
        self.appendRow(item)


class PlotListDelegate(QStyledItemDelegate):
    def __init__(self):
        super(PlotListDelegate, self).__init__()
    
    def paint(self, painter, option, index):
        super(PlotListDelegate, self).paint(painter, option, index)
        painter.save()
        icon = index.data(ICON_ROLE)
        painter.drawPixmap(0, 0, icon.pixmap(16, 16))
        painter.restore()
