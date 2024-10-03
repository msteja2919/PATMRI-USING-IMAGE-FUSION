from flask import Flask, render_template, request, redirect, url_for
from fusion import fuse_images, describe_image
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/fused_images'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_images():
    if request.method == 'POST':
        # Get PAT and MRI image files
        pat_image = request.files['pat_image']
        mri_image = request.files['mri_image']
        
        # Save the images locally
        pat_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'pat_image.jpg')
        mri_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'mri_image.jpg')
        
        pat_image.save(pat_image_path)
        mri_image.save(mri_image_path)
        
        # Fuse the images
        fused_image_path = fuse_images(pat_image_path, mri_image_path)
        
        # Get description using ChatGPT or Gemini
        description = describe_image(fused_image_path)
        
        # Render the result page
        return render_template('result.html', fused_image=fused_image_path, description=description)

if __name__ == '__main__':
    app.run(debug=True)
