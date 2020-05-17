import os
from glob import glob
import cv2
from dataAugmentation import readxyxy
import numpy as np

def cropImage(img, xmin, ymin, xmax, ymax):

    print("Execute Crop Image.")
    img = img[ymin:ymax, xmin:xmax]
    return img


def readImageAndXML(imageFolder, xmlFolder, storageFolder):
    
    print("INFO \' read ImageAndXML\'")

    images = glob(os.path.join(imageFolder, "*.jpg"))
    xmls = glob(os.path.join(xmlFolder, "*.xml"))
    
    images = sorted(images)
    xmls = sorted(xmls)

    i = 0

    for image, xml in zip(images, xmls):
        
        print("INFO porcess image:{} , xml:{} ".format(image, xml))
        xmin, ymin, xmax, ymax = readxyxy(xml)
        img = cv2.imread(image)

        crop_img = cropImage(img, xmin, ymin, xmax, ymax)

        cv2.imwrite(os.path.join(storageFolder, str(i).zfill(3) + ".jpg"), crop_img)
        i+= 1

def composite(foreground, background):
    
    fh, fw = foreground.shape[:2]
    bh, bw = background.shape[:2]

    src_x = np.random.randint(0, bw-fw)
    src_y = np.random.randint(0, bh-fh)

    dst_x = src_x + fw
    dst_y = src_y + fh

    com_image = background
    '''
    for h in range(fh):
        for w in range(fw):
            if not 150 <= foreground[h][w][1] <= 190 and \
               not  (150 <= foreground[h][w][2] <= 190) and not (30 <= foreground[h][w][0]):

                com_image[h+src_y, w+src_x] = foreground[h, w]
    '''
    com_image[src_y:dst_y, src_x:dst_x] = foreground

    return com_image

def com_main():

    folders = os.listdir("./cropImages")
    folders = sorted(folders)
    storage_path = "./testImage"
    backgrounds = glob(os.path.join("./backgrounds", "*.jpg"))

    for f in folders:

        storage_folder = os.path.join(storage_path, f)
        if not os.path.exists(storage_folder):
            os.mkdir(storage_folder)

        foregrounds = glob(os.path.join("./cropImages", f, "*.jpg"))

        for i in range(100):
            print("folder: {}, composite: {}".format(f, i))
            b_choice = np.random.randint(0, 9)
            f_choice = np.random.randint(0, len(foregrounds))

            bg = cv2.imread(backgrounds[b_choice])
            fg = cv2.imread(foregrounds[f_choice])

            img = composite(fg, bg)
            cv2.imwrite(os.path.join(storage_folder, str(i).zfill(3) + ".jpg"), img)
            

def main():

    folders = os.listdir("./new datasets")
    
    for f in folders:

        image_folder = os.path.join("./new datasets", f)
        xml_folder = os.path.join("./new datasets", f)
        storage_folder = os.path.join("./cropImages", f)
        if not os.path.exists(storage_folder):
            os.mkdir(storage_folder)

        readImageAndXML(imageFolder=image_folder, xmlFolder=xml_folder, storageFolder=storage_folder)


if __name__ == "__main__":
    #main()
    com_main()
        

    