import sys
from abc import ABCMeta, abstractmethod

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class UIEvent(metaclass=ABCMeta):
    @abstractmethod
    def to_do(self, **kwargs):
        pass


class MainWidget(QWidget):
    _MAX_CONF_COUNT = 4

    def __init__(self,
                 x: int,
                 y: int,
                 width: int,
                 height: int,
                 version: float,
                 events: dict = None,
                 img_w: int = 640,
                 img_h: int = 640):
        super().__init__()
        self.lb_title = QLabel(f'MetaArtClient v{version:.2f}', self)
        self.lb_result = QLabel(self)
        self.lb_images = QLabel('images')
        self.led_input = QLineEdit(self)
        self.sld_images = QSlider(Qt.Horizontal, self)
        self.btn_test = QPushButton('Test', self)
        self.btn_go = QPushButton('Go', self)
        self.btn_save = QPushButton('Save', self)
        self.font = {'h1': QFont('Monaco', 48, QFont.Bold),
                     'h2': QFont('Monaco', 36, QFont.Bold),
                     'h3': QFont('D2Coding', 24, QFont.DemiBold),
                     'h4': QFont('D2Coding', 12)}
        self._res_wh = (img_w, img_h)
        self.event_dict = events
        self._init_signal()
        self._init_ui(x, y, width, height)

    def _init_signal(self):
        if self.event_dict is not None:
            self.btn_test.clicked.connect(self.test_event)
            self.btn_go.clicked.connect(self.go_event)
            self.btn_save.clicked.connect(self.save_event)

    def _init_ui(self, x, y, width, height):
        # 전체 Font 초기화
        self.lb_title.setFont(self.font['h1'])
        self.lb_images.setFont(self.font['h3'])
        self.btn_go.setFont(self.font['h3'])
        self.btn_test.setFont(self.font['h3'])
        self.btn_save.setFont(self.font['h3'])
        self.led_input.setFont(self.font['h4'])
        # 결과창 초기화
        self.lb_result.setFixedWidth(self._res_wh[0])
        self.lb_result.setFixedHeight(self._res_wh[1])
        # 설정창 초기화
        hbox_conf = QHBoxLayout()
        self.sld_images.setTickPosition(QSlider.TicksBelow)
        self.sld_images.setRange(1, 4)
        self.sld_images.setSingleStep(1)
        hbox_conf.addWidget(self.lb_images)
        hbox_conf.addWidget(self.sld_images)
        # 연결창 초기화
        hbox_comm = QHBoxLayout()
        hbox_comm.addStretch(1)
        hbox_comm.addWidget(self.btn_test)
        hbox_comm.addWidget(self.btn_go)
        hbox_comm.addWidget(self.btn_save)
        # 메인 화면 초기화
        vbox_main = QVBoxLayout()
        vbox_main.addWidget(self.lb_title)
        vbox_main.addWidget(self.led_input)
        vbox_main.addWidget(self.lb_result)
        vbox_main.addLayout(hbox_conf)
        vbox_main.addLayout(hbox_comm)
        # 전체 초기화
        self.setLayout(vbox_main)
        self.setGeometry(x, y, width, height)
        self.show()

    def test_event(self):
        if 'test' in self.event_dict:
            event = self.event_dict['test']
            assert isinstance(event, UIEvent)
            event.to_do()

    def go_event(self):
        if 'go' in self.event_dict:
            text = self.led_input.text()
            cnt = self.sld_images.value()
            event = self.event_dict['go']
            assert isinstance(event, UIEvent)
            event.to_do(num_image=cnt, text=text)

    def save_event(self):
        if 'save' in self.event_dict:
            title = self.led_input.text().replace(' ', '_')
            event = self.event_dict['save']
            assert isinstance(event, UIEvent)
            event.to_do(title=title)


def init(x: int,
         y: int,
         width: int,
         height: int,
         version: float,
         events: dict = None):
    app = QApplication(sys.argv)
    form = MainWidget(x, y, width, height, version, events)
    sys.exit(app.exec_())


if __name__ == "__main__":
    class TestEvent(UIEvent):

        def to_do(self, **kwargs):
            print("test!")

    class GoEvent(UIEvent):

        def to_do(self, **kwargs):
            print(f"num_image={kwargs['num_image']}, text={kwargs['text']}")


    test_event, go_event = TestEvent(), GoEvent()
    init(10, 30, 1280, 800, 0.0, events={'test': test_event, 'go': go_event})
