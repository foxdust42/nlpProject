import os
import csv
import sys
from typing import List
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from articleinfo import ArticleInfo


## this takes output from analyser and displays it for editing

def init_right_textboxes(w : QWidget ,r : QLayout, l : List[QWidget]):
    cont = QWidget(w)
    cont_l = QHBoxLayout(cont)
    cont.setLayout(cont_l)
    
    label = QLabel(cont)
    
    label.setText("Test")
    
    box = QLineEdit(cont)
    
    box.setText("adknaoidnasod")
    box.setEnabled(False)
    box.setStyleSheet(":disabled{ color: white; background-color : black;}")
    cont_l.addWidget(label)
    cont_l.addWidget(box) 
    
    r.addWidget(cont)
    pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = QWidget()
    
    w.setWindowTitle("Correcter")
    w.show()
    
    ml = QGridLayout(w)

    w.setLayout(ml)

    title = QLabel(w)
    ml.addWidget(title, 1, 1) 
    
    raw_text = QTextEdit(w)
    ml.addWidget(raw_text, 2, 1)

    rightside = QWidget(w)
    rightside_l = QVBoxLayout(rightside)
    
    rightside.setLayout(rightside_l)
    
    ml.addWidget(rightside, 1, 2, 2, 1)    

    init_right_textboxes(w, rightside_l)
    
    sys.exit(app.exec_())