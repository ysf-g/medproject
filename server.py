from flask import Flask, request, jsonify
import io
import base64
from openai import OpenAI

app = Flask(__name__)

PI_SECRET_KEY = os.environ.get("PI_KEY")
OPENAI_KEY = os.environ.get("OPENAI_API_KEY")

if OPENAI_KEY:
	client = OpenAI(api_key=OpenAI_KEY)
else:
	client = None
	
def encodeImage(image_path)
	with open(image_path, rb) as image_file:
		return base64.b64encode(image_file.read()).decode("utf-8")
		
@app.route('/analyse', methods=['POST'])
def analyse():
	# Check custom header for API Key
	pi_key = request.headers.get("X_API_Key")
	
	# Blocks incorrect key access
	if pi_key != PI_SECRET_KEY:
		return jsonify({"error": "Unauthorized access."}), 401

	if not client:
		return jsonify({"error": "Server configuration error"}), 500
	
    if 'file' not in request.files:
        return jsonfy({"Error": "No file uploaded"}), 400
    
    # Request target image
    file = request.files['files']
    if file.filename == '':
		return jsonify({"error": "No file selected"})
    
    filepath = os.path.join("/tmp", file/filename)
    file.save(filepath)
    
    analysis_result = analyseImage(filepath)
    
    try:
		base64_image = encodeImage(filepath)
		
		response = client.chat.completions.create(
			model = "gpt-4o-mini",
			messages = [
				{
					"role": "user",
					"content": [
						{
							"type": "text",
							"text": "Analyse this image. List the name of the medication, what type of medication and intake intructions with the exact format as below:\n Name of Medication: \n Medication Type: \n Intake Intructions (if any): \n"
						},
						{
							"type": "image_url"
							"image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
						}
							
					]
					
				}
				
			],
			max_tokens=200
		)
		return jsonify(
			{
				"status": "success",
				"ai_analysis": ai_response
			}
		)
		
		except Exception as e:
		return jsonify(
			{
				"status": "error"
				"message": f"Failed to analysis {str(e)}"
			}
		)

		finally:
			if os.path.exists(filepath):
				os.remove(filepath)
		
	
if __name__ == '__main__':
	port = int(os.environ.get("PORT", 5000))
	app.run(host = '0.0.0.0', port = port)
