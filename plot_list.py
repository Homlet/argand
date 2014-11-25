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
        self.itemDelegate().deleted_item.connect(self.clearSelection)
        self.installEventFilter(self)

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

    def eventFilter(self, object, event):
        if event.type() == QEvent.Leave:
            self.itemDelegate().mouseLeft(self.model())
        return False


class PlotListModel(QStandardItemModel):
    def __init__(self):
        super(PlotListModel, self).__init__()
    
    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled
    
    def append(self, plot):
        self.appendRow([plot, QStandardItem()])


class PlotListDelegate(QStyledItemDelegate):
    deleted_item = pyqtSignal()

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
        """Handles delete button logic."""
        if index.column() == COL_BUTTON:
            if index != self.hover:
                if self.hover.isValid():
                    model.setData(self.hover, STATE_NORMAL, ROLE_BUTTON_STATE)
                if index.isValid():
                    self.hover = index
                else:
                    self.hover = QModelIndex()

            next_state = {
                QEvent.MouseMove: STATE_HOVER,
                QEvent.MouseButtonPress: STATE_DOWN,
                QEvent.MouseButtonDblClick: STATE_DOWN}
            if index.isValid() and event.type() in next_state:
                # If the mouse is moved over the button while pressed, don't
                # revert to the hover state.
                if not (event.type() == QEvent.MouseMove
                   and  index.data(ROLE_BUTTON_STATE) == STATE_DOWN):
                    model.setData(index,
                        next_state[event.type()], ROLE_BUTTON_STATE)

            # If the button is released, delete the index from the model.
            if event.type() == QEvent.MouseButtonRelease \
            and index.data(ROLE_BUTTON_STATE) == STATE_DOWN:
                self.delete_item(model, index)

        return super(PlotListDelegate, self).editorEvent(
            event, model, option, index)

    def delete_item(self, model, index):
        """Deletes a single index from its parent model.
           Also resets the self.hover pointer just in case."""
        model.removeRow(index.row())
        self.hover = QModelIndex()
        self.deleted_item.emit()

    def mouseLeft(self, model):
        """Called when the mouse leaves the parent widget's viewport.
           Resets the self.hover pointer."""
        if self.hover.isValid():
            model.setData(self.hover, STATE_NORMAL, ROLE_BUTTON_STATE)
            self.hover = QModelIndex()
