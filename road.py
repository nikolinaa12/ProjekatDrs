from PyQt5.QtWidgets import QGraphicsScene, QGraphicsRectItem, QGraphicsView, QPushButton
from PyQt5.QtGui import QBrush
from PyQt5.QtCore import Qt
from car import Car

LINE_COUNT = 5
LINE_W = 20
LINE_H = 120
ROAD_SPEED = 10  # px/frame

class Road(QGraphicsView):
    def __init__(self, parent):
        QGraphicsView.__init__(self, parent=parent)
        
        self.stopGameButton = QPushButton("X")
        self.stopGameButton.hide()
        self.stopGameButton.setFixedWidth(30)
        self.stopGameButton.setFixedHeight(30)
        self.stopGameButton.setGeometry(0,0,0,0)
        self.stopGameButton.clicked.connect(parent.stop)
        
        self.scene = QGraphicsScene(self)
        self.makeRoad(parent)        
        self.scene.addWidget(self.stopGameButton)
        self.setScene(self.scene)
        
    def makeRoad(self, parent):
        self.line_space = (parent.height() / (LINE_COUNT-2)) - LINE_H
        
        bg = QGraphicsRectItem()
        bg.setRect(0, 0, parent.width(), parent.height())
        bg.setBrush(QBrush(Qt.gray))
        self.scene.addItem(bg)
        
        self.lines = []
        self.topLineIndex = 0
        ax = (parent.width()/2) - (LINE_W/2)
        
        for i in range(LINE_COUNT):
            line = QGraphicsRectItem()
            ay = (i-1)*(LINE_H + self.line_space)
            line.setRect(0, 0, LINE_W, LINE_H)
            line.setPos(ax, ay)
            line.setBrush(QBrush(Qt.white))
            self.scene.addItem(line)
            self.lines.append(line)
        
        """ Because of the lines, the scene isn't in the middle """
        """ So we add an extra rectangle to center the scene """
        spaceFill = QGraphicsRectItem()
        ay = (LINE_COUNT-1)*(LINE_H + self.line_space) - self.line_space
        spaceFill.setRect(ax, ay, LINE_W, self.line_space)
        self.scene.addItem(spaceFill)
        
        self.setFixedSize(parent.width(), parent.height())
        
    def gameUpdate(self, parent):
        index = 0
        for line in self.lines:
            line.setPos(line.x(), line.y() + ROAD_SPEED)
            if line.y() > parent.height():
                line.setPos(line.x(), self.lines[self.topLineIndex].y() - self.line_space - LINE_H)
                self.topLineIndex = index
            index += 1
    
    # Disable scrolling window with wheel
    def wheelEvent(self, event):
        event.ignore()