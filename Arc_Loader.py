# ///////////////////////////////////////////////////////////////
# Developer: Mehdi Sameni
# Designer: Mehdi Sameni
# PyQt6
# Python 3.10
# ///////////////////////////////////////////////////////////////


from PyQt6.QtCore import QVariantAnimation, QEasingCurve, QSequentialAnimationGroup, QParallelAnimationGroup, Qt
from PyQt6.QtGui import QColor, QPainter, QPen
from PyQt6.QtWidgets import QFrame


# Class Arc Loader
class ArcLoader:
    def __init__(
            self,
            parent=None,
            spacer=0,
            startAngle=270,
            spanAngle=1/16,
            direction=True,
            duration=4000
            ):
        self.parent = parent
        self.spacer = spacer
        self.startAngle = startAngle
        self.fixedStartAngle = self.startAngle
        self.spanAngle = spanAngle
        self.direction = direction
        self.duration = duration

        self.clockWise = True
        self.antiClockWise = False

    # Make Rotation Animation
    def getRotationAnimation(self):
        animation = QVariantAnimation(self.parent)
        animation.setStartValue(self.spacer)
        animation.setEndValue(self.spacer+360*2)
        animation.setDuration(self.duration)
        animation.setEasingCurve(QEasingCurve.Type.OutInSine)
        animation.valueChanged.connect(self.updateSpacer)
        return animation

    # Make Span Angle Animation
    def getSpanAngleAnimation(self):
        animation = QVariantAnimation(self.parent)
        animation.setStartValue(1/16)
        animation.setEndValue(1/16+360)
        animation.setDuration(int(self.duration*.5))
        animation.finished.connect(self.animationFinished)
        animation.valueChanged.connect(self.updateSpanAngle)
        return animation

    # First Start Animation
    def getStartAngleAnimation(self):
        animation = QVariantAnimation(self.parent)
        animation.setStartValue(270)
        animation.setEndValue(270+360)
        animation.setDuration(int(self.duration*.5))
        animation.finished.connect(self.startAnimationFinished)
        animation.valueChanged.connect(self.updateStartAngle)
        return animation

    # Finished First Animation
    def startAnimationFinished(self):
        self.startAngle = 270
        self.fixedStartAngle = self.startAngle
        self.spanAngle = 1/16
        self.direction = not self.direction

    # Start All Animation
    def startAnimations(self):
        seqGroup = QSequentialAnimationGroup(self.parent)
        if self.direction:
            seqGroup.addAnimation(self.getSpanAngleAnimation())
            seqGroup.addAnimation(self.getStartAngleAnimation())
        else:
            seqGroup.addAnimation(self.getStartAngleAnimation())
            seqGroup.addAnimation(self.getSpanAngleAnimation())
        parGroup = QParallelAnimationGroup(self.parent)
        parGroup.addAnimation(self.getRotationAnimation())
        parGroup.addAnimation(seqGroup)
        parGroup.setLoopCount(10)
        parGroup.start()

    def animationFinished(self):
        self.direction = not self.direction

    def updateStartAngle(self, newValue):
        self.startAngle = newValue
        self.parent.update()

    def updateSpacer(self, newValue):
        self.spacer = newValue
        self.parent.update()
    
    def updateSpanAngle(self, newValue):
        self.spanAngle = newValue
        self.parent.update()


class UseArcLoader(QFrame):
    def __init__(
            self, 
            parent=None,
            color=QColor("#ffffff"),
            penWidth=20,
            diameter=150
            ):
        QFrame.__init__(self, parent=parent)

        try:
            print(f"{diameter=}")
            self.setFrameShape(QFrame.Shape.NoFrame)
            self.setFixedSize(diameter, diameter)
            self.color = color
            self.initPen(penWidth)

            self.arc1 = ArcLoader(self, 0, 270, 1/16, True, 4*1000)
            self.arc1.startAnimations()
        except Exception as e:
            print("[__init__]-", e)

    def calculateXR(self, level):
        x = self.pen.width()*level/2
        r = self.width()-self.pen.width()*level
        return x, r
    
    def draw(self):
        try:
            x, r = self.calculateXR(1)
            arc = self.arc1
            if arc.direction:
                spanAngle = arc.startAngle-arc.fixedStartAngle+arc.spanAngle
            else:
                spanAngle = 360-(arc.startAngle-arc.fixedStartAngle)
            if spanAngle < 1/16:
                spanAngle = 1/16
            self.painter.drawArc(int(x), int(x), int(r), int(r), -(arc.spacer+arc.startAngle)*16, int(-spanAngle*16))

            x, r = self.calculateXR(4)
            self.painter.drawArc(int(x), int(x), int(r), int(r), -(arc.spacer+arc.startAngle)*16, int((360-spanAngle)*16))
        except Exception as e:
            print("[draw]", e)

    def initPen(self, penWidth):
        try:
            self.pen = QPen()
            self.pen.setColor(self.color)
            self.pen.setWidth(penWidth)
            self.pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        except Exception as e:
            print("[initPen]", e)

    def paintEvent(self, e):
        try:
            self.painter = QPainter(self)
            self.painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            self.painter.setPen(self.pen)
            self.draw()
            self.painter.end()
        except Exception as e:
            print("[paintEvent]", e)

