from joblib import Parallel, delayed
import pandas as pd
import os
import requests

def get_company_name(name):
  return name.split()[0]

def download_images(row):
  name = row.Name
  company_name = get_company_name(name)
  company_folder = f'Images_Downloaded\\{company_name}'
  model_folder = f'{company_folder}\\{name.replace(" ", "_")}'
  
  os.makedirs(company_folder, exist_ok=True)
  os.makedirs(model_folder, exist_ok=True)
  
  image_count = 0
  for filename in os.listdir(model_folder):
    if filename.lower().endswith(('.webp')):
      image_count += 1

  image_urls = row.Images.split('\t')
  image_count += 1
  for url in image_urls:
    try:
      response = requests.get(url)
      if response.status_code == 200:
        with open(f'{model_folder}/image_{image_count}.webp', 'wb') as f:
          f.write(response.content)
          print(f'Downloaded {url}')
        image_count += 1
      else:
        print(f'Failed to download {url}. Status code: {response.status_code}')
    except Exception as e:
      print(f'Failed to download {url}. Error: {e}')

# Define a wrapper function for Joblib
def download_images_wrapper(df):
  return Parallel(n_jobs=-1)(delayed(download_images)(row) for row in df.itertuples())

df = pd.read_csv('pakwheels\data.csv')
null_images = df[df['Images'].isnull()]
print(null_images)
print('-'*99)
print('-'*99)
df = df.dropna(subset=['Images'])

# Use Joblib to parallelize download_images across rows
download_images_wrapper(df.copy())
