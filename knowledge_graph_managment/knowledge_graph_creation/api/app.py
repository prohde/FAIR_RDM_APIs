from rdfizer import semantify
import os
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

def config_generation(mapping_file,output):
	config_file = "[default]\nmain_directory: .\n\n"
	config_file += "[datasets]\nnumber_of_datasets: 1\noutput_folder: " + output
	config_file += "\nremove_duplicate: yes\nall_in_one_file: no\nordered: yes\nenrichment: yes\nname: KG\n"
	config_file += "\n"
	config_file += "[dataset1]\nname: KG\n"
	config_file += "mapping: " + mapping_file + "\n"
	mapping_file = open(output + "/config.ini","w")
	mapping_file.write(config_file)
	mapping_file.close()

@app.route("/")
def home():
    return jsonify({"message": "Flask File API is running"})

@app.route("/kg_creation", methods=["POST"])
def kg_creation():
	mapping = request.form.get("mapping")
	output = request.form.get("output")
	config_generation(mapping,output)
	semantify(output + "/config.ini")
	return "Knowledge Graph generated succesfully.\n"

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8001, debug=True)