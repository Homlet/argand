"""Argand Diagram Plotter

plot_list_delegate.py - Implements view and model class
                        for the list in the plots dialog.

Written by Sam Hubbard - samlhub@gmail.com
"""

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from plot import *


class PlotListModel(QStandardItemModel):
    def __init__(self):
        super(PlotListModel, self).__init__()
    
    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled


class PlotListDelegate(QStyledItemDelegate):
    def __init__(self):
        super(PlotListDelegate, self).__init__()
    
    def sizeHint(self, option, index):
        return QSize(24, 24)

    def paint(self, painter, option, index):
        # Load data from index.
        equation = index.data(EQUATION_ROLE)
        color = index.data(COLOR_ROLE)
        bounds = option.rect
        bounds.adjust(0, 0, 0, -1)
        
        size = self.sizeHint(option, index)
        font = QApplication.font()
        font_metrics = QFontMetrics(font)
        
        # Save so we can return to the previous pen.
        painter.save()
        painter.setPen(Qt.NoPen)
        
        if option.state & QStyle.State_Selected:
            painter.setBrush(QBrush(option.palette.highlight()))
            painter.drawRect(bounds)
        
        painter.setBrush(QBrush(color))
        painter.drawRect(bounds.x(), bounds.y(), 10, bounds.height())
        
        painter.restore()
        
        text_bounds = font_metrics.boundingRect(equation)
        text_point = QPointF(
            bounds.x() + 18,
            bounds.y() + (bounds.height() - text_bounds.y()) / 2
        )
        painter.drawText(text_point, equation)
