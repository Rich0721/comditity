import os
import cv2
from glob import glob
import numpy as np
from Process_xml import processXML

class composite(object):

    def __init__(self, background_folder, froeground_folder, numbers=1, quantity=100, storage_dataset="./testImage", storage_folder="test_1"):
        
        '''
            background_folder: Storage background images' folder.
            froeground_folder: Storage commdities' folder.
            numbers: How many commdities on per composite image. 
            background_type: I have three type of background. 
            quantity: Product images' quantity.
        '''

        self._background_images = glob(os.path.join(background_folder, '*.jpg'))
        
        self._background_type = ['background_1', 'background_2', 'background_3']
        self._foreground_folders = froeground_folder
        self._commdity_orders = os.listdir(os.path.join(froeground_folder, self._background_type[0]))
        self._numbers = numbers
        self._quantity = quantity

        self._storage_dataset = storage_dataset
        self._storage_folder = storage_folder
        if not os.path.exists(os.path.join(storage_dataset,storage_folder)):
            os.mkdir(os.path.join(storage_dataset,storage_folder))

        self._write_xml = processXML()

    def fusion(self):
        '''
            Fusion background and foregrond.
        '''
        for q in range(self._quantity):
            background_random = np.random.randint(0, 3)
            background_image = cv2.imread(self._background_images[background_random])
            bg_h, bg_w = background_image.shape[:2]
            commdity_orders = np.random.randint(0, len(self._commdity_orders), size=self._numbers)

            areas = []
            objects_name = []

            
            for o in commdity_orders:
                images = glob(os.path.join(self._foreground_folders, self._background_type[background_random], self._commdity_orders[o], "*.jpg"))
                images_random = np.random.randint(0, len(images))
                fg = cv2.imread(images[images_random])

                fg_h, fg_w = fg.shape[:2]

                start_height = np.random.randint(0, bg_h-fg_h)
                start_width = np.random.randint(0, bg_w-fg_w)
                

                xmin = start_width
                ymin = start_height
                xmax = start_width + fg_w
                ymax = start_height + fg_h

                areas.append([xmin, ymin, xmax, ymax])
                objects_name.append(self._commdity_orders[o])

                for h in range(fg_h):
                    for w in range(fg_w):
                        
                        if fg[h, w, 0] > 10 or fg[h, w, 1] > 10 or  fg[h, w, 2] > 10 :
                            background_image[h+start_height, w + start_width, 0] = fg[h, w, 0]
                            background_image[h+start_height, w + start_width, 1] = fg[h, w, 1]
                            background_image[h+start_height, w + start_width, 2] = fg[h, w, 2]
        
            self._write_xml.xmlFactory(self._storage_dataset, self._storage_folder, str(q).zfill(4) + ".jpg", areas=areas, object_name=objects_name)
            self._write_xml.writeXMLFile()
            cv2.imwrite(os.path.join(self._storage_dataset, self._storage_folder, str(q).zfill(4) + ".jpg"), background_image)
            print("{}".format((os.path.join(self._storage_dataset, self._storage_folder, str(q).zfill(4) + ".jpg"))))


if __name__ == "__main__":
    c = composite("./backgrounds", "./grab_images", numbers=2)
    c.fusion()

            
            



        