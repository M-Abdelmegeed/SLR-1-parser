from re import X
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi
import nltk
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
from nltk import pos_tag, word_tokenize, RegexpParser
# Obtaining the token list

import re



class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("phase2.ui", self)
        self.browse.clicked.connect(self.browsefiles)
        self.proceed.clicked.connect(self.gotoScreen2)

    def browsefiles(self):
        fname = QFileDialog.getOpenFileName(
            self, 'C:/Users/DELL/Desktop', '*.txt')
        self.filename.setText(fname[0])
        global txt
        txt = fname[0]

    def gotoScreen2(self):

        screen2 = Screen2()
        widget.addWidget(screen2)
        widget.setCurrentIndex(widget.currentIndex()+1)


class Screen2(QDialog):
    def __init__(self):
        super(Screen2, self).__init__()
        loadUi("screen2.ui", self)
        self.back.clicked.connect(self.gotomainpage)
        self.parse.clicked.connect(self.parsing)
        
        
   

    def gotomainpage(self):
        mainwindow = MainWindow()
        widget.addWidget(mainwindow)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def parsing(self):
        file = open(txt)
        operators = {'=':'EQUAL',':=' : 'ASSIGN','+' : 'PLUS','-' : 'MINUS','/' : 'DIV','*' : 'MULT','<' : 'LESSTHAN','>' : 'GREATERTHAN' }
        operators_key = operators.keys()

        data_type = {'int' : 'INTEGER TYPE', 'float': 'FLOATING POINT' , 'char' : 'CHARACTER TYPE', 'long' : 'LONG INT' }
        data_type_key = data_type.keys()

        punctuation_symbol = { ':' : 'COLON', ';' : 'SEMI-COLON', '.' : 'DOT' , ',' : 'COMMA' }
        punctuation_symbol_key = punctuation_symbol.keys()

        identifier = {"ID":['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l','m', "n", "o", "p", "q", "r", "s", 't', 'u', 'v', "x", 'y','z','xyz','A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L','M', "N", "O", "P", "Q", "R", "S", 'T', 'U', 'V', "X", 'Y','Z','XYZ']}
        identifier_key = identifier.keys()
        identifier_values=identifier.values()
        arrval=[]
        for value in identifier_values:
            arrval=value


        key_words={'if':'IF', 'then':'THEN', 'end':'END', 'else':'ELSE','read':'READ', 'write':'WRITE', 'until':'UNTIL', 'repeat':'REPEAT'}
        key_word_keys=key_words.keys()


        a_list = list(range(1, 10000))
        a_list=str(a_list)
        numbers={"NUMBER":a_list}
        number_values=numbers.values()
        arrvalnum=[]
        for value in number_values:
            arrvalnum=value
        for i in range(0, len(arrvalnum)):
            if arrvalnum[i]=="":
                arrvalnum.remove(arrvalnum[i])
        dataFlag = False

        a=file.read()
        tokenType=[];
        oringinalTokens=[];
        originalTokens=a.split(" ")
        count=0
        program = a.split("\n")
        for line in program:
            count = count + 1
            # print("line#" , count, "\n" , line)
            tokens=line.split(' ')
            while("" in tokens) :
                tokens.remove("")
            # # print("Tokens are " , tokens)
            # print("Line#", count, "properties \n")
            for token in tokens:
                if token in operators_key:
                    # print('<' + token + " , " + operators[token] + '>')
                    tokenType.append(operators[token]);
                elif token in data_type_key:
                    # print("datatype is", data_type[token])
                    tokenType.append(data_type[token]);
                elif token in punctuation_symbol_key:
                    # print ('<' + token + " , " + punctuation_symbol[token] + '>')
                    tokenType.append(punctuation_symbol[token]);
                elif token in arrvalnum:
                    # print ('<' + token + " , " + "NUMBER" + '>')
                    tokenType.append("NUMBER");
                elif token in key_words:
                    # print ('<' + token + " , " + key_words[token] + '>' )
                    tokenType.append(key_words[token]);
                        # if token in arrval:
                elif bool(re.match('[A-Za-z][A-Za-z0-9]*', token)):
                    # print('<' + token + " , " + "ID" + '>')
                    tokenType.append("ID");
                        
            dataFlag=False
            # print("_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _")
            # print("")
            # print(tokenType)
            # print(originalTokens)


        # Example text

        # Find all parts of speech in above sentence
        # tagged = pos_tag(tokenType)
        # print(tagged)


        tagged2 = list(zip(originalTokens,tokenType))
        print(tagged2)

        #Extract all parts of speech from any text
        # case_grammar = RegexpParser("""
        #                             stmt-seq: {<stmt-seq statement | statement>} #
        #                             statement: {<if-stmt | assign-stmt >}#
        #                             if-stmt: {<IF NUMBER THEN stmt-seq END >}#
        #                             assign-stmt: {<ID ASSIGN factor SEMI-COLON>} #
        #                             factor: {<ID | NUMBER>} #
        #                             """)
        case_grammar2 =         nltk.CFG.fromstring("""
                                    stmt-seq -> stmt-seq statement | statement
                                    statement -> if-stmt | assign-stmt
                                    if-stmt -> 'IF' 'NUMBER' 'THEN' stmt-seq 'END'
                                    assign-stmt -> 'ID' 'ASSIGN' factor 'SEMI-COLON'
                                    factor -> 'ID' | 'NUMBER'
                                    """)

        # Print all parts of speech in above sentence
        # output = case_grammar.parse(tagged2)

        parser = nltk.ChartParser(case_grammar2)
        output2 =parser.parse(tokenType)

        for tree in parser.parse(tokenType):
            print(tree)
            tree.draw()
            

    
    
        


app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
mainwindow = MainWindow()
widget.addWidget(mainwindow)
widget.setFixedWidth(959)
widget.setFixedHeight(872)
widget.setWindowTitle("Phase 2")
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")
