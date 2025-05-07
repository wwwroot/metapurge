from flask import Flask, render_template, request, send_file
from PIL import Image
import piexif
import io
import os
import re
import random
import zipfile
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'webp', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def process_single_image(img, credit_text, original_ext):
    output = io.BytesIO()
    
    if original_ext.lower() in ('jpg', 'jpeg'):
        exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}}
        if credit_text:
            exif_dict["0th"][piexif.ImageIFD.Copyright] = credit_text.encode('utf-8')
            exif_dict["0th"][piexif.ImageIFD.Artist] = credit_text.encode('utf-8')
        
        exif_bytes = piexif.dump(exif_dict)
        img.save(output, format='JPEG', exif=exif_bytes, quality=95)
    else:
        new_img = Image.new(img.mode, img.size)
        new_img.putdata(list(img.getdata()))
        
        if original_ext.lower() == 'png':
            new_img.save(output, format='PNG', optimize=True)
        elif original_ext.lower() == 'webp':
            new_img.save(output, format='WEBP', quality=95)
        elif original_ext.lower() == 'gif':
            new_img.save(output, format='GIF', save_all=True)
    
    output.seek(0)
    return output

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'images' not in request.files:
            return 'No files uploaded', 400
            
        files = request.files.getlist('images')
        credit_text = request.form.get('credit', '')
        remove_digital = 'remove_digital' in request.form
        
        processed_files = []
        
        for file in files:
            if file and allowed_file(file.filename):
                try:
                    img = Image.open(file.stream)
                    original_ext = file.filename.split('.')[-1].lower()
                    
                    processed = process_single_image(img, credit_text, original_ext)
                    
                    clean_credit = re.sub(r'[^\w-]', '', credit_text.replace(' ', '_'))[:20]
                    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                    filename = f"{clean_credit}-{timestamp}-{random.randint(1000,9999)}.{original_ext}" if clean_credit else f"cleaned-{timestamp}-{random.randint(1000,9999)}.{original_ext}"
                    
                    processed_files.append((filename, processed))
                    
                except Exception as e:
                    return f'Error processing {file.filename}: {str(e)}', 500

        if not processed_files:
            return 'No valid images processed', 400

        # Create ZIP archive
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for filename, file_data in processed_files:
                zip_file.writestr(filename, file_data.getvalue())
        
        zip_buffer.seek(0)
        return send_file(
            zip_buffer,
            mimetype='application/zip',
            download_name='processed_images.zip',
            as_attachment=True
        )

    return render_template('index.html')

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
