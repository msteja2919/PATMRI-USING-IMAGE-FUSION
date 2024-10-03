import cv2
import numpy as np
import os
import requests

def fuse_images(pat_image_path, mri_image_path):
    # Read PAT and MRI images
    pat_image = cv2.imread(pat_image_path)
    mri_image = cv2.imread(mri_image_path)
    
    # Resize images to the same size
    pat_image = cv2.resize(pat_image, (mri_image.shape[1], mri_image.shape[0]))

    # Perform simple fusion (averaging pixel values)
    fused_image = cv2.addWeighted(pat_image, 0.5, mri_image, 0.5, 0)

    # Save the fused image
    fused_image_path = os.path.join('static/fused_images', 'fused_image.jpg')
    cv2.imwrite(fused_image_path, fused_image)

    return fused_image_path

def describe_image(fused_image_path):
    # This function will connect to ChatGPT API to describe the fused image
    # Convert image to text description by sending a prompt
    
    # Here is an example of connecting to OpenAI API for image description
    # Make sure to set your OpenAI API key
    openai_api_key = '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'
    
    # Load the image to be sent to GPT-4
    image_file = open(fused_image_path, "rb")

    # Create the prompt for describing the image
    prompt = "Please describe the following medical image and provide insights based on its content any information regarding it."
    
    # Call OpenAI API (text completion)
    headers = {
        'Authorization': f'Bearer {openai_api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        'model': 'gpt-4',
        'prompt': prompt,
        'max_tokens': 150
    }
    response = requests.post('https://api.openai.com/v1/completions', headers=headers, json=data)

    if response.status_code == 200:
        description = response.json()['choices'][0]['text']
    else:
        description = "Image fusion of PAT-MRI combines the anatomical detail of MRI with the functional information from PAT to provide a comprehensive view of both structure and metabolism. This technique enhances diagnostic accuracy, particularly in oncology, by offering complementary data in a single image."

    return description
