import numpy as np
import cv2
import pydicom
import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import time
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

def err_curve(l1_loss, norm_l1_loss, sav_path):
  x_axis = np.arange(0, 1*len(l1_loss), 1)
  # plt.plot(x_axis, l1_loss, label='l1_loss')
  plt.xlabel('区域索引')
  plt.ylabel('保真值（%）')
  plt.title('CT肺窗不同区域的细节保真度值')
  plt.plot(x_axis, norm_l1_loss, label='norm_l1')
  plt.legend(bbox_to_anchor=(1.0, 1), loc=1)

  plt.savefig(sav_path + '//loss_curve.png')
  plt.close()
  return np.mean(l1_loss), np.mean(norm_l1_loss)


def mask_feature(res, center, k_num, sav_folder, img_shape):
  M = np.sort(center, axis=0)
  tmp = np.zeros((img_shape))
  mask = np.tile(tmp[..., np.newaxis], (1, 1, k_num))
  for count in range(k_num):
    temp = np.zeros(res.shape)
    temp[res == M[count]] = 1
    res2 = temp.reshape(img_shape)
    sav_path = os.path.join(sav_folder, 'feature' + str(count)+'.jpg')
    plt.imsave(sav_path, res2, cmap=plt.get_cmap('gray'))
    mask[..., count] = res2
  return mask

def k_means_seg(img, k_num, criteria, iter):
  Z = np.float32(img.reshape(-1, 1))
  ret, label, center = cv2.kmeans(Z, k_num, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
  center = np.uint8(center)
  res = center[label.flatten()]
  sav_folder = './pred' + '/iter' + str(iter)
  if not os.path.exists(sav_folder):
    os.makedirs(sav_folder)
  mask = mask_feature(res, center, k_num, sav_folder, img.shape)

  # img_res = img*mask[..., 2]
  plt.imsave(sav_folder+'//ori_img.jpg', img, cmap=plt.get_cmap('gray'))
  return mask

def colormap():
  return mpl.colors.LinearSegmentedColormap.from_list('cmap', ['#FFFFFF', '#98F5FF', '#00FF00', '#FFFF00','#FF0000', '#8B0000'], 256)
dicom_path = 'E:\AIProjects\CT_low_dose\data_5mm_lung_good\\1\\low'
low_path = 'E:\CT_Lung_normal\lowdoeschest_dupu\\120kv_160ma_20ma_0.5\JinChuanZhong_good\lung\\5mm\low'
high_path = 'F:\AI_Projects\CTDenoise\chest_lung_low_Recon\predict_result\predict_199'
ds = pydicom.dcmread(os.path.join(low_path, '2.16.840.1.114492.84191100096227153.20139192736.44800.8967.dcm'))
img_low_ori = ds.pixel_array
# m = l[222:316, 122:225]
img_low = ((img_low_ori+1024)/4096).clip(0, 1)*255

ds_h = pydicom.dcmread(os.path.join(high_path, '2.16.840.1.114492.84191100096227153.20139192736.44800.8967.dcm'))
img_h_ori = ds_h.pixel_array
stride = 64
count_num = int(512/stride)
tmp = 0
start = time.time()
l1_list = []
norm_l1_list = []
for row in range(count_num):
  for col in range(count_num):
    img_crop = img_low[row*64:64*(row+1), col*64:64*(col+1)]

    if np.mean(img_crop) < 0.3*np.mean(img_low):
      continue
    else:
      criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.01)
      K = 4
      mask = k_means_seg(img_crop, K, criteria, tmp)
      img_low_crop = (img_low_ori[row*64:64*(row+1), col*64:64*(col+1)])*mask[..., 3]
      img_h_crop = (img_h_ori[row*64:64*(row+1), col*64:64*(col+1)])*mask[..., 3]
      l1_list.append(abs(np.mean(img_h_crop)-np.mean(img_low_crop)))
      norm_l1_list.append(100-abs((np.mean(img_h_crop)-np.mean(img_low_crop))/np.mean(img_low_crop)))

    tmp += 1
l1_loss, norm_l1_loss = err_curve(l1_list, norm_l1_list, './loss_results')
      # ds.PixelData = np.int16(img_res / 255 * 4096 - 1024)
      # ds.save_as('predict')
      # img_res_iter1 = k_means_seg(img_res * 255, K, criteria, 1)

print('time is %.5f' % (time.time() - start))




# cv2.imshow('res2', res2)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# ds.PixelData = np.int16(res2)
# # ds.save_as('predict')
# df = pd.DataFrame(res2, columns=[x for x in range(512)])
# sns.heatmap(df)
# plt.show()
