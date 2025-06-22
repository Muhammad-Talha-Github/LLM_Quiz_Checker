import os
from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from PIL import Image
import google.generativeai as genai
import shutil

#configuring Gemini API with direct key
genai.configure(api_key="") # write your API key here

#using flask to setup the app 
app = Flask(__name__)
app.secret_key = "supersecretkey"  

#folder paths
INPUT_FOLDER = "input"
OUTPUT_FOLDER = "output"
os.makedirs(INPUT_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

#initializing the Gemini model
try:
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    model = None
    print(f"Error initializing model: {e}")

def process_quizzes(files_to_process):
    
    #Process the selected uploaded quizzes using the Gemini API and save results.
    if not files_to_process:
        flash("No files selected for processing.")
        return

    #clearing the output folder before processing
    if os.path.exists(OUTPUT_FOLDER):
        shutil.rmtree(OUTPUT_FOLDER)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    for input_path in files_to_process:
        file_name = os.path.basename(input_path)
        output_path = os.path.join(OUTPUT_FOLDER, f"{os.path.splitext(file_name)[0]}_graded.txt")
        try:
            #opening the image
            image = Image.open(input_path)

            #sending image to the Gemini API
            prompt = "Extract the content (text or diagrams) from this quiz. Provide a brief analysis at the start and a suggestion to improve. Grade the quiz out of 10. The grade should be in the format Grade: /10 in a separate line at the end."
            if model:
                response = model.generate_content([prompt, image])

                #saving the response to a file
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(response.text)
            else:
                raise ValueError("Model not initialized.")
        except Exception as e:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(f"Error processing {file_name}: {e}")
            flash(f"Error processing {file_name}: {e}")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        #checking if files are included in the request
        if "quiz_files" not in request.files:
            flash("No files part in the request")
            return redirect(request.url)
        
        files = request.files.getlist("quiz_files")
        if not files:
            flash("No file selected")
            return redirect(request.url)

        #printing received files to the console to verify the form submission
        print("Files received:", [file.filename for file in files])

        #saving uploaded files temporarily
        uploaded_files = []
        for file in files:
            if file and file.filename.endswith((".png", ".jpg", ".jpeg")):
                file_path = os.path.join(INPUT_FOLDER, file.filename)
                file.save(file_path)
                uploaded_files.append(file_path)

        #processing only the uploaded files
        process_quizzes(uploaded_files)
        return redirect(url_for("success"))

    return render_template("index.html")


@app.route("/success", methods=["GET", "POST"])
def success():
    """
    Success page to download results after processing quizzes.
    """
    if request.method == "POST":
        #creating zip archive of output files
        zip_path = "processed_quizzes.zip"
        shutil.make_archive("processed_quizzes", "zip", OUTPUT_FOLDER)

        #serving the ZIP file for download
        response = send_file(zip_path, as_attachment=True)

        #cleanup ZIP file after download
        try:
            os.remove(zip_path)
        except Exception as e:
            print(f"Error deleting ZIP file: {e}")

        return response

    return render_template("success.html")

if __name__ == "__main__":
    app.run(debug=True)