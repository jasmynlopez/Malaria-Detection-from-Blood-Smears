import json
from PIL import Image
import matplotlib.pyplot as plt
import sys
import numpy as np
from skimage.filters import unsharp_mask
from skimage.filters import threshold_otsu
from skimage.filters import gaussian
from skimage.filters import threshold_mean
from scipy import ndimage as ndi
from skimage.segmentation import watershed
from skimage.feature import peak_local_max
from skimage import io

def load_image(filename):
    """
    Loads a provided image and returns it as a numpy
    array.

    filename: String representing image filename.
    """
    im = Image.open(filename)
    im_array = np.array(im)
    return im_array

def main():

    args = sys.argv
    # Make sure that file name is entered
    if len(args) != 2:
        print("Please specify a filename.")

    # Open the json file and parse info into a dictionary
    with open('training.json') as f:
        data = json.load(f)
    dict = {}
    #for elem in data:
    for i in range(1208):
        path = data[i]['image']['pathname']
        features = data[i]['objects']
        dict[path] = features
    with open('test.json') as f:
        data2 = json.load(f)
    for i in range(120):
        path = data2[i]['image']['pathname']
        features = data2[i]['objects']
        dict[path] = features
   
    # Plot original image
    filename = args[1]
    im_array = load_image(filename)
    plt.figure('original image') # make a new figure so they all plot at the same time
    plt.imshow(im_array)

    key = str("/" + filename)
    #print(dict)
    img_info = dict[key]
    
    for cell in img_info:
        bbox = cell['bounding_box']
        cell_type = cell['category']
        if (cell_type == 'leukocyte' or cell_type == 'red blood cell'):
            continue
        
        print(cell_type)
        x = bbox['minimum']['c'] + 30
        y = bbox['minimum']['r'] + 64
        plt.text(x, y, cell_type, color='orange', weight='bold', size=8)
        plt.plot(x, y, marker='.', color='white')
        print(x)
        print(y)
        
    plt.show()

    

if __name__ == "__main__":
    main()
