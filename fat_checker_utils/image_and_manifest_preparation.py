import os
import random
import argparse

import numpy as np

from PIL import Image, ImageDraw, ImageFont

def make_blank_placeholder(image_file, out_file):
  #print(out_file)
  image = np.asarray(Image.open(image_file))
  blank = np.ones(image.shape)*255
  blank = blank.astype(np.uint8)
  #print(blank.shape)
  im = Image.fromarray(blank)
  draw = ImageDraw.Draw(im)
  (x, y) = ((image.shape[0]//2)-50+random.randint(-10,10), (image.shape[1]//2)-50+random.randint(-10,10))
  font = ImageFont.truetype('/Library/Fonts/Arial Bold.ttf', 45)
  message = "No Data"
  color = 'rgb(0, 0, 0)' # black color
  draw.text((x, y), message, fill=color, font=font)
  #im.convert('L')
  im.save(out_file)

def reduce_quality(image_file):
  im = Image.open(image_file)
  im.save(image_file, quality=90)

def main():
  parser = argparse.ArgumentParser(description='Process some images.')
  parser.add_argument('--path', metavar='path', type=str,
                      help='path to images')
  parser.add_argument('--volume_identifier', metavar='vol_id', type=str,
                      help='unique volume identifier e.g. 3R_ROI1')
  
  args = parser.parse_args()
  path = args.path
  vol_id = args.volume_identifier
  #old_dirpath=None
  images = []
  id_nums = []
  '''
  metadata = {'Raw Z resolution (nm)': 50,
              'Raw XY resolution (nm)': 10,
              'Volume ID': vol_id,
              'default_frame': 3,
              '#set': None}
  '''
  manifest = open(os.path.join(path+'manifest.csv'),'w')
  manifest.write((',').join(['image1', 'image2', 'image3', 'image4', 'image5', 'Raw Z resolution (nm)', 'Raw XY resolution (nm)', 'Volume ID', 'default_frame', '#set\n']))
  for (dirpath, dirnames, filenames) in os.walk(path):
    #if dirpath != old_dirpath:
    #  images = []
    #  id_nums = []
    for f in filenames:
      '''
      metadata = {'Raw Z resolution (nm)': 50,
                  'Raw XY resolution (nm)': 10,
                  'default_frame': 3}
      '''
      image_file = os.path.join(dirpath, f)
      if '.DS_Store' in image_file:
        continue
      if '.csv' in image_file:
        continue
      #print(image_file)
      #if 'ROI1' in image_file:
      #  reduce_quality(image_file)
      file_stub = image_file.strip('.jpg')[:-3] + '%03d_blank.jpg'
      id_num = image_file.strip('.jpg')[-3:]
      if id_num  == 'ank':
        continue
      if id_num == 'opy':
        id_num = image_file.strip(' copy.jpg')[-3:]
        file_stub = image_file.strip(' copy.jpg')[:-3] + '%03d_blank.jpg'
      id_nums.append(int(id_num))
      images.append(image_file)
    if images == []:
      continue
    sorted_images = [x for _,x in sorted(zip(id_nums,images))]
    id_nums.sort()
    make_blank_placeholder(images[0], file_stub%(id_nums[0]-2))
    make_blank_placeholder(images[0], file_stub%(id_nums[0]-1))
    make_blank_placeholder(images[0], file_stub%(id_nums[-1]+1))
    make_blank_placeholder(images[0], file_stub%(id_nums[-1]+2))
    images = [file_stub%(id_nums[0]-2), file_stub%(id_nums[0]-1)] + \
             sorted_images + \
             [file_stub%(id_nums[-1]+1), file_stub%(id_nums[-1]+2)]
    #print(len(images))
    for i in range(2,len(images)-2, 1):
      #print(len(images[i-2:i+3]))
      print(images[i-2:i+3])
      #print(','.join(images[i-2:i+2]))
      manifest.write((',').join([im.split('/')[-1] for im in images[i-2:i+3]]+['50', '10', vol_id, '3', dirpath.split('/')[-1]])+'\n')


if __name__ == '__main__':
  main()
