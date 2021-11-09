import cv2
import os
import xml.etree.ElementTree as ET
from matplotlib import pyplot as plt
import numpy as np
import glob


def readPascalVoc(xml_file: str):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    list_with_all_boxes = []

    for boxes in root.iter('object'):

        ymin, xmin, ymax, xmax, name = None, None, None, None, None
        
        
        name = boxes.find('name').text
        ymin = int(boxes.find("bndbox/ymin").text)
        xmin = int(boxes.find("bndbox/xmin").text)
        ymax = int(boxes.find("bndbox/ymax").text)
        xmax = int(boxes.find("bndbox/xmax").text)

        list_with_single_boxes = (name,[xmin, ymin, xmax, ymax])
        list_with_all_boxes.append(list_with_single_boxes)

    return list_with_all_boxes

def readImagesFromAnnotation(annotation: str,pathToAnnotation:str,pathToImg:str):
    fichierXML = os.path.join(pathToAnnotation,annotation)
    boxes = readPascalVoc(fichierXML)
    fichierImage = os.path.join(pathToImg,os.path.basename(annotation.replace(".xml","")))
    fichierImage = glob.glob(fichierImage+".*")
    if len(fichierImage) == 1:
        fichierImage = fichierImage[0]
    else:
        print(fichierImage,"N images ?")
    image = None
    if os.path.exists(fichierImage):
        image = cv2.imread(fichierImage)
    else:
        print(fichierImage,"inexistant traitement passé")
        return (None,None,None)
    sizeX,sizeY = image.shape[:2]
    image_with_mask = np.zeros((sizeX,sizeY,1), np.uint8)
    image_without_mask = np.zeros((sizeX,sizeY,1), np.uint8)
    image_with_incorrect_mask = np.zeros((sizeX,sizeY,1), np.uint8)
    for visage in boxes:
        couleur = 255
        point1 = (visage[1][0],visage[1][1])
        point2 = (visage[1][2],visage[1][3])
        if "with_mask" in visage[0]:
            cv2.rectangle(image_with_mask, point1, point2, couleur,-1)

        if "without_mask" in visage[0]:
            cv2.rectangle(image_without_mask, point1, point2, couleur,-1)

        if "mask_weared_incorrect" in visage[0] or "with_incorrect_mask" in visage[0]:
            cv2.rectangle(image_with_incorrect_mask, point1, point2, couleur,-1)
    basseresolution = (512,512)
    image_with_mask= cv2.resize(image_with_mask,basseresolution,interpolation = cv2.INTER_NEAREST)
    image_without_mask =cv2.resize(image_without_mask,basseresolution,interpolation = cv2.INTER_NEAREST)
    image_with_incorrect_mask =cv2.resize(image_with_incorrect_mask,basseresolution,interpolation = cv2.INTER_NEAREST)
    return (image_with_mask,image_without_mask,image_with_incorrect_mask)

def showAnnotation(annotation: str,pathToAnnotation:str,pathToImg:str):
    image_with_mask,image_without_mask,image_with_incorrect_mask = readImagesFromAnnotation(annotation,pathToAnnotation,pathToImg)

    plt.figure(figsize=(120, 80))
    ax = plt.subplot(1, 4, 1)
    plt.imshow(image_with_mask,cmap=plt.cm.gray)
    ax = plt.subplot(1, 4, 2)
    plt.imshow(image_without_mask,cmap=plt.cm.gray)
    ax = plt.subplot(1, 4, 3)
    plt.imshow(image_with_incorrect_mask,cmap=plt.cm.gray)

    plt.show()