#!/usr/bin/env python
"""
predict.py – Main inference code for LatentSync that conditionally applies superresolution
using GFPGAN and/or CodeFormer on the generated (lipsynced) subframe.
"""

import os
import cv2
import numpy as np

# -------------------------------
# Superresolution helper functions
# -------------------------------

def GFPGAN_enhance(image, scale_factor):
    """
    Enhance the image using GFPGAN.
    (This is a placeholder function. In a real implementation, you would load
    and apply the GFPGAN model here.)
    For demonstration, we use cv2.resize with cubic interpolation.
    """
    new_width = int(image.shape[1] * scale_factor)
    new_height = int(image.shape[0] * scale_factor)
    enhanced = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
    return enhanced

def CodeFormer_enhance(image, scale_factor):
    """
    Enhance the image using CodeFormer.
    (This is a placeholder function. Replace it with the actual CodeFormer API call.)
    Here we use cv2.resize with linear interpolation for demonstration.
    """
    new_width = int(image.shape[1] * scale_factor)
    new_height = int(image.shape[0] * scale_factor)
    enhanced = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
    return enhanced

def apply_superres(image, scale_factor, method):
    """
    Apply superresolution on the given image using the specified method(s).
    
    Parameters:
        image       : numpy array of the subframe image.
        scale_factor: factor by which the image should be upscaled.
        method      : string indicating which method(s) to use (e.g., 'GFPGAN', 'CodeFormer', or 'GFPGAN,CodeFormer').
    
    Returns:
        The enhanced image as a numpy array.
    """
    # If the method contains a comma, split into multiple methods.
    if ',' in method:
        methods = [m.strip() for m in method.split(',')]
    else:
        methods = [method.strip()]

    output = image
    for m in methods:
        if m.lower() == 'gfpgan':
            output = GFPGAN_enhance(output, scale_factor)
        elif m.lower() == 'codeformer':
            output = CodeFormer_enhance(output, scale_factor)
        else:
            raise ValueError(f"Unknown superres method: {m}")
    return output

# -------------------------------
# Frame processing functions
# -------------------------------

def upscale_if_needed(generated_region, original_region, method):
    """
    Compare the resolution of the generated subframe with the original region.
    If the generated region is lower resolution, upscale it using the specified method.
    
    Parameters:
        generated_region: numpy array of the generated (lipsynced) subframe.
        original_region : numpy array of the corresponding region from the original frame.
        method          : string indicating the superresolution method to use.
    
    Returns:
        The enhanced (upscaled) region as a numpy array.
    """
    gen_h, gen_w = generated_region.shape[:2]
    orig_h, orig_w = original_region.shape[:2]
    
    scale_w = orig_w / gen_w
    scale_h = orig_h / gen_h

    # If either scaling factor is greater than 1, we need to upscale.
    if scale_w > 1 or scale_h > 1:
        scale_factor = max(scale_w, scale_h)
        enhanced_region = apply_superres(generated_region, scale_factor, method)
        # Resize the enhanced region exactly to the original dimensions.
        enhanced_region = cv2.resize(enhanced_region, (orig_w, orig_h), interpolation=cv2.INTER_CUBIC)
        return enhanced_region
    else:
        return generated_region

def process_frame(frame, region_coords, generated_region):
    """
    Replace the lower-resolution generated region in the full frame with an enhanced version.
    
    Parameters:
        frame           : numpy array representing the full video frame.
        region_coords   : a tuple (x, y, w, h) specifying the location of the generated subframe.
        generated_region: numpy array of the generated subframe.
    
    Returns:
        The full frame with the enhanced subframe.
    """
    x, y, w, h = region_coords
    original_region = frame[y:y+h, x:x+w]
    
    # Read the superresolution method from the environment variable (set by inference.sh)
    method = os.environ.get('SUPERRES_METHOD', 'none')
    if method.lower() != 'none':
        enhanced_region = upscale_if_needed(generated_region, original_region, method)
        frame[y:y+h, x:x+w] = enhanced_region
    else:
        frame[y:y+h, x:x+w] = generated_region

    return frame

# -------------------------------
# Main inference routine
# -------------------------------

def main():
    """
    Main function for processing a single frame.
    In a real system, this would loop over all frames in a video.
    """
    # For demonstration, load an example full frame and a generated subframe.
    # Replace these file names with your actual frame extraction code.
    frame = cv2.imread("input_frame.png")  # the full original frame
    generated_region = cv2.imread("generated_face.png")  # the lipsynced generated region
    
    if frame is None or generated_region is None:
        print("Error: Could not load the required images. Make sure 'input_frame.png' and 'generated_face.png' exist.")
        return

    # Define where in the full frame the generated region should go.
    # For example, (x, y, width, height) = (100, 50, 200, 200)
    region_coords = (100, 50, 200, 200)
    
    # Process the frame: this will compare the region sizes and apply superresolution if needed.
    processed_frame = process_frame(frame, region_coords, generated_region)
    
    # Save the processed frame so you can see the result.
    cv2.imwrite("processed_frame.png", processed_frame)
    print("Processed frame saved as 'processed_frame.png'.")

if __name__ == "__main__":
    main()
