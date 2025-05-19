# Data labelling using Argilla and Machine Learning applications

This repository was developed for a [workshop session for ESCoE](https://www.escoe.ac.uk/events/data-visualisation-and-data-labelling-for-machine-learning-applications-workshop-with-nesta/) on 20th May 2025.

Suitable data isn’t always available to train a machine learning model, and often data scientists need to label their own. Sometimes this process can be done in a rudimentary way, for example creating binary classifications as a column in a spreadsheet. However for more complex labelling tasks, like selecting parts of text that correspond to people’s names, and labelling software is essential. 

In this session we will use Argilla, an open-source labelling software, to set up a labelling task. We will spend some time labelling data and using it to create a machine learning model. We will touch on:
- The practicalities of setting up a labelling task
- The importance of thinking about the design of a labelling task
- Dealing with multiple labellers and measuring consensus

The full workshop slide deck with enhanced setup information can be found [here](https://docs.google.com/presentation/d/1lsBFrrhIaWLc5554YSUwzUAchMtvgUkPo53Wywb6j8M/edit#slide=id.g3503473b950_0_0).

## Prerequisites ✅

Your system must have
- python installed
- access to run commands in the terminal

You need to set up:
- A Hugging Face account - you can do this [here](https://huggingface.co/join)
- Deply Argilla from Hugging Face spaces - set up is [here](https://huggingface.co/new-space?template=argilla/argilla-template-space&name=my-argilla)


## Setup 💻

Create and activate the virtual environment:
```
python3.10 -m venv .venv
source .venv/bin/activate # Or .venv\Scripts\activate in Windows
pip install -r requirements.txt
```

or in conda:

```
conda create -n myenv python=3.10
conda activate myenv
pip install -r requirements.txt
```

Add your Argilla API key to the environmental variables (you can find this in your Argilla profile settings):

```
export ARGILLA_KEY="**** **** **** ****”
```

## Run labelling 🏷️

```
python escoe_workshop_labelling/pipeline/run_argilla/run_labelling.py

```
to start up the labelling task.

You can save the labels as you go in this command by entering 's' everytime you want to save.

Alternatively (or if you accidentally close this terminal), after labelling you can save the data by running
```
python escoe_workshop_labelling/pipeline/run_argilla/save_labelling.py
```


## Process the labelled data into a format to train a SpaCy NER model 🔍

```
python escoe_workshop_labelling/pipeline/train_ner/spacy_format.py

```

## Train the NER model 💪

In the command line:

```
python -m spacy train config.cfg --output ./outputs/software_ner/ --paths.train ./outputs/software_ner/spacy_records.spacy --paths.dev ./outputs/software_ner/spacy_records.spacy
```

## See what software is most asked for in data jobs 👩‍💻

```
python escoe_workshop_labelling/pipeline/train_ner/apply_software_ner.py

```

## Contributor guidelines

[Technical and working style guidelines](https://github.com/nestauk/ds-cookiecutter/blob/master/GUIDELINES.md)

---

<small><p>Project based on <a target="_blank" href="https://github.com/nestauk/ds-cookiecutter">Nesta's data science project template</a>
(<a href="http://nestauk.github.io/ds-cookiecutter">Read the docs here</a>).
</small>
