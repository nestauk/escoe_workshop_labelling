import json
import spacy
from spacy.training import Example
from spacy.tokens import DocBin

import os

output_dir = "outputs/software_ner"

if __name__ == '__main__':
    
    with open(os.path.join(output_dir, 'records.json')) as json_data:
        all_to_be_labelled_data = json.load(json_data)
        json_data.close()

    labelled_data = [v for v in all_to_be_labelled_data if v['status']=='completed']

    has_entity = [v for v in labelled_data if v['responses']['span_label'][0]['value']!=[]]

    # Format for spacy training [('I want apples', {'entities': [(2, 5, 'COMMAND'), (7, 12, 'FRUIT')]})]
    # Trust the first annotators labels
    spacy_labelled_data = [
        (v['fields']['text'],
         {'entities': [(ents['start'], ents['end'], ents['label']
                       ) for ents in v['responses']['span_label'][0]['value']]}) for v in labelled_data]

    nlp = spacy.blank("en")
    db = DocBin()

    for text, annotations in spacy_labelled_data:
        example = Example.from_dict(nlp.make_doc(text), annotations)
        db.add(example.reference)

    db.to_disk(os.path.join(output_dir, 'spacy_records.spacy'))