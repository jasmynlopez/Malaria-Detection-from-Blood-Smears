# Image Analysis Pipeline

We began our analysis by acquiring a substantial microscopy image dataset of malaria infected human blood smears stained with Giemsa reagent.[11] We developed a comprehensive image analysis pipeline composed of 4 stages: preprocessing, segmentation, morphological filtering, and validation. Fig. 1 shows a block diagram broadly outlining this algorithm below.
<div align="center">
    <img width="778" alt="MethodsFlowChart" src="https://github.com/jasmynlopez/Malaria-Detection-from-Blood-Smears/assets/141966948/deb7c06f-7b40-4864-a293-cab64bdba2dd">
</div>
<div align="center">
    <em><strong>Figure 1:</strong> Methods Flow Chart</em>
</div>
The preprocessing phase begins with image resizing to guarantee uniform pixel dimensions across all images and facilitate accurate size comparison of infected cells for subsequent analysis. Fig. 3 shows the original image after image resizing. Next, to reduce variations in the images, we applied low-pass Gaussian filtering to reduce the influence of high-frequency features.[12] The Gaussian filter significantly reduced noise, however, Fig. 4 shows the collateral reduction in edge definition. In order to preserve edges and details in our image following the Gaussian smoothing, we employed unsharp masking to increase the contrast of edges, effectively delineating clear bounds for infected cells. Layering the Gaussian filter and unsharp mask reveal a sharpened image with reduced noise as depicted in Fig. 5. Finally, by converting images to the HSV (hue, saturation, value) color space, we were able to normalize color intensity to allow for comparison of purple intensities across microscopy images taken under varying lighting conditions. This standardization enables reliable comparisons of our images by providing a consistent basis for color intensity analysis. For visualization purposes, Fig. 6 shows our colorized normal image in the RGB colorspace, while Fig. 8 shows the same image represented in the HSV colorspace.
</br>
</br>
<div align="center">
<img width="387" alt="Screenshot 2024-07-11 at 1 50 03 PM" src="https://github.com/user-attachments/assets/0cc81f16-a25c-44d6-a35e-cc0b016ec9ff">
    </br>
    <em><strong>Figure 3:</strong> Resized Original Image</em>
</div>
</br>

<div align="center">
    <img width="387" alt="Screenshot 2024-07-11 at 1 49 35 PM" src="https://github.com/user-attachments/assets/4044f32d-d627-4e84-a38c-42f6613cf484">
    </br>
    <em><strong>Figure 4:</strong> Gaussian</em>
</div>
</br>


<div align="center">
    <img width="387" alt="Screenshot 2024-07-11 at 1 49 51 PM" src="https://github.com/jasmynlopez/Malaria-Detection-from-Blood-Smears/assets/141966948/6a036b41-3036-43c5-bc4d-aca4524df50e">
    </br>
    <em><strong>Figure 5:</strong> Unsharp Mask </em>
</div>
</br>



<div align="center">
    <img width="387" alt="Screenshot 2024-07-11 at 1 49 41 PM" src="https://github.com/jasmynlopez/Malaria-Detection-from-Blood-Smears/assets/141966948/d6184fae-4bde-4f5f-ae1a-92e595c478cb">
    </br>
    <em><strong>Figure 6:</strong> Normalize Color Intensity (RGB)</em>
</div>
</br>

After the image preprocessing phase, we began to focus on cell segmentation. Our approach combined the Otsu mask and color segmentation to isolate infected cells using thresholding techniques. Otsu’s method is a technique used to perform automatic thresholding, separating pixels from the foreground and background into two classes.[14] In order to segment cells from the background image, we applied Otsu segmentation on grayscaled Fig. 5. The resulting binary segmentation is seen in Fig. 6. Next, we overlaid the HSV intensities (Fig. 7) with our Otsu mask (Fig. 6) to isolate all cells and represent their respective color intensities in the HSV color space. To apply color thresholding, we first designed a purple mask representing the purple hues within our HSV image. Overlaying this purple mask seen in Fig. 8 onto our Otsu mask refined our image to the purple hues of our Otsu masked HSV image, creating Fig. 9. After calculating the mean purple intensity within our segmented cells (Fig. 7), we established a threshold by applying a data-informed factor to this average. This threshold improved the accuracy of our classification and allowed for unique segmentation based on average purple intensities for individual images.
</br>

<div align="center">
<img width="387" alt="Screenshot 2024-07-11 at 1 50 21 PM" src="https://github.com/user-attachments/assets/f9c18b10-fb01-4aca-8b60-c8fbbb4599cb">
    </br>
    <em><strong>Figure 7:</strong> Otsu Mask </em>
</div>
</br>



<div align="center">
<img width="387" alt="Screenshot 2024-07-11 at 1 50 29 PM" src="https://github.com/user-attachments/assets/1d870084-774a-4ea4-a5a4-807bd876feec">
    </br>
    <em><strong>Figure 8:</strong> Normalize Color Intensity (HSV)</em>
</div>
</br>



zoom in images 
<div align="center">
    <img width="402" alt="Screenshot 2024-07-11 at 3 56 37 PM" src="https://github.com/user-attachments/assets/83d316dc-a1fa-4d95-a238-d2c3703cd910">
    </br>
    <em><strong>Figure 9:</strong> Purple Thresholding </em>
</div>
</br>



<div align="center">
<img width="399" alt="Screenshot 2024-07-11 at 3 56 58 PM" src="https://github.com/user-attachments/assets/79c9436e-3b70-401c-a575-6a862ab8ef00">
    </br>
    <em><strong>Figure 10:</strong> Otsu * Purple Thresholding </em>
</div>
</br>

purple image 
<div align="center">
    <img width="491" alt="Screenshot 2024-07-11 at 1 53 22 PM" src="https://github.com/jasmynlopez/Malaria-Detection-from-Blood-Smears/assets/141966948/6332d6b4-5b08-40fe-ae1c-41c2031fae00">
</div>








