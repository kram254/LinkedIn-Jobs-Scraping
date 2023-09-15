import requests
from bs4 import BeautifulSoup
import pandas as pd

# Initialize empty list for job data
job_data = []

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}

target_url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=python%20developer&location=Worldwide&trk=homepage-basic_jobs-search-bar-search-submit&currentJobId=3719184773&start={}"

for i in range(0, 300, 25):
    res = requests.get(target_url.format(i), headers=headers)
    if res.status_code != 200:
        print(f"Failed to fetch data for offset {i}")
        continue

    soup = BeautifulSoup(res.text, 'html.parser')
    job_cards = soup.find_all('div', class_='base-card')

    for job_card in job_cards:
        job_title = job_card.find('h3', class_='base-search-card__title').text.strip()
        company = job_card.find('h4', class_='base-search-card__subtitle').text.strip()
        location = job_card.find('span', class_='job-search-card__location').text.strip()

        job_data.append({
            "company": company,
            "job_title": job_title,
            "location": location
        })

df = pd.DataFrame(job_data)

# Save the DataFrame to a CSV file
df.to_csv('Python_jobs.csv', index=False, encoding='utf-8')
print("CSV file 'Python_jobs.csv' has been created.")
