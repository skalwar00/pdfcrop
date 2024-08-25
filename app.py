from flask import Flask, render_template, request, send_file, jsonify
import os
from PyPDF2 import PdfReader, PdfWriter

app = Flask(__name__)

# Ensure the "uploads" and "processed" directories exist
os.makedirs("uploads", exist_ok=True)
os.makedirs("processed", exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Save the uploaded file
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            file_path = os.path.join("uploads", uploaded_file.filename)
            uploaded_file.save(file_path)

            # Process the PDF (crop it)
            reader = PdfReader(file_path)
            writer = PdfWriter()

            # Use the first page only as an example
            page = reader.pages[0]
            page.cropbox.upper_left = (178, 461)
            page.cropbox.lower_right = (178 + 218, 461 - 358)

            writer.add_page(page)

            # Save the cropped PDF
            output_path = os.path.join("processed", "cropped_" + uploaded_file.filename)
            with open(output_path, "wb") as output_pdf:
                writer.write(output_pdf)

            # Send a JSON response back to the client
            return jsonify({"message": "PDF cropped successfully", "filename": "cropped_" + uploaded_file.filename})

    return render_template('index.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join("processed", filename), as_attachment=True)

if __name__ == '__main__':
app.run(host='0.0.0.0', port=5000)
