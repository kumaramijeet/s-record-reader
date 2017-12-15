
import sys
import csv
import sip



#!/usr/bin/env python
#-*- coding:utf-8 -*-



sip.setapi('QString', 2)
sip.setapi('QVariant', 2)
from PyQt4 import QtGui, QtCore


path = ""
location = "C:\Temp\workfile.csv"



######################################## function to create a csv file######################
def create_csv(location):
     file1 = open(location, 'a')
     print "csv file created........"

########################################################################

create_csv(location)            ###### calling create csv


class MyWindow(QtGui.QWidget):

    def __init__(self,location, parent=None):                      ########################### the constructor
        super(MyWindow, self).__init__(parent)

        self.fileName = ""
        self.locate = location

        #headerview = header()

        self.model = QtGui.QStandardItemModel(self)

        self.tableView = QtGui.QTableView(self)
        self.tableView.setModel(self.model)
       # self.tableView.setHorizontalHeader(self, headerview)
        self.tableView.horizontalHeader().setStretchLastSection(False)

        self.pushButtonLoad = QtGui.QPushButton(self)
        self.pushButtonLoad.setText("Load File!")
        self.pushButtonLoad.clicked.connect(self.on_pushButtonLoad_clicked)

        self.pushButtonWrite = QtGui.QPushButton(self)
        self.pushButtonWrite.setText("Write in File!")
        self.pushButtonWrite.clicked.connect(self.on_pushButtonWrite_clicked)

        self.lbl = QtGui.QLabel('No file selected')                                                               #####  adding label
        #self.lbl2 = QtGui.QLabel('Source file not selected')

        btn = QtGui.QPushButton('Choose File')                                                                    ##### button added
        #btn2 = QtGui.QPushButton('location to store (should be an empty .csv file )')



        self.layoutVertical = QtGui.QVBoxLayout(self)
        self.layoutVertical.addWidget(self.tableView)
        self.layoutVertical.addWidget(self.pushButtonLoad)
        self.layoutVertical.addWidget(self.pushButtonWrite)
        self.layoutVertical.addWidget(self.lbl)
        self.layoutVertical.addWidget(btn)
        #self.layoutVertical.addWidget(self.lbl2)
        #self.layoutVertical.addWidget(btn2)


        self.setGeometry(100,100,950,500)
        self.setWindowTitle("my table")

        self.connect(btn, QtCore.SIGNAL('clicked()'),self.get_fname)             ########## emitting signal when button is clicked
        #self.connect(btn2, QtCore.SIGNAL('clicked()'),self.get_destname)           ########## emitting signal when button is clicked


    def get_fname(self):
        fname = QtGui.QFileDialog.getOpenFileName(self,'Select .S19 File')
        if fname:
            self.lbl.setText(fname)
            self.fileName = fname
        else:
            self.lbl.setText('No File Selected')

        return fname

    '''def get_destname(self):
        destname = QtGui.QFileDialog.getOpenFileName(self, 'Select File')
        if destname:
            self.lbl2.setText(destname)
            self.location = destname
        else:
            self.lbl.setText('No File Selected')

        return destname '''



    def loadCsv(self, locate):
        with open(locate, "rb") as fileInput:
            for row in csv.reader(fileInput):
                items = [QtGui.QStandardItem(field) for field in row]
                self.model.appendRow(items)

    def writeCsv(self, locate):
        with open(locate, "wb") as fileOutput:
            writer = csv.writer(fileOutput)
            for rowNumber in range(self.model.rowCount()):
                fields = [self.model.data(self.model.index(rowNumber, columnNumber), QtCore.Qt.DisplayRole)for columnNumber in range(self.model.columnCount())]
                writer.writerow(fields)

    #@QtCore.pyqtSlot()
    def on_pushButtonWrite_clicked(self):
        self.writeCsv(self.locate)

    #@QtCore.pyqtSlot()
    def on_pushButtonLoad_clicked(self):
        self.loadCsv(self.locate)

#def header(QHeaderView):












def decode():

    print "hi"


    #############################   function for creating a backup file   ########################################
    def create_file():
        file1 = open("C:\Users\Amijeet Kumar\Desktop\Backup.S19",'a')
        print "Backup file created....."

    ############################################################################



    ######## ########################## function to check sum  ##########################
    def s19_checksum(line):
        length = int (line [2:4] , 16)
        bytes = [int (line [i*2:i*2+2] , 16)   for i in range (1,length+1)]

        return ~sum(bytes) &0xff
    #####################################################################################



    #inputfile = "C:\Users\Amijeet Kumar\Desktop\DMS1_MIOS2.s19"
    print "below is the path"
    inputfile2  = path
    print "path %s" %path

    create_file()           #### calling function create_file


    outputfile = "C:\Users\Amijeet Kumar\Desktop\Backup.S19"


    ##############################  opening the source file to read  ##################################
    fh = file(inputfile2 , 'r')
    subject = fh.read()
    fh.close()

    ########################################################################################


    ################################### writing in backup file #############################


    fh2 = file(outputfile , 'w' )

    fh2.write(subject)
    print subject


    fh2.close()
    ##########################################################################################

    ################################# writing in csv file#################################

    pen = csv.writer(open("C:\Temp\workfile.csv" , "wb"))
    pen.writerow(["Addr","Hex","Description","Value","Min","Max","Default","type","Size"])
    pen.writerow(["","","MIOS CONFIG","","","","","",""])

    ##########################################################################################


    ######################################## function to define mode in which section is operating ############
    def sectmode( input ):
        if ( input == '00' ):
            return ""
        elif (input == '01'):
            return "safe mode"
        elif (input == '02'):
            return "mixed mode"
        else :
            return "undefined"


    ###########################################################################################################





    ###################### calculating and displaying checksum for each line    ##########################
    with open(inputfile2 , 'r') as f:
        for line in f:

            line_length = int(line[2:4],16)
            address = line[4:8]

            ####################################         decrypting each line           ######################

            if line.startswith('S1130000'):
                print "address: %s" %address
                value = line[8:12]
                print "value %s"%value
                pen.writerow([int(address,16),hex(int(address,16)),"Configuration Plug format code",int(value),"0","65535","7","UINT 16",""])

                config_ver = line[16:20]
                print "configuration version %s" %config_ver
                pen.writerow([int(address,16), hex(int(address,16)), "Configuration version", int(config_ver), "", "", "0.0.0.0","IP", "9"])

            if line.startswith('S1130020'):
                unit_type_desig = line[20:39]
                print "unit type designation  %s" %unit_type_desig

                val = ''                                                           ########### converting hex into ascii
                for i in range(0, len(unit_type_desig), 2):
                    val += chr(int(unit_type_desig[i:i + 2], 16))

                pen.writerow([int(address,16), hex(int(address,16)), "Unit type designation", val , "", "", "DCS 2222C","TEXT", "15"])

                req_func_inter = line[38:41]
                print "required functional interface %s" %req_func_inter
                pen.writerow([int(address,16), hex(int(address,16)), "required functional ",req_func_inter , "0", "255", "0", "UINT 8", ""])



            if line.startswith('S1130040'):

                mvb_base_add = line[14:16]
                print "mvb_base_add %s" %mvb_base_add
                pen.writerow([int(address,16), hex(int(address,16)), "MVB Base Address", mvb_base_add, "0", "255", "0", "UINT 8",""])

                mvb_esd_emd = line[16:18]
                print "mvb_esd_emd %s" % mvb_esd_emd
                pen.writerow([int(address,16), hex(int(address,16)), "MVB_ESD+/EMD ", mvb_esd_emd, "0", "255", "1", "UINT 8",""])

                pen.writerow(["","", "SDT v2 Channel Monitoring ", "", "", "", "", "",""])

                CMThr = line[18:20]
                print "CMThr %s" %CMThr
                pen.writerow([int(address,16), hex(int(address,16)), "CMT hr ", CMThr, "0", "4294967295", "4294967295", "UINT 32",""])

                ########################################### section 1 starts ########################################


                pen.writerow(["", "", "Section 1 configuration", "", "", "", "", "", ""])

                SDTv2_protocol = line[26:28]
                print "SDTv2 protocol enable %s" %SDTv2_protocol

                sect1mode = sectmode(SDTv2_protocol)

                pen.writerow(["", "", "SDT v2 Protocol Enable (sect 1)", sect1mode , "", "", "", "", ""])

                print "output ttx period: "
                otpp_min_val = 0
                otpp_max_val = 2047
                otpp_default = 0
                otpp_type = "UINT 16"

                op_ttx_port = []

                pen.writerow(["", "", "Output ttx period", "", "", "", "", "", ""])

                op_ttx_port.insert(0,line[28:32])
                print "output_ttx_period_port0: %s" %op_ttx_port[0]


                op_ttx_port.insert(1,line[32:36])
                print "output_ttx_period_port1: %s"%op_ttx_port[1]

                op_ttx_port.insert(2, line[36:40])
                print "%s" %op_ttx_port[2]


            if line.startswith('S1130050') :

                op_ttx_port.insert(3, line[8:12])
                print "%s" %op_ttx_port[3]

                op_ttx_port.insert(4,line[12:16])
                print "%s" %op_ttx_port[4]

                op_ttx_port.insert(5,line[16:20])
                print "%s" %op_ttx_port[5]

                op_ttx_port.insert(6,line[20:24])
                print "%s" %op_ttx_port[6]

                op_ttx_port.insert(7,line[24:28])
                print "%s" %op_ttx_port[7]

                for j in range(0,len(op_ttx_port)):
                    pen.writerow([int(address,16), hex(int(address,16)), " Output Ttx peroid port "+ str(j), op_ttx_port[j], otpp_min_val, otpp_max_val, otpp_default, otpp_type, ""])

                print "TRX period starts: "


                trxpp_min_val = 0
                trxpp_max_val = 2047
                trxpp_default = 0
                trxpp_type = "UINT 16"

                trx_port = ["no data","no data","no data","no data","no data","no data","no data","no data"]

                trx_port.insert(8,line[28:32])
                print "TRX period port 8  %s" %trx_port[8]

                trx_port.insert(9,line[32:36])
                print "%s" %trx_port[9]

                trx_port.insert(10,line[36:40])
                print "%s" %trx_port[10]


            if line.startswith('S1130060'):

                trx_port.insert(11,line[8:12])
                print "%s" %trx_port[11]

                trx_port.insert(12,line[12:16])
                print "%s" %trx_port[12]

                trx_port.insert(13,line[16:20])
                print "%s" %trx_port[13]

                trx_port.insert(14,line[20:24])
                print "%s" %trx_port[14]

                trx_port.insert(15,line[24:28])
                print "%s" %trx_port[15]

                for j in range(8,len(trx_port)):
                    pen.writerow([int(address,16), hex(int(address,16)), " TRX_port_period" + str(j), trx_port[j], trxpp_min_val,trxpp_max_val, trxpp_default, trxpp_type, ""])



                print "MVB time out starts...."

                mvb_to_min_value = 0
                mvb_to_max_value = 8191
                mvb_to_default = 0
                mvb_to_type = "UINT 16"

                mvb_to_port = ["no data","no data","no data","no data","no data","no data","no data","no data"]

                mvb_to_port.insert(8,line[28:32])
                print "mvb_timeout_port8  %s" %mvb_to_port[8]

                mvb_to_port.insert(9,line[32:36])
                print "%s " %mvb_to_port[9]

                mvb_to_port.insert(10,line[36:40])
                print "%s " %mvb_to_port[10]

            if line.startswith('S1130070'):

                mvb_to_port.insert(11,line[8:12])
                print "%s " %mvb_to_port[11]

                mvb_to_port.insert(12,line[12:16])
                print "%s" %mvb_to_port[12]

                mvb_to_port.insert(13,line[16:20])
                print "%s" %mvb_to_port[13]

                mvb_to_port.insert(14,line[20:24])
                print "%s " %mvb_to_port[14]

                mvb_to_port.insert(15,line[24:28])
                print "%s " %mvb_to_port[15]

                for j in range(8,len(mvb_to_port)):
                    pen.writerow([int(address,16), hex(int(address,16)), " MVB_TIMEOUT_PORT" + str(j), mvb_to_port[j], mvb_to_min_value, mvb_to_max_value, mvb_to_default, mvb_to_type, ""])

                print "safe message identifier:  "

                op_smi_min_val = 0
                op_smi_max_val = 4294967295
                op_smi_default = 0
                op_smi_type = "UINT 32"

                op_smi_port = []

                op_smi_port.insert(0,line[28:36])
                print"output SMI port 0:  %s" %op_smi_port[0]

                op_smi_port1_1 = line[36:40]

            if line.startswith('S1130080'):

                op_smi_port1_2 = line[8:12]
                op_smi_port.insert(1,op_smi_port1_1 + op_smi_port1_2)
                print"%s " %op_smi_port[1]

                op_smi_port.insert(2,line[12:20])
                print "%s " %op_smi_port[2]

                op_smi_port.insert(3,line[20:28])
                print "%s " %op_smi_port[3]

                op_smi_port.insert(4,line[28:36])
                print "%s " %op_smi_port[4]

                op_smi_port5_1 = line[36:40]

            if line.startswith('S1130090'):

                op_smi_port5_2 = line[8:12]
                op_smi_port.insert(5,op_smi_port5_1 + op_smi_port5_2)
                print "%s " %op_smi_port[5]

                op_smi_port.insert(6,line[12:20])
                print "%s " %op_smi_port[6]

                op_smi_port.insert(7,line[20:28])
                print "%s " %op_smi_port[7]


                for j in range(0,len(op_smi_port)):
                    pen.writerow([int(address,16), hex(int(address,16)), " Output SMI port" + str(j), op_smi_port[j], op_smi_min_val,op_smi_max_val, op_smi_default, op_smi_type, ""])



                print "SMI port starts: "


                smi_port_min_val = 0
                smi_port_max_val = 4294967295
                smi_port_default = 0
                smi_port_type = "UINT 32"

                smi_1_port = ["no data","no data","no data","no data","no data","no data","no data","no data"]
                smi_2_port = ["no data","no data","no data","no data","no data","no data","no data","no data"]



                smi_1_port.insert(8,line[28:36])
                print "SMI_1_port 8  %s:   " %smi_1_port[8]

                smi_2_port8_1 = line[36:40]

            if line.startswith('S11300A0'):
                smi_2_port8_2 = line[8:12]
                smi_2_port.insert(8,smi_2_port8_1 + smi_2_port8_2)
                print "%s " %smi_2_port[8]

                smi_1_port.insert(9, line[12:20])
                print " port 9  %s " %smi_1_port[9]

                smi_2_port.insert(9,line[20:28])
                print "port 9 %s " %smi_2_port[9]

                smi_1_port.insert(10,line[28:36])
                print "port 10 %s "%smi_1_port[10]

                smi_2_port10_1 = line[36:40]

            if line.startswith('S11300B0'):

                smi_2_port10_2 = line[8:12]
                smi_2_port.insert(10,smi_2_port10_1 + smi_2_port10_2)
                print"%s " %smi_2_port[10]

                smi_1_port.insert(11, line[12:20])
                print " port 11 %s " %smi_1_port[11]

                smi_2_port.insert(11,line[20:28])
                print "port 11 %s " %smi_2_port[11]

                smi_1_port.insert(12 ,line[28:36])
                print "port 12 %s " %smi_1_port[12]

                smi_2_port12_1 = line[36:40]

            if line.startswith('S11300C0'):

                smi_2_port12_2 = line[8:12]
                smi_2_port.insert(12,smi_2_port12_1 + smi_2_port12_2)

                smi_1_port.insert(13,line[12:20])
                print "port 13 %s "%smi_1_port[13]

                smi_2_port.insert(13,line[20:28])
                print "port 13 %s " %smi_2_port[13]

                smi_1_port.insert(14 , line[28:36])
                print "port 14 %s " %smi_1_port[14]

                smi_2_port14_1 = line[36:40]

            if line.startswith('S11300D0'):

                smi_2_port14_2 = line[8:12]
                smi_2_port.insert(14,smi_2_port14_1 + smi_2_port14_2)
                print "%s " %smi_2_port[14]

                smi_1_port.insert(15, line[12:20])
                print "port 15 %s " %smi_1_port[15]

                smi_2_port.insert(15,line[20:28])
                print "port 15 %s " %smi_2_port[15]


                for j in range(8,len(smi_1_port)):
                    pen.writerow([int(address,16), hex(int(address,16)), " SMI 1 port" + str(j), smi_1_port[j], smi_port_min_val,smi_port_max_val, smi_port_default, smi_port_type, ""])
                    pen.writerow([int(address,16), hex(int(address,16)), " SMI 2 port" + str(j), smi_2_port[j], smi_port_min_val,smi_port_max_val, smi_port_default, smi_port_type, ""])





                print "N_guard starts: "

                nguard_port = ["no data","no data","no data","no data","no data","no data","no data","no data"]

                nguard_min = 0
                nguard_max = 255
                nguard_default = 255
                nguard_type = "UINT 8"




                nguard_port.insert(8, line[28:30])
                print "N_Guard port 8: %s " %nguard_port[8]

                nguard_port.insert(9, line[30:32])
                print " %s " %nguard_port[9]

                nguard_port.insert( 10, line[32:34])
                print " %s " %nguard_port[10]

                nguard_port.insert(11 ,line[34:36])
                print " %s " %nguard_port[11]

                nguard_port.insert(12,line[36:38])
                print " %s" %nguard_port[12]

                nguard_port.insert(13 ,line[38:40])
                print " %s" %nguard_port[13]

            if line.startswith('S11300E0'):

                nguard_port.insert(14 ,line[8:10])
                print " %s" %nguard_port[14]

                nguard_port.insert(15 ,line[10:12])
                print " %s" %nguard_port[15]

                for j in range(8,len(nguard_port)):
                    pen.writerow([int(address,16), hex(int(address,16)), " nguard_port" + str(j), nguard_port[j], nguard_min,nguard_max, nguard_default, nguard_type, ""])



                print "NRX safe starts:  "

                nrx_safe_min = 0
                nrx_safe_max = 255
                nrx_safe_default = 0
                nrx_safe_type = "UINT 8"

                nrx_safe_port = ["no data","no data","no data","no data","no data","no data","no data","no data"]

                nrx_safe_port.insert(8 , line[12:14])
                print " NRX safe port 8 %s " %nrx_safe_port[8]

                nrx_safe_port.insert(9 , line[14:16])
                print " %s " %nrx_safe_port[9]

                nrx_safe_port.insert(10 , line[16:18])
                print " %s" %nrx_safe_port[10]

                nrx_safe_port.insert(11 , line[18:20])
                print " %s " %nrx_safe_port[11]

                nrx_safe_port.insert(12, line[20:22])
                print " %s " %nrx_safe_port[12]

                nrx_safe_port.insert(13, line[22:24])
                print " %s " %nrx_safe_port[13]

                nrx_safe_port.insert(14, line[24:26])
                print " %s " %nrx_safe_port[14]

                nrx_safe_port.insert(15, line[26:28])
                print " %s " %nrx_safe_port[15]


                for j in range(8,len(nrx_safe_port)):
                    pen.writerow([int(address,16), hex(int(address,16)), " Nrxsafe_port" + str(j), nrx_safe_port[j], nrx_safe_min,nrx_safe_max, nrx_safe_default, nrx_safe_type, ""])


                print "Ttx period starts: "

                ttx_pd_min = 0
                ttx_pd_max = 2047
                ttx_pd_default = 0
                ttx_pd_type = "UINT 8"

                ttx_pd_port = ["no data","no data","no data","no data","no data","no data","no data","no data"]

                ttx_pd_port.insert( 8, line[28:32])
                print " ttx period port 8 %s " %ttx_pd_port[8]

                ttx_pd_port.insert(9 , line[32:36])
                print " %s " %ttx_pd_port[9]

                ttx_pd_port.insert(10 , line[36:40])
                print " %s " %ttx_pd_port[10]

            if line.startswith('S11300F0'):

                ttx_pd_port.insert(11 , line[8:12])
                print " %s " %ttx_pd_port[11]

                ttx_pd_port.insert( 12, line[12:16])
                print " %s " %ttx_pd_port[12]

                ttx_pd_port.insert(13 , line[16:20])
                print " %s " %ttx_pd_port[13]

                ttx_pd_port.insert(14 , line[20:24])
                print " %s " %ttx_pd_port[14]

                ttx_pd_port.insert(15 , line[24:28])
                print " %s " %ttx_pd_port[15]

                for j in range(8, len(ttx_pd_port)):
                    pen.writerow([int(address, 16), hex(int(address, 16)), "Ttx_period_port" + str(j), ttx_pd_port[j], ttx_pd_min,ttx_pd_max, ttx_pd_default, ttx_pd_type, ""])

            if line.startswith('S1130100'):

                required_inter_ver = line[28:30]
                print " required interface version %s " %required_inter_ver
                pen.writerow([int(address, 16), hex(int(address, 16)), "Required Functional Interface", required_inter_ver, "0","255", "0", "UINT 8", ""])


                print "AIN_AX starts ......... "

                ain_ax_min = 0
                ain_ax_max = 255
                ain_ax_default = 0
                ain_ax_type = "BiTFIELD 8"
                ain_ax_bit_default = "0x0"
                ain_ax_bit_type = "BIT"

                ain_fun_a = ["no data"]


            if line.startswith('S1130110'):

                ain_fun_a.insert(1,line[12:14])
                print "ain a1 function : %s " %ain_fun_a[1]

                #########################33##################### AIN A1 Function (definition for each bit) ######################
                data = bin(int(ain_fun_a[1],16))[2:]

                Filter_bit0 = int(data)%10
                pen.writerow([int(address, 16), hex(int(address, 16))+"_0", "Filter (Bit0)", Filter_bit0, "","", "0x0", "BIT", ""])
                Filter_bit1 = (int(data)/10)%10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_1", "Filter (Bit1)", Filter_bit1, "", "", "0x0", "BIT",""])
                Filter_bit2 = (int(data)/100)%10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_2", "Filter (Bit2)", Filter_bit2, "", "", "0x0", "BIT",""])
                bit_0or1 = (int(data)/10000)%10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_4", "'0'= (+/-)10v ; '1'= (+/-)2.5v", bit_0or1, "", "", "0x0", "BIT",""])
                resist_measure = (int(data)/100000)%10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_5", "Resistance measurement", resist_measure, "", "", "0x0", "BIT",""])
                channel_safe_measure = (int(data)/1000000)%10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_6", "Channel Safe Measurement", channel_safe_measure, "", "", "0x0", "BIT",""])


                #################################################################################################################

                ain_fun_a.insert(2 ,line[14:16])
                print "a2 %s " %ain_fun_a[2]

                #########################33##################### AIN A1 Function (definition for each bit) ######################
                data = bin(int(ain_fun_a[2], 16))[2:]

                Filter_bit0 = int(data) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_0", "Filter (Bit0)", Filter_bit0, "", "", "0x0", "BIT",""])
                Filter_bit1 = (int(data) / 10) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_1", "Filter (Bit1)", Filter_bit1, "", "", "0x0", "BIT",""])
                Filter_bit2 = (int(data) / 100) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_2", "Filter (Bit2)", Filter_bit2, "", "", "0x0", "BIT",""])
                bit_0or1 = (int(data) / 10000) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_4", "'0'= (+/-)10v ; '1'= (+/-)2.5v", bit_0or1, "", "","0x0", "BIT", ""])
                resist_measure = (int(data) / 100000) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_5", "Resistance measurement", resist_measure, "", "","0x0", "BIT", ""])
                channel_safe_measure = (int(data) / 1000000) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_6", "Channel Safe Measurement", channel_safe_measure, "", "", "0x0", "BIT", ""])

                #################################################################################################################





                ain_fun_a.insert(3 ,line[16:18])
                print "a3 %s " %ain_fun_a[3]

                #########################33##################### AIN A1 Function (definition for each bit) ######################
                data = bin(int(ain_fun_a[3], 16))[2:]

                Filter_bit0 = int(data) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_0", "Filter (Bit0)", Filter_bit0, "", "", "0x0", "BIT",""])
                Filter_bit1 = (int(data) / 10) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_1", "Filter (Bit1)", Filter_bit1, "", "", "0x0", "BIT",""])
                Filter_bit2 = (int(data) / 100) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_2", "Filter (Bit2)", Filter_bit2, "", "", "0x0", "BIT",""])
                bit_0or1 = (int(data) / 10000) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_4", "'0'= (+/-)10v ; '1'= (+/-)2.5v", bit_0or1, "", "","0x0", "BIT", ""])
                resist_measure = (int(data) / 100000) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_5", "Resistance measurement", resist_measure, "", "","0x0", "BIT", ""])
                channel_safe_measure = (int(data) / 1000000) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_6", "Channel Safe Measurement", channel_safe_measure, "", "", "0x0", "BIT", ""])

                #################################################################################################################

                ain_fun_a.insert(4, line[18:20])
                print "a4 %s " %ain_fun_a[4]

                #########################33##################### AIN A1 Function (definition for each bit) ######################
                data = bin(int(ain_fun_a[4], 16))[2:]

                Filter_bit0 = int(data) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_0", "Filter (Bit0)", Filter_bit0, "", "", "0x0", "BIT", ""])
                Filter_bit1 = (int(data) / 10) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_1", "Filter (Bit1)", Filter_bit1, "", "", "0x0", "BIT", ""])
                Filter_bit2 = (int(data) / 100) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_2", "Filter (Bit2)", Filter_bit2, "", "", "0x0", "BIT", ""])
                bit_0or1 = (int(data) / 10000) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_4", "'0'= (+/-)10v ; '1'= (+/-)2.5v", bit_0or1, "", "","0x0", "BIT", ""])
                resist_measure = (int(data) / 100000) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_5", "Resistance measurement", resist_measure, "", "","0x0", "BIT", ""])
                channel_safe_measure = (int(data) / 1000000) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_6", "Channel Safe Measurement", channel_safe_measure, "","", "0x0", "BIT", ""])

                #################################################################################################################

                ain_fun_a.insert(5, line[20:22])
                print "a5 %s " %ain_fun_a[5]

                #########################33##################### AIN A1 Function (definition for each bit) ######################
                data = bin(int(ain_fun_a[5], 16))[2:]

                Filter_bit0 = int(data) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_0", "Filter (Bit0)", Filter_bit0, "", "", "0x0", "BIT", ""])
                Filter_bit1 = (int(data) / 10) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_1", "Filter (Bit1)", Filter_bit1, "", "", "0x0", "BIT", ""])
                Filter_bit2 = (int(data) / 100) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_2", "Filter (Bit2)", Filter_bit2, "", "", "0x0", "BIT",""])
                bit_0or1 = (int(data) / 10000) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_4", "'0'= (+/-)10v ; '1'= (+/-)2.5v", bit_0or1, "", "","0x0", "BIT", ""])
                resist_measure = (int(data) / 100000) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_5", "Resistance measurement", resist_measure, "", "", "0x0", "BIT", ""])
                channel_safe_measure = (int(data) / 1000000) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_6", "Channel Safe Measurement", channel_safe_measure, "", "", "0x0", "BIT", ""])

                #################################################################################################################

                ain_fun_a.insert(6, line[22:24])
                print "a6 %s " %ain_fun_a[6]

                #########################33##################### AIN A1 Function (definition for each bit) ######################
                data = bin(int(ain_fun_a[6], 16))[2:]

                Filter_bit0 = int(data) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_0", "Filter (Bit0)", Filter_bit0, "", "", "0x0", "BIT",""])
                Filter_bit1 = (int(data) / 10) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_1", "Filter (Bit1)", Filter_bit1, "", "", "0x0", "BIT", ""])
                Filter_bit2 = (int(data) / 100) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_2", "Filter (Bit2)", Filter_bit2, "", "", "0x0", "BIT", ""])
                bit_0or1 = (int(data) / 10000) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_4", "'0'= (+/-)10v ; '1'= (+/-)2.5v", bit_0or1, "", "","0x0", "BIT", ""])
                resist_measure = (int(data) / 100000) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_5", "Resistance measurement", resist_measure, "", "", "0x0", "BIT", ""])
                channel_safe_measure = (int(data) / 1000000) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_6", "Channel Safe Measurement", channel_safe_measure, "", "", "0x0", "BIT", ""])

                #################################################################################################################

                ain_fun_a.insert(7, line[24:26])
                print "a7 %s " %ain_fun_a[7]

                #########################33##################### AIN A1 Function (definition for each bit) ######################
                data = bin(int(ain_fun_a[7], 16))[2:]

                Filter_bit0 = int(data) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_0", "Filter (Bit0)", Filter_bit0, "", "", "0x0", "BIT", ""])
                Filter_bit1 = (int(data) / 10) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_1", "Filter (Bit1)", Filter_bit1, "", "", "0x0", "BIT", ""])
                Filter_bit2 = (int(data) / 100) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_2", "Filter (Bit2)", Filter_bit2, "", "", "0x0", "BIT",""])
                bit_0or1 = (int(data) / 10000) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_4", "'0'= (+/-)10v ; '1'= (+/-)2.5v", bit_0or1, "", "", "0x0", "BIT", ""])
                resist_measure = (int(data) / 100000) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_5", "Resistance measurement", resist_measure, "", "","0x0", "BIT", ""])
                channel_safe_measure = (int(data) / 1000000) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_6", "Channel Safe Measurement", channel_safe_measure, "","", "0x0", "BIT", ""])

                #################################################################################################################


                ain_fun_a.insert(8, line[26:28])
                print " a8 %s " %ain_fun_a[8]

                #########################33##################### AIN A1 Function (definition for each bit) ######################
                data = bin(int(ain_fun_a[8], 16))[2:]

                Filter_bit0 = int(data) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_0", "Filter (Bit0)", Filter_bit0, "", "", "0x0", "BIT",""])
                Filter_bit1 = (int(data) / 10) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_1", "Filter (Bit1)", Filter_bit1, "", "", "0x0", "BIT",""])
                Filter_bit2 = (int(data) / 100) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_2", "Filter (Bit2)", Filter_bit2, "", "", "0x0", "BIT",""])
                bit_0or1 = (int(data) / 10000) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_4", "'0'= (+/-)10v ; '1'= (+/-)2.5v", bit_0or1, "", "","0x0", "BIT", ""])
                resist_measure = (int(data) / 100000) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_5", "Resistance measurement", resist_measure, "", "","0x0", "BIT", ""])
                channel_safe_measure = (int(data) / 1000000) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_6", "Channel Safe Measurement", channel_safe_measure, "","", "0x0", "BIT", ""])

                #################################################################################################################



                print "BIN _bx starts....... "

                ain_fun_b = ["no data"]

                ain_fun_b.insert(1, line[28:30])
                print " b1 %s " %ain_fun_b[1]

                #########################33##################### AIN B1 Function (definition for each bit) ######################
                data = bin(int(ain_fun_b[1], 16))[2:]

                Filter_bit0 = int(data) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_0", "Filter (Bit0)", Filter_bit0, "", "", "0x0", "BIT",""])
                Filter_bit1 = (int(data) / 10) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_1", "Filter (Bit1)", Filter_bit1, "", "", "0x0", "BIT",""])
                Filter_bit2 = (int(data) / 100) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_2", "Filter (Bit2)", Filter_bit2, "", "", "0x0", "BIT",""])
                bit_0or1 = (int(data) / 10000) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_4", "'0'= (+/-)10v ; '1'= (+/-)2.5v", bit_0or1, "", "","0x0", "BIT", ""])
                resist_measure = (int(data) / 100000) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_5", "Resistance measurement", resist_measure, "", "","0x0", "BIT", ""])
                channel_safe_measure = (int(data) / 1000000) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_6", "Channel Safe Measurement", channel_safe_measure, "","", "0x0", "BIT", ""])

                #################################################################################################################





                ain_fun_b.insert(2, line[30:32])
                print "b2 %s " %ain_fun_b[2]

                #########################33##################### AIN B1 Function (definition for each bit) ######################
                data = bin(int(ain_fun_b[2], 16))[2:]

                Filter_bit0 = int(data) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_0", "Filter (Bit0)", Filter_bit0, "", "", "0x0", "BIT",""])
                Filter_bit1 = (int(data) / 10) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_1", "Filter (Bit1)", Filter_bit1, "", "", "0x0", "BIT",""])
                Filter_bit2 = (int(data) / 100) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_2", "Filter (Bit2)", Filter_bit2, "", "", "0x0", "BIT",""])
                bit_0or1 = (int(data) / 10000) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_4", "'0'= (+/-)10v ; '1'= (+/-)2.5v", bit_0or1, "", "","0x0", "BIT", ""])
                resist_measure = (int(data) / 100000) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_5", "Resistance measurement", resist_measure, "", "","0x0", "BIT", ""])
                channel_safe_measure = (int(data) / 1000000) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_6", "Channel Safe Measurement", channel_safe_measure, "","", "0x0", "BIT", ""])

                #################################################################################################################


                ain_fun_b.insert(3, line[32:34])
                print "b3 %s " %ain_fun_b[3]

                #########################33##################### AIN B1 Function (definition for each bit) ######################
                data = bin(int(ain_fun_b[3], 16))[2:]

                Filter_bit0 = int(data) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_0", "Filter (Bit0)", Filter_bit0, "", "", "0x0", "BIT",""])
                Filter_bit1 = (int(data) / 10) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_1", "Filter (Bit1)", Filter_bit1, "", "", "0x0", "BIT",""])
                Filter_bit2 = (int(data) / 100) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_2", "Filter (Bit2)", Filter_bit2, "", "", "0x0", "BIT",""])
                bit_0or1 = (int(data) / 10000) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_4", "'0'= (+/-)10v ; '1'= (+/-)2.5v", bit_0or1, "", "","0x0", "BIT", ""])
                resist_measure = (int(data) / 100000) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_5", "Resistance measurement", resist_measure, "", "","0x0", "BIT", ""])
                channel_safe_measure = (int(data) / 1000000) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_6", "Channel Safe Measurement", channel_safe_measure, "","", "0x0", "BIT", ""])

                #################################################################################################################


                ain_fun_b.insert(4, line[34:36])
                print "b4 %s " %ain_fun_b[4]

                #########################33##################### AIN B1 Function (definition for each bit) ######################
                data = bin(int(ain_fun_b[4], 16))[2:]

                Filter_bit0 = int(data) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_0", "Filter (Bit0)", Filter_bit0, "", "", "0x0", "BIT",""])
                Filter_bit1 = (int(data) / 10) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_1", "Filter (Bit1)", Filter_bit1, "", "", "0x0", "BIT",""])
                Filter_bit2 = (int(data) / 100) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_2", "Filter (Bit2)", Filter_bit2, "", "", "0x0", "BIT",""])
                bit_0or1 = (int(data) / 10000) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_4", "'0'= (+/-)10v ; '1'= (+/-)2.5v", bit_0or1, "", "","0x0", "BIT", ""])
                resist_measure = (int(data) / 100000) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_5", "Resistance measurement", resist_measure, "", "","0x0", "BIT", ""])
                channel_safe_measure = (int(data) / 1000000) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_6", "Channel Safe Measurement", channel_safe_measure, "", "", "0x0", "BIT", ""])

                #################################################################################################################


                ain_fun_b.insert(5, line[36:38])
                print "b5 %s " %ain_fun_b[5]

                #########################33##################### AIN A1 Function (definition for each bit) ######################
                data = bin(int(ain_fun_b[5], 16))[2:]

                Filter_bit0 = int(data) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_0", "Filter (Bit0)", Filter_bit0, "", "", "0x0", "BIT", ""])
                Filter_bit1 = (int(data) / 10) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_1", "Filter (Bit1)", Filter_bit1, "", "", "0x0", "BIT", ""])
                Filter_bit2 = (int(data) / 100) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_2", "Filter (Bit2)", Filter_bit2, "", "", "0x0", "BIT", ""])
                bit_0or1 = (int(data) / 10000) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_4", "'0'= (+/-)10v ; '1'= (+/-)2.5v", bit_0or1, "", "","0x0", "BIT", ""])
                resist_measure = (int(data) / 100000) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_5", "Resistance measurement", resist_measure, "", "", "0x0", "BIT", ""])
                channel_safe_measure = (int(data) / 1000000) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_6", "Channel Safe Measurement", channel_safe_measure, "","", "0x0", "BIT", ""])

                #################################################################################################################


                ain_fun_b.insert(6, line[38:40])
                print "b6 %s " %ain_fun_b[6]

                #########################33##################### AIN A1 Function (definition for each bit) ######################
                data = bin(int(ain_fun_b[6], 16))[2:]

                Filter_bit0 = int(data) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_0", "Filter (Bit0)", Filter_bit0, "", "", "0x0", "BIT",""])
                Filter_bit1 = (int(data) / 10) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_1", "Filter (Bit1)", Filter_bit1, "", "", "0x0", "BIT",""])
                Filter_bit2 = (int(data) / 100) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_2", "Filter (Bit2)", Filter_bit2, "", "", "0x0", "BIT", ""])
                bit_0or1 = (int(data) / 10000) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_4", "'0'= (+/-)10v ; '1'= (+/-)2.5v", bit_0or1, "", "", "0x0", "BIT", ""])
                resist_measure = (int(data) / 100000) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_5", "Resistance measurement", resist_measure, "", "", "0x0", "BIT", ""])
                channel_safe_measure = (int(data) / 1000000) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_6", "Channel Safe Measurement", channel_safe_measure, "","", "0x0", "BIT", ""])

                #################################################################################################################

            if line.startswith('S1130120'):

                ain_fun_b.insert(7, line[8:10])
                print "b7 %s " %ain_fun_b[7]

                #########################33##################### AIN A1 Function (definition for each bit) ######################
                data = bin(int(ain_fun_b[7], 16))[2:]

                Filter_bit0 = int(data) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_0", "Filter (Bit0)", Filter_bit0, "", "", "0x0", "BIT",""])
                Filter_bit1 = (int(data) / 10) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_1", "Filter (Bit1)", Filter_bit1, "", "", "0x0", "BIT",""])
                Filter_bit2 = (int(data) / 100) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_2", "Filter (Bit2)", Filter_bit2, "", "", "0x0", "BIT",""])
                bit_0or1 = (int(data) / 10000) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_4", "'0'= (+/-)10v ; '1'= (+/-)2.5v", bit_0or1, "", "","0x0", "BIT", ""])
                resist_measure = (int(data) / 100000) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_5", "Resistance measurement", resist_measure, "", "","0x0", "BIT", ""])
                channel_safe_measure = (int(data) / 1000000) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_6", "Channel Safe Measurement", channel_safe_measure, "","", "0x0", "BIT", ""])

                #################################################################################################################


                ain_fun_b.insert(8, line[10:12])
                print"b8 %s " %ain_fun_b[8]

                #########################33##################### AIN A1 Function (definition for each bit) ######################
                data = bin(int(ain_fun_b[8], 16))[2:]

                Filter_bit0 = int(data) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_0", "Filter (Bit0)", Filter_bit0, "", "", "0x0", "BIT", ""])
                Filter_bit1 = (int(data) / 10) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_1", "Filter (Bit1)", Filter_bit1, "", "", "0x0", "BIT", ""])
                Filter_bit2 = (int(data) / 100) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_2", "Filter (Bit2)", Filter_bit2, "", "", "0x0", "BIT",""])
                bit_0or1 = (int(data) / 10000) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_4", "'0'= (+/-)10v ; '1'= (+/-)2.5v", bit_0or1, "", "", "0x0", "BIT", ""])
                resist_measure = (int(data) / 100000) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_5", "Resistance measurement", resist_measure, "", "", "0x0", "BIT", ""])
                channel_safe_measure = (int(data) / 1000000) % 10
                pen.writerow([int(address, 16), hex(int(address, 16)) + "_6", "Channel Safe Measurement", channel_safe_measure, "","", "0x0", "BIT", ""])

                #################################################################################################################


                print " AIN_xx_safe_adc_min_max....."


                ain_safe_min_val = -4096
                ain_safe_max_val = 4095
                ain_safe_adc_min_default = 1
                ain_safe_adc_max_default = 0
                ain_safe_type = "INT 13"


                ain_safe_adc_min = ["no data"]
                ain_safe_adc_max = ["no data"]


                ain_safe_adc_min.insert(1, line[12:16])
                print " %s " %ain_safe_adc_min[1]

                ain_safe_adc_max.insert(1, line[16:20])
                print " %s " %ain_safe_adc_max[1]

                ain_safe_adc_min.insert(2, line[20:24])
                print "%s " %ain_safe_adc_min[2]

                ain_safe_adc_max.insert(2, line[24:28])
                print "%s " %ain_safe_adc_max[2]

                ain_safe_adc_min.insert(3, line[28:32])
                print "%s " %ain_safe_adc_min[3]

                ain_safe_adc_max.insert(3, line[32:36])
                print "%s " %ain_safe_adc_max[3]

                ain_safe_adc_min.insert(4, line[36:40])
                print "%s " %ain_safe_adc_min[4]

            if line.startswith('S1130130'):

                ain_safe_adc_max.insert(4, line[8:12])
                print "%s " %ain_safe_adc_max[4]



                ain_safe_adc_min.insert(5, line[12:16])
                print "%s " %ain_safe_adc_min[5]

                ain_safe_adc_max.insert(5, line[16:20])
                print "%s " %ain_safe_adc_max[5]

                ain_safe_adc_min.insert(6, line[20:24])
                print "%s " %ain_safe_adc_min[6]

                ain_safe_adc_max.insert(6, line[24:28])
                print "%s " %ain_safe_adc_max[6]

                ain_safe_adc_min.insert(7, line[28:32])
                print "%s " %ain_safe_adc_min[7]

                ain_safe_adc_max.insert(7, line[32:36])
                print "%s " %ain_safe_adc_max[7]

                ain_safe_adc_min.insert(8, line[36:40])
                print "%s " %ain_safe_adc_min[8]

            if line.startswith('S1130140'):

                ain_safe_adc_max.insert(8, line[8:12])
                print "%s " %ain_safe_adc_max[8]


                for j in range (1,len(ain_safe_adc_min)):
                    pen.writerow([int(address, 16), hex(int(address, 16)), "AIN" + str(j) + "_SAFE_ADC_MIN", ain_safe_adc_min[j],ain_safe_min_val, ain_safe_max_val, ain_safe_adc_min_default, ain_safe_type, ""])
                    pen.writerow([int(address, 16), hex(int(address, 16)), "AIN" + str(j) + "_SAFE_ADC_MAX", ain_safe_adc_max[j],ain_safe_min_val, ain_safe_max_val, ain_safe_adc_max_default, ain_safe_type, ""])



            if line.startswith('S1130160'):

                #pen = csv.writer(open("C:\Users\Amijeet Kumar\Desktop\workfile.csv", 'a'))
                pen.writerow(["", "", "SECTION 2 CONFIGURATION", "", "", "", "", ""])

                SDTv2_protocol = line[12:14]
                print "SDTv2 protocol enable %s" % SDTv2_protocol
                pen.writerow(["", "", "SDTv2 Protocol Enable", sectmode(SDTv2_protocol), "", "", "", ""])

                print "output ttx period: "

                op_ttx_port = []

                op_ttx_port.insert(0, line[14:18])
                print "output_ttx_period_port0: %s" % op_ttx_port[0]

                op_ttx_port.insert(1, line[18:22])
                print "output_ttx_period_port1: %s" % op_ttx_port[1]

                op_ttx_port.insert(2, line[22:26])
                print "%s" % op_ttx_port[2]

                op_ttx_port.insert(3, line[26:30])
                print "%s" % op_ttx_port[3]

                op_ttx_port.insert(4, line[30:34])
                print "%s" % op_ttx_port[4]

                op_ttx_port.insert(5, line[34:38])
                print "%s" % op_ttx_port[5]

                op_ttx_port6_1 = line[38:40]

            if line.startswith('S1130170'):

                op_ttx_port6_2 = line[8:10]
                op_ttx_port.insert(6, op_ttx_port6_1 + op_ttx_port6_2)
                print"%s " % op_ttx_port[6]

                op_ttx_port.insert(7, line[10:14])
                print "%s" % op_ttx_port[7]

                for j in range(0, len(op_ttx_port)):
                    pen.writerow(
                        [int(address,16), hex(int(address,16)), "op_ttx_port" + str(j), op_ttx_port[j], "0", "2047", "0", "UINT 16", ""])

                print "TRX period starts: "

                trx_port = ["no data", "no data", "no data", "no data", "no data", "no data", "no data", "no data"]

                trx_port.insert(8, line[14:18])
                print "TRX period port 8  %s" % trx_port[8]

                trx_port.insert(9, line[18:22])
                print "%s" % trx_port[9]

                trx_port.insert(10, line[22:26])
                print "%s" % trx_port[10]

                trx_port.insert(11, line[26:30])
                print "%s" % trx_port[11]

                trx_port.insert(12, line[30:34])
                print "%s" % trx_port[12]

                trx_port.insert(13, line[34:38])
                print "%s" % trx_port[13]

                trx_port14_1 = line[38:40]

            if line.startswith('S1130180'):

                trx_port14_2 = line[8:10]
                trx_port.insert(14, trx_port14_1 + trx_port14_2)
                print "%s " % trx_port[14]

                trx_port.insert(15, line[10:14])
                print "%s" % trx_port[15]

                for j in range(8, len(trx_port)):
                    pen.writerow(
                        [int(address,16), hex(int(address,16)), "trx_port" + str(j), trx_port[j], "0", "2047", "0", "UINT 16", ""])

                print "MVB time out starts...."

                mvb_to_port = ["no data", "no data", "no data", "no data", "no data", "no data", "no data", "no data"]

                mvb_to_port.insert(8, line[14:18])
                print "mvb_timeout_port8  %s" % mvb_to_port[8]

                mvb_to_port.insert(9, line[18:22])
                print "%s " % mvb_to_port[9]

                mvb_to_port.insert(10, line[22:26])
                print "%s " % mvb_to_port[10]

                mvb_to_port.insert(11, line[26:30])
                print "%s " % mvb_to_port[11]

                mvb_to_port.insert(12, line[30:34])
                print "%s" % mvb_to_port[12]

                mvb_to_port.insert(13, line[34:38])
                print "%s" % mvb_to_port[13]

                mvb_to_port14_1 = line[38:40]

            if line.startswith('S1130190'):

                mvb_to_port14_2 = line[8:10]
                mvb_to_port.insert(14, mvb_to_port14_1 + mvb_to_port14_2)
                print "%s " % mvb_to_port[14]

                mvb_to_port.insert(15, line[10:14])
                print "%s " % mvb_to_port[15]

                for j in range(8, len(mvb_to_port)):
                    pen.writerow(
                        [int(address,16), hex(int(address,16)), "mvb_timeout_port" + str(j), mvb_to_port[j], "0", "8191", "0", "UINT 16",
                         ""])

                print "safe message identifier:  "

                op_smi_port = []

                op_smi_port.insert(0, line[14:22])
                print"output SMI port 0:  %s" % op_smi_port[0]

                op_smi_port.insert(1, line[22:30])
                print "%s " % op_smi_port[1]

                op_smi_port.insert(2, line[30:38])
                print "%s " % op_smi_port[2]

                op_smi_port3_1 = line[38:40]

            if line.startswith('S11301A0'):
                op_smi_port3_2 = line[8:14]
                op_smi_port.insert(3, op_smi_port3_1 + op_smi_port3_2)
                print "%s " % op_smi_port[3]

                op_smi_port.insert(4, line[14:22])
                print "%s " % op_smi_port[4]

                op_smi_port.insert(5, line[22:30])
                print "%s " % op_smi_port[5]

                op_smi_port.insert(6, line[30:38])
                print "%s " % op_smi_port[6]

                op_smi_port7_1 = line[38:40]

            if line.startswith('S11301B0'):

                op_smi_port7_2 = line[8:14]
                op_smi_port.insert(7, op_smi_port7_1 + op_smi_port7_2)
                print "%s " % op_smi_port[7]

                for j in range(0, len(op_smi_port)):
                    pen.writerow(
                        [int(address, 16), hex(int(address, 16)), "Output_SMI_Port" + str(j), op_smi_port[j], "0", "4294967295",
                         "0", "UINT 32", ""])

                print "SMI port starts: "

                smi_1_port = ["no data", "no data", "no data", "no data", "no data", "no data", "no data", "no data"]
                smi_2_port = ["no data", "no data", "no data", "no data", "no data", "no data", "no data", "no data"]

                smi_1_port.insert(8, line[14:22])
                print "SMI_1_port 8  %s:   " % smi_1_port[8]

                smi_2_port.insert(8, line[22:30])
                print "SMI_2_port8 %s  " % smi_2_port[8]

                smi_1_port.insert(9, line[30:38])
                print " port 9  %s " % smi_1_port[9]

                smi_2_port9_1 = line[38:40]

            if line.startswith('S11301C0'):
                smi_2_port9_2 = line[8:14]
                smi_2_port.insert(9, smi_2_port9_1 + smi_2_port9_2)
                print "%s " % smi_2_port[9]

                smi_1_port.insert(10, line[14:22])
                print "port 10 %s " % smi_1_port[10]

                smi_2_port.insert(10, line[22:30])
                print "%s " % smi_2_port[10]

                smi_1_port.insert(11, line[30:38])
                print " port 11 %s " % smi_1_port[11]

                smi_2_port11_1 = line[38:40]

            if line.startswith('S11301D0'):
                smi_2_port11_2 = line[8:14]
                smi_2_port.insert(11, smi_2_port11_1 + smi_2_port11_2)
                print " %s " % smi_2_port[11]

                smi_1_port.insert(12, line[14:22])
                print "port 12 %s " % smi_1_port[12]

                smi_2_port.insert(12, line[22:30])
                print "port 12 %s " % smi_2_port[12]

                smi_1_port.insert(13, line[30:38])
                print "port 13 %s " % smi_1_port[13]

                smi_2_port13_1 = line[38:40]

            if line.startswith('S11301E0'):
                smi_2_port13_2 = line[8:14]
                smi_2_port.insert(13, smi_2_port13_1 + smi_2_port13_2)
                print " %s " % smi_2_port[13]

                smi_1_port.insert(14, line[14:22])
                print "port 14 %s " % smi_1_port[14]

                smi_2_port.insert(14, line[22:30])
                print "port 14 %s " % smi_2_port[14]

                smi_1_port.insert(15, line[30:38])
                print "port 15 %s " % smi_1_port[15]

                smi_2_port15_1 = line[38:40]

            if line.startswith('S11301F0'):

                smi_2_port15_2 = line[8:14]
                smi_2_port.insert(15, smi_2_port15_1 + smi_2_port15_2)
                print "port 15 %s " % smi_2_port[15]

                for j in range(8, len(smi_1_port)):
                    pen.writerow([int(address, 16), hex(int(address, 16)), "SMI_1_Port" + str(j), smi_1_port[j], "0", "4294967295", "0", "UINT 32", ""])
                    pen.writerow([int(address, 16), hex(int(address, 16)), "SMI_2_Port" + str(j), smi_2_port[j], "0", "4294967295", "0", "UINT 32", ""])

                print "N_guard starts: "

                nguard_port = ["no data", "no data", "no data", "no data", "no data", "no data", "no data", "no data"]

                nguard_port.insert(8, line[14:16])
                print "N_Guard port 8: %s " % nguard_port[8]

                nguard_port.insert(9, line[16:18])
                print " %s " % nguard_port[9]

                nguard_port.insert(10, line[18:20])
                print " %s " % nguard_port[10]

                nguard_port.insert(11, line[20:22])
                print " %s " % nguard_port[11]

                nguard_port.insert(12, line[22:24])
                print " %s" % nguard_port[12]

                nguard_port.insert(13, line[24:26])
                print " %s" % nguard_port[13]

                nguard_port.insert(14, line[26:28])
                print " %s" % nguard_port[14]

                nguard_port.insert(15, line[28:30])
                print " %s" % nguard_port[15]

                for j in range(8, len(nguard_port)):
                    pen.writerow(
                        [int(address, 16), hex(int(address, 16)), "Nguard_Port" + str(j), nguard_port[j], "0", "255", "255",
                         "UINT 8", ""])

                print "NRX safe starts:  "

                nrx_safe_port = ["no data", "no data", "no data", "no data", "no data", "no data", "no data", "no data"]

                nrx_safe_port.insert(8, line[30:32])
                print " NRX safe port 8 %s " % nrx_safe_port[8]

                nrx_safe_port.insert(9, line[32:34])
                print " %s " % nrx_safe_port[9]

                nrx_safe_port.insert(10, line[34:36])
                print " %s" % nrx_safe_port[10]

                nrx_safe_port.insert(11, line[36:38])
                print " %s " % nrx_safe_port[11]

                nrx_safe_port.insert(12, line[38:40])
                print " %s " % nrx_safe_port[12]

            if line.startswith('S1130200'):

                nrx_safe_port.insert(13, line[8:10])
                print " %s " % nrx_safe_port[13]

                nrx_safe_port.insert(14, line[10:12])
                print " %s " % nrx_safe_port[14]

                nrx_safe_port.insert(15, line[12:14])
                print " %s " % nrx_safe_port[15]

                for j in range(8, len(nrx_safe_port)):
                    pen.writerow([int(address, 16), hex(int(address, 16)), "Nrxsafe_Port" + str(j), nrx_safe_port[j], "0", "255", "0", "UINT 8", ""])

                print "Ttx period starts: "

                ttx_pd_port = ["no data", "no data", "no data", "no data", "no data", "no data", "no data", "no data"]

                ttx_pd_port.insert(8, line[14:18])
                print " ttx period port 8 %s " % ttx_pd_port[8]

                ttx_pd_port.insert(9, line[18:22])
                print " %s " % ttx_pd_port[9]

                ttx_pd_port.insert(10, line[22:26])
                print " %s " % ttx_pd_port[10]

                ttx_pd_port.insert(11, line[26:30])
                print " %s " % ttx_pd_port[11]

                ttx_pd_port.insert(12, line[30:34])
                print " %s " % ttx_pd_port[12]

                ttx_pd_port.insert(13, line[34:38])
                print " %s " % ttx_pd_port[13]

                ttx_pd_port14_1 = line[38:40]

            if line.startswith('S1130210'):

                ttx_pd_port14_2 = line[8:10]
                ttx_pd_port.insert(14, ttx_pd_port14_1 + ttx_pd_port14_2)
                print "port_14 %s " % ttx_pd_port[14]

                ttx_pd_port.insert(15, line[10:14])
                print "port 15 %s " % ttx_pd_port[15]

                for j in range(8, len(ttx_pd_port)):
                    pen.writerow([int(address,16), hex(int(address,16)), "Ttx_period_Port" + str(j), ttx_pd_port[j], "0", "2047", "0", "UINT 16", ""])

            if line.startswith('S1130220'):
                req_func_inter = line[14:16]
                pen.writerow([int(address,16), hex(int(address,16)), "Required Functional Interface", req_func_inter, "", "", "", "", ""])

                ###############################  DX min time starts #############

                min_time = ["no data"]

                min_time.insert(1, line[29:30])
                min_time.insert(2, line[30:31])
                min_time.insert(3, line[31:32])
                min_time.insert(4, line[32:33])
                min_time.insert(5, line[33:34])
                min_time.insert(6, line[34:35])
                min_time.insert(7, line[35:36])
                min_time.insert(8, line[36:37])
                min_time.insert(9, line[38:39])
                min_time.insert(10, line[39:40])

            if line.startswith('S1130230'):

                min_time.insert(11, line[8:10])
                min_time.insert(12, line[10:12])

                for j in range(1, len(min_time)):
                    pen.writerow([int(address,16), hex(int(address,16)), "MIN_TIME_" + str(j), hex(int(min_time[j])), "", "", "0", "RADIO_NIBBLE", ""])

                print "DX_ADIF_Time starts: "

                dx_adf_time = ["no data"]

                dx_adf_time.insert(1, line[22:23])
                print " dx_adf_time_1 %s " % dx_adf_time[1]

                dx_adf_time.insert(2, line[23:24])
                print " %s " % dx_adf_time[2]

                dx_adf_time.insert(3, line[24:25])
                print " %s " % dx_adf_time[3]

                dx_adf_time.insert(4, line[25:26])
                print " %s " % dx_adf_time[4]

                dx_adf_time.insert(5, line[26:27])
                print " %s " % dx_adf_time[5]

                dx_adf_time.insert(6, line[27:28])
                print " %s " % dx_adf_time[6]

                dx_adf_time.insert(7, line[28:29])
                print " %s " % dx_adf_time[7]

                dx_adf_time.insert(8, line[29:30])
                print " %s " % dx_adf_time[8]

                dx_adf_time.insert(9, line[30:31])
                print " %s " % dx_adf_time[9]

                dx_adf_time.insert(10, line[31:32])
                print "%s " % dx_adf_time[10]

                dx_adf_time.insert(11, line[32:33])
                print  "%s " % dx_adf_time[11]

                dx_adf_time.insert(12, line[33:34])
                print " %s " % dx_adf_time[12]

                for j in range(1, len(dx_adf_time)):
                    pen.writerow([int(address,16), hex(int(address,16)), "DX_ADF_TIME_" + str(j), dx_adf_time[j], "", "", "0", "RADIO_NIBBLE", ""])

            if line.startswith('S1130240'):
                print "DO SAFE/REGULAR starts.... "

                do_safe_regular_ch_1_4 = line[14:16]
                print "do_safe_regular_ch_1_4"

                #################### defining each bit ###########

                data = bin(int(do_safe_regular_ch_1_4, 16))[2:]  # .zfill(8)  ## to convert string into a number of required base

                channel_1_safe = int(data) % 10
                print "%s   %s" % (channel_1_safe, data)

                channel_1_reg = (int(data) / 10) % 10
                print "%s   %s" % (channel_1_reg, data)

                channel_2_safe = (int(data) / 100) % 10
                print "%s   %s" % (channel_2_safe, data)

                channel_2_reg = (int(data) / 1000) % 10
                print "%s   %s" % (channel_2_reg, data)

                channel_3_safe = (int(data) / 10000) % 10
                print "%s   %s" % (channel_3_safe, data)

                channel_3_reg = (int(data) / 100000) % 10
                print "%s   %s" % (channel_3_reg, data)

                channel_4_safe = (int(data) / 1000000) % 10
                print "%s   %s" % (channel_4_safe, data)

                channel_4_reg = (int(data) / 10000000) % 10
                print "%s   %s" % (channel_4_reg, data)

                ###########################################################
                pen.writerow([int(address,16), hex(int(address,16)), "Channel 4 Regular", channel_4_reg, "", "", "0x0", "BIT", ""])
                pen.writerow([int(address,16), hex(int(address,16)), "Channel 4 SAFE", channel_4_safe, "", "", "0x0", "BIT", ""])
                pen.writerow([int(address,16), hex(int(address,16)), "Channel 3 Regular", channel_3_reg, "", "", "0x0", "BIT", ""])
                pen.writerow([int(address,16), hex(int(address,16)), "Channel 3 SAFE", channel_3_safe, "", "", "0x0", "BIT", ""])
                pen.writerow([int(address,16), hex(int(address,16)), "Channel 2 Regular", channel_2_reg, "", "", "0x0", "BIT", ""])
                pen.writerow([int(address,16), hex(int(address,16)), "Channel 2 SAFE", channel_2_safe, "", "", "0x0", "BIT", ""])
                pen.writerow([int(address,16), hex(int(address,16)), "Channel 1 Regular", channel_1_reg, "", "", "0x0", "BIT", ""])
                pen.writerow([int(address,16), hex(int(address,16)), "Channel 1 SAFE", channel_1_safe, "", "", "0x0", "BIT", ""])

                #############################################################

                do_safe_regular_ch_5_6 = line[16:18]
                print "do_safe_regular_ch_5_6 "

                ###################################### again defining each bit ############################

                data = bin(int(do_safe_regular_ch_5_6, 16))[2:]
                # .zfill(8)  ## to convert string into a number of required base

                channel_5_safe = int(data) % 10
                print "%s   %s" % (channel_5_safe, data)

                channel_5_reg = (int(data) / 10) % 10
                print "%s   %s" % (channel_5_reg, data)

                channel_6_safe = (int(data) / 100) % 10
                print "%s   %s" % (channel_6_safe, data)

                channel_6_reg = (int(data) / 1000) % 10
                print "%s   %s" % (channel_6_reg, data)

                ########################################################################3

                ###########################################################
                pen.writerow([int(address,16), hex(int(address,16)), "Channel 6 Regular", channel_6_reg, "", "", "0x0", "BIT", ""])
                pen.writerow([int(address,16), hex(int(address,16)), "Channel 6 SAFE", channel_6_safe, "", "", "0x0", "BIT", ""])
                pen.writerow([int(address,16), hex(int(address,16)), "Channel 5 Regular", channel_5_reg, "", "", "0x0", "BIT", ""])
                pen.writerow([int(address,16), hex(int(address,16)), "Channel 5 SAFE", channel_5_safe, "", "", "0x0", "BIT", ""])
                ###########################################################






                    ########################################### section 3 starts #########################33


            if line.startswith('S1130270'):

                #pen = csv.writer(open("C:\Users\Amijeet Kumar\Desktop\workfile.csv", 'a'))
                pen.writerow(["", "", "SECTION 3 CONFIGURATION", "", "", "", "", ""])

                SDTv2_protocol = line[30:32]
                print "SDTv2 protocol enable %s" % SDTv2_protocol
                pen.writerow(["", "", "SDTv2 Protocol Enable", sectmode(SDTv2_protocol), "", "", "", ""])

                print "output ttx period: "

                op_ttx_port = []

                op_ttx_port.insert(0, line[32:36])
                print "output_ttx_period_port0: %s" % op_ttx_port[0]

                op_ttx_port.insert(1, line[36:40])
                print "output_ttx_period_port1: %s" % op_ttx_port[1]


            if line.startswith('S1130280'):

                op_ttx_port.insert(2, line[8:12])
                print "%s" % op_ttx_port[2]


                op_ttx_port.insert(3, line[12:16])
                print "%s" % op_ttx_port[3]

                op_ttx_port.insert(4, line[16:20])
                print "%s" % op_ttx_port[4]

                op_ttx_port.insert(5, line[20:24])
                print "%s" % op_ttx_port[5]

                op_ttx_port.insert(6, line[24:28])
                print "%s " % op_ttx_port[6]


                op_ttx_port.insert(7, line[28:32])
                print "%s" % op_ttx_port[7]

                for j in range(0, len(op_ttx_port)):
                    pen.writerow([int(address,16), hex(int(address,16)), "op_ttx_port" + str(j), op_ttx_port[j], "0", "2047", "0","UINT 16", ""])

                print "TRX period starts: "

                trx_port = ["no data","no data","no data","no data","no data","no data","no data","no data"]

                trx_port.insert(8, line[32:36])
                print "TRX period port 8  %s" % trx_port[8]

                trx_port.insert(9, line[36:40])
                print "%s" % trx_port[9]


            if line.startswith('S1130290'):

                trx_port.insert(10, line[8:12])
                print "%s" % trx_port[10]

                trx_port.insert(11, line[12:16])
                print "%s" % trx_port[11]

                trx_port.insert(12, line[16:20])
                print "%s" % trx_port[12]

                trx_port.insert(13, line[20:24])
                print "%s" % trx_port[13]

                trx_port.insert(14, line[24:28])
                print "%s " %trx_port[14]

                trx_port.insert(15, line[28:32])
                print "%s" % trx_port[15]

                for j in range(8, len(trx_port)):
                    pen.writerow([int(address,16), hex(int(address,16)), "trx_port" + str(j), trx_port[j], "0", "2047", "0", "UINT 16", ""])



                print "MVB time out starts...."

                mvb_to_port = ["no data","no data","no data","no data","no data","no data","no data","no data"]

                mvb_to_port.insert(8, line[32:36])
                print "mvb_timeout_port8  %s" % mvb_to_port[8]

                mvb_to_port.insert(9, line[36:40])
                print "%s " % mvb_to_port[9]

            if line.startswith('S11302A0'):

                mvb_to_port.insert(10, line[8:12])
                print "%s " % mvb_to_port[10]

                mvb_to_port.insert(11, line[12:16])
                print "%s " % mvb_to_port[11]

                mvb_to_port.insert(12, line[16:20])
                print "%s" % mvb_to_port[12]

                mvb_to_port.insert(13, line[20:24])
                print "%s" % mvb_to_port[13]

                mvb_to_port.insert(14, line[24:28])
                print "%s " %mvb_to_port[14]

                mvb_to_port.insert(15, line[28:32])
                print "%s " % mvb_to_port[15]

                for j in range(8, len(mvb_to_port)):
                    pen.writerow([int(address, 16), hex(int(address, 16)), "mvb_timeout_port" + str(j), mvb_to_port[j], "0", "8191", "0", "UINT 16", ""])


                print "safe message identifier:  "

                op_smi_port = []

                op_smi_port.insert(0, line[32:40])
                print"output SMI port 0:  %s" % op_smi_port[0]

            if line.startswith('S11302B0'):

                op_smi_port.insert(1, line[8:16])
                print "%s " % op_smi_port[1]

                op_smi_port.insert(2, line[16:24])
                print "%s " % op_smi_port[2]

                op_smi_port.insert(3, line[24:32])
                print "%s " %op_smi_port[3]

                op_smi_port.insert(4, line[32:40])
                print "%s " % op_smi_port[4]

            if line.startswith('S11302C0'):

                op_smi_port.insert(5, line[8:16])
                print "%s " % op_smi_port[5]

                op_smi_port.insert(6, line[16:24])
                print "%s " % op_smi_port[6]

                op_smi_port.insert(7, line[24:32])
                print "%s " %op_smi_port[7]

                for j in range(0, len(op_smi_port)):
                    pen.writerow([int(address, 16), hex(int(address, 16)), "Output_SMI_Port" + str(j), op_smi_port[j], "0", "4294967295", "0", "UINT 32", ""])

                print "SMI port starts: "

                smi_1_port = ["no data","no data","no data","no data","no data","no data","no data","no data"]
                smi_2_port = ["no data","no data","no data","no data","no data","no data","no data","no data"]

                smi_1_port.insert(8, line[32:40])
                print "SMI_1_port 8  %s:   " % smi_1_port[8]

            if line.startswith('S11302D0'):

                smi_2_port.insert(8, line[8:16])
                print "SMI_2_port8 %s  " % smi_2_port[8]

                smi_1_port.insert(9, line[16:24])
                print " port 9  %s " % smi_1_port[9]

                smi_2_port.insert(9, line[24:32])
                print "%s " % smi_2_port[9]

                smi_1_port.insert(10, line[32:40])
                print "port 10 %s " % smi_1_port[10]

            if line.startswith('S11302E0'):

                smi_2_port.insert(10, line[8:16])
                print "%s " %smi_2_port[10]

                smi_1_port.insert(11, line[16:24])
                print " port 11 %s " % smi_1_port[11]

                smi_2_port.insert(11, line[24:32])
                print " %s " %smi_2_port[11]

                smi_1_port.insert(12, line[32:40])
                print "port 12 %s " % smi_1_port[12]

            if line.startswith('S11302F0'):

                smi_2_port.insert(12, line[8:16])
                print "port 12 %s " % smi_2_port[12]

                smi_1_port.insert(13, line[16:24])
                print "port 13 %s " % smi_1_port[13]

                smi_2_port.insert(13, line[24:32])
                print " %s " %smi_2_port[13]

                smi_1_port.insert(14, line[32:40])
                print "port 14 %s " % smi_1_port[14]


            if line.startswith('S1130300'):

                smi_2_port.insert(14, line[8:16])
                print "port 14 %s " %smi_2_port[14]

                smi_1_port.insert(15, line[16:24])
                print "port 15 %s " %smi_1_port[15]

                smi_2_port.insert(15, line[24:32])
                print "port 15 %s " % smi_2_port[15]

                for j in range(8, len(smi_1_port)):
                    pen.writerow([int(address, 16), hex(int(address, 16)), "SMI_1_Port" + str(j), smi_1_port[j], "0", "4294967295", "0", "UINT 32", ""])
                    pen.writerow([int(address, 16), hex(int(address, 16)), "SMI_2_Port" + str(j), smi_2_port[j], "0", "4294967295", "0", "UINT 32", ""])


                print "N_guard starts: "

                nguard_port = ["no data","no data","no data","no data","no data","no data","no data","no data"]

                nguard_port.insert(8, line[32:34])
                print "N_Guard port 8: %s " % nguard_port[8]

                nguard_port.insert(9, line[34:36])
                print " %s " % nguard_port[9]

                nguard_port.insert(10, line[36:38])
                print " %s " % nguard_port[10]

                nguard_port.insert(11, line[38:40])
                print " %s " % nguard_port[11]

            if line.startswith('S1130310'):

                nguard_port.insert(12, line[8:10])
                print " %s" % nguard_port[12]

                nguard_port.insert(13, line[10:12])
                print " %s" % nguard_port[13]

                nguard_port.insert(14, line[12:14])
                print " %s" % nguard_port[14]

                nguard_port.insert(15, line[14:16])
                print " %s" % nguard_port[15]

                for j in range(8, len(nguard_port)):
                    pen.writerow([int(address, 16), hex(int(address, 16)), "Nguard_Port" + str(j), nguard_port[j], "0", "255", "255", "UINT 8", ""])


                print "NRX safe starts:  "

                nrx_safe_port = ["no data","no data","no data","no data","no data","no data","no data","no data"]

                nrx_safe_port.insert(8, line[16:18])
                print " NRX safe port 8 %s " % nrx_safe_port[8]

                nrx_safe_port.insert(9, line[18:20])
                print " %s " % nrx_safe_port[9]

                nrx_safe_port.insert(10, line[20:22])
                print " %s" % nrx_safe_port[10]

                nrx_safe_port.insert(11, line[22:24])
                print " %s " % nrx_safe_port[11]

                nrx_safe_port.insert(12, line[24:26])
                print " %s " % nrx_safe_port[12]

                nrx_safe_port.insert(13 , line[26:28])
                print " %s " % nrx_safe_port[13]

                nrx_safe_port.insert(14, line[28:30])
                print " %s " % nrx_safe_port[14]

                nrx_safe_port.insert(15, line[30:32])
                print " %s " % nrx_safe_port[15]

                for j in range(8, len(nrx_safe_port)):
                    pen.writerow([int(address,16), hex(int(address,16)), "Nrxsafe_Port" + str(j), nrx_safe_port[j], "0", "255", "0", "UINT 8", ""])



                print "Ttx period starts: "

                ttx_pd_port = ["no data","no data","no data","no data","no data","no data","no data","no data"]

                ttx_pd_port.insert(8, line[32:36])
                print " ttx period port 8 %s " % ttx_pd_port[8]

                ttx_pd_port.insert(9, line[36:40])
                print " %s " % ttx_pd_port[9]

            if line.startswith('S1130320'):

                ttx_pd_port.insert(10, line[8:12])
                print " %s " % ttx_pd_port[10]

                ttx_pd_port.insert(11, line[12:16])
                print " %s " % ttx_pd_port[11]

                ttx_pd_port.insert(12, line[16:20])
                print " %s " % ttx_pd_port[12]

                ttx_pd_port.insert(13, line[20:24])
                print " %s " % ttx_pd_port[13]

                ttx_pd_port.insert(14, line[24:28])
                print "port_14 %s " % ttx_pd_port[14]

                ttx_pd_port.insert(15, line[28:32])
                print "port 15 %s "% ttx_pd_port[15]

                for j in range(8, len(ttx_pd_port)):
                    pen.writerow([int(address,16), hex(int(address,16)), "Ttx_period_Port" + str(j), ttx_pd_port[j], "0", "2047", "0", "UINT 16", ""])


            if line.startswith('S1130330'):
                req_func_inter = line[30:32]
                pen.writerow([int(address,16), hex(int(address,16)), "Required Functional Interface", req_func_inter, "", "", "", "", ""])
                ###############################  DX min time starts #############


            if line.startswith('S1130340'):

                min_time = []

                min_time.insert(1, line[16:17])
                min_time.insert(2, line[17:18])
                min_time.insert(3, line[18:19])
                min_time.insert(4, line[19:20])
                min_time.insert(5, line[20:21])
                min_time.insert(6, line[21:22])
                min_time.insert(7, line[22:23])
                min_time.insert(8, line[23:24])
                min_time.insert(9 , line[24:25])
                min_time.insert(10, line[25:26])
                min_time.insert(11, line[26:27])
                min_time.insert(12, line[27:28])

                for j in range(1, len(min_time)):
                    pen.writerow([int(address,16), hex(int(address,16)), "MIN_TIME_" + str(j), hex(int(min_time[j])), "", "", "0","RADIO_NIBBLE", ""])

            if line.startswith('S1130350'):
                print "DX_ADIF_Time starts: "


                dx_adf_time = ["no data"]

                dx_adf_time.insert(1, line[8:9])
                print " dx_adf_time_1 %s " %dx_adf_time[1]

                dx_adf_time.insert(2, line[9:10])
                print " %s " %dx_adf_time[2]

                dx_adf_time.insert(3, line[10:11])
                print " %s " %dx_adf_time[3]

                dx_adf_time.insert(4, line[11:12])
                print " %s " %dx_adf_time[4]

                dx_adf_time.insert(5, line[12:13])
                print " %s " %dx_adf_time[5]

                dx_adf_time.insert(6, line[13:14])
                print " %s " %dx_adf_time[6]

                dx_adf_time.insert(7, line[14:15])
                print " %s " %dx_adf_time[7]

                dx_adf_time.insert(8, line[15:16])
                print " %s " %dx_adf_time[8]

                dx_adf_time.insert(9, line[16:17])
                print " %s " %dx_adf_time[9]

                dx_adf_time.insert(10, line[17:18])
                print "%s " %dx_adf_time[10]

                dx_adf_time.insert(11, line[18:19])
                print  "%s " %dx_adf_time[11]

                dx_adf_time.insert(12, line[19:20])
                print " %s " %dx_adf_time[12]

                for j in range(1, len(dx_adf_time)):
                    pen.writerow([int(address,16), hex(int(address,16)), "DX_ADF_TIME_" + str(j), dx_adf_time[j], "", "", "0","RADIO_NIBBLE", ""])



                print "DO SAFE/REGULAR starts.... "


                do_safe_regular_ch_1_4 = line[32:34]
                print "do_safe_regular_ch_1_4 "

                #################### defining each bit ###########

                data = bin(int(do_safe_regular_ch_1_4,16))[2:]#.zfill(8)  ## to convert string into a number of required base

                channel_1_safe =  int(data) %10
                print "%s   %s" % (channel_1_safe,data)

                channel_1_reg = (int(data)/10)%10
                print "%s   %s" %(channel_1_reg,data)

                channel_2_safe = (int(data) / 100) % 10
                print "%s   %s" % (channel_2_safe, data)

                channel_2_reg = (int(data) / 1000) % 10
                print "%s   %s" % (channel_2_reg, data)

                channel_3_safe = (int(data) / 10000) % 10
                print "%s   %s" % (channel_3_safe, data)

                channel_3_reg = (int(data) / 100000) % 10
                print "%s   %s" % (channel_3_reg, data)

                channel_4_safe = (int(data) / 1000000) % 10
                print "%s   %s" % (channel_4_safe, data)

                channel_4_reg = (int(data) / 10000000) % 10
                print "%s   %s" % (channel_4_reg, data)

                ###########################################################


                ###########################################################
                pen.writerow([int(address,16), hex(int(address,16)), "Channel 4 Regular", channel_4_reg, "", "", "0x0", "BIT", ""])
                pen.writerow([int(address,16), hex(int(address,16)), "Channel 4 SAFE", channel_4_safe, "", "", "0x0", "BIT", ""])
                pen.writerow([int(address,16), hex(int(address,16)), "Channel 3 Regular", channel_3_reg, "", "", "0x0", "BIT", ""])
                pen.writerow([int(address,16), hex(int(address,16)), "Channel 3 SAFE", channel_3_safe, "", "", "0x0", "BIT", ""])
                pen.writerow([int(address,16), hex(int(address,16)), "Channel 2 Regular", channel_2_reg, "", "", "0x0", "BIT", ""])
                pen.writerow([int(address,16), hex(int(address,16)), "Channel 2 SAFE", channel_2_safe, "", "", "0x0", "BIT", ""])
                pen.writerow([int(address,16), hex(int(address,16)), "Channel 1 Regular", channel_1_reg, "", "", "0x0", "BIT", ""])
                pen.writerow([int(address,16), hex(int(address,16)), "Channel 1 SAFE", channel_1_safe, "", "", "0x0", "BIT", ""])

                #############################################################







                do_safe_regular_ch_5_6 = line[34:36]
                print "do_safe_regular_ch_5_6 "


            ###################################### again defining each bit ############################

                data = bin(int(do_safe_regular_ch_5_6, 16))[2:]
                # .zfill(8)  ## to convert string into a number of required base

                channel_5_safe = int(data) % 10
                print "%s   %s" % (channel_5_safe, data)

                channel_5_reg = (int(data) / 10) % 10
                print "%s   %s" % (channel_5_reg, data)

                channel_6_safe = (int(data) / 100) % 10
                print "%s   %s" % (channel_6_safe, data)

                channel_6_reg = (int(data) / 1000) % 10
                print "%s   %s" % (channel_6_reg, data)


            ########################################################################3


                ###########################################################
                pen.writerow([int(address,16), hex(int(address,16)), "Channel 6 Regular", channel_6_reg, "", "", "0x0", "BIT", ""])
                pen.writerow([int(address,16), hex(int(address,16)), "Channel 6 SAFE", channel_6_safe, "", "", "0x0", "BIT", ""])
                pen.writerow([int(address,16), hex(int(address,16)), "Channel 5 Regular", channel_5_reg, "", "", "0x0", "BIT", ""])
                pen.writerow([int(address,16), hex(int(address,16)), "Channel 5 SAFE", channel_5_safe, "", "", "0x0", "BIT", ""])
                ###########################################################


                ############################################3  sectoij 4 config. starts ######################################

            if line.startswith('S1130390'):

                #pen = csv.writer(open("C:\Users\Amijeet Kumar\Desktop\workfile.csv", 'a'))
                pen.writerow(["", "", "SECTION 4 CONFIGURATION", "", "", "", "", ""])

                SDTv2_protocol = line[16:18]
                print "SDTv2 protocol enable %s" % SDTv2_protocol
                pen.writerow(["", "", "SDTv2 Protocol Enable", sectmode(SDTv2_protocol), "", "", "", ""])



                print "output ttx period: "

                op_ttx_port = []

                op_ttx_port.insert(0, line[18:22])
                print "output_ttx_period_port0: %s" % op_ttx_port[0]

                op_ttx_port.insert(1, line[22:26])
                print "output_ttx_period_port1: %s" % op_ttx_port[1]



                op_ttx_port.insert(2, line[26:30])
                print "%s" % op_ttx_port[2]


                op_ttx_port.insert(3, line[30:34])
                print "%s" % op_ttx_port[3]

                op_ttx_port.insert(4, line[34:38])
                print "%s" % op_ttx_port[4]

                op_ttx_port5_1 = line[38:40]

            if line.startswith('S11303A0'):

                op_ttx_port5_2 = line[8:10]
                op_ttx_port.insert(5, op_ttx_port5_1 + op_ttx_port5_2)
                print "%s " %op_ttx_port[5]

                op_ttx_port.insert(6, line[10:14])
                print "%s " % op_ttx_port[6]


                op_ttx_port.insert(7, line[14:18])
                print "%s" % op_ttx_port[7]

                for j in range(0, len(op_ttx_port)):
                    pen.writerow([int(address, 16), hex(int(address, 16)), "op_ttx_port" + str(j), op_ttx_port[j], "0", "2047", "0", "UINT 16", ""])


                print "TRX period starts: "

                trx_port = ["no data","no data","no data","no data","no data","no data","no data","no data"]

                trx_port.insert(8 , line[18:22])
                print "TRX period port 8  %s" % trx_port[8]

                trx_port.insert(9, line[22:26])
                print "%s" % trx_port[9]


                trx_port.insert(10, line[26:30])
                print "%s" % trx_port[10]

                trx_port.insert(11, line[30:34])
                print "%s" % trx_port[11]

                trx_port.insert(12, line[34:38])
                print "%s" % trx_port[12]

                trx_port13_1 = line[38:40]

            if line.startswith('S11303B0'):

                trx_port13_2 = line[8:12]
                trx_port.insert(13, trx_port13_1 + trx_port13_2)
                print "%s " %trx_port[13]

                trx_port.insert(14, line[12:14])
                print "%s " %trx_port[14]

                trx_port.insert(15, line[14:18])
                print "%s" % trx_port[15]

                for j in range(8, len(trx_port)):
                    pen.writerow([int(address, 16), hex(int(address, 16)), "trx_port" + str(j), trx_port[j], "0", "2047", "0", "UINT 16", ""])


                print "MVB time out starts...."

                mvb_to_port = ["no data","no data","no data","no data","no data","no data","no data","no data"]

                mvb_to_port.insert(8, line[18:22])
                print "mvb_timeout_port8  %s" % mvb_to_port[8]

                mvb_to_port.insert(9, line[22:26])
                print "%s " % mvb_to_port[9]


                mvb_to_port.insert(10, line[26:30])
                print "%s " % mvb_to_port[10]

                mvb_to_port.insert(11, line[30:34])
                print "%s " % mvb_to_port[11]

                mvb_to_port.insert(12, line[34:38])
                print "%s" % mvb_to_port[12]

                mvb_to_port13_1 = line[38:40]

            if line.startswith('S11303C0'):

                mvb_to_port13_2 = line[8:10]
                mvb_to_port.insert(13, mvb_to_port13_1 + mvb_to_port13_2)
                print "port 13 %s " % mvb_to_port[13]

                mvb_to_port.insert(14, line[10:14])
                print "%s " %mvb_to_port[14]

                mvb_to_port.insert(15, line[14:18])
                print "%s " % mvb_to_port[15]

                for j in range(8, len(mvb_to_port)):
                    pen.writerow([int(address, 16), hex(int(address, 16)), "mvb_timeout_port" + str(j), mvb_to_port[j], "0", "8191", "0", "UINT 16", ""])

                print "safe message identifier:  "

                op_smi_port = []

                op_smi_port.insert(0, line[18:26])
                print"output SMI port 0:  %s" % op_smi_port[0]


                op_smi_port.insert(1, line[26:34])
                print "%s " % op_smi_port[1]

                op_smi_port2_1 = line[34:40]


            if line.startswith('S11303D0'):

                op_smi_port2_2 = line[8:10]
                op_smi_port.insert(2, op_smi_port2_1 + op_smi_port2_2)
                print "%s " % op_smi_port[2]

                op_smi_port.insert(3, line[10:18])
                print "%s " %op_smi_port[3]

                op_smi_port.insert(4, line[18:26])
                print "%s " % op_smi_port[4]

                op_smi_port.insert(5, line[26:34])
                print "%s " % op_smi_port[5]

                op_smi_port6_1 = line[34:38]

            if line.startswith('S11303E0'):

                op_smi_port6_2 = line[8:12]
                op_smi_port.insert(6, op_smi_port6_1 + op_smi_port6_2)
                print "%s " % op_smi_port[6]

                op_smi_port.insert(7, line[12:18])
                print "%s " %op_smi_port[7]

                for j in range(0, len(op_smi_port)):
                    pen.writerow([int(address, 16), hex(int(address, 16)), "Output_SMI_Port" + str(j), op_smi_port[j], "0", "4294967295", "0", "UINT 32", ""])


                print "SMI port starts: "

                smi_1_port = ["no data","no data","no data","no data","no data","no data","no data","no data"]
                smi_2_port = ["no data","no data","no data","no data","no data","no data","no data","no data"]

                smi_1_port.insert(8, line[18:26])
                print "SMI_1_port 8  %s:   " % smi_1_port[8]

                smi_2_port.insert(8, line[26:34])
                print "SMI_2_port8 %s  " % smi_2_port[8]

                smi_1_port9_1 = line[34:40]

            if line.startswith('S11303F0'):

                smi_1_port9_2 = line[8:10]
                smi_1_port.insert(9, smi_1_port9_1 + smi_1_port9_2)
                print "%s " % smi_1_port[9]

                smi_2_port.insert(9, line[10:18])
                print "%s " % smi_2_port[9]

                smi_1_port.insert(10, line[18:26])
                print "port 10 %s " % smi_1_port[10]

                smi_2_port.insert(10, line[26:34])
                print "%s " %smi_2_port[10]

                smi_1_port11_1 = line[34:40]

            if line.startswith('S1130400'):

                smi_1_port11_2 = line[8:10]
                smi_1_port.insert(11, smi_1_port11_1 + smi_1_port11_2)
                print "%s " % smi_1_port[11]

                smi_2_port.insert(11, line[10:18])
                print " %s " %smi_2_port[11]

                smi_1_port.insert(12, line[18:26])
                print "port 12 %s " % smi_1_port[12]

                smi_2_port.insert(12, line[26:34])
                print "port 12 %s " % smi_2_port[12]

                smi_1_port13_1 = line[34:40]

            if line.startswith('S1130410'):

                smi_1_port13_2 = line[8:10]
                smi_1_port.insert(13, smi_1_port13_1 + smi_1_port13_2)
                print "%s " % smi_1_port[13]

                smi_2_port.insert(13, line[10:18])
                print " %s " %smi_2_port[13]

                smi_1_port.insert(14, line[18:26])
                print "port 14 %s " % smi_1_port[14]

                smi_2_port.insert(14, line[26:34])
                print "port 14 %s " %smi_2_port[14]

                smi_1_port15_1  = line[34:40]

            if line.startswith('S1130420'):

                smi_1_port15_2 = line[8:10]
                smi_1_port.insert(15, smi_1_port15_1 + smi_1_port15_2)
                print "%s " % smi_1_port[15]

                smi_2_port.insert(15, line[10:18])
                print "port 15 %s " % smi_2_port[15]

                for j in range(8, len(smi_1_port)):
                    pen.writerow([int(address, 16), hex(int(address, 16)), "SMI_1_Port" + str(j), smi_1_port[j], "0", "4294967295", "0", "UINT 32", ""])
                    pen.writerow([int(address, 16), hex(int(address, 16)), "SMI_2_Port" + str(j), smi_2_port[j], "0", "4294967295", "0", "UINT 32", ""])


                print "N_guard starts: "

                nguard_port = ["no data","no data","no data","no data","no data","no data","no data","no data"]

                nguard_port.insert(8, line[18:20])
                print "N_Guard port 8: %s " % nguard_port[8]

                nguard_port.insert(9, line[20:22])
                print " %s " % nguard_port[9]

                nguard_port.insert(10, line[22:24])
                print " %s " % nguard_port[10]

                nguard_port.insert(11, line[24:26])
                print " %s " % nguard_port[11]

                nguard_port.insert(12, line[26:28])
                print " %s" % nguard_port[12]

                nguard_port.insert(13, line[28:30])
                print " %s" % nguard_port[13]

                nguard_port.insert(14, line[30:32])
                print " %s" % nguard_port[14]

                nguard_port.insert(15, line[32:34])
                print " %s" % nguard_port[15]

                for j in range(8, len(nguard_port)):
                    pen.writerow([int(address, 16), hex(int(address, 16)), "Nguard_Port" + str(j), nguard_port[j], "0", "255", "255", "UINT 8", ""])


                print "NRX safe starts:  "

                nrx_safe_port = ["no data","no data","no data","no data","no data","no data","no data","no data"]

                nrx_safe_port.insert(8, line[34:36])
                print " NRX safe port 8 %s " % nrx_safe_port[8]

                nrx_safe_port.insert(9, line[36:38])
                print " %s " % nrx_safe_port[9]

                nrx_safe_port.insert(10, line[38:40])
                print " %s" % nrx_safe_port[10]

            if line.startswith('S1130430'):

                nrx_safe_port.insert(11, line[8:10])
                print " %s " % nrx_safe_port[11]

                nrx_safe_port.insert(12, line[10:12])
                print " %s " % nrx_safe_port[12]

                nrx_safe_port.insert(13 , line[12:14])
                print " %s " % nrx_safe_port[13]

                nrx_safe_port.insert(14, line[14:16])
                print " %s " % nrx_safe_port[14]

                nrx_safe_port.insert(15, line[16:18])
                print " %s " % nrx_safe_port[15]

                for j in range(8, len(nrx_safe_port)):
                    pen.writerow([int(address,16), hex(int(address,16)), "Nrxsafe_Port" + str(j), nrx_safe_port[j], "0", "255", "0","UINT 8", ""])


                print "Ttx period starts: "

                ttx_pd_port = ["no data","no data","no data","no data","no data","no data","no data","no data"]

                ttx_pd_port.insert(8, line[18:20])
                print " ttx period port 8 %s " % ttx_pd_port[8]

                ttx_pd_port.insert(9, line[20:22])
                print " %s " % ttx_pd_port[9]

                ttx_pd_port.insert(10, line[22:24])
                print " %s " % ttx_pd_port[10]

                ttx_pd_port.insert(11, line[24:26])
                print " %s " % ttx_pd_port[11]

                ttx_pd_port.insert(12, line[26:28])
                print " %s " % ttx_pd_port[12]

                ttx_pd_port.insert(13, line[28:30])
                print " %s " % ttx_pd_port[13]

                ttx_pd_port.insert(14, line[30:32])
                print "port_14 %s " % ttx_pd_port[14]

                ttx_pd_port.insert(15, line[32:34])
                print "port 15 %s "% ttx_pd_port[15]

                for j in range(8, len(ttx_pd_port)):
                    pen.writerow([int(address,16), hex(int(address,16)), "Ttx_period_Port" + str(j), ttx_pd_port[j], "0", "2047", "0", "UINT 16", ""])


            if line.startswith('S1130450'):
                req_func_inter = line[18:20]
                pen.writerow([int(address,16), hex(int(address,16)), "Required Functional Interface", req_func_inter, "", "", "", "", ""])

                ###############################  DX min time starts #############


                min_time = ["no data"]


                min_time.insert(1, line[34:35])
                min_time.insert(2 , line[35:36])
                min_time.insert(3, line[36:37])
                min_time.insert(4, line[37:38])
                min_time.insert(5, line[38:39])
                min_time.insert(6, line[39:40])
            if line.startswith('S1130460'):
                min_time.insert(7, line[8:9])
                min_time.insert(8, line[9:10])
                min_time.insert(9, line[10:11])
                min_time.insert(10, line[11:12])
                min_time.insert(11, line[12:13])
                min_time.insert(12, line[13:14])

                for j in range(1, len(min_time)):
                    pen.writerow([int(address,16), hex(int(address,16)), "MIN_TIME_" + str(j), hex(int(min_time[j])), "", "", "0", "RADIO_NIBBLE", ""])



                print "DX_ADIF_Time starts: "

                dx_adf_time = ["no data"]

                dx_adf_time.insert(1, line[26:27])
                print " dx_adf_time_1 %s " %dx_adf_time[1]

                dx_adf_time.insert(2, line[27:28])
                print " %s " %dx_adf_time[2]

                dx_adf_time.insert(3, line[28:29])
                print " %s " %dx_adf_time[3]

                dx_adf_time.insert(4, line[29:30])
                print " %s " %dx_adf_time[4]

                dx_adf_time.insert(5, line[30:31])
                print " %s " %dx_adf_time[5]

                dx_adf_time.insert(6, line[31:32])
                print " %s " %dx_adf_time[6]

                dx_adf_time.insert(7, line[32:33])
                print " %s " %dx_adf_time[7]

                dx_adf_time.insert(8, line[33:34])
                print " %s " %dx_adf_time[8]

                dx_adf_time.insert(9, line[34:35])
                print " %s " %dx_adf_time[9]

                dx_adf_time.insert(10, line[35:36])
                print "%s " %dx_adf_time[10]

                dx_adf_time.insert(11, line[36:37])
                print  "%s " %dx_adf_time[11]

                dx_adf_time.insert(12, line[37:38])
                print " %s " %dx_adf_time[12]

                for j in range(1, len(dx_adf_time)):
                    pen.writerow([int(address,16), hex(int(address,16)), "DX_ADF_TIME_" + str(j), dx_adf_time[j], "", "", "0", "RADIO_NIBBLE", ""])


            if line.startswith('S1130470'):
                print "DO SAFE/REGULAR starts.... "

                do_safe_regular_ch_1_4 = line[18:20]
                print "do_safe_regular_ch_1_4 "

                #################### defining each bit ###########

                data = bin(int(do_safe_regular_ch_1_4, 16))[2:]  # .zfill(8)  ## to convert string into a number of required base

                channel_1_safe = int(data) % 10
                print "%s   %s" % (channel_1_safe, data)

                channel_1_reg = (int(data) / 10) % 10
                print "%s   %s" % (channel_1_reg, data)

                channel_2_safe = (int(data) / 100) % 10
                print "%s   %s" % (channel_2_safe, data)

                channel_2_reg = (int(data) / 1000) % 10
                print "%s   %s" % (channel_2_reg, data)

                channel_3_safe = (int(data) / 10000) % 10
                print "%s   %s" % (channel_3_safe, data)

                channel_3_reg = (int(data) / 100000) % 10
                print "%s   %s" % (channel_3_reg, data)

                channel_4_safe = (int(data) / 1000000) % 10
                print "%s   %s" % (channel_4_safe, data)

                channel_4_reg = (int(data) / 10000000) % 10
                print "%s   %s" % (channel_4_reg, data)

                ###########################################################

                ###########################################################
                pen.writerow([int(address,16), hex(int(address,16)), "Channel 4 Regular", channel_4_reg, "", "", "0x0", "BIT", ""])
                pen.writerow([int(address,16), hex(int(address,16)), "Channel 4 SAFE", channel_4_safe, "", "", "0x0", "BIT", ""])
                pen.writerow([int(address,16), hex(int(address,16)), "Channel 3 Regular", channel_3_reg, "", "", "0x0", "BIT", ""])
                pen.writerow([int(address,16), hex(int(address,16)), "Channel 3 SAFE", channel_3_safe, "", "", "0x0", "BIT", ""])
                pen.writerow([int(address,16), hex(int(address,16)), "Channel 2 Regular", channel_2_reg, "", "", "0x0", "BIT", ""])
                pen.writerow([int(address,16), hex(int(address,16)), "Channel 2 SAFE", channel_2_safe, "", "", "0x0", "BIT", ""])
                pen.writerow([int(address,16), hex(int(address,16)), "Channel 1 Regular", channel_1_reg, "", "", "0x0", "BIT", ""])
                pen.writerow([int(address,16), hex(int(address,16)), "Channel 1 SAFE", channel_1_safe, "", "", "0x0", "BIT", ""])

                #############################################################




                do_safe_regular_ch_5_6 = line[20:22]
                print "do_safe_regular_ch_5_6 "

                ###################################### again defining each bit ############################

                data = bin(int(do_safe_regular_ch_5_6, 16))[2:]
                # .zfill(8)  ## to convert string into a number of required base

                channel_5_safe = int(data) % 10
                print "%s   %s" % (channel_5_safe, data)

                channel_5_reg = (int(data) / 10) % 10
                print "%s   %s" % (channel_5_reg, data)

                channel_6_safe = (int(data) / 100) % 10
                print "%s   %s" % (channel_6_safe, data)

                channel_6_reg = (int(data) / 1000) % 10
                print "%s   %s" % (channel_6_reg, data)


                ########################################################################3


                ###########################################################
                pen.writerow([int(address,16), hex(int(address,16)), "Channel 6 Regular", channel_6_reg, "", "", "0x0", "BIT", ""])
                pen.writerow([int(address,16), hex(int(address,16)), "Channel 6 SAFE", channel_6_safe, "", "", "0x0", "BIT", ""])
                pen.writerow([int(address,16), hex(int(address,16)), "Channel 5 Regular", channel_5_reg, "", "", "0x0", "BIT", ""])
                pen.writerow([int(address,16), hex(int(address,16)), "Channel 5 SAFE", channel_5_safe, "", "", "0x0", "BIT", ""])
                ###########################################################



                ###### definition of CRC 32 _ trans should come here........

            if line.startswith('S11304A0'):
                    crc32_trans_1 = line[34:40]
            if line.startswith('S11304B0'):
                    crc32_trans_2 = line[8:10]

                    crc32_trans = crc32_trans_1 + crc32_trans_2

                    print "crc32_trans  %s" %crc32_trans
                    pen.writerow([int(address , 16), hex(int(address , 16)), "CRC 32 TRANS", crc32_trans, "","","","CRC 32 TRANS",""])





if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('MyWindow')

    main = MyWindow(location)
    main.show()

    path = main.get_fname()
    print path
    print "yes that's the path (above)"


    decode()


    sys.exit(app.exec_())
