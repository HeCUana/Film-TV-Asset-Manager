from enum import Enum
from PyQt6.QtWidgets import QWidget,QApplication,QPushButton,QFrame,QHBoxLayout
import sys
from qfluentwidgets import StyleSheetBase, Theme, isDarkTheme, qconfig,PushButton
from qfluentwidgets import NavigationItemPosition, FluentWindow, SubtitleLabel, setFont

# class StyleSheet(StyleSheetBase, Enum):
#     """ Style sheet  """

#     WINDOW = "window"

#     def path(self, theme=Theme.AUTO):
#         theme = qconfig.theme if theme == Theme.AUTO else theme
#         return f"qss/{theme.value.lower()}/{self.value}.qss"

class Widget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)

class Window(FluentWindow):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.W1 = Widget("W1",self)
        self.addSubInterface(self.W1, None, 'Home')
    def initWindow(self):
        self.resize(900, 700)
        self.setWindowTitle('Windows')
    # def initUI(self)

    #     self.setToolTip('This is a <b>QWidget</b> widget')

    #     btn = QPushButton('Button', self)
    #     btn.setToolTip('This is a <b>QPushButton</b> widget')
    #     btn.resize(btn.sizeHint())
    #     btn.move(50, 50)

    #     self.setGeometry(300, 300, 300, 200)
    #     self.setWindowTitle('Tooltips')
    #     self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    w = QWidget()
    w.resize(250, 200)
    w.move(300, 300)
    window.show()
    app.exec()
