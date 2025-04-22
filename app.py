from flask import Flask, render_template, request, send_file
from PIL import Image
import piexif
import io
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

def remove_metadata(img, credit_text, remove_digital_source):
    """Remove metadata dan edit credit"""
    try:
        exif_dict = piexif.load(img.info['exif'])
    except:
        exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}}
    
    # Hapus Digital Source metadata
    if remove_digital_source:
        if piexif.ImageIFD.Copyright in exif_dict["0th"]:
            del exif_dict["0th"][piexif.ImageIFD.Copyright]
        
        # Hapus IPTC metadata
        if "1st" in exif_dict:
            if 33723 in exif_dict["1st"]:  # DigitalSourceType
                del exif_dict["1st"][33723]
            if 33724 in exif_dict["1st"]:  # DigitalSourceFileType
                del exif_dict["1st"][33724]
    
    # Update credit
    if credit_text:
        exif_dict["0th"][piexif.ImageIFD.Copyright] = credit_text.encode('utf-8')
    
    # Hapus metadata yang tidak diperlukan
    for key in list(exif_dict["Exif"]):
        if key not in [piexif.ExifIFD.DateTimeOriginal]:
            del exif_dict["Exif"][key]
    
    return piexif.dump(exif_dict)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Terima file dan form data
        file = request.files['image']
        credit_text = request.form.get('credit', '')
        remove_digital = 'remove_digital' in request.form
        
        # Proses image
        img = Image.open(file.stream)
        exif_bytes = remove_metadata(img, credit_text, remove_digital)
        
        # Simpan ke buffer
        output = io.BytesIO()
        img.save(output, format='JPEG', exif=exif_bytes, quality=95)
        output.seek(0)
        
        # Generate filename
        import re
        import random
        clean_credit = re.sub(r'[^a-zA-Z0-9]', '', credit_text.replace(' ', '_'))[:20]
        random_num = random.randint(1000, 9999)
        filename = f"{clean_credit}-{random_num}.jpg" if credit_text else f"cleaned-{random_num}.jpg"
        
        return send_file(
            output,
            mimetype='image/jpeg',
            download_name=filename,
            as_attachment=True
        )
    
    return render_template('index.html')

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)