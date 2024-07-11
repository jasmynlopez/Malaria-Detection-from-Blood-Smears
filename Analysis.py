"""
Usage: python Analysis.py <image_folder>
Program for pre-processing, segmentation, and classification of P. vivax (malaria) infected human blood smears stained with Giemsa reagent.
"""

from PIL import Image
import matplotlib.pyplot as plt
import sys
import numpy as np
import json
from skimage.filters import unsharp_mask
from skimage.filters import threshold_otsu
from skimage.filters import gaussian
from scipy import ndimage as ndi
from skimage import transform
from skimage.segmentation import watershed
from skimage.feature import peak_local_max
from skimage.color import rgb2hsv, hsv2rgb, rgb2gray

def load_image(filename):
    """
    Returns image as a numpy array
    """
    im = Image.open(filename)
    im_array = np.array(im)
    return im_array


def sharpen_image(im_array):
    """
    Applies the sci-kit unsharp mask to image
    """
    im_sharp = unsharp_mask(im_array, radius=50, amount=1)
    return im_sharp


def gaussian_image(im_array):
    """
    Applies the sci-kit gaussian mask to image
    """
    im_smooth = gaussian(im_array, sigma=0.5, mode='reflect', channel_axis=-1) # sigma is strength of smoothing
    return im_smooth


def otsu(im_array): # im_array = im_sharpsmooth
    """
    Uses skimage Otsu thresholding to return a binary, segmented image
    """
    thresh = threshold_otsu(im_array)
    im_otsu = im_array < thresh
    return im_otsu


def infected_segmentation(im_array1, im_array2): # im_array1 = im_otsu im_array2 = im_hsv
    """
    Returns a segmented image based on a scaled, high contrast
    """
    lower_purple = np.array([240/360, 0.3, 0.1])
    upper_purple = np.array([310/360, 1, 1])
    cell_mask = im_array1 == 1
    cell_hsv = im_array2 * cell_mask[..., np.newaxis]
    purple_mask = np.all((cell_hsv >= lower_purple) & (cell_hsv <= upper_purple), axis=-1)
    purple_cell_mask = im_array2
    purple_cell_mask[~purple_mask] = 0
    purple_threshold = np.mean(purple_cell_mask[:,:, 2]) * 10
    im_infected_binary = np.where(im_array2[:,:, 2] > purple_threshold, 1, 0)
    return im_infected_binary


def watershed_segmentation(im_array): # im_array = im_infected_binary (separate infected regions)
    """
    Applies a watershed algorithm to separate unique infected regions (groups unique regions within 20 pixels)
    """
    smoothed = ndi.morphology.grey_opening(im_array, size=(20,20))
    distance = ndi.distance_transform_edt(im_array)
    coords = peak_local_max(distance, footprint=np.ones((20, 20)), labels=im_array)
    mask = np.zeros(distance.shape, dtype=bool)
    mask[tuple(coords.T)] = True
    dilated_mask = ndi.morphology.binary_dilation(mask, structure=np.ones((20,20)))
    markers, _ = ndi.label(dilated_mask)
    im_watershed = watershed(-distance, markers, mask=im_array)
    return im_watershed, markers


def parse_json():
    """
    Parses annotated data from json file into dict (dict[pathname] = {"gametocyte": 0, "schizont": 0, "ring": 0, "trophozoite": 0})
    """
    dict = {}
    with open('training.json') as f:
        data = json.load(f)
    for i in range(1208):
        pathname = data[i]['image']['pathname']
        all_cells = data[i]['objects']
        dict[pathname] = {"gametocyte": 0, "schizont": 0, "ring": 0, "trophozoite": 0}
        for cell in all_cells:
            cell_type = cell['category']
            if cell_type in list(dict[pathname].keys()): dict[pathname][str(cell_type)] += 1
    with open('test.json') as f:
        data2 = json.load(f)
    for i in range(120):
        pathname = data2[i]['image']['pathname']
        all_cells = data2[i]['objects']
        dict[pathname] = {"gametocyte": 0, "schizont": 0, "ring": 0, "trophozoite": 0}
        for cell in all_cells:
            cell_type = cell['category']
            if cell_type in list(dict[pathname].keys()): dict[pathname][str(cell_type)] += 1
    return dict


def main():
    args = sys.argv
    if len(args) < 2:
        print("Please specify an image folder name.")
    else:
        # JSON PARSING

        dict = parse_json()

        # IMAGE PROCESSING
        data = {}
        total_infected = {}
        for filename in dict.keys():
            filename = filename[1:]
            im_array = load_image(filename)
            im_array = transform.resize(im_array, (280, 400), anti_aliasing=True)
            im_smooth = gaussian_image(im_array)
            im_sharpsmooth = sharpen_image(im_smooth)
            im_hsv = rgb2hsv(im_sharpsmooth)
            im_hsv[:,:,2] = im_hsv[:,:,2] / np.amax(im_hsv[:,:,2])
            im_norm_rgb = hsv2rgb(im_hsv)
            im_norm_gray = rgb2gray(im_norm_rgb)
            im_otsu = otsu(im_norm_gray)
            im_infected_binary = infected_segmentation(im_otsu, im_hsv)
            im_watershed, markers = watershed_segmentation(im_infected_binary)

            # DATA COLLECTION
            sizes = {}
            for row in markers:
                for col in row:
                    if col != 0:
                        if col not in sizes.keys():
                            sizes[col] = 0
                        sizes[col] += 1
            infected_counts = {'gametocytes': 0, 'schizonts': 0, 'rings': 0, 'trophozoites': 0}
            for infected_cell in sizes.keys():
                if sizes[infected_cell] > 500:
                    if sizes[infected_cell] < 700:
                        infected_counts['rings'] += 1
                    elif sizes[infected_cell] < 1200:
                        infected_counts['trophozoites'] += 1
                    elif sizes[infected_cell] < 1300:
                        infected_counts['schizonts'] += 1
                    elif sizes[infected_cell] < 1400:
                        infected_counts['gametocytes'] += 1
            data[filename] = infected_counts
            total_infected[filename] = infected_counts['rings'] + infected_counts['trophozoites'] + infected_counts['gametocytes'] + infected_counts['schizonts']


        # PLOTTING
        x = range(len(dict.keys()))

        # plot of total infected cell counts program vs. json
        true_counts = []
        im_counts = []
        total_errors = []
        for image in dict.keys():
            true_count = dict[image]["gametocyte"] + dict[image]["schizont"] + dict[image]["ring"] + dict[image]["trophozoite"]
            true_counts.append(true_count)
            image = image[1:]
            im_counts.append(total_infected[image])
            if true_count != 0:
                total_errors.append(abs(((true_count - total_infected[image])/true_count) * 100))

        plt.figure('Total Infected Cell Counts')
        plt.xlabel('Image Number')
        plt.bar(x, true_counts, color='r', alpha=0.5)
        plt.bar(x, im_counts, color='b', alpha=0.5)
        plt.ylabel('Infected Cell Count')
        plt.title('Total Infected Cell Counts \n Average Error = ' + str(round(np.mean(total_errors)/len(total_errors), 2)))

        # plots of each infected cell type program vs. json

        # rings
        true_ring = []
        im_ring = []
        ring_errors = []
        for image in dict.keys():
            true_ring.append(dict[image]["ring"])
            image = image[1:]
            im_ring.append(data[image]['rings'])
            if dict['/' + image]["ring"] != 0:
                ring_errors.append(abs(((dict['/' + image]["ring"] - data[image]['rings'])/dict['/' + image]["ring"]) * 100))


        plt.figure('Infected Cell Counts by Type', figsize=(10,8))
        plt.subplots_adjust(hspace=0.5)
        plt.subplot(2, 2, 1)
        plt.xlabel('Image Number')
        plt.bar(x, true_ring, color='r', alpha=0.5)
        plt.bar(x, im_ring, color='b', alpha=0.5)
        plt.ylabel('Ring Cell Count')
        plt.title('Ring Cell Counts \n Average Error = ' + str(round(np.mean(ring_errors)/len(ring_errors), 2)))

        # trophozoites
        true_trophozoite = []
        im_trophozoite = []
        trophozoite_errors = []
        for image in dict.keys():
        #for i in range(1000):
            #image = images[i]

            true_trophozoite.append(dict[image]["trophozoite"])
            image = image[1:]
            im_trophozoite.append(data[image]['trophozoites'])
            if dict['/' + image]["trophozoite"] != 0:
                trophozoite_errors.append(abs(((dict['/' + image]["trophozoite"] - data[image]['trophozoites'])/dict['/' + image]["trophozoite"]) * 100))

        plt.subplot(2, 2, 2)
        plt.xlabel('Image Number')
        plt.bar(x, true_trophozoite, color='r', alpha=0.5)
        plt.bar(x, im_trophozoite, color='b', alpha=0.5)
        plt.ylabel('Trophozoite Cell Count')
        plt.title('Trophozoite Cell Counts \n Average Error = ' + str(round(np.mean(trophozoite_errors)/len(trophozoite_errors), 2)))

        # gametocytes
        true_gametocyte = []
        im_gametocyte = []
        gametocyte_errors = []
        for image in dict.keys():
        #for i in range(1000):
            #image = images[i]

            true_gametocyte.append(dict[image]["gametocyte"])
            image = image[1:]
            im_gametocyte.append(data[image]['gametocytes'])
            if dict['/' + image]["gametocyte"] != 0:
                gametocyte_errors.append(abs(((dict['/' + image]["gametocyte"] - data[image]['gametocytes'])/dict['/' + image]["gametocyte"]) * 100))

        plt.subplot(2, 2, 3)
        plt.xlabel('Image Number')
        plt.bar(x, true_gametocyte, color='r', alpha=0.5)
        plt.bar(x, im_gametocyte, color='b', alpha=0.5)
        plt.ylabel('Gametocyte Cell Count')
        plt.title('Gametocyte Cell Counts \n Average Error = ' + str(round(np.mean(gametocyte_errors)/len(gametocyte_errors), 2)))

        # schizonts
        true_schizont = []
        im_schizont = []
        schizont_errors = []
        for image in dict.keys():
        #for i in range(1000):
            #image = images[i]

            true_schizont.append(dict[image]["schizont"])
            image = image[1:]
            im_schizont.append(data[image]['schizonts'])
            if dict['/' + image]["schizont"] != 0:
                schizont_errors.append(abs(((dict['/' + image]["schizont"] - data[image]['schizonts'])/dict['/' + image]["schizont"]) * 100))

        plt.subplot(2, 2, 4)
        plt.xlabel('Image Number')
        plt.bar(x, true_schizont, color='r', alpha=0.5)
        plt.bar(x, im_schizont, color='b', alpha=0.5)
        plt.ylabel('Schizont Cell Count')
        plt.title('Schizont Cell Counts \n Average Error = ' + str(round(np.mean(schizont_errors)/len(schizont_errors), 2)))

        plt.show()

if __name__ == "__main__":
    main()
