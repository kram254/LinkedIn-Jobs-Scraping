import tkinter as tk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape and export job details to CSV
def scrape_jobs():
    job_title = job_title_entry.get()
    location = location_entry.get()
    
    # Initialize empty list for job data
    job_data = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }

    target_url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={}&location={}&trk=homepage-basic_jobs-search-bar-search-submit&currentJobId=3719184773&start={}"

    for i in range(0, 300, 25):
        res = requests.get(target_url.format(job_title, location, i), headers=headers)
        if res.status_code != 200:
            messagebox.showerror("Error", f"Failed to fetch data for offset {i}")
            return

        soup = BeautifulSoup(res.text, 'html.parser')
        job_cards = soup.find_all('div', class_='base-card')

        for job_card in job_cards:
            job_title = job_card.find('h3', class_='base-search-card__title').text.strip()
            company = job_card.find('h4', class_='base-search-card__subtitle').text.strip()
            location = job_card.find('span', class_='job-search-card__location').text.strip()

            # Get the URL link to the job
            job_link = job_card.find('a', class_='base-card__full-link')['href']

            job_data.append({
                "company": company,
                "job_title": job_title,
                "location": location,
                "job_link": f"https://www.linkedin.com{job_link}"
            })

    df = pd.DataFrame(job_data)

    # Save the DataFrame to a CSV file
    filename = f"{job_title}_{location}_jobs.csv"
    df.to_csv(filename, index=False, encoding='utf-8')
    messagebox.showinfo("Success", f"CSV file '{filename}' has been created.")

# Create the tkinter window
window = tk.Tk()
window.title("LinkedIn Job Scraper")

# Create and place labels and entry widgets
job_title_label = tk.Label(window, text="Job Title:")
job_title_label.pack()
job_title_entry = tk.Entry(window)
job_title_entry.pack()

location_label = tk.Label(window, text="Location:")
location_label.pack()
location_entry = tk.Entry(window)
location_entry.pack()

# Create and place the scrape button
scrape_button = tk.Button(window, text="Scrape Jobs", command=scrape_jobs)
scrape_button.pack()

# Start the tkinter main loop
window.mainloop()
