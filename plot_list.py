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
        self.hover = QModelIndex()
    
    def sizeHint(self, option, index):
        return QSize(24, 24)

    def paint(self, painter, option, index):
        # Load data from index.
        equation = index.data(ROLE_EQUATION)
        color = index.data(ROLE_COLOR)
        button_state = index.data(ROLE_BUTTON_STATE)
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
        painter.drawRect(bounds.x(), bounds.y(), 12, bounds.height())
        
        painter.restore()
        
        # Write out the equation.
        text_bounds = font_metrics.boundingRect(equation)
        text_point = QPointF(
            bounds.x() + 20,
            bounds.y() + (bounds.height() - text_bounds.y()) / 2
        )
        painter.drawText(text_point, equation)

        # Draw the delete button.
        button = QStyleOptionButton()
        if button_state == STATE_HOVER:
            button.state |= QStyle.State_MouseOver
        if button_state == STATE_DOWN:
            button.state |= QStyle.State_Sunken
        button.state |= QStyle.State_Enabled
        button.rect = QRect(
            bounds.width() - 15, bounds.y() - 1,
            16, bounds.height() + 2
        )
        button.text = u"\u00D7"
        QApplication.style().drawControl(QStyle.CE_PushButton, button, painter)

    def editorEvent(self, event, model, option, index):
        state = {
            QEvent.MouseMove: STATE_HOVER,
            QEvent.MouseButtonPress: STATE_DOWN,
            QEvent.MouseButtonDblClick: STATE_DOWN,
            QEvent.MouseButtonRelease: STATE_NORMAL
        }
        
        # If the event 
        if index != self.hover and self.hover.isValid():
            model.setData(self.hover, STATE_NORMAL, ROLE_BUTTON_STATE)
        elif index.isValid():
            self.hover = index
        else:
            self.hover = QModelIndex()

        if index.isValid():
            if event.type() == QEvent.MouseMove:
                pass  # Check if mouse in button rect.
            model.setData(index, state[event.type()], ROLE_BUTTON_STATE)
        
        return super(PlotListDelegate, self).editorEvent(
            event, model, option, index)
