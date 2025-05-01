# Nesta set-up

This folder can be ignored by participants of the ESCoE workshop.

## Processing the OJO job advert data

Run
```
python escoe_workshop_labelling/pipeline/backstage_process_data/create_jobs_data.py
```

to filter and concatenate job advert data for 'data' jobs - which are 'Data Engineer', 'Data Scientist', and 'Data Analyst'.

Then run
```
python escoe_workshop_labelling/pipeline/backstage_process_data/process_job_data_for_labelling.py
```
which splits the advert texts into sentences, and puts them into the format needed for labelling in Argilla.

These data files need to be then uploaded to S3 in the `s3://nesta-open-data/escoe_workshop/data/` folder and permissions set to publically readable.

The key files created are:
1. `s3://nesta-open-data/escoe_workshop/data/jobs_data_by_sentence_df_sample.csv`: A sample of 2000 sentences from job adverts for labelling, read in `run_labelling.py`. Unlikely people will label more than 2000 (200 took Liz 20 mins).
2. `s3://nesta-open-data/escoe_workshop/data/data_jobs_df.parquet`: The full dataset of 'data' jobs, this will be read in `apply_software_ner.py` to find the most common software skills asked for.