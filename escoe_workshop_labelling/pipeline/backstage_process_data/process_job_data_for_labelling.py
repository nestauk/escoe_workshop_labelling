"""
Get the jobs data into the format needed to label in Argilla

We will be labelling job adverts per sentence for software/programming languages
"""

import pandas as pd
from escoe_workshop_labelling.pipeline.backstage_process_data.job_advert_cleaning import split_sentences

if __name__ == '__main__':
    
    jobs_data = pd.read_parquet("s3://nesta-open-data/escoe_workshop/data/data_jobs_df.parquet")

    jobs_data_by_sentence = []
    unique_id = 0
    for i, row in jobs_data.iterrows():
        sents = split_sentences(row['text'])
        for sent in sents:
            if len(sent) in range(75,100): # Only use sentences from an average length
                jobs_data_by_sentence.append(
                    {
                        "id": unique_id, # needs a unique id
                        "job_id": row['id'],
                         "text": sent,
                    }
                )
                unique_id+=1

    jobs_data_by_sentence_df = pd.DataFrame(jobs_data_by_sentence)

    # TODO: remove duplicate sentences
    jobs_data_by_sentence_df.to_csv("inputs/jobs_data_by_sentence_df.csv")
    jobs_data_by_sentence_df.sample(2000, random_state=42).to_csv("inputs/jobs_data_by_sentence_df_sample.csv")