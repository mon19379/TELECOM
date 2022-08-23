from multiprocessing.connection import answer_challenge
from PyQt5 import QtCore, QtGui, QtWidgets
import requests
import array as arr
from pyvis.network import Network



con = 0
ye = []

exit=False


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(140, 90, 113, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(140, 140, 113, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(Form)
        self.lineEdit_3.setGeometry(QtCore.QRect(140, 180, 113, 20))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(110, 90, 21, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(50, 140, 81, 20))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(60, 180, 81, 20))
        self.label_3.setObjectName("label_3")
        self.lineEdit_4 = QtWidgets.QLineEdit(Form)
        self.lineEdit_4.setGeometry(QtCore.QRect(140, 50, 113, 20))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(100, 50, 31, 16))
        self.label_4.setObjectName("label_4")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(50, 240, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_1 = QtWidgets.QPushButton(Form)
        self.pushButton_1.setGeometry(QtCore.QRect(150, 240, 75, 23))
        self.pushButton_1.setObjectName("pushButton_1")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(250, 240, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(270,50, 75, 23))
        self.pushButton_3.setObjectName("pushButton_3")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.pushButton.clicked.connect(self.run)
        self.pushButton_1.clicked.connect(self.run1)
        self.pushButton_2.clicked.connect(self.run2)
        self.pushButton_3.clicked.connect(self.bot)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "ASN"))
        self.label_2.setText(_translate("Form", "TIEMPO INICIO"))
        self.label_3.setText(_translate("Form", "TIEMPO FINAL"))
        self.label_4.setText(_translate("Form", "Prefijo"))
        self.pushButton.setText(_translate("Form", "Run"))
        self.pushButton_1.setText(_translate("Form", "Estado inicial"))
        self.pushButton_2.setText(_translate("Form", "Cambios"))
        self.pushButton_3.setText(_translate("Form", "Next"))


    
    
    
    def run(self):
        net = Network()
        p = []
        t = {}
        paths = []

        ip = self.lineEdit_4.text()
        url = 'https://stat.ripe.net/data/ris-peerings/data.json?resource={}'.format(ip)
        resp = requests.get(url)
        


        
        for i in range(len(resp.json()['data']['peerings'])):
            #print('peering: ', i)
            t[i] = {}
            for j in range(len(resp.json()['data']['peerings'][i]['peers'])):
                #print('peer: ', j)
                t[i][j] = {}                
                for k in resp.json()['data']['peerings'][i]['peers'][j]['routes']:
                    temp = k['as_path']
                    t[i][j] = temp
                    p = t[i][j]
                    #print (p)
                    paths.append(p)
                    #print("as_path: ")
                    for v in temp:
                        # print(v)
                        net.add_node(v, label = str(v))
                    for r in range(1,len(p)):
                        net.add_edge(p[r],p[r-1])                                               
                        
        net.show('Todo.html')
        


    def run1(self):
        net1 = Network()
        trash1 = []
        f1 = {}
        y1 = []
        lista1 = []
        
        pre = self.lineEdit_4.text()
        asn = self.lineEdit.text()
        TI = self.lineEdit_2.text()
        TF = self.lineEdit_3.text()

        url1 = 'https://stat.ripe.net/data/bgplay/data.json?resource={}&starttime={}&endtime={}'.format(pre,TI,TF) 
        
        resp1 = requests.get(url1)
        for at in range(len(resp1.json()['data']['initial_state'])):
            f1[at] = {}
            
            for pi in range(len(resp1.json()['data']['initial_state'][at])):
                f1[at][pi] = resp1.json()['data']['initial_state'][at]['path']
                ini = f1[at][pi]
                #print(ini)
                lista1 = list(map(int,ini))
                
                if int(asn) in lista1:
                    y1.append(lista1)
                else:
                    trash1.append(lista1)

        str(y1)
        for u1 in y1:
            for m1 in u1:
                net1.add_node(m1, label = str(m1))
            for n1 in range(1, len(u1)):
                net1.add_edge(u1[n1],u1[n1-1])

        net1.show('Inicial.html')
        
   
   
    def run2(self):
        global ye
        global con
        trash = []
        net2 = Network()
        q = []
        lista = []
        f = {} 
        y = []
        pre = self.lineEdit_4.text()
        asn = self.lineEdit.text()
        TI = self.lineEdit_2.text()
        TF = self.lineEdit_3.text()
    


        link = 'https://stat.ripe.net/data/bgplay/data.json?resource={}&starttime={}&endtime={}'.format(pre,TI,TF) 
        resp2 = requests.get(link)

        for a in range(len(resp2.json()['data']['events'])):
            f[a] = {}  
            if((len(resp2.json()['data']['events'][a]['attrs'])) > 2):
                f[a] =  resp2.json()['data']['events'][a]['attrs']['path'] 
                q = f[a] 
                #print(len(f))
                lista = list(map(int,q))
                
                if int(asn) in lista:
                        y.append(lista)
                        #print(y)
                else:
                        trash.append(lista)
                        #print(trash)
        str(y)
        ye = y
        print(y)
        for m in y[con]:
            net2.add_node(m, label = str(m))
    
        for n in range(1, len(y[con])):
            net2.add_edge(y[con][n],y[con][n-1])
        
        net2.show('Cambios.html')
        if con > (len(ye)):
            con = 0

       

    def bot(self):
        global ye
        global con
        
        print(con)
        print(len(ye))
        con = con+1
        
        
            
        

'''
        for u in y[con]:
            print(u)
            for m in u:
                net2.add_node(m, label = str(m))
            for n in range(1, len(u)):
                net2.add_edge(u[n],u[n-1])
        net2.show('Cambios.html')
        
'''
    

    


        


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_Form()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())