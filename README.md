# LatentSync Superresolution Patch

This repository is a modified version of [LatentSync](https://github.com/bytedance/LatentSync) that adds an extra step to enhance the generated (lipsynced) subframes using superresolution models (GFPGAN and/or CodeFormer). The patch compares the resolution of the generated subframe with the original frame and, if needed, automatically upscales it using the specified superresolution method(s).

## Features

- **Conditional Superresolution:** Applies GFPGAN and/or CodeFormer only to the generated subframe when its resolution is lower than the corresponding region in the original frame.
- **Flexible Superres Options:** Pass a parameter (`--superres`) to choose `GFPGAN`, `CodeFormer`, or both (e.g. `GFPGAN,CodeFormer`).
- **Cog Predictor Interface:** The project is set up as a Cog predictor so that it can be deployed on platforms that support Cog.
- **Standalone Running Option:** For macOS users where the Cog CLI may not be available, you can run the predictor as a standalone Python script.

## Requirements

- **Python 3.9+** (or your preferred Python 3 version)
- **Required Python Packages:**  
  - `cog` (if using Cog; otherwise not required for standalone execution)
  - `opencv-python`
  - Other dependencies as required by the original LatentSync project
- **Additional Tools:**  
  - `pget` (for downloading model weights)  
  - *Optional:* Docker (if you wish to run Cog inside a container)

## Repository Structure

LatentSync-patch-2/ ├── checkpoints/ # Pre-trained model weights and auxiliary files ├── configs/ # Configuration files (e.g. second_stage.yaml) ├── scripts/ │ └── inference # Inference script used by the predictor ├── predict.py # Cog predictor interface (with superres integration) ├── inference.sh # Launcher shell script that sets the SUPERRES_METHOD env variable └── README.md # This file

Install Dependencies:
It is recommended to use a virtual environment:
python3 -m venv venv
source venv/bin/activate
Then install the required packages:
pip install -r requirements.txt
If you plan to use the Cog CLI (on supported systems), also install Cog:
pip install cog
Ensure Auxiliary Tools are Installed:
Make sure you have pget installed in your PATH (used for downloading model weights). If not, install it or modify download_weights accordingly.
How to Run the Code

There are two main options to run the project:

Option 1: Run as a Standalone Python Script
You can run the predictor directly without using Cog.

Edit predict.py (if necessary):
Ensure the bottom of your predict.py includes a main block similar to:
if __name__ == "__main__":
    from pathlib import Path

    predictor = Predictor()
    predictor.setup()

    # Provide your video file (MP4 with audio)
    video_path = Path("/path/to/your/video.mp4")
    audio_path = Path("/path/to/your/video.mp4")  # Same file if no separate audio

    guidance_scale = 1.0
    seed = 0  # 0 to auto-generate a seed

    output = predictor.predict(
        video=video_path,
        audio=audio_path,
        guidance_scale=guidance_scale,
        seed=seed
    )
    print("Output video saved at:", output)
Set the Superresolution Method:
Before running, set the environment variable for the superresolution method. For example:
export SUPERRES_METHOD="GFPGAN,CodeFormer"
Run the Predictor:
python3 predict.py

Option 2: Run via Docker with Cog (if preferred)
If you wish to use the Cog interface and your system supports Docker, you can run Cog inside a container.

Install Docker Desktop from Docker's website.
Create a Dockerfile in the repository (if not already provided):
FROM python:3.9-slim

# Install dependencies
RUN pip install cog opencv-python

# Copy your project files
COPY . /app
WORKDIR /app

# Set default command to run the predictor
CMD ["cog", "predict"]

Build the Docker Image:
docker build -t latentsync-cog .
Run the Container:
Mount your local project folder into the container and supply your video file:
docker run --rm -v /path/to/your/video.mp4:/app/your_video.mp4 latentsync-cog --video=@/app/your_video.mp4 --audio=@/app/your_video.mp4 --guidance_scale=1.0 --seed=0 --superres=GFPGAN,CodeFormer



</div>

## 📖 Abstract

We present *LatentSync*, an end-to-end lip sync framework based on audio conditioned latent diffusion models without any intermediate motion representation, diverging from previous diffusion-based lip sync methods based on pixel space diffusion or two-stage generation. Our framework can leverage the powerful capabilities of Stable Diffusion to directly model complex audio-visual correlations. Additionally, we found that the diffusion-based lip sync methods exhibit inferior temporal consistency due to the inconsistency in the diffusion process across different frames. We propose *Temporal REPresentation Alignment (TREPA)* to enhance temporal consistency while preserving lip-sync accuracy. TREPA uses temporal representations extracted by large-scale self-supervised video models to align the generated frames with the ground truth frames.

## 🏗️ Framework

<p align="center">
<img src="assets/framework.png" width=100%>
<p>

LatentSync uses the [Whisper](https://github.com/openai/whisper) to convert melspectrogram into audio embeddings, which are then integrated into the U-Net via cross-attention layers. The reference and masked frames are channel-wise concatenated with noised latents as the input of U-Net. In the training process, we use a one-step method to get estimated clean latents from predicted noises, which are then decoded to obtain the estimated clean frames. The TREPA, [LPIPS](https://arxiv.org/abs/1801.03924) and [SyncNet](https://www.robots.ox.ac.uk/~vgg/publications/2016/Chung16a/chung16a.pdf) losses are added in the pixel space.

## 🎬 Demo

<table class="center">
  <tr style="font-weight: bolder;text-align:center;">
        <td width="50%"><b>Original video</b></td>
        <td width="50%"><b>Lip-synced video</b></td>
  </tr>
  <tr>
    <td>
      <video src=https://github.com/user-attachments/assets/ff3a84da-dc9b-498a-950f-5c54f58dd5c5 controls preload></video>
    </td>
    <td>
      <video src=https://github.com/user-attachments/assets/150e00fd-381e-4421-a478-a9ea3d1212a8 controls preload></video>
    </td>
  </tr>
  <tr>
    <td>
      <video src=https://github.com/user-attachments/assets/32c830a9-4d7d-4044-9b33-b184d8e11010 controls preload></video>
    </td>
    <td>
      <video src=https://github.com/user-attachments/assets/84e4fe9d-b108-44a4-8712-13a012348145 controls preload></video>
    </td>
  </tr>
  <tr>
    <td>
      <video src=https://github.com/user-attachments/assets/7510a448-255a-44ee-b093-a1b98bd3961d controls preload></video>
    </td>
    <td>
      <video src=https://github.com/user-attachments/assets/6150c453-c559-4ae0-bb00-c565f135ff41 controls preload></video>
    </td>
  </tr>
  <tr>
    <td width=300px>
      <video src=https://github.com/user-attachments/assets/0f7f9845-68b2-4165-bd08-c7bbe01a0e52 controls preload></video>
    </td>
    <td width=300px>
      <video src=https://github.com/user-attachments/assets/c34fe89d-0c09-4de3-8601-3d01229a69e3 controls preload></video>
    </td>
  </tr>
  <tr>
    <td>
      <video src=https://github.com/user-attachments/assets/7ce04d50-d39f-4154-932a-ec3a590a8f64 controls preload></video>
    </td>
    <td>
      <video src=https://github.com/user-attachments/assets/70bde520-42fa-4a0e-b66c-d3040ae5e065 controls preload></video>
    </td>
  </tr>
</table>

(Photorealistic videos are filmed by contracted models, and anime videos are from [VASA-1](https://www.microsoft.com/en-us/research/project/vasa-1/) and [EMO](https://humanaigc.github.io/emote-portrait-alive/))

## 📑 Open-source Plan

- [x] Inference code and checkpoints
- [x] Data processing pipeline
- [x] Training code

## 🔧 Setting up the Environment

Install the required packages and download the checkpoints via:

```bash
source setup_env.sh
```

If the download is successful, the checkpoints should appear as follows:

```
./checkpoints/
|-- latentsync_unet.pt
|-- latentsync_syncnet.pt
|-- whisper
|   `-- tiny.pt
|-- auxiliary
|   |-- 2DFAN4-cd938726ad.zip
|   |-- i3d_torchscript.pt
|   |-- koniq_pretrained.pkl
|   |-- s3fd-619a316812.pth
|   |-- sfd_face.pth
|   |-- syncnet_v2.model
|   |-- vgg16-397923af.pth
|   `-- vit_g_hybrid_pt_1200e_ssv2_ft.pth
```

These already include all the checkpoints required for latentsync training and inference. If you just want to try inference, you only need to download `latentsync_unet.pt` and `tiny.pt` from our [HuggingFace repo](https://huggingface.co/ByteDance/LatentSync)

## 🚀 Inference

There are two ways to perform inference, and both require 6.5 GB of VRAM.

### 1. Gradio App

Run the Gradio app for inference:

```bash
python gradio_app.py
```

### 2. Command Line Interface

Run the script for inference:

```bash
./inference.sh
```

You can change the parameters `inference_steps` and `guidance_scale` to see more results.

## 🔄 Data Processing Pipeline

The complete data processing pipeline includes the following steps:

1. Remove the broken video files.
2. Resample the video FPS to 25, and resample the audio to 16000 Hz.
3. Scene detect via [PySceneDetect](https://github.com/Breakthrough/PySceneDetect).
4. Split each video into 5-10 second segments.
5. Remove videos where the face is smaller than 256 $\times$ 256, as well as videos with more than one face.
6. Affine transform the faces according to the landmarks detected by [face-alignment](https://github.com/1adrianb/face-alignment), then resize to 256 $\times$ 256.
7. Remove videos with [sync confidence score](https://www.robots.ox.ac.uk/~vgg/publications/2016/Chung16a/chung16a.pdf) lower than 3, and adjust the audio-visual offset to 0.
8. Calculate [hyperIQA](https://openaccess.thecvf.com/content_CVPR_2020/papers/Su_Blindly_Assess_Image_Quality_in_the_Wild_Guided_by_a_CVPR_2020_paper.pdf) score, and remove videos with scores lower than 40.

Run the script to execute the data processing pipeline:

```bash
./data_processing_pipeline.sh
```

You can change the parameter `input_dir` in the script to specify the data directory to be processed. The processed data will be saved in the `high_visual_quality` directory. Each step will generate a new directory to prevent the need to redo the entire pipeline in case the process is interrupted by an unexpected error.

## 🏋️‍♂️ Training U-Net

Before training, you must process the data as described above and download all the checkpoints. We released a pretrained SyncNet with 94% accuracy on the VoxCeleb2 dataset for the supervision of U-Net training. Note that this SyncNet is trained on affine transformed videos, so when using or evaluating this SyncNet, you need to perform affine transformation on the video first (the code of affine transformation is included in the data processing pipeline).

If all the preparations are complete, you can train the U-Net with the following script:

```bash
./train_unet.sh
```

You should change the parameters in U-Net config file to specify the data directory, checkpoint save path, and other training hyperparameters.

## 🏋️‍♂️ Training SyncNet

In case you want to train SyncNet on your own datasets, you can run the following script. The data processing pipeline for SyncNet is the same as U-Net. 

```bash
./train_syncnet.sh
```

After `validations_steps` training, the loss charts will be saved in `train_output_dir`. They contain both the training and validation loss.

## 📊 Evaluation

You can evaluate the [sync confidence score](https://www.robots.ox.ac.uk/~vgg/publications/2016/Chung16a/chung16a.pdf) of a generated video by running the following script:

```bash
./eval/eval_sync_conf.sh
```

You can evaluate the accuracy of SyncNet on a dataset by running the following script:

```bash
./eval/eval_syncnet_acc.sh
```

## 🙏 Acknowledgement

- Our code is built on [AnimateDiff](https://github.com/guoyww/AnimateDiff). 
- Some code are borrowed from [MuseTalk](https://github.com/TMElyralab/MuseTalk), [StyleSync](https://github.com/guanjz20/StyleSync), [SyncNet](https://github.com/joonson/syncnet_python), [Wav2Lip](https://github.com/Rudrabha/Wav2Lip).

Thanks for their generous contributions to the open-source community.
