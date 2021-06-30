#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import time
import pysnooper

from common.convert_txt import txt_format_2_utf8
from common.log import logger


def get_files_by_suffix(path, suffix_name):
    """
    获取指定路径下所有带有.xxx后缀名的文件
    Args:
        path: 指定的文件夹路径
        suffix_name: 固定格式，为 suffix_name=".apk"

    Returns: files of list

    """

    file_num = 0
    res = []
    # 遍历该文件夹
    # 默认先读取当前文件夹里面的文件，如果存在子文件夹，读完当前再遍历子文件夹里面的
    for root, dirs, files in os.walk(path):
        # print(files)
        for file in files:  # 遍历刚获得的文件名files
            filename, extension = os.path.splitext(file)  # 将文件名拆分为文件名与后缀
            if extension == suffix_name:  # 判断该后缀是否为.X文件
                file_num = file_num + 1  # 文件个数标记
                # print(file_num, os.path.join(root,filename)) #输出文件号以及对应的路径加文件名
                # res.append(filename)  # ["a","b"]格式，不带后缀名，需要自己拼接.apk后缀
                # res.append(filename + suffix_name)  # ["a.x","b,x"]格式
                res.append(root + '/' + filename + suffix_name)  # ["C:\\a.x"]格式
    logger.info("[file_tools]找到文件列表={}".format(res))
    if not res:
        logger.error("[file_tools]输入的路径不存在.{}文件！".format(suffix_name))
        return None
    else:
        return res


def write_file(save_file_path, save_content):
    with open(save_file_path, 'w', encoding='utf-8') as f:
        logger.info(f'打开要写入保存的文件{save_file_path}')
        f.write(save_content)
    logger.info(f'成功写入文件：{save_file_path}')


def merge_two_txt(a_txt, b_txt, save_file_path):
    # 讲2个txt路径拼接到List中，保持之前的结构
    logger.info('合并的txt A = {}'.format(a_txt))
    logger.info('合并的txt B = {}'.format(b_txt))

    # 将txt编码格式转为utf-8
    txt_format_2_utf8(a_txt)
    txt_format_2_utf8(b_txt)

    files = [a_txt, b_txt]
    # 获取当前时间
    current_time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
    final_file = f'{save_file_path}merged_2_txt_{current_time}.txt'

    logger.info('开始合并...')

    # 原来合并正常，但是有中文乱码的
    # 2个文本合并后的路径，需要考虑放在哪里，暂时以w_file 或当前路径下/data/文件夹中
    # w_file = open(final_file, "wb")
    # for file in files:
    #     logger.info(f'读取file={file}')
    #     with open(file, 'rb') as f:
    #         w_file.write(f.read())
    #     w_file.write(os.linesep)  # 换行符，匹配不同操作系统的EOL，Unix：\n Mac：\r Windows：\r\n
    # w_file.close()

    with open(final_file, 'w', encoding='utf-8') as f1:
        logger.info(f'打开{final_file}写入保存的文件')
        for txt_file in files:
            with open(txt_file, 'r', encoding='utf-8') as f:
                logger.info(f'读取{txt_file}文件')
                f1.write(f.read())
            f1.write(os.linesep)  # 换行符，匹配不同操作系统的EOL，Unix：\n Mac：\r Windows：\r\n

    logger.info('合并成功...')
    logger.info('合并后的txt = {}'.format(final_file))

    # 返回合并后txt的名字
    return final_file


@pysnooper.snoop()
def merge_all_txt(txt_list, save_file_path):
    # 讲2个txt路径拼接到List中，保持之前的结构
    logger.info('All txt:合并的txt_list = {}'.format(txt_list))

    # 获取当前时间
    current_time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
    save_file_txt = f'{save_file_path}All_txt_merged_{current_time}.txt'

    logger.info('All txt:开始合并...')

    # 2个文本合并后的路径，需要考虑放在哪里，暂时以w_file 或当前路径下/data/文件夹中
    with open(save_file_txt, 'w', encoding='utf-8') as f1:
        logger.info(f'打开{save_file_txt}写入保存的文件')
        for txt_file in txt_list:
            # 将txt编码格式转为utf-8
            txt_format_2_utf8(txt_file)
            with open(txt_file, 'r', encoding='utf-8') as f:
                logger.info(f'读取{txt_file}文件')
                f1.write(f.read())
            f1.write(os.linesep)  # 换行符，匹配不同操作系统的EOL，Unix：\n Mac：\r Windows：\r\n

    logger.info('All txt:合并成功...')
    logger.info('All txt:合并后的txt = {}'.format(save_file_txt))

    # 返回合并后txt的名字
    return save_file_txt


if __name__ == "__main__":
    # aa = merge_two_txt(r'../data/test1.txt', r'../data/test2.txt', save_file_path='../outputs/')
    # print(aa)
    # get_files_by_suffix(path='../', suffix_name='.txt')

    merge_all_txt(txt_list=['C:/Users/Administrator/Desktop/ba_papers_50/“巴黎贝甜”在中国的营销策略分析.txt'],
                  save_file_path='./outputs/')
