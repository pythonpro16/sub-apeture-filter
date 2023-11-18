import os
import cv2
import numpy as np
import glob

# Load Data
u, v = 376, 541  # spatial samples
x, y = 14, 14    # angular samples
start_x, start_y = 4, 4
sub_aperture = np.zeros((u, v, 3), dtype=np.uint8)

data_dir = 'data/Flowers_8bit'
if not os.path.isdir(data_dir):
    print(f"Error: The folder does not exist: {data_dir}")
    exit()

file_pattern = os.path.join(data_dir, '*.png')
png_files = glob.glob(file_pattern)
for k, png_file in enumerate(png_files):
    base_file_name = os.path.basename(png_file)
    current_data_name, _ = os.path.splitext(base_file_name)
    full_file_name = os.path.join(data_dir, base_file_name)
    data = cv2.imread(full_file_name)

    size_x, size_y, _ = data.shape  # data size

    folder_name = f'result/{current_data_name}'
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)

    for select_pix_x in range(start_x, x - 2):
        for select_pix_y in range(start_y, y - 2):
            for i in range(0, size_x, x):
                for j in range(0, size_y, y):
                    extract_each_microlens = data[i:i + (x - 1), j:j + (y - 1), :]
                    select_position = extract_each_microlens[select_pix_x, select_pix_y, :]
                    sub_aperture[i // x, j // y, :] = select_position

            file_name = f'{folder_name}/HR_{k}_{select_pix_x}_{select_pix_y}.png'
            cv2.imwrite(file_name, sub_aperture)