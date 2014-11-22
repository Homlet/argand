"""Argand Diagram Plotter

plot_list_delegate.py - Implements view and model class
                        for the list in the plots dialog.

Written by Sam Hubbard - samlhub@gmail.com
"""

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from plot import *


COL_EQUATION = 0
COL_BUTTON = 1

BUTTON_WIDTH = 34


class PlotListTable(QTableView):
    def __init__(self, model):
        super(PlotListTable, self).__init__()

        self.setModel(model)
        self.setItemDelegate(PlotListDelegate())
        self.itemDelegate().delete_item.connect(self.clearSelection)

        self.setShowGrid(False)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setVisible(False)

        self.horizontalHeader().setResizeMode(
            COL_EQUATION, QHeaderView.Stretch)
        self.horizontalHeader().setResizeMode(
            COL_BUTTON, QHeaderView.ResizeToContents)
        self.resizeColumnsToContents()

        self.viewport().setAttribute(Qt.WA_Hover, True)
        self.viewport().setMouseTracking(True)

        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)


class PlotListModel(QStandardItemModel):
    def __init__(self):
        super(PlotListModel, self).__init__()
    
    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled
    
    def append(self, plot):
        self.appendRow([plot, QStandardItem()])


class PlotListDelegate(QStyledItemDelegate):
    delete_item = pyqtSignal()

    def __init__(self):
        super(PlotListDelegate, self).__init__()
        self.hover = QModelIndex()
    
    def sizeHint(self, option, index):
        if index.column() == COL_EQUATION:
            return QSize(0, 24)
        if index.column() == COL_BUTTON:
            return QSize(BUTTON_WIDTH, 24)

    def paint(self, painter, option, index):
        # Load data from index.
        equation = index.data(ROLE_EQUATION)
        color = index.data(ROLE_COLOR)
        button_state = index.data(ROLE_BUTTON_STATE)
        bounds = option.rect
        bounds.adjust(0, 0, 0, -1)

        font = QApplication.font()
        font_metrics = QFontMetrics(font)
        

        if option.state & QStyle.State_Selected:
            # Highlight the row when selected.
            painter.save()
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(option.palette.highlight()))
            painter.drawRect(bounds)
            painter.restore()

            # Draw the delete button when row selected.
            if index.column() == COL_BUTTON:
                button = QStyleOptionButton()
                if button_state == STATE_HOVER \
                and option.state & QStyle.State_MouseOver:
                    button.state |= QStyle.State_MouseOver
                if button_state == STATE_DOWN:
                    button.state |= QStyle.State_Sunken
                button.state |= QStyle.State_Enabled
                button.rect = bounds
                button.text = u"\u00D7"
                QApplication.style().drawControl(
                    QStyle.CE_PushButton, button, painter)

        if index.column() == COL_EQUATION:
            # Draw the coloured block.
            painter.save()
            painter.setPen(Qt.NoPen)
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
        

    def editorEvent(self, event, model, option, index):
        if index.column() == COL_BUTTON:
            state = {
                QEvent.MouseMove: STATE_HOVER,
                QEvent.MouseButtonPress: STATE_DOWN,
                QEvent.MouseButtonDblClick: STATE_DOWN,
                QEvent.MouseButtonRelease: STATE_NORMAL
            }
            if index != self.hover:
                if self.hover.isValid():
                    model.setData(self.hover, STATE_NORMAL, ROLE_BUTTON_STATE)
                if index.isValid():
                    self.hover = index
                else:
                    self.hover = QModelIndex()

            if index.isValid() and event.type() in state:
                # If the mouse is moved over the button while pressed, don't
                # revert to the hover state.
                if not (event.type() == QEvent.MouseMove
                   and  index.data(ROLE_BUTTON_STATE) == STATE_DOWN):
                    model.setData(index,
                        state[event.type()], ROLE_BUTTON_STATE)

            if event.type() == QEvent.MouseButtonRelease:
                model.removeRow(index.row())
                self.delete_item.emit()

        return super(PlotListDelegate, self).editorEvent(
            event, model, option, index)
