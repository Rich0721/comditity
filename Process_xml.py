import xml.etree.ElementTree as ET
import os
import os.path as osp

class processXML:
    

    def xmlFactory(self, datasetName, imageFolder, imageName, areas, object_name):
        self._datasetName = datasetName
        self._imageFolder = imageFolder
        self._imageName = imageName
        self._areas = areas
        self._objcet_name = object_name   

    def tabXML(self, element, indent, newline, level=0):

        if element:
            if element.text == None or element.text.isspace():
                element.text = newline + indent * (level + 1)
            else:
                element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)
        
        temp = list(element)
        for subelement in temp:
            if temp.index(subelement) < (len(temp) - 1):
                subelement.tail = newline + indent * (level + 1)
            else:
                subelement.tail = newline + indent * level
            self.tabXML(subelement, indent, newline, level=level+1)
    
    def writeXMLFile(self):

        annotation = ET.Element("annotation")
        filename = ET.SubElement(annotation, "filename")
        filename.text = self._imageName
        path = ET.SubElement(annotation, "path")
        path.text = osp.abspath(osp.join(self._datasetName, "JPEGImages", self._imageName))

        source = ET.SubElement(annotation, "source")
        database = ET.SubElement(source, "database")    
        database.text = "Unknown"

        size = ET.SubElement(annotation, "size")
        width = ET.SubElement(size, "width")
        height = ET.SubElement(size, "height")
        depth = ET.SubElement(size, "depth")
        width.text = "960"
        height.text = "540"
        depth.text = "3"

        segmented = ET.SubElement(annotation, "segmented")
        segmented.text = "0"
        
        for n, areas in zip(self._objcet_name, self._areas):
            objects = ET.SubElement(annotation, "object")
        
            name = ET.SubElement(objects, "name")
            pose = ET.SubElement(objects, "pose")
            truncated = ET.SubElement(objects, "truncated")
            difficult = ET.SubElement(objects, "difficult")
            name.text = n
            
            pose.text = "Unspecified"
            truncated.text = "0"
            difficult.text = "0"
            bndbox = ET.SubElement(objects, "bndbox")

            xmin = ET.SubElement(bndbox, "xmin")
            ymin = ET.SubElement(bndbox, "ymin")
            xmax = ET.SubElement(bndbox, "xmax")
            ymax = ET.SubElement(bndbox, "ymax")

            xmin.text = str(areas[0])
            ymin.text = str(areas[1])
            xmax.text = str(areas[2])
            ymax.text = str(areas[3])
        
        tree = ET.ElementTree(annotation)
        root = tree.getroot()
        self.tabXML(root, '\t', '\n')
        tree.write(osp.join(self._datasetName, self._imageFolder, self._imageName[:-4] + ".xml"), encoding='UTF-8')
    