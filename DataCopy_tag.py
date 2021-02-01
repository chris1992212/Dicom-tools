"""
This script is used to extract the dicom data to specific file, according the tags we want
Created by chenmingliang in 2020/11/17

"""
import pydicom
import os
import shutil

# tags = ['Exposure', 'KVP', 'ConvolutionKernel', 'SliceThickness']
# standard1 = [10, 120, 'CHEST_STND', 1]
# standard2 = [10, 120, 'LIMB_STND', 1]
# standard = [standard1, standard2]
tags = ['ConvolutionKernel']
standard = [['LIMB_BONE']]
ori_path = 'E:\卷叠伪影\XFFS\Jupiter\\test'
Target_path = './Data'

def loadFileInformation(filename):

    information = {}
    ds = pydicom.read_file(filename)
    for tag in tags:
        tmp = 'ds.' + tag
        information[tag] = eval(tmp)
        # information[tags[0]] = ds.Exposure
        # information[tags[1]] = ds.SliceThickness
        # information[tags[2]] = ds.ConvolutionKernel
        # information[tags[3]] = ds.KVP
        # information[tags[4]] = ds.StationName
    return information


def Is_file(information):

    """
    This function is used to choose the specific file, according the demand.
    :return:
    """
    for standard_tmp in standard:
        is_file = True
        for count in range(len(information)):
                if information[tags[count]] == standard_tmp[count]:
                    continue
                else:
                    is_file = False
                    break
        if is_file:
            break
        else:
            continue
    return is_file


def copy_file(inputPath, targetPath, count):
    if os.path.exists(targetPath):
        shutil.rmtree(targetPath)
    shutil.copytree(inputPath, targetPath)
    print('Finish %d dir' % count)

if __name__ == '__main__':
    # file = 'E:\CT_Lung_normal\lowdoeschest_dupu\\120kv_160ma_30ma_0.5\DPC004663\lung\\5mm\\normal'
    # filenames = os.listdir(file)
    # for i in filenames:
    #     d = loadFileInformation(os.path.join(file, i))

    count = 0
    for root, dirs, files in os.walk(ori_path):
        if not files == []:
            if os.path.splitext(files[0])[-1] == '.dcm':
                if len(files) > 30:
                    tmp_file = os.path.join(root, files[0])
                    info = loadFileInformation(tmp_file)
                    is_file = Is_file(info)
                    if is_file:
                        count += 1
                        target_path = os.path.join(Target_path, str(count))
                        copy_file(root, target_path, count)
