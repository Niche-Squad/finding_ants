# Materials and Methods

## Data Collection and Annotation

The image dataset used in this study was organized into seven distinct subsets, as shown in Figure 1a. The dataset properties, including the number of images and the average number of ants per image, are summarized in Table 1. The dataset was collected using GoPro Hero 9 and ensure the resolution of at least 1920 x 1080 pixels. [lighting details. The images were taken under consistent lighting conditions to ensure uniform image quality. 

The "Calibration" subset shares a similar imaging background with the subsets labeled “A” (i.e., “A01”, “A02”, and “A03”). In contrast, the “B” subsets exhibit more complex imaging conditions: “B01” includes images with black stains resembling ants, “B02” contains images with non-uniform backgrounds, and “B03” represents images with dense ant populations containing more than 700 ants per image on average.

The images were annotated using the YOLO object detection format [cite] to calibrate the CV system to recognize ants. As depicted in Figure 1b, in this format, each ant is marked with a bounding box, defined by four parameters: the x and y coordinates of the box’s center, along with its width and height. These values are normalized to the range [0, 1] by dividing the x and y coordinates by the image’s width and height, respectively. For instance, in a 1920 x 1080 image, a bounding box with a center at (960, 540) and dimensions of 100 x 100 pixels would be represented as (0.5, 0.5, 0.0521, 0.0926), where 0.0521 and 0.0926 are the normalized width and height. Each ant was assigned a class ID. Since the study focuses exclusively on detecting ants without differentiating between species, all ants were assigned a class ID of 0.

Figure 1: (a) Overview of the dataset subsets used in this study. (b) Example of ant annotation in the YOLO object detection format.
alt text: (a) Visual summary of the different data sets used in the study. (b) An image showing an ant marked with a box to demonstrate how the computer detects it.

## Study 1: Determining the Amount of Image Resources Required for Generalization

The "Calibration" subset was used to "teach" the CV system how the ant morphology appears in images, while the other subsets were employed to evaluate its generalization capabilities. The “A” subsets were designed to mimic the system being deployed in an ongoing and repetitive experiment, with images with similar imaging backgrounds over time. In contrast, the “B” subsets aim to test the system robustness in handling images with less controlled imaging conditions. Except for the subset "B03", in which the number of ants per image was significantly higher than in the other subsets and required additional procedures to calibrate the system, this study focused on the performance of the CV system with different number of available images for the model calibration. The availalbe images were randomly sampled from the "Calibration" subset given the numbers of 64, 128, 256, 512, and 1024. Since the number of available images was only 954, when the sampled number was 1024, the system will sample the images with replacement until the number of images reaches 1024. The sampling process was repeated 30 times for each subset and each available numbers to avoid sampling bias. 


## Study 2: Strategies for Handling Dense Imaging Scenarios

Detecting ants in a dense population, such as in subset "B03", is challenging despite an abundance of image data, due to the limitations of the model architecture described in the introduction. Inspired by the Slicing Aided Hyper Inference technique [cite], which improves detection accuracy by dividing input images into smaller patches for separate object detection, this study explores an optimized patch size for subset "B03". To avoid bias from varied sampling, all available images—excluding the "B03" subset—were used for model calibration. The system was calibrated using 1,597 images containing 16,368 total ant instances.

During the calibration process, multiple candidate model weights were generated, and the model with the best performance on two randomly selected images from the "B03" subset was selected for further evaluation. These two images were excluded from subsequent evaluation steps. Finally, the model was evaluated on the "B03" subset using the optimized slicing size. The original images, with a resolution of 1636 x 2180 pixels, were divided into different patch sizes: 818 x 1090 (2 x 2 patches), 818 x 545 (2 x 4 patches), 409 x 545 (4 x 4 patches), 409 x 218 (4 x 10 patches), and 204 x 218 (8 x 10 patches), as shown in Figure 2. The evaluation aimed to identify the optimal patch size for this dense imaging scenario.

Figure 2. Illustration of the image slicing process for the "B03" subset. The original image is divided into patches of different sizes for object detection.

alt txt: An illustration of how an original image from the “B03” set is divided into smaller pieces to help detect ants

## Study 3: Enhancing Understanding of Spatial and Temporal Aspects of Ant Foraging Behaviors

In the object detection format, the precise location and size of each ant in an image are tracked, allowing the CV system to provide more detailed insights into ant foraging behavior than manual counting, which only captures the number of ants in an image. This study utilizes this data format and a Gaussian inference approach [cite] to generate an ant activity heatmap, visualizing the spatial distribution of ant activity across images taken over hours to days.

The first step involves converting each detection’s bounding box—which contains the (x, y) coordinates and its width and height—into a circle. The center of the circle is at (x, y), and the radius (r) is the average of the width and height. An all-zero grid with a resolution of 1000 x 1000 pixels (arbitrarily selected) is then initialized as a placeholder matrix for the heatmap. For each ant detection, the Euclidean distance (d) from the center of the circle to each pixel in the grid is calculated. The squared distance, d², is divided by the squared radius, r², to determine an inverse intensity value—greater distances correspond to lower intensities. The intensity values are exponentiated to ensure a smooth gradient representation for each ant (Eq. 1). These values are accumulated on the grid for all ant detections across all images, producing a heatmap that visually represents areas of higher ant activity.

In addition to spatial data, temporal changes in ant presence were analyzed to examine the relationship between the number of ants and time during the study period. For example, in subset “B02,” where two bait types—sucrose (labeled ‘S’) and peptone (labeled ‘P’)—were placed in the same image, the aim was to understand the ants’ foraging preferences. If the sucrose bait was positioned in the upper-right and the peptone in the lower-left of the image, a simple linear function L(x, y) = y - ax - b was used to separate the ants based on their attraction to the respective baits. Here, a is the slope, b is the intercept, and (x, y) represents the center of the ant detection. If the result of L(x, y) is positive, the ant is located on the upper (right) side of the line and is attracted to the sucrose; if negative, the ant is on the lower (left) side of the line and is attracted to the peptone.

## Model Calibration and Evaluation

The CV detection system is based on the YOLOv8 architecture [cite]. Given that ant detection is relatively straightforward compared to general object detection tasks involving over 50 object classes [cite], the smallest model version, YOLOv8n, with 3.2 million parameters, was chosen to balance detection accuracy and computational efficiency. This model version is suitable for deployment on most personal computers due to its minimal hardware requirements (e.g., GPU or high memory), without compromising detection performance, particularly for simple tasks [cite].

The model was calibrated using the designated number of images and subsets from Studies 1 and 2. To mitigate imaging biases caused by inconsistent camera angles, lighting conditions, and ant distribution, data augmentation was applied during the calibration process. This augmentation involved introducing random noise, rotation, scaling, and cropping to the original images, enhancing the model’s robustness to such variations. The model was calibrated with the Adam optimizer [cite], using a learning rate scheduler that started at 0.001 and decreased by 10% every 10 epochs. The batch size was set to 16, and the calibration was conducted for a total of 100 epochs. Twenty percent of the calibration dataset was randomly selected as the validation set to monitor performance during calibration. The model achieving the best performance on the validation set was chosen for subsequent evaluation. Calibration was conducted using the Ultralytics framework on NVIDIA A100 GPUs.

Model evaluation was performed on the designated subsets from Studies 1 and 2, using metrics such as recall, precision, R², and Root Mean Square Error (RMSE). Recall and precision were calculated based on the number of true positive (TP), false positive (FP), and false negative (FN) detections:


\text{Recall} = \frac{TP}{TP + FN}

\text{Precision} = \frac{TP}{TP + FP}


A high recall indicates that the model successfully detected most ants in the images, while a high precision indicates that the detections were mostly correct with few false positives. Two additional criteria were considered when calculating precision and recall: Intersection over Union (IoU) and confidence threshold. IoU measures the ratio of overlap between the detected bounding box and the actual area occupied by the ant, while the confidence threshold is the minimum confidence score required for a detection to be included in the final results. In this study, the IoU and confidence threshold were set at 0.6 and 0.25, respectively. In addition to evaluating detection performance, R² and RMSE were calculated to compare automated counting results with manual counts. 

\text{r} =(\frac{\text{cov}(\hat{Y}, Y)}{\sigma_\hat{Y} \sigma_Y}) ^ 2

\text{RMSE} = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (\hat{Y}_i - Y_i)^2}
where Y and \hat{Y} are the manual and automated counts, respectively, and n is the total number of images. \sigma_Y and \sigma_\hat{Y} are the standard deviations of the manual and automated counts, respectively. R² assesses the agreement between automated and manual counting results, while RMSE measures the absolute difference between them. Depending on different needs of model accuracy, such as focusing on precise localization or counting, these metrics provide a comprehensive evaluation of the model’s effectiveness and reliability for automated ant detection and counting.

R² assesses the agreement between automated and manual counting results, while RMSE measures the absolute difference between them. Depends on different needs of model accuracy, such as focusing on precise localization or counting, these metrics provide a comprehensive evaluation of the model’s effectiveness and reliability for automated ant detection and counting