import os
import csv
import sys
from typing import List, Dict
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget
from articleinfo import ArticleInfo
from datetime import datetime
import articleinfo
#from PyQt5.QtCore import pyqtSlot


## this takes output from analyser and displays it for editing

class QBDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        value = index.data(QtCore.Qt.ItemDataRole.EditRole)
        if isinstance(value, PlainList):
            editor = QComboBox(parent)
            editor.setModel(value)
            editor.setEditable(True)
            editor.setCurrentIndex(value.currentIndex)
            # submit the data whenever the index changes
            editor.currentIndexChanged.connect(
                lambda: self.commitData.emit(editor))
        else:
            editor = super().createEditor(parent, option, index)
        return editor

    def setModelData(self, editor, model, index):
        if isinstance(editor, QComboBox):
            # the default implementation tries to set the text if the
            # editor is a combobox, but we need to set the index
            model.setData(index, editor.currentIndex())
        else:
            super().setModelData(editor, model, index)

class PlainList(QtCore.QAbstractListModel):
    currentIndex = 0
    def __init__(self, elements):
        super().__init__()
        self.elements = []
        for element in elements:
            if isinstance(element, (tuple, list)) and element:
                element = PlainList(element)
            self.elements.append(element)
        
    def data(self, index, role= QtCore.Qt.ItemDataRole.DisplayRole):
        if role == QtCore.Qt.ItemDataRole.EditRole:
            return self.elements[index.row()]
        elif role == QtCore.Qt.ItemDataRole.DisplayRole:
            value = self.elements[index.row()]
            if isinstance(value, PlainList):
                return value.elements[value.currentIndex]
            else:
                return value
    
    def get_elements(self):
        return self.elements
    
    def flags(self, index):
        flags = super().flags(index)
        if isinstance(index.data(QtCore.Qt.ItemDataRole.EditRole), PlainList):
            flags |= QtCore.Qt.ItemFlag.ItemIsEditable
        return flags

    def setData(self, index, value, role= QtCore.Qt.ItemDataRole.EditRole):
        if role == QtCore.Qt.ItemDataRole.EditRole:
            item = self.elements[index.row()]
            if isinstance(item, PlainList):
                item.currentIndex = value
            else:
                self.elements[index.row()] = value
        return True

    def delRow(self):
        if self.elements.__len__() > 0:
            self.elements.pop()
            
    
    def rowCount(self, parent=None):
        return len(self.elements)
    
    def append(self, elements):
        for element in elements:
            if isinstance(element, (tuple, list)) and element:
                element = PlainList(element)
            self.elements.append(element)


class MWindow(QWidget):
    def __init__(self, parent : QWidget = None) -> None:
        super().__init__(parent)
        
        self.ages_widget : QListWidget = None
        self.vechicles_widget : QListView = None
        self.raw_text : QWidget = None
        try:
            self.outfile = open("tagged_final.csv", 'w', newline='')
        except OSError:
            print("Failed to open dest. file")
            sys.exit(-1)
       
        self.output = csv.writer(self.outfile, delimiter=';', quoting=csv.QUOTE_ALL, strict=True)
       
        try:
            self.infile = open("tagged_unchecked.csv", 'r', newline='')
        except OSError:
            print("Failed to open input file")
            sys.exit(-1)
            
        self.input = csv.reader(self.infile, delimiter=';', quoting=csv.QUOTE_ALL, strict=True)

        title_row = self.input.__next__()
        print(title_row)
        
        self.short = QShortcut(QtGui.QKeySequence("Ctrl+N"), self)
        self.short.activated.connect(self.next)
        
        self.w_dict : Dict[str, QWidget] = None
    
    def dest(self):
        self.outfile.close()
    
    @QtCore.pyqtSlot()
    def skip(self):
        self.extract_vechicles()
     
    @QtCore.pyqtSlot()
    def next(self):
        #print("aaaa")
        self.write_output_line()
        self.load_line()
        pass 
    
    def extract_vechicles(self) -> List[str]:
        list = []
        for i in range(0, self.vechicles_widget.model().rowCount()):
            ind = self.vechicles_widget.model().createIndex(i, 0)
            list.append(self.vechicles_widget.model().data(ind))
        return list
    
    def extract_ages(self) -> List[str]:
        list = []
        for i in range(0, self.ages_widget.count()):
            list.append(self.ages_widget.item(i).text())
        return list
    
    def load_line(self):
        try:
            line = next(self.input)
        except StopIteration:
            print("All is done")
            QApplication.quit()
            return
        
        self.w_dict["url"].setText(line[0]),
        self.w_dict["pub_meta"].setDateTime(datetime.fromisoformat(line[1])),
        self.w_dict["loc_meta"].setText(line[2]),
        self.w_dict["title"].setText(line[3]),
        self.raw_text.setPlainText(line[4]),
        self.w_dict["number_of_accidents_occured"].setValue(int(line[5])),
        tmp = self.w_dict["is_the_accident_data_yearly_monthly_or_daily"].findText(line[6])
        if tmp == -1:
            self.w_dict["is_the_accident_data_yearly_monthly_or_daily"].setCurrentText(ArticleInfo.nullstring),
        else:
            self.w_dict["is_the_accident_data_yearly_monthly_or_daily"].setCurrentIndex(tmp)
             
        tmp = self.w_dict["day_of_the_week_of_the_accident"].findText(line[7])
        if tmp == -1:
            self.w_dict["day_of_the_week_of_the_accident"].setCurrentText(ArticleInfo.nullstring),
        else:
            self.w_dict["day_of_the_week_of_the_accident"].setCurrentIndex(tmp)
             
        self.w_dict["exact_location_of_accident"].text(),
        self.w_dict["area_of_accident"].text(),
        self.w_dict["division_of_accident"].currentText(),
        self.w_dict["district_of_accident"].currentText(),
        self.w_dict["subdistrict_or_upazila_of_accident"].currentText(),
        self.w_dict["is_place_of_accident_highway_or_expressway_or_water_or_other"].text(),
        self.w_dict["is_country_bangladesh_or_other_country"].text(),
        self.w_dict["is_type_of_accident_road_accident_or_train_accident_or_waterways_accident_or_plane_accident"].currentText(),
        self.w_dict["total_number_of_people_killed"].text(),
        self.w_dict["total_number_of_people_injured"].text(),
        self.w_dict["is_reason_or_cause_for_the_accident_ploughed_or_ram_or_hit_or_collision_or_breakfail_or_others"].text(),
        self.w_dict["primary_vehicle_involved"].currentText(),
        self.w_dict["secondary_vehicle_involved"].currentText(),
        self.w_dict["tertiary_vehicle_involved"].currentText(),
        self.extract_vechicles(), #self.w_dict["any_more_vehicles_involved"].text(),
        self.extract_ages(),#self.w_dict["available_ages_of_the_deceased"].text(),
        self.w_dict["accident_datetime_from_url"].text()
        
        pass
    
    def write_output_line(self):
        print(self.w_dict["url"].text())
        #self.output.writerow([d["url"]])

        out = [
            self.w_dict["url"].text(),
            self.w_dict["pub_meta"].text(),
            self.w_dict["loc_meta"].text(),
            self.w_dict["title"].text(),
            self.raw_text.toPlainText(),
            self.w_dict["number_of_accidents_occured"].text(),
            self.w_dict["is_the_accident_data_yearly_monthly_or_daily"].currentText(),
            self.w_dict["day_of_the_week_of_the_accident"].currentText(),
            self.w_dict["exact_location_of_accident"].text(),
            self.w_dict["area_of_accident"].text(),
            self.w_dict["division_of_accident"].currentText(),
            self.w_dict["district_of_accident"].currentText(),
            self.w_dict["subdistrict_or_upazila_of_accident"].currentText(),
            self.w_dict["is_place_of_accident_highway_or_expressway_or_water_or_other"].text(),
            self.w_dict["is_country_bangladesh_or_other_country"].text(),
            self.w_dict["is_type_of_accident_road_accident_or_train_accident_or_waterways_accident_or_plane_accident"].currentText(),
            self.w_dict["total_number_of_people_killed"].text(),
            self.w_dict["total_number_of_people_injured"].text(),
            self.w_dict["is_reason_or_cause_for_the_accident_ploughed_or_ram_or_hit_or_collision_or_breakfail_or_others"].text(),
            self.w_dict["primary_vehicle_involved"].currentText(),
            self.w_dict["secondary_vehicle_involved"].currentText(),
            self.w_dict["tertiary_vehicle_involved"].currentText(),
            self.extract_vechicles(), #self.w_dict["any_more_vehicles_involved"].text(),
            self.extract_ages(),#self.w_dict["available_ages_of_the_deceased"].text(),
            self.w_dict["accident_datetime_from_url"].text()
        ]
        print (out)
        self.output.writerow(out)
        pass
    
    @QtCore.pyqtSlot()
    def add_age(self):
        if self.ages_widget is None:
            return
        item = QListWidgetItem("10", self.ages_widget)
        item.setFlags(item.flags() | QtCore.Qt.ItemFlag.ItemIsEditable)
        self.ages_widget.addItem(item)
        
    @QtCore.pyqtSlot()
    def sub_age(self):
        if self.ages_widget is None:
            return
        selection = self.ages_widget.currentRow()
        self.ages_widget.takeItem(selection)
    
    @QtCore.pyqtSlot()
    def add_vechicle(self):
        if self.vechicles_widget is None:
            return
        self.vechicles_widget.model().append([[e.value for e in articleinfo.VechicleType]])
        self.vechicles_widget.setItemDelegate(QBDelegate(self.vechicles_widget.model()))
    
    @QtCore.pyqtSlot()
    def sub_vechicle(self):
        if self.vechicles_widget is None:
            return
        #for index in self.vechicles_widget.selectedIndexes():
        self.vechicles_widget.model().delRow()
            # self.vechicles_widget.model().removeRow(index.row())
        self.vechicles_widget.setItemDelegate(QBDelegate(self.vechicles_widget.model()))

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
                box = QWidget(cont)
                box_l = QHBoxLayout()
                box.setLayout(box_l)
                lw = QListWidget(box)
                lw.setFlow(QListView.Flow.LeftToRight)
                item = QListWidgetItem("1", lw)
                item.setFlags(item.flags() | QtCore.Qt.ItemFlag.ItemIsEditable)
                lw.addItem(item)
                item = QListWidgetItem("2", lw)
                item.setFlags(item.flags() | QtCore.Qt.ItemFlag.ItemIsEditable)
                lw.addItem(item)
                lw.setContentsMargins(0,0,0,0)
                lw.setMaximumHeight( 30 )
                lw.adjustSize()
                lw.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
                
                self.ages_widget = lw
                
                btn_add = QPushButton("+", box)
                btn_add.clicked.connect(self.add_age)
                
                
                btn_sub = QPushButton("-", box)
                btn_sub.clicked.connect(self.sub_age)
                
                box_l.setSpacing(1)
                box_l.setContentsMargins(0,0,0,0)
                box_l.addWidget(lw)
                
                box_l.addWidget(btn_add)
                box_l.addWidget(btn_sub)
                
                box.setContentsMargins(0,0,0,0)
                
                box.adjustSize()
                
                
                #box.setStyleSheet("background-color: red;")

                widget = box
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
            elif field in ["any_more_vehicles_involved"]:
                # https://stackoverflow.com/questions/71931807/how-to-use-an-active-qcombobox-as-an-element-of-qlistview-in-pyqt5
                box = QWidget(cont)
                box_l = QHBoxLayout()
                box.setLayout(box_l)
                lw = QListView()

                list = PlainList([[e.value for e in articleinfo.VechicleType]])
                
                lw.setModel(list)
                lw.model()
                lw.setItemDelegate(QBDelegate(lw))
                
                self.vechicles_widget = lw
                self.vechicles_widget.model().append([[e.value for e in articleinfo.VechicleType]])
                
                #lw.setFlow(QListView.Flow.LeftToRight)

                lw.setContentsMargins(0,0,0,0)
                lw.setMaximumHeight( 50 )
                lw.adjustSize()
                lw.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
                
                btn_add = QPushButton("+", box)
                btn_add.clicked.connect(self.add_vechicle)
                
                btn_sub = QPushButton("-", box)
                btn_sub.clicked.connect(self.sub_vechicle)
                
                box_l.setSpacing(0)
                box_l.setContentsMargins(0,0,0,0)
                box_l.addWidget(lw)
                
                box_l.addWidget(btn_add)
                box_l.addWidget(btn_sub)
                
                box.setContentsMargins(0,0,0,0)
                box.adjustSize()
                #box.setStyleSheet("background-color: red; padding: 0em")
                widget = box
            else:
                i += 1
                continue
           
            widget.setContentsMargins(0,0,0,0)
           
            cont_l.addWidget(label)
            cont_l.addWidget(widget)
            
            cont_l.setSpacing(2)
            cont.adjustSize()
            
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
    w.raw_text = raw_text
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
    
    #for i in range(0, names.__len__()):
    #    print(names[i], "->", type(widgets[i]))
    
    btn_skip = QPushButton("Skip", w)
    btn_next = QPushButton("Next", w)
    
    btn_next.clicked.connect(w.next)
    btn_skip.clicked.connect(w.skip)
     
    cont = QWidget(w)
    cont_l = QHBoxLayout(cont)
    cont.setLayout(cont_l)
    
    cont_l.addWidget(btn_skip)
    
    cont_l.addWidget(btn_next)
    
    rightside_l.addWidget(cont)
    
    w.showMaximized()

    for name, widget in w.w_dict.items():
        print(name) #, "-->", type(widget))
    
    print(w.extract_vechicles())
    
    w.output.writerow(articleinfo.ArticleInfo.title_row())
    
    ret : int = app.exec_()
   
    w.dest()
    
    sys.exit(ret)