import os
import polars as pl

from escoe_workshop_labelling.pipeline.backstage_process_data.job_advert_cleaning import clean_text

job_advert_s3_location = "s3://prinz-green-jobs/outputs/data/ojo_application"

key_columns_file = os.path.join(
    job_advert_s3_location,
    "deduplicated_sample/20241114/latest_update_20241114_key_columns.parquet",
)

titles_file = os.path.join(
    job_advert_s3_location,
    "deduplicated_sample/20241114/latest_update_20241114_titles.parquet",
)

desc_file = os.path.join(
    job_advert_s3_location,
    "deduplicated_sample/20241114/latest_update_20241114_descriptions.parquet",
)

salaries_file = os.path.join(
    job_advert_s3_location,
    "deduplicated_sample/20241114/latest_update_20241114_salaries.parquet",
)

if __name__ == '__main__':
    created_date = pl.read_parquet(key_columns_file)
    titles_df = pl.read_parquet(titles_file)
    salaries_df = pl.read_parquet(salaries_file)

    data_titles = titles_df.filter(pl.col("occupation").is_in([
        'Data Engineer', 'Data Scientist', 'Data Analyst',]))
    len(data_titles) # 24810 jobs

    data_job_ids = set(data_titles['id'].unique().to_list())

    desc_data = pl.read_parquet(desc_file)

    subset_desc = desc_data.filter(pl.col('id').is_in(data_job_ids))
    subset_key_cols = created_date.filter(pl.col('id').is_in(data_job_ids))
    subset_salaries = salaries_df.filter(pl.col('id').is_in(data_job_ids))

    # Merge together
    data_jobs_df = data_titles.join(subset_desc, on="id", how='left')
    data_jobs_df = data_jobs_df.join(subset_key_cols, on="id", how='left')
    data_jobs_df = data_jobs_df.join(subset_salaries, on="id", how='left')

    data_jobs_df = data_jobs_df.with_columns(pl.col("description").map_elements(clean_text).alias('clean_description'))

    data_jobs_df = data_jobs_df[[
    'id', 'created', 'itl_3_name', 'job_title_raw',
    'occupation','sector', 'parent_sector', 'knowledge_domain',
     'min_annualised_salary', 'max_annualised_salary', 'clean_description',]]

    data_jobs_df = data_jobs_df.rename({
        'created': 'date_posted', 'itl_3_name': 'location',
     'min_annualised_salary' : 'min_salary', 'max_annualised_salary': 'max_salary',
     'clean_description': 'text'})

    # Drop duplicate descriptions
    data_jobs_df = data_jobs_df.unique(subset=["text"])

    data_jobs_df.write_parquet("inputs/data_jobs_df.parquet")
    data_jobs_df.sample(500, seed=42).write_csv("inputs/data_jobs_df_sample.csv")

    