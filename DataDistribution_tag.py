"""
This script is used to image the data distribution, according to the specific tags of dicom.
Created by chenmingliang in 2020/11/18
"""

import pydicom
import os
import shutil
import matplotlib.pyplot as plt
from prettytable import PrettyTable

# tags = ['Exposure', 'SliceThickness', 'ConvolutionKernel', 'KVP', 'StationName']
# ori_path = 'E:\CT_Lung\CT16\ShaoXing dongpuzhen hospital\\120kv_160ma_20ma_0.5'
tags = ['StationName', 'BodyPartExamined', 'SliceThickness', 'ConvolutionKernel',  'Exposure']
# tags = ['Exposure']
ori_path = 'F:\AI_Projects\CT_artifacts\\version1_pytorch\\train\Aliasing_artifacts'
# ori_path = 'E:\卷叠伪影消除结果\\result_0120'


# standard = [80, 120, 'CHEST_LUNG', 1]

def loadFileInformation(filename):

    information = {}
    ds = pydicom.read_file(filename)
    for tag in tags:
        tmp = 'ds.' + tag
        try:
            information[tag] = str(eval(tmp))
        except:
            information[tag] = 'None'
        # information[tags[0]] = ds.Exposure
        # information[tags[1]] = ds.SliceThickness
        # information[tags[2]] = ds.ConvolutionKernel
        # information[tags[3]] = ds.KVP
        # information[tags[4]] = ds.StationName
    return information


def get_list_count(information, count_temp, item_list):

    """
    This function is used to choose the different information into the list, and calc the count num
    :param information:
    :param list_all:
    :return:
    """
    label = True
    for k in range(len(item_list)):
        temp_item = item_list[k].copy()
        temp_item.pop('Count')
        if information == temp_item:
            item_list[k]['Count'] += count_temp
            label = False
            break
    if label:
        information.update({'Count': count_temp})
        item_list.append(information)
    return item_list


def draw_img(count_list, item_list):

    """
    This
    :param count_list:
    :param item_list:
    :return:
    """
    label = []
    for k in range(len(item_list)):
        label.append(str(item_list[k]))
    size = count_list
    # explode = (0, 0.1, 0, 0)
    plt.pie(size, labels=label, autopct='%1.1f%%', shadow=True, startangle=90)
    plt.axis('equal')
    plt.show()


def sort_list(mea_list):

    # for tag in tags:
    #     s = e.__getitem__(tag)

    new_s = sorted(mea_list, key=lambda e: list(map(lambda tag: e.__getitem__(tag), tags)))

    # new_s = sorted(mea_list, key=lambda e: (e.__getitem__('Exposure'), e.__getitem__('SliceThickness'), e.__getitem__('ConvolutionKernel')))
    return new_s


def draw_img2(item_list):
    item_list = sort_list(item_list)
    temp = list(item_list[0])
    table = PrettyTable(temp)
    for k in range(len(item_list)):
        temp2 = list(item_list[k].values())
        table.add_row(temp2)
    print(table)

if __name__ == '__main__':


    item_list = []
    count_list = []
    count = 0
    for root, dirs, files in os.walk(ori_path):
        if not files == []:
            if os.path.splitext(files[0])[-1] == '.dcm':
                if len(files) > 30:
                    tmp_file = os.path.join(root, files[0])
                    info = loadFileInformation(tmp_file)
                    count_temp = len(os.listdir(root))
                    if item_list == []:
                        info.update({'Count': count_temp})
                        item_list.append(info)
                    else:
                        item_list = get_list_count(info, count_temp, item_list)
    draw_img2(item_list)
