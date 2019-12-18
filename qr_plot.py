import csv
import os

import matplotlib.pyplot as plt
import numpy as np
import PIL
import qrcode
from PIL import Image


def __get_qr_str_img(csv_file_path):
    qr_str_img_list = []
    with open('name_string.csv', 'r', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            print(', '.join(row))
            img = qrcode.make(row[1])
            str_img = [row[0], img]
            qr_str_img_list.append(str_img)

    return qr_str_img_list


def __plot_qr_str_img(qr_str_img_sub_list):
    num_of_qr_str_img = len(qr_str_img_sub_list)
    if num_of_qr_str_img == 0:
        print('[Error] empty list')
        return

    firt_qr_img = qr_str_img_sub_list[0][1]
    height = width = firt_qr_img.width

    num_of_imgs = 3
    fig, axes = plt.subplots(num_of_imgs * 2, 3, figsize=(8, 8*height/width))

    for i in range(num_of_imgs):
        for j in range(6):
            ax = axes[i * 2 + j // 3][j % 3]
            ax.set_xticks([])
            ax.set_yticks([])

            if i < num_of_qr_str_img and j in [0, 1, 2, 4]:
                qr_str, qr_img = qr_str_img_sub_list[i]
                assert qr_img.width == firt_qr_img.width
                ax.imshow(qr_img, cmap='gray')
                ax.set_xlabel(qr_str)
            else:
                ax.axis('off')

    plt.show(block=False)
    plt.pause(0.001)

    fig.canvas.draw()
    fig_np = np.array(fig.canvas.renderer._renderer)

    return fig_np


def qr_plot(csv_file_path):
    qr_str_img_list = __get_qr_str_img(csv_file_path)
    file_path, _ = os.path.splitext(csv_file_path)

    n = 3
    for i in range((len(qr_str_img_list) + n - 1) // n):
        qr_str_img_sub_list = qr_str_img_list[i * n:(i + 1) * n]
        fig_np = __plot_qr_str_img(qr_str_img_sub_list)

        plot_file_path = '%s_%d.png' % (file_path, i)
        im = Image.fromarray(fig_np)
        im.save(plot_file_path)


if __name__ == '__main__':
    _dir_path = os.path.dirname(__file__)
    _csv_file_path = os.path.join(_dir_path, 'name_string.csv')
    qr_plot(_csv_file_path)
