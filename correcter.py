import os
import csv
import sys
from typing import List
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from articleinfo import ArticleInfo


## this takes output from analyser and displays it for editing



def init_meta(w : QWidget, r: QLayout):
    for i in range(0,5):
        cont = QWidget(w)
        cont_l = QHBoxLayout(cont)
        cont.setLayout(cont_l)
        
        label = QLabel(cont)
    

def init_right_textboxes(w : QWidget ,r : QLayout, l : List[QWidget]):
    generic_article = ArticleInfo("a", 'December 28, 2023, 03:06 am', "b", "c", "d")    
    i=0
    for field in vars(generic_article):
        
        cont = QWidget(w)
        cont_l = QHBoxLayout(cont)
        cont.setLayout(cont_l)

        label = QLabel(cont)
        label.setText(field)
        
        if i in [0,2,3,4,7,8,9,10,11,12,13]:
            widget = QLineEdit(cont)
        elif i in [1, 24]:
            widget = QDateTimeEdit(cont)
        elif i in [5, 16, 17]:
            widget = QSpinBox(cont)
        elif i in [6, 14, 15, 18, 19, 20, 21, 22, 23]:
            continue
        
        cont_l.addWidget(label)
        cont_l.addWidget(widget)
        r.addWidget(cont)
        
        l += widget
        
        i += 1
    
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

    widgets : List[QWidget] = []
    
    init_right_textboxes(w, rightside_l, widgets)
    
    sys.exit(app.exec_())