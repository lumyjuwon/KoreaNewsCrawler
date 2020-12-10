from PyQt5.QtWidgets import * #QApplication, QWidget, QLabel, QTextEdit
from PyQt5.QtCore import QThread
from korea_news_crawler.articlecrawler import ArticleCrawler
import sys

Crawler = ArticleCrawler()

class gui(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.set_done = False
        self.shown = False

    def initUI(self):
        label0 = QLabel('크롤러를 설정해주세요.', self)
        label0.move(50, 30)
        font0 = label0.font()
        font0.setBold(True)
        font0.setPointSize(14)
        label0.setFont(font0)

        self.rbtn1 = QRadioButton('카테고리별 크롤링', self)
        self.rbtn1.setChecked(True)
        self.rbtn1.move(50, 70)
        self.rbtn1.clicked.connect(self.onClicked)

        self.catLabel = QLabel('1. 정치  2. 경제  3. 사회  4. 생활문화  5. 세계  6. IT과학  7. 오피니언', self)
        self.catLabel.move(50, 100)

        self.selectLabel1 = QLabel('카테고리 선택 : ', self)
        self.selectLabel1.move(50, 130)
        self.catEdit = QLineEdit(self)
        self.catEdit.move(180, 128)
        self.catEdit.textChanged[str].connect(self.catChanged)

        self.timeLabel1 = QLabel('시작 년도: ', self)
        self.timeEdit1 = QLineEdit(self)
        self.timeLabel2 = QLabel('시작 월: ', self)
        self.timeEdit2 = QLineEdit(self)
        self.timeLabel3 = QLabel('끝 년도: ', self)
        self.timeEdit3 = QLineEdit(self)
        self.timeLabel4 = QLabel('끝 월: ', self)
        self.timeEdit4 = QLineEdit(self)
        self.timeLabel1.move(50, 160)
        self.timeEdit1.move(140, 158)
        self.timeLabel2.move(360, 160)
        self.timeEdit2.move(440, 158)
        self.timeLabel3.move(50, 190)
        self.timeEdit3.move(140, 188)
        self.timeLabel4.move(360, 190)
        self.timeEdit4.move(440, 188)

        self.timeEdit1.textChanged[str].connect(self.timeChanged1)
        self.timeEdit2.textChanged[str].connect(self.timeChanged2)
        self.timeEdit3.textChanged[str].connect(self.timeChanged3)
        self.timeEdit4.textChanged[str].connect(self.timeChanged4)

        self.btn1 = QPushButton(self)
        self.btn1.setText('크롤링 시작')
        self.btn1.move(50, 225)
        self.btn1.clicked.connect(self.btn1Clicked)

        self.option1 = [self.selectLabel1, self.catLabel, self.catEdit, self.timeLabel1, self.timeLabel2,
                        self.timeLabel3, self.timeLabel4, \
                        self.timeEdit1, self.timeEdit2, self.timeEdit3, self.timeEdit4, self.btn1]

        self.resize(700, 300)
        self.setWindowTitle("뉴스 기사 크롤링")
        self.show()

    def onClicked(self):
        if self.rbtn1.isChecked():
            for option in self.option2:
                option.hide()
            for option in self.option1:
                option.show()
            for option in self.option3:
                option.hide()
            for option in self.option4:
                option.hide()
            self.pbar.show()
            self.pbar.setGeometry(50, 270, 400, 30)

    def catChanged(self, num):
        if num:
            self.cat = int(num)

    def timeChanged1(self, num):
        if num:
            self.startYear = int(num)

    def timeChanged2(self, num):
        if num:
            self.startMonth = int(num)

    def timeChanged3(self, num):
        if num:
            self.endYear = int(num)

    def timeChanged4(self, num):
        if num:
            self.endMonth = int(num)

    def btn1Clicked(self):
        if self.cat == 1:
            ss1 = "정치"
        if self.cat == 2:
            ss1 = "경제"
        if self.cat == 3:
            ss1 = "사회"
        if self.cat == 4:
            ss1 = "생활문화"
        if self.cat == 5:
            ss1 = "세계"
        if self.cat == 6:
            ss1 = "IT과학"
        if self.cat == 7:
            ss1 = "오피니언"
        self.set_done = True

        Crawler.set_category(ss1)
        Crawler.set_date_range(self.startYear, self.startMonth, self.endYear, self.endMonth)
        x = crawler1(self)
        x.start()

class crawler1(QThread):
    def run(self):
        Crawler.start()

def Crawl_With_Gui():
    app = QApplication(sys.argv)
    w = gui()
    app.exec_()

if __name__ == "__main__":
    Crawl_With_Gui()