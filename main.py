#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import time

import pkuseg
import jieba
import jieba.posseg as posseg
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTabWidget

from common.convert_txt import txt_format_2_utf8
from common.file_tools import merge_two_txt, get_files_by_suffix, merge_all_txt, write_file
from PyQt5.Qt import QIcon
from common.log import logger

# 以默认配置加载模型 启动时初始化，减少后面加载的性能时间
logger.info('Running...')
logger.info('加载初始化中，请您耐心等待...')
seg = pkuseg.pkuseg(postag=True)  # 加载默认模型
jieba.initialize()  # 初始化jieba分词


class Ui_TabWidget(QTabWidget):
    def __init__(self, parent=None):
        super(Ui_TabWidget, self).__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("NLP常用工具")
        self.setObjectName("TabWidget")
        self.resize(640, 480)
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")

        self.addTab(self.tab, "")
        self.addTab(self.tab_2, "")
        self.addTab(self.tab_3, "")
        self.addTab(self.tab_4, "")

        self.tab1UI()
        self.tab2UI()
        self.tab3UI()
        self.tab4UI()
        self.retranslateUi(self)
        self.setCurrentIndex(0)
        self.pushButton_1_txt.clicked.connect(self.pushButton_1_txt.showMenu)
        QtCore.QMetaObject.connectSlotsByName(self)

    def tab1UI(self):
        self.pushButton_1_txt = QtWidgets.QPushButton(self.tab)
        self.pushButton_1_txt.setGeometry(QtCore.QRect(70, 45, 140, 40))  # 前两个参数是组件的左上角的位置，后面是组件的宽度和高度
        self.pushButton_1_txt.setObjectName("pushButton_1_txt")
        self.pushButton_2_txt = QtWidgets.QPushButton(self.tab)
        self.pushButton_2_txt.setGeometry(QtCore.QRect(70, 95, 141, 41))
        self.pushButton_2_txt.setObjectName("pushButton_2_txt")
        self.pushButton_2_txt_merged = QtWidgets.QPushButton(self.tab)
        self.pushButton_2_txt_merged.setGeometry(QtCore.QRect(70, 145, 141, 41))
        self.pushButton_2_txt_merged.setObjectName("pushButton_2_txt_merged")
        self.textEdit_1_txt = QtWidgets.QTextEdit(self.tab)
        self.textEdit_1_txt.setGeometry(QtCore.QRect(220, 49, 380, 32))
        self.textEdit_1_txt.setObjectName("textEdit_1_txt")
        self.textEdit_2_txt = QtWidgets.QTextEdit(self.tab)
        self.textEdit_2_txt.setGeometry(QtCore.QRect(220, 100, 380, 32))
        self.textEdit_2_txt.setObjectName("textEdit_2_txt")
        self.textEdit_2_txt_merged = QtWidgets.QTextEdit(self.tab)
        self.textEdit_2_txt_merged.setGeometry(QtCore.QRect(220, 150, 380, 32))
        self.textEdit_2_txt_merged.setObjectName("textEdit_2_txt_merged")

    def tab2UI(self):
        self.pushButton_txt_folder = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_txt_folder.setGeometry(QtCore.QRect(70, 45, 140, 40))
        self.pushButton_txt_folder.setObjectName("pushButton_txt_folder")
        self.pushButton_txt_folder_merged = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_txt_folder_merged.setGeometry(QtCore.QRect(70, 95, 141, 41))
        self.pushButton_txt_folder_merged.setObjectName("pushButton_txt_folder_merged")
        self.textEdit_txt_folder = QtWidgets.QTextEdit(self.tab_2)
        self.textEdit_txt_folder.setGeometry(QtCore.QRect(220, 49, 380, 32))
        self.textEdit_txt_folder.setObjectName("textEdit_txt_folder")
        self.textEdit_txt_folder_merged = QtWidgets.QTextEdit(self.tab_2)
        self.textEdit_txt_folder_merged.setGeometry(QtCore.QRect(220, 100, 380, 32))
        self.textEdit_txt_folder_merged.setObjectName("textEdit_txt_folder_merged")

    def tab3UI(self):
        # 【按钮】自定义字典
        self.pushButton_pku_self_dict = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_pku_self_dict.setGeometry(QtCore.QRect(70, 5, 140, 40))
        self.pushButton_pku_self_dict.setObjectName("pushButton_pku_self_dict")
        # 【按钮】打开txt文件夹
        self.pushButton_pku_txt = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_pku_txt.setGeometry(QtCore.QRect(70, 45, 140, 40))
        self.pushButton_pku_txt.setObjectName("pushButton_pku_txt")
        # 【按钮】pku 分词
        self.pushButton_pku_segment = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_pku_segment.setGeometry(QtCore.QRect(70, 95, 141, 41))
        self.pushButton_pku_segment.setObjectName("pushButton_pku_segment")
        # 【按钮】pku 词性标注
        self.pushButton_pku_pos = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_pku_pos.setGeometry(QtCore.QRect(70, 255, 141, 41))
        self.pushButton_pku_pos.setObjectName("pushButton_pku_pos")
        # 【按钮】自定义字典 词性标注——右边的文本框
        self.textEdit_pku_self_dict = QtWidgets.QTextEdit(self.tab_3)
        self.textEdit_pku_self_dict.setGeometry(QtCore.QRect(220, 9, 380, 32))  # 前两个参数是组件的左上角的位置，后面是组件的宽度和高度
        self.textEdit_pku_self_dict.setObjectName("textEdit_pku_self_dict")
        # 【按钮】打开txt文件夹 ——右边的文本框
        self.textEdit_pku_txt = QtWidgets.QTextEdit(self.tab_3)
        self.textEdit_pku_txt.setGeometry(QtCore.QRect(220, 49, 380, 32))
        self.textEdit_pku_txt.setObjectName("textEdit_pku_txt")
        # 【按钮】pku 分词 ——右边的文本框
        self.textEdit_pku_segment = QtWidgets.QTextEdit(self.tab_3)
        self.textEdit_pku_segment.setGeometry(QtCore.QRect(220, 100, 380, 150))
        self.textEdit_pku_segment.setObjectName("textEdit_pku_segment")
        # 【按钮】pku 词性标注——右边的文本框
        self.textEdit_pku_pos = QtWidgets.QTextEdit(self.tab_3)
        self.textEdit_pku_pos.setGeometry(QtCore.QRect(220, 260, 380, 150))
        self.textEdit_pku_pos.setObjectName("textEdit_pku_pos")

    def tab4UI(self):
        self.pushButton_jieba_self_dict = QtWidgets.QPushButton(self.tab_4)
        self.pushButton_jieba_self_dict.setGeometry(QtCore.QRect(70, 5, 140, 40))
        self.pushButton_jieba_self_dict.setObjectName("pushButton_jieba_self_dict")

        self.pushButton_jieba_txt = QtWidgets.QPushButton(self.tab_4)
        self.pushButton_jieba_txt.setGeometry(QtCore.QRect(70, 45, 140, 40))
        self.pushButton_jieba_txt.setObjectName("pushButton_jieba_txt")

        self.pushButton_jieba_segment = QtWidgets.QPushButton(self.tab_4)
        self.pushButton_jieba_segment.setGeometry(QtCore.QRect(70, 95, 141, 41))
        self.pushButton_jieba_segment.setObjectName("pushButton_jieba_segment")

        self.pushButton_jieba_pos = QtWidgets.QPushButton(self.tab_4)
        self.pushButton_jieba_pos.setGeometry(QtCore.QRect(70, 260, 141, 41))
        self.pushButton_jieba_pos.setObjectName("pushButton_jieba_pos")

        # 【按钮】自定义字典 词性标注——右边的文本框
        self.textEdit_jieba_self_dict = QtWidgets.QTextEdit(self.tab_4)
        self.textEdit_jieba_self_dict.setGeometry(QtCore.QRect(220, 9, 380, 32))  # 前两个参数是组件的左上角的位置，后面是组件的宽度和高度
        self.textEdit_jieba_self_dict.setObjectName("textEdit_jieba_self_dict")

        self.textEdit_jieba_txt = QtWidgets.QTextEdit(self.tab_4)
        self.textEdit_jieba_txt.setGeometry(QtCore.QRect(220, 49, 380, 32))
        self.textEdit_jieba_txt.setObjectName("textEdit_jieba_txt")

        self.textEdit_jieba_segment = QtWidgets.QTextEdit(self.tab_4)
        self.textEdit_jieba_segment.setGeometry(QtCore.QRect(220, 100, 380, 150))
        self.textEdit_jieba_segment.setObjectName("textEdit_jieba_segment")

        self.textEdit_jieba_pos = QtWidgets.QTextEdit(self.tab_4)
        self.textEdit_jieba_pos.setGeometry(QtCore.QRect(220, 260, 385, 150))
        self.textEdit_jieba_pos.setObjectName("textEdit_jieba_pos")

    def retranslateUi(self, TabWidget):
        _translate = QtCore.QCoreApplication.translate
        TabWidget.setWindowTitle(_translate("TabWidget", "☁️NLP工具小助手☁️"))
        # 【合并2个txt】第1个tab
        self.pushButton_1_txt.setText(_translate("TabWidget", "打开第1个txt文件"))
        self.pushButton_2_txt.setText(_translate("TabWidget", "打开第2个txt文件"))
        self.pushButton_2_txt_merged.setText(_translate("TabWidget", "合并2个txt文件"))
        TabWidget.setTabText(TabWidget.indexOf(self.tab), _translate("TabWidget", "合并2个txt"))
        # 【合并txt文件夹】第2个tab
        self.pushButton_txt_folder.setText(_translate("TabWidget", "打开文件夹"))
        self.pushButton_txt_folder_merged.setText(_translate("TabWidget", "合并所有txt文件"))
        TabWidget.setTabText(TabWidget.indexOf(self.tab_2), _translate("TabWidget", "合并txt文件夹"))
        # 【pku分词】第3个tab
        self.pushButton_pku_self_dict.setText(_translate("TabWidget", "自定义词典"))
        self.textEdit_pku_self_dict.setText(_translate("TabWidget", "默认不加载"))
        self.pushButton_pku_txt.setText(_translate("TabWidget", "打开txt文件夹"))
        self.pushButton_pku_segment.setText(_translate("TabWidget", "pku分词"))
        self.pushButton_pku_pos.setText(_translate("TabWidget", "pku词性标注"))
        TabWidget.setTabText(TabWidget.indexOf(self.tab_3), _translate("TabWidget", "pku分词与标注"))
        # 【结巴分词】第4个tab
        self.pushButton_jieba_self_dict.setText(_translate("TabWidget", "自定义词典"))
        self.textEdit_jieba_self_dict.setText(_translate("TabWidget", "默认不加载"))
        self.pushButton_jieba_txt.setText(_translate("TabWidget", "打开txt文件夹"))
        self.pushButton_jieba_segment.setText(_translate("TabWidget", "结巴分词"))
        self.pushButton_jieba_pos.setText(_translate("TabWidget", "结巴词性标注"))
        TabWidget.setTabText(TabWidget.indexOf(self.tab_4), _translate("TabWidget", "结巴分词与标注"))


class MyMainForm(Ui_TabWidget, QMainWindow):
    def __init__(self):
        super(MyMainForm, self).__init__()
        # 【合并2个txt】第1个tab
        self.pushButton_1_txt.clicked.connect(self.openFile_first)
        self.pushButton_2_txt.clicked.connect(self.openFile_second)
        self.pushButton_2_txt_merged.clicked.connect(self.two_txt_merge)
        # 【合并txt文件夹】第2个tab
        self.pushButton_txt_folder.clicked.connect(self.openFolder)
        self.pushButton_txt_folder_merged.clicked.connect(self.folder_all_txt_merge)
        # 【pku分词】第3个tab
        self.pushButton_pku_self_dict.clicked.connect(self.pku_open_self_dict)
        self.pushButton_pku_txt.clicked.connect(self.pku_openFile_txt)
        self.pushButton_pku_segment.clicked.connect(self.pku_seg_txt)
        self.pushButton_pku_pos.clicked.connect(self.pku_pos_txt)
        # 【结巴分词】第4个tab
        self.pushButton_jieba_self_dict.clicked.connect(self.jieba_open_self_dict)
        self.pushButton_jieba_txt.clicked.connect(self.jieba_openFile_txt)
        self.pushButton_jieba_segment.clicked.connect(self.jieba_seg_txt)
        self.pushButton_jieba_pos.clicked.connect(self.jieba_pos_txt)

        self.first_txt_path = ''
        self.second_txt_path = ''
        self.merge_txt_path = ''
        self.selected_txt_folder = ''
        self.pku_open_self_dict_path = ''
        self.pku_txt_path = ''
        self.pku_text_cut_to_pos = []
        self.pku_pos_dict = []
        self.jieba_open_self_dict_path = ''
        self.jiaba_txt = ''
        self.jiaba_txt_folder = ''
        self.jieba_txt_path = ''
        self.jieba_text_cut_to_pos = ''

        self.setWindowIcon(QIcon('data/安卓小人.jpg'))

    def openFile_first(self):
        get_filename_path, ok = QFileDialog.getOpenFileName(self,
                                                            "选取单个文件",
                                                            "C:/",
                                                            "All Files (*);;Text Files (*.txt)")
        if ok:
            self.textEdit_1_txt.setText(str(get_filename_path))
            self.first_txt_path = str(get_filename_path)

    def openFile_second(self):
        get_filename_path, ok = QFileDialog.getOpenFileName(self,
                                                            "选取单个文件",
                                                            "C:/",
                                                            "All Files (*);;Text Files (*.txt)")
        if ok:
            self.textEdit_2_txt.setText(str(get_filename_path))
            self.second_txt_path = str(get_filename_path)

    # 合并2个txt文本
    def two_txt_merge(self):
        if not self.first_txt_path or not self.second_txt_path:
            self.textEdit_2_txt_merged.setText(str('[请您请选择要合并的txt...]'))
            return
        try:
            self.textEdit_2_txt_merged.setText('[合并中...]')
            # 这里需要指定2个txt合并后的保存路径
            merge_file_path = merge_two_txt(self.first_txt_path, self.second_txt_path, save_file_path=r'./outputs/')
            # 在编辑框显示合并后的文件名称
            self.textEdit_2_txt_merged.setText('[合并完成]' + str(merge_file_path))
        except Exception as e:
            self.textEdit_2_txt_merged.setText('[合并出现异常！！！]')
            logger.error(f'合并2个txt文本 异常：{e}')

    def openFolder(self):
        get_directory_path = QFileDialog.getExistingDirectory(self,
                                                              "选取指定文件夹",
                                                              "C:/")
        self.textEdit_txt_folder.setText(str(get_directory_path))
        self.selected_txt_folder = str(get_directory_path)

    # 合并文件夹所有txt
    def folder_all_txt_merge(self):
        if not self.selected_txt_folder:
            self.textEdit_txt_folder_merged.setText(str('[请您点击上面的打开txt文件夹...]'))
            return
        try:
            self.textEdit_txt_folder_merged.setText('[合并中...]')
            all_txt_list = get_files_by_suffix(path=self.selected_txt_folder, suffix_name='.txt')
            # 这里需要指定2个txt合并后的保存路径
            merge_file_path = merge_all_txt(all_txt_list, save_file_path=r'./outputs/')
            # 在编辑框显示all合并后的文件名称
            self.textEdit_txt_folder_merged.setText('[合并完成]' + str(merge_file_path))
        except Exception as e:
            self.textEdit_txt_folder_merged.setText('[合并出现异常！！！]')
            logger.error(f'合并文件夹所有txt 异常：{e}')

    # 3.
    # 打开文件夹 ，从原来的打开文件改为文件夹
    def pku_open_self_dict(self):
        get_filename_path, ok = QFileDialog.getOpenFileName(self,
                                                            "选取单个文件",
                                                            "C:/",
                                                            "All Files (*);;Text Files (*.txt)")
        if ok:
            self.textEdit_pku_self_dict.setText(str(get_filename_path))
            self.pku_open_self_dict_path = str(get_filename_path)

    # 打开文件夹 ，从原来的打开文件改为文件夹
    def pku_openFile_txt(self):
        # get_filename_path, ok = QFileDialog.getOpenFileName(self,
        #                                                     "选取单个文件",
        #                                                     "C:/",
        #                                                     "All Files (*);;Text Files (*.txt)")
        # if ok:
        #     self.textEdit_pku_txt.setText(str(get_filename_path))
        #     self.pku_txt_path = str(get_filename_path)

        get_directory_path = QFileDialog.getExistingDirectory(self,
                                                              "选取指定文件夹",
                                                              "C:/")
        self.pku_txt_path = str(get_directory_path)
        # 将结果展示到QT上
        self.textEdit_pku_txt.setText(str(get_directory_path))

    # pku 分词
    # 3.“pku分词与词性标注”与“结巴分词与标注” 读取文件都是单个文件，可否改为读取文件夹
    def pku_seg_txt(self):
        if not self.pku_txt_path:
            self.textEdit_pku_segment.setText(str('[请您点击上面的打开txt文件夹...]'))
            return
        logger.info(f'[pku分词]打开pku文件{self.pku_txt_path}')
        self.textEdit_pku_segment.setText(str('[pku分词中...]'))
        # 选择自定义词典
        if self.pku_open_self_dict_path:
            logger.info(f'[pku分词]加载用户词典{self.pku_open_self_dict_path}')
            txt_format_2_utf8(self.pku_open_self_dict_path)
            new_seg = pkuseg.pkuseg(postag=True, user_dict=self.pku_open_self_dict_path)  # 重新加载模型
        else:
            new_seg = seg

        try:
            # 对文件夹所有txt进行处理
            all_txt_list = get_files_by_suffix(path=self.pku_txt_path, suffix_name='.txt')
            results = ''
            for txt_file in all_txt_list:
                # 忽略过已处理文件如果该文件名含有jieba_cut或jieba_pos或pku_cut或pku_pos
                if 'jieba_cut' in txt_file or 'pku_cut' in txt_file or 'jieba_pos' in txt_file or 'jieba_dict.txt' in txt_file or 'pku_dict' in txt_file or '自定义词典' in txt_file or 'pku_pos' in txt_file or 'pku_dict.txt' in txt_file or 'pku_pos' in txt_file or 'jieba_dict.txt' in txt_file or '自定义词典' in txt_file or 'pku_pos' in txt_file:
                    logger.info(f'[pku分词]忽略过已处理过的文件{txt_file}')
                    continue
                with open(txt_file, 'r', encoding='utf-8') as f:  # 打开example文档，r表示读，encoding表示用“utf-8”的形式编码
                    text = f.read()  # 读文件并赋值给text
                    logger.info(f'[pku分词]调用seg对{txt_file}分词')
                    pku_seg_words = new_seg.cut(text)  # 调用seg对text分词
                    # 对pku分词结果进行处理
                    # 2.“pku分词” 单纯的分词功能，可否不带标签和括号， 返回结果为词+空格，分词后的结果为：“巴黎  贝甜  在  中国  的  营销 ”

                    if pku_seg_words:
                        logger.info(f'[pku分词]pku_seg_words={pku_seg_words}')
                        save_one_file_cut = ''
                        for text in pku_seg_words:
                            results = results + ' ' + text[0]
                            save_one_file_cut = save_one_file_cut + ' ' + text[0]
                    else:
                        results = 'pku分词失败'

                    # 更新所有pku_seg的结果
                    self.pku_text_cut_to_pos = self.pku_text_cut_to_pos + pku_seg_words

                    # 更新所有pku_seg的结果
                    self.pku_pos_dict.append({
                        "filename": txt_file,
                        "pku_cut": pku_seg_words,
                    })

                    # 在对应文件夹写入生成分词后的文件
                    save_txt_file = txt_file.split('.')[0]
                    write_file(f'{save_txt_file}.pku_cut.txt', save_one_file_cut)
            # 将结果展示到QT上
            self.textEdit_pku_segment.clear()
            self.textEdit_pku_segment.setText(results)

            # 2.1 文件夹分词功能 添加一个保存到本地
            # 获取当前时间
            current_time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
            write_file('./outputs/pku_cut_txt_all_folder_{}.txt'.format(current_time), results)
        except Exception as e:
            self.textEdit_pku_segment.setText('pku分词异常!!!')
            logger.error(f'[pku分词]pku分词异常，{e}')

    # pku 词性标注
    def pku_pos_txt(self):
        self.textEdit_pku_pos.setText(str('[pku词性标注中...]'))
        if not self.pku_text_cut_to_pos:
            # 将结果展示到QT上
            self.textEdit_pku_pos.setText(str('[pku词性标注]失败！请先点击上面的pku分词~'))
            return None
        try:
            # 任务：将列表中的元组拼接成字符串。 比如拼接成“谢谢/nr 你/r 所/u 做/v 的/uj 一切/r ”
            results = ''
            logger.info(f'[pku词性标注]self.pku_text_cut_to_pos={self.pku_text_cut_to_pos}')
            for item in self.pku_text_cut_to_pos:
                word_pos = ' ' + '/'.join(item)
                results += word_pos
            # 将结果展示到QT上
            self.textEdit_pku_pos.setText(str(results))
            logger.info(f'[pku词性标注]self.pku_pos_dict={self.pku_pos_dict}')
            if self.pku_pos_dict:
                for pku_pos in self.pku_pos_dict:
                    pku_pos_results = ''
                    for pku_cut in pku_pos['pku_cut']:
                        word_pos = ' ' + '/'.join(pku_cut)
                        pku_pos_results += word_pos
                    # 在对应文件夹写入生成分词后的文件
                    save_txt_file = pku_pos['filename'].split('.')[0]
                    write_file(f'{save_txt_file}.pku_pos.txt', pku_pos_results)

            # 2.1 文件夹分词功能 添加一个保存到本地
            # 获取当前时间
            current_time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
            write_file('./outputs/pku_pos_txt_all_folder_{}.txt'.format(current_time), results)
        except Exception as e:
            self.textEdit_pku_pos.setText('pku词性标注 异常!!!')
            logger.error(f'pku 词性标注 异常：{e}')

    # 3.“pku分词与词性标注”与“结巴分词与标注” 读取文件都是单个文件，可否改为读取文件夹
    def jieba_openFile_txt(self):
        # get_filename_path, ok = QFileDialog.getOpenFileName(self,
        #                                                     "选取单个文件",
        #                                                     "C:/",
        #                                                     "All Files (*);;Text Files (*.txt)")
        # if ok:
        #     self.textEdit_jieba_txt.setText(str(get_filename_path))
        #     self.jieba_txt_path = str(get_filename_path)
        get_directory_path = QFileDialog.getExistingDirectory(self,
                                                              "选取指定文件夹",
                                                              "C:/")
        self.textEdit_jieba_txt.setText(str(get_directory_path))
        self.jieba_txt_path = str(get_directory_path)

    # 4.
    # 打开文件夹 ，从原来的打开文件改为文件夹
    def jieba_open_self_dict(self):
        get_filename_path, ok = QFileDialog.getOpenFileName(self,
                                                            "选取单个文件",
                                                            "C:/",
                                                            "All Files (*);;Text Files (*.txt)")
        if ok:
            self.textEdit_jieba_self_dict.setText(str(get_filename_path))
            self.jieba_open_self_dict_path = str(get_filename_path)

    # jieba 分词
    def jieba_seg_txt(self):
        if not self.jieba_txt_path:
            self.textEdit_jieba_segment.setText(str('请您点击上面的打开txt文件夹...'))
            return None
        # 选择自定义词典
        if self.jieba_open_self_dict_path:
            logger.info(f'[jiab分词]加载用户词典{self.jieba_open_self_dict_path}')
            txt_format_2_utf8(self.pku_open_self_dict_path)
            jieba.load_userdict(self.jieba_open_self_dict_path)
        logger.info(f'[jiab分词]打开jieba分词文件{self.jieba_txt_path}')
        self.textEdit_jieba_segment.setText('[jieba分词中...]')
        try:
            # 对文件夹所有txt进行处理
            all_txt_list = get_files_by_suffix(path=self.jieba_txt_path, suffix_name='.txt')
            results = ''
            for txt_file in all_txt_list:
                # 忽略过已处理文件如果该文件名含有jieba_cut或jieba_pos或pku_cut或pku_pos
                if 'jieba_cut' in txt_file or 'pku_cut' in txt_file or 'jieba_pos' in txt_file or 'jieba_dict.txt' in txt_file or 'pku_dict' in txt_file or '自定义词典' in txt_file or 'pku_pos' in txt_file or 'pku_dict.txt' in txt_file or 'pku_pos' in txt_file or 'jieba_dict.txt' in txt_file or '自定义词典' in txt_file or 'pku_pos' in txt_file:
                    logger.info(f'[jiab分词]忽略过已处理过的文件{txt_file}')
                    continue
                with open(txt_file, 'r', encoding='utf-8') as f:  # 打开example文档，r表示读，encoding表示用“utf-8”的形式编码
                    self.jiaba_txt = f.read()  # 读文件并赋值给text
                    self.jiaba_txt_folder = self.jiaba_txt_folder + self.jiaba_txt
                    logger.info(f'[jiab分词]调用jiaba对text{txt_file}分词')
                    seg_list = jieba.cut(self.jiaba_txt, cut_all=False)
                    logger.info(f'{seg_list}')
                    jieba_seg_words = " ".join(seg_list)
                    logger.info(f'[jiab分词]jieba_seg_words的类型={type(jieba_seg_words)}')
                    logger.info(f'[jiab分词]jieba_seg_words={jieba_seg_words}')

                    # 更新所有jieba_seg的结果
                    self.jieba_text_cut_to_pos = self.jieba_text_cut_to_pos + jieba_seg_words

                    # 合并文件夹所有txt的分词
                    if jieba_seg_words:
                        for text in jieba_seg_words:
                            results = results + ' ' + text[0]
                    else:
                        results = 'jieba分词失败'

                    # 在对应文件夹写入生成分词后的文件
                    save_txt_file = txt_file.split('.')[0]
                    write_file(f'{save_txt_file}.jieba_cut.txt', jieba_seg_words)
            # 将结果展示到QT上
            self.textEdit_jieba_segment.setText(str(self.jieba_text_cut_to_pos))
            # 2.1 文件夹分词功能 添加一个保存到本地
            # 获取当前时间
            current_time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
            write_file('./outputs/jieba_cut_txt_{}.txt'.format(current_time), results)
        except Exception as e:
            self.textEdit_jieba_segment.setText('jieba分词异常!!!')
            logger.error(f'[jiab分词]jieba分词异常，{e}')

    # jieba 词性标注
    def jieba_pos_txt(self):
        if not self.jiaba_txt_folder:
            self.textEdit_jieba_pos.setText(str('请您点击上面的分词...'))
            return None
        # 选择自定义词典
        if self.jieba_open_self_dict_path:
            logger.info(f'[jiab 词性标注]加载用户词典{self.jieba_open_self_dict_path}')
            txt_format_2_utf8(self.pku_open_self_dict_path)
            jieba.load_userdict(self.jieba_open_self_dict_path)
        try:
            self.textEdit_jieba_pos.setText('[jieba词性标注中...]')
            logger.info(f'[jieba 词性标注]self.jiaba_txt_folder={self.jiaba_txt_folder}')

            # 对文件夹所有txt进行处理
            all_txt_list = get_files_by_suffix(path=self.jieba_txt_path, suffix_name='.txt')

            jieba_pos_all_results = ''
            for txt_file in all_txt_list:
                # 忽略过已处理文件如果该文件名含有jieba_cut或jieba_pos或pku_cut或pku_pos
                if 'jieba_cut' in txt_file or 'pku_cut' in txt_file or 'jieba_pos' in txt_file or 'jieba_dict.txt' in txt_file or 'pku_dict' in txt_file or '自定义词典' in txt_file or 'pku_pos' in txt_file or 'pku_dict.txt' in txt_file or 'pku_pos' in txt_file or 'jieba_dict.txt' in txt_file or '自定义词典' in txt_file or 'pku_pos' in txt_file:
                    logger.info(f'[jieba 词性标注]忽略过已处理过的文件{txt_file}')
                    continue
                with open(txt_file, 'r', encoding='utf-8') as f:  # 打开example文档，r表示读，encoding表示用“utf-8”的形式编码
                    jiaba_pos_txt = f.read()  # 读文件并赋值给text

                    jieba_pos_list = posseg.cut(jiaba_pos_txt)
                    logger.info(f'[jieba 词性标注]jieba_pos_list={jieba_pos_list}')

                    jieba_pos_one_file_result = ''
                    # tag_list = []
                    for tag in jieba_pos_list:
                        # 拼接成字典
                        # pos_word = {}
                        # pos_word['word'] = tag.word
                        # pos_word['pos'] = tag.flag
                        # tag_list.append(pos_word)
                        jieba_pos_one_file_result = jieba_pos_one_file_result + tag.word + '/' + tag.flag + ' '

                    # 在对应文件夹写入生成分词后的文件
                    save_txt_file = txt_file.split('.')[0]
                    write_file(f'{save_txt_file}.jieba_pos.txt', jieba_pos_one_file_result)

                # for拼接最后的结果
                jieba_pos_all_results = jieba_pos_all_results + jieba_pos_one_file_result

            # 将结果展示到QT上
            self.textEdit_jieba_pos.setText(str(jieba_pos_all_results))

            # 2.1 文件夹分词功能 添加一个保存到本地
            # 获取当前时间
            current_time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
            write_file('./outputs/jieba_pos_txt_all_folder_{}.txt'.format(current_time), str(jieba_pos_all_results))
        except Exception as e:
            self.textEdit_jieba_pos.setText('jieba词性标注 异常!!!')
            logger.error(f'pku 词性标注 异常：{e}')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainForm()
    myWin.show()
    sys.exit(app.exec_())
