import os
import csv
import sys
from typing import List, Dict
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget
from articleinfo import ArticleInfo
import articleinfo
#from PyQt5.QtCore import pyqtSlot


## this takes output from analyser and displays it for editing

class MWindow(QWidget):
    def __init__(self, parent : QWidget = None) -> None:
        super().__init__(parent)
        
        try:
            self.outfile = open("tagged_final.csv", 'w', newline='')
        except OSError:
            print("Failed to open dest. file")
            sys.exit(-1)
       
        self.output = csv.writer(self.outfile, delimiter=';', quoting=csv.QUOTE_ALL, strict=True)
        
        self.short = QShortcut(QtGui.QKeySequence("Ctrl+N"), self)
        self.short.activated.connect(self.next)
        
        self.w_dict : Dict[str, QWidget] = None
    
    def dest(self):
        self.outfile.close()
     
    @QtCore.pyqtSlot()
    def next(self):
        print("aaaa")
        self.write_output_line()
        pass 
    
    def write_output_line(self):
        print(self.w_dict["url"].text())
        #self.output.writerow([d["url"]])
        pass
    
    def init_right_textboxes(self, r : QLayout, l : List[QWidget], n : List[str], d : Dict[str, QWidget]):
        #generic_article = ArticleInfo("a", 'December 28, 2023, 03:06PM\0', "b", "c", "d")    
        #generic_article.setdate(datetime(2022, 6, 12, 12, 34))

        generic_article = articleinfo.GenericArticle()

        i=0

        #print(vars(generic_article))

        for field in vars(generic_article):

            # print(i)
            # print(field)

            cont = QWidget(self)
            cont_l = QHBoxLayout(cont)
            cont.setLayout(cont_l)
            
            cont.setContentsMargins(0,0,0,0)
            
            label = QLabel(cont)
            label.setText(field)
            
            

            if field in ["url", "loc_meta", "title",
                         "exact_location_of_accident", "area_of_accident", "is_place_of_accident_highway_or_expressway_or_water_or_other",
                         "is_reason_or_cause_for_the_accident_ploughed_or_ram_or_hit_or_collision_or_breakfail_or_others"]:
                widget = QLineEdit(cont)
            elif field in ["pub_meta", "accident_datetime_from_url"]:
                widget = QDateTimeEdit(cont)
            elif field in ["number_of_accidents_occured", "total_number_of_people_killed", "total_number_of_people_injured"]:
                widget = QSpinBox(cont)
            elif field in ["day_of_the_week_of_the_accident"]:
                cb = QComboBox(cont)
                cb.setEditable(True)
                cb.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
                for val in articleinfo.Weekday:
                    cb.addItem(val.__str__())
                widget = cb
            elif field in ["is_the_accident_data_yearly_monthly_or_daily"]: ## Accident data type
                cb = QComboBox(cont)
                cb.setEditable(True)
                cb.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
                for val in articleinfo.AccidentData:
                    cb.addItem(val.__str__())
                widget = cb
            elif field in ["division_of_accident", "district_of_accident", "subdistrict_or_upazila_of_accident"]: # divisions -> districts -> subdistricts 
                cb = QComboBox(cont)
                cb.setEditable(True)
                cb.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
                if field == "division_of_accident":
                    cb.addItems(ArticleInfo.list_divisions)
                elif field == "district_of_accident":
                    cb.addItems(ArticleInfo.list_districts)
                else:
                    cb.addItems(ArticleInfo.list_subdistricts)
                cb.addItem("<NA>")
                widget = cb
            elif field in ["is_country_bangladesh_or_other_country"]:
                cb = QCheckBox(cont)
                cb.setChecked(True)
                widget = cb
            elif field in ["available_ages_of_the_deceased"]:
                lw = QListWidget(cont)
                lw.setFlow(QListView.Flow.LeftToRight)
                item = QListWidgetItem("1", lw)
                item.setFlags(item.flags() | QtCore.Qt.ItemFlag.ItemIsEditable)
                lw.addItem(item)
                item = QListWidgetItem("2", lw)
                item.setFlags(item.flags() | QtCore.Qt.ItemFlag.ItemIsEditable)
                lw.addItem(item)
                lw.setMaximumHeight( 50 )
                lw.adjustSize()
                widget =lw
            elif field in ["primary_vehicle_involved", "secondary_vehicle_involved", "tertiary_vehicle_involved"]:
                cb = QComboBox(cont)
                cb.setEditable(True)
                cb.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
                for val in articleinfo.VechicleType:
                    cb.addItem(val.__str__())
                widget = cb
            elif field in ["is_type_of_accident_road_accident_or_train_accident_or_waterways_accident_or_plane_accident"]:
                cb = QComboBox(cont)
                cb.setEditable(True)
                cb.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
                for val in articleinfo.AccidentType:
                    cb.addItem(val.__str__())
                widget = cb
            elif field in ["any_more_vehicles_involved", "available_ages_of_the_deceased"]:
                i += 1
                continue
            else:
                i += 1
                continue
           
            
            
            
            cont_l.addWidget(label)
            cont_l.addWidget(widget)
            
            cont_l.setSpacing(2)
            
            r.addWidget(cont)
            
            l.append(widget)
            n.append(field)
            
            d[field] = widget

            i += 1
        pass

@QtCore.pyqtSlot()
def Say_Hello():
    print("ssss")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MWindow()
    w.show()
    
    w.setWindowTitle("Correcter")
    
    ml = QGridLayout(w)

    w.setLayout(ml)

    # title = QLabel(w)
    # ml.addWidget(title, 1, 1) 
    
    raw_text = QTextEdit(w)
    ml.addWidget(raw_text, 2, 1)

    rightside = QWidget(w)
    rightside_l = QVBoxLayout(rightside)
    
    rightside.setLayout(rightside_l)
    
    ml.addWidget(rightside, 1, 2, 2, 1)    

    rightside_l.setSpacing(0)
    rightside_l.setContentsMargins(0,0,0,0)

    widgets : List[QWidget] = []
    names : List[str] = []
    name_to_widget : Dict[str, QWidget] = {}
    w.init_right_textboxes(rightside_l, widgets, names, name_to_widget)
    
    w.w_dict = name_to_widget
    
    for i in range(0, names.__len__()):
        print(names[i], "->", type(widgets[i]))
    
    btn_skip = QPushButton("Skip", w)
    btn_next = QPushButton("Next", w)
    
    btn_next.clicked.connect(w.next)
     
    cont = QWidget(w)
    cont_l = QHBoxLayout(cont)
    cont.setLayout(cont_l)
    
    cont_l.addWidget(btn_skip)
    
    cont_l.addWidget(btn_next)
    
    rightside_l.addWidget(cont)
    
    w.showMaximized()

    ret : int = app.exec_()
   
    w.dest()
    
    sys.exit(ret)