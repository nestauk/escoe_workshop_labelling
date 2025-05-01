import spacy
import pandas as pd

from collections import Counter
from tqdm import tqdm

import os

output_dir = "outputs/software_ner"

if __name__ == '__main__':

    nlp_ner = spacy.load(os.path.join(output_dir, "model-best"))

    example_sentences = [
        'Experience with workflow orchestration tools, ideally Airflow or AWS Step Functions',
        'Experience with Microsoft Excel',
        'Experience using tools like Flourish and Canva' # Something it might not have seen!
    ]

    for sentence in example_sentences:
        doc = nlp_ner(sentence)
        print(f"\nEntities in '{sentence}':")
        print(doc.ents)
        # spacy.displacy.render(doc, style="ent", jupyter=True)

    jobs_data = pd.read_parquet("inputs/data_jobs_df.parquet")

    # Just n jobs
    # n = 1000
    n = input(f"How many job adverts (a maximum of {len(jobs_data)}) would you like to apply this to? (1000 will take around 30 seconds):")

    try:
        n = int(n)
    except:
        n = 1000
        print(f"Applying to {n} job adverts, next time type an integer value")

    n = min(n, len(jobs_data))

    software_found = []
    for text in tqdm(jobs_data['text'].sample(n, random_state=42).to_list()):
        doc = nlp_ner(text)
        software_found += list(set([str(d) for d in doc.ents]))

    print(f"Most common software mentioned in {n} job adverts:")
    print(Counter(software_found).most_common(20))