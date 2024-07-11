# Malaria-Detection-from-Blood-Smears
## Content: 
This repository contains an automated image processing pipeline for quantification and stage categorization of P. vivax from blood smears. We used an image set BBBC041v1, available from the Broad Bioimage Benchmark Collection [Ljosa et al., Nature Methods, 2012] with 1,364 images and ~80,000 cells. Contributors: Jasmyn Lopez and Anthony Chen

## Introduction: 
Despite advancements in malaria control worldwide, the disease remains an immense global health burden. In 2022, the WHO reported 247 million cases and estimated 608,000 deaths.[1] As the deadliest malaria strains (P. falciparum and P. vivax) develop resistance to antimalarial artemisinins and evasion strategies to rapid diagnostic testing, the need for an improved diagnostic solution is greater than ever.[2, 3] Traditionally, malaria diagnosis is conducted via light microscopy or rapid diagnostic testing (RDT). However, due to the large time and expertise cost of light microscopy diagnosis, RDT’s based on Histidine-rich protein II (HRP2) and pan-Plasmodium antigen lactate dehydrogenase (pLDH) are the preferred method for fast, low-cost, point-of-care diagnosis. As a result of selection pressures, P. falciparum have developed pfhrp2 deletions to evade RDT detection, resulting in false negatives and compromising surveillance efforts.[4] In order to reduce the global burden of malaria and progress towards eradication, new, accurate approaches to surveillance testing must be developed.


## Background: 
A number of image analysis and machine learning methods have been developed to automate the detection of infected cells from blood smears.[5] However, these approaches generally do not subcategorize infected cells into their stage of the malaria life cycle. The few that do subcategorize focus on the most virulent strain, P. falciparum.[6] Since the progression of malaria is highly variable (symptoms may emerge 7 days to 1 year after infection), the stage of infected cells provide important indications of disease progression which are crucial for accurate prognosis and treatment.[7] Additionally, stage-specific diagnosis would bolster our understanding of the disease evolution and accelerate the ongoing development of stage-specific drugs, vaccines, and care protocols.[8, 9,10] Considering these advantages and the current gap in scientific literature, we sought to develop an automated image analysis program to quantify and categorize P. vivax infected cells by stage from blood smears. We utilized the “P. vivax (malaria) infected human blood smears” annotated image collection from the Broad Institute, consisting of three sets of images sourced from Brazil (Stefanie Lopes), Southeast Asia (Benoit Malleret), and Penn State University (Gabriel Rangel).[11] The dataset consisted of thick and thin blood smear images totalling 1,364 (~80,000 cells), with each cell labeled as uninfected (RBC or leukocyte) or infected (gametocyte, ring, trophozoite or schizont) for validation purposes.

## Methodology: 
<div align="center">
    <img width="778" alt="MethodsFlowChart" src="https://github.com/jasmynlopez/Malaria-Detection-from-Blood-Smears/assets/141966948/037bdbcb-6073-4356-85f9-712bb62ca7c0">
</div>
<div align="center">
    <em><strong>Figure 1:</strong> Methods Flow Chart</em>
</div>

## Results: 
<div align="center">
	<img width="1019" alt="Results Plots" src="https://github.com/jasmynlopez/Malaria-Detection-from-Blood-Smears/assets/141966948/eeef2855-7fce-4ded-b040-223b297abc94">
</div>

<div align="center">
    <em><strong>Figure 2:</strong>  Infected Cell Counts by Category (left) and Total (right) 
	    Blue indicates the calculated number of infected cells based on our pipeline. Red indicates the true number of infected cells based on the annotated data. Purple indicates the overlap between the two regions (successful identification of infected cells/stages).</em>
</div>
<br />
As can be seen in Fig. 2, our pipeline accurately identified the majority of infected cells and sub-categorized them into their respective stages. Across all images in the dataset, our algorithm’s average percent error was 0.22 cells, with 0.3, 0.22, 0.57, and 0.55 cells for ring, trophozoite, schizont, and gametocyte identification, respectively. 


