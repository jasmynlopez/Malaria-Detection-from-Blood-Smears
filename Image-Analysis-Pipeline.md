# Image Analysis Pipeline

We began our analysis by acquiring a substantial microscopy image dataset of malaria infected human blood smears stained with Giemsa reagent.[11] We developed a comprehensive image analysis pipeline composed of 4 stages: preprocessing, segmentation, morphological filtering, and validation. Fig. 1 shows a block diagram broadly outlining this algorithm below.
<div align="center">
    <img width="778" alt="MethodsFlowChart" src="https://github.com/jasmynlopez/Malaria-Detection-from-Blood-Smears/assets/141966948/deb7c06f-7b40-4864-a293-cab64bdba2dd">
</div>
<div align="center">
    <em><strong>Figure 1:</strong> Methods Flow Chart</em>
</div>
The preprocessing phase begins with image resizing to guarantee uniform pixel dimensions across all images and facilitate accurate size comparison of infected cells for subsequent analysis. Fig. 3 shows the original image after image resizing. Next, to reduce variations in the images, we applied low-pass Gaussian filtering to reduce the influence of high-frequency features.[12] The Gaussian filter significantly reduced noise, however, Fig. 4 shows the collateral reduction in edge definition. In order to preserve edges and details in our image following the Gaussian smoothing, we employed unsharp masking to increase the contrast of edges, effectively delineating clear bounds for infected cells. Layering the Gaussian filter and unsharp mask reveal a sharpened image with reduced noise as depicted in Fig. 5. Finally, by converting images to the HSV (hue, saturation, value) color space, we were able to normalize color intensity to allow for comparison of purple intensities across microscopy images taken under varying lighting conditions. This standardization enables reliable comparisons of our images by providing a consistent basis for color intensity analysis. For visualization purposes, Fig. 6 shows our colorized normal image in the RGB colorspace, while Fig. 8 shows the same image represented in the HSV colorspace.

<div align="center">
    <img width="387" alt="Screenshot 2024-07-11 at 1 50 03 PM" src="https://github.com/jasmynlopez/Malaria-Detection-from-Blood-Smears/assets/141966948/8cb5b71e-d5a2-4f87-83df-805929e9e709">
    </br>
    <em><strong>Figure 3:</strong> Methods Flow Chart </em>
</div>
</br>



<div align="center">
     <img width="387" alt="Screenshot 2024-07-11 at 1 49 35 PM" src="https://github.com/jasmynlopez/Malaria-Detection-from-Blood-Smears/assets/141966948/f02f402b-2b1f-448c-8ec5-5e4451b75200">
    </br>
    <em><strong>Figure 4:</strong> Methods Flow Chart</em>
</div>
</br>





<div align="center">
    <img width="387" alt="Screenshot 2024-07-11 at 1 49 51 PM" src="https://github.com/jasmynlopez/Malaria-Detection-from-Blood-Smears/assets/141966948/6a036b41-3036-43c5-bc4d-aca4524df50e">
    <img width="387" alt="Screenshot 2024-07-11 at 1 49 41 PM" src="https://github.com/jasmynlopez/Malaria-Detection-from-Blood-Smears/assets/141966948/d6184fae-4bde-4f5f-ae1a-92e595c478cb">
</div>
</br>

next two images
<div align="center">
    <img width="387" alt="Screenshot 2024-07-11 at 1 50 21 PM" src="https://github.com/jasmynlopez/Malaria-Detection-from-Blood-Smears/assets/141966948/77ffd073-0559-4ce4-aced-a14b2bb546df">
    <img width="387" alt="Screenshot 2024-07-11 at 1 50 29 PM" src="https://github.com/jasmynlopez/Malaria-Detection-from-Blood-Smears/assets/141966948/ade23a66-30dc-4805-b729-80aa85014b69">
</div>
</br>



zoom in images 
<div align="center">
    <img width="902" alt="Screenshot 2024-07-11 at 1 50 55 PM" src="https://github.com/jasmynlopez/Malaria-Detection-from-Blood-Smears/assets/141966948/9920ae0b-becb-4118-9761-5a9dd02e456b">
</div>
</br>

purple image 
<div align="center">
    <img width="491" alt="Screenshot 2024-07-11 at 1 53 22 PM" src="https://github.com/jasmynlopez/Malaria-Detection-from-Blood-Smears/assets/141966948/6332d6b4-5b08-40fe-ae1c-41c2031fae00">
</div>





