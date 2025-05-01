import argilla as rg
import pandas as pd

import os
import shutil 

argilla_url  = os.environ["ARGILLA_URL"]
argilla_api_key = os.environ["ARGILLA_KEY"]

if __name__ == '__main__':

    print("Setting up and running Argilla labelling task...")

    client = rg.Argilla(
        api_url=argilla_url,
        api_key=argilla_api_key
    )

    settings = rg.Settings(
        guidelines="These are some guidelines.",
        fields=[
            rg.TextField(
                name="text",
            ),
        ],
        questions=[
            rg.SpanQuestion(
                name="span_label",
                field="text",
                labels=["software"],
                title="Classify the tokens according to the specified categories.",
                allow_overlapping=False,
            )
        ],
    )

    # Read the CSV file into a pandas DataFrame
    dataframe = pd.read_csv("inputs/jobs_data_by_sentence_df_sample.csv") # neccessary for Argilla that the text column is called 'text'

    # An exception will be raised if this dataset already exists, so delete it
    dataset_name = "software_ner"
    dataset = client.datasets(name=dataset_name)

    if dataset is not None:
        print(f"Deleting and recreating dataset {dataset_name}")
        delete_continue = input("Continue? (y/n): ")
        if delete_continue=='y':
            dataset.delete()
        else:
            print("Not deleting dataset, so rest of flow won't work")

    dataset = rg.Dataset(
        name="software_ner",
        settings=settings,
    )

    dataset.create()
    records = dataframe.to_dict(orient='records') # Needs to be in the format [{"text": "this is text"}, {"text": "this is another text"},]

    dataset.records.log(records)

    print(f"Argilla labelling task running on {argilla_url} - click on url to start labelling!")
    
    dataset.update()

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