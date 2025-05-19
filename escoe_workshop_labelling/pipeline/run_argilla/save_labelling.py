"""
Save labels if you accidentally closed the terminal

python -i escoe_workshop_labelling/pipeline/run_argilla/save_labelling.py
"""

import argilla as rg
import pandas as pd

import os
import shutil 

argilla_url  = os.environ["ARGILLA_URL"]
argilla_api_key = os.environ["ARGILLA_KEY"]

if __name__ == '__main__':
	client = rg.Argilla(
		api_url=argilla_url,
		api_key=argilla_api_key
	)

	while True:
		save_now = input("When you have finished labelling save labels by typing 'S' or 's', if you aren't ready there is no need to type anything:")

		if save_now in ['S', 's']:

			# download the labelled data
			dataset_labelled = client.datasets(name="software_ner")

			# Will download all data not just the status="completed" labelled ones
			# has a "user_id" field

			output_dir = "outputs/software_ner/"
			if not os.path.exists(output_dir):
				os.makedirs(output_dir)
			else:
				overwrite_file_name = os.path.join(output_dir, 'records.json')
				if os.path.isfile(overwrite_file_name):
					print("Replacing existing download, old version will be kept in records_previous.json")
					os.rename(overwrite_file_name, "outputs/software_ner/records_previous.json")
				argilla_folder_name = os.path.join(output_dir, '.argilla/')
				if os.path.isdir(argilla_folder_name):
					shutil.rmtree(argilla_folder_name)

			dataset_labelled.to_disk(path=output_dir)
			print(f"Dataset saved to {output_dir}")
	
		elif save_now == '':  # If the user just presses Enter
			print("Continuing labelling...")
			continue  # Go back to the beginning of the while loop
		else:
			print("Invalid input. Please type 'S' or 's' to save, or press Enter to continue labelling.")