from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sys
import csv

engine = create_engine('sqlite:///tanamshromlebi.db')
Base = declarative_base()


class Tanamshromeli(Base):
    __tablename__ = 'tanamshromlebi'
    id = Column(Integer, primary_key=True)
    saxeli = Column(String, nullable=False)
    tanamdeboba = Column(String, nullable=False)
    departamenti = Column(String, nullable=False)
    xelfasi = Column(Float, nullable=False)
    dasawyebis_tarigi = Column(Date, nullable=False)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
sessia = Session()


class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('tanamshromlebi.ui', self)

        self.btn_damateba.clicked.connect(self.damateba)
        self.btn_redaqtireba.clicked.connect(self.redaqtireba)
        self.btn_washla.clicked.connect(self.washla)
        self.btn_export.clicked.connect(self.export_csv)

        self.tanamshromlebis_cargeba()

    def tanamshromlebis_cargeba(self):
        self.tableWidget.setRowCount(0)
        tanamshromlebi = sessia.query(Tanamshromeli).all()
        for row_num, tanamshromeli in enumerate(tanamshromlebi):
            self.tableWidget.insertRow(row_num)
            self.tableWidget.setItem(row_num, 0, QTableWidgetItem(str(tanamshromeli.id)))
            self.tableWidget.setItem(row_num, 1, QTableWidgetItem(tanamshromeli.saxeli))
            self.tableWidget.setItem(row_num, 2, QTableWidgetItem(tanamshromeli.tanamdeboba))
            self.tableWidget.setItem(row_num, 3, QTableWidgetItem(tanamshromeli.departamenti))
            self.tableWidget.setItem(row_num, 4, QTableWidgetItem(str(tanamshromeli.xelfasi)))
            self.tableWidget.setItem(row_num, 5, QTableWidgetItem(str(tanamshromeli.dasawyebis_tarigi)))

    def damateba(self):
        saxeli = self.input_saxeli.text()
        tanamdeboba = self.input_tanamdeboba.text()
        departamenti = self.input_departamenti.text()
        xelfasi = float(self.input_xelfasi.text())
        dasawyebis_tarigi = self.input_dasawyebis_tarigi.text()

        if saxeli and tanamdeboba and departamenti and xelfasi and dasawyebis_tarigi:
            axali_tanamshromeli = Tanamshromeli(
                saxeli=saxeli,
                tanamdeboba=tanamdeboba,
                departamenti=departamenti,
                xelfasi=xelfasi,
                dasawyebis_tarigi=dasawyebis_tarigi
            )
            sessia.add(axali_tanamshromeli)
            sessia.commit()
            self.tanamshromlebis_cargeba()
        else:
            QMessageBox.warning(self, "შეცდომა", "გთხოვთ შეავსოთ ყველა ველი!")

    def redaqtireba(self):
        current_row = self.tableWidget.currentRow()
        if current_row != -1:
            tanamshromeli_id = int(self.tableWidget.item(current_row, 0).text())
            tanamshromeli = sessia.query(Tanamshromeli).get(tanamshromeli_id)
            tanamshromeli.saxeli = self.input_saxeli.text()
            tanamshromeli.tanamdeboba = self.input_tanamdeboba.text()
            tanamshromeli.departamenti = self.input_departamenti.text()
            tanamshromeli.xelfasi = float(self.input_xelfasi.text())
            tanamshromeli.dasawyebis_tarigi = self.input_dasawyebis_tarigi.text()
            sessia.commit()
            self.tanamshromlebis_cargeba()
        else:
            QMessageBox.warning(self, "შეცდომა", "გთხოვთ აირჩიოთ თანამშრომელი!")

    def washla(self):
        current_row = self.tableWidget.currentRow()
        if current_row != -1:
            tanamshromeli_id = int(self.tableWidget.item(current_row, 0).text())
            tanamshromeli = sessia.query(Tanamshromeli).get(tanamshromeli_id)
            sessia.delete(tanamshromeli)
            sessia.commit()
            self.tanamshromlebis_cargeba()
        else:
            QMessageBox.warning(self, "შეცდომა", "გთხოვთ აირჩიოთ თანამშრომელი!")

    def export_csv(self):
        with open('tanamshromlebi.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "სახელი", "თანამდებობა", "დეპარტამენტი", "ხელფასი", "დაწყების თარიღი"])
            tanamshromlebi = sessia.query(Tanamshromeli).all()
            for tanamshromeli in tanamshromlebi:
                writer.writerow([tanamshromeli.id, tanamshromeli.saxeli, tanamshromeli.tanamdeboba,
                                 tanamshromeli.departamenti, tanamshromeli.xelfasi, tanamshromeli.dasawyebis_tarigi])
        QMessageBox.information(self, "ექსპორტი", "მონაცემები ექსპორტირებულია CSV ფაილში.")


app = QtWidgets.QApplication(sys.argv)
window = MainApp()
window.show()
sys.exit(app.exec_())