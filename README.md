# 🔒 MetaPurge - Intelligent Image Sanitizer

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Flask](https://img.shields.io/badge/Flask-2.0%2B-lightgrey)](https://flask.palletsprojects.com)

Professional image metadata cleaner with advanced features for digital security and content integrity protection. Perfect for journalists, photographers, and privacy-conscious users.

![Demo Screenshot](docs/demo.gif)

## 🌟 Key Features
- 🚫 Remove EXIF/IPTC/XMP metadata
- 🔍 Detect and clean AI-generated content markers
- 📸 Support only formats (JPG, JPEG)
- 🛡️ Digital source type sanitization
- ✏️ Custom credit/copyright watermarking
- 🖥️ Real-time image preview
- 📥 One-click secure download

## ⚙️ Installation
```bash
# Clone repository
git clone https://github.com/wwwroot/MetaPurge.git
cd MetaPurge

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
```
Visit `http://localhost:5000` in your browser

## 🖱️ Usage
1. **Upload** image via drag-drop or file picker
2. **Edit** metadata fields as needed
3. **Preview** sanitized image
4. **Download** clean version with auto-generated filename

## 🧠 Tech Stack
- **Core**: Python 3.8+
- **Web Framework**: Flask
- **Image Processing**: Pillow, Piexif
- **Security**: Secure filename handling, Metadata pattern detection
- **UI**: Modern CSS3, Responsive Design

## 🤝 Contributing
We welcome contributions! Please follow these steps:
1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License
Distributed under the MIT License. See `LICENSE` for more information.

## ✉️ Contact
Project Maintainer: Aji - septianajisanjaya@live.com

Project Link: [https://github.com/wwwroot/MetaPurge](https://github.com/wwwroot/MetaPurge)

## 🙏 Acknowledgements
- Flask Community
- Pillow Library Maintainers
- EXIF Standards Organization
