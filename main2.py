import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = "https://www.indeed.com/jobs?q=technical+program+manager&l=New+York,+NY&jt=fulltime&salarymin=120000"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="resultsCol")
job_elems = soup.find_all("div", class_="jobsearch-SerpJobCard")

job_links = []
for job_elem in job_elems:
    title_elem = job_elem.find("h2", class_="title")
    link_elem = title_elem.find("a", href=True)
    if link_elem:
        job_links.append("https://www.indeed.com" + link_elem["href"])

job_data = pd.DataFrame(columns=["Title", "Company", "Location", "Salary", "Summary"])

for link in job_links:
    job_page = requests.get(link)
    job_soup = BeautifulSoup(job_page.content, "html.parser")

    try:
        title = job_soup.find("h1", class_="icl-u-xs-mb--xs").text.strip()
    except:
        title = ""

    try:
        company = job_soup.find("div", class_="icl-u-lg-mr--sm icl-u-xs-mr--xs").text.strip()
    except:
        company = ""

    try:
        location = job_soup.find("div", class_="icl-u-xs-mt--xs icl-u-textColor--secondary jobsearch-JobInfoHeader-secondary").find_all("div")[0].text.strip()
    except:
        location = ""

    try:
        salary = job_soup.find("div", class_="jobsearch-JobMetadataHeader-item").text.strip()
    except:
        salary = ""

    try:
        summary = job_soup.find("div", class_="jobsearch-jobDescriptionText").text.strip()
    except:
        summary = ""

    job_data = job_data.append({"Title": title, "Company": company, "Location": location, "Salary": salary, "Summary": summary}, ignore_index=True)

job_data.to_csv("job_data.csv", index=False)


import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv("job_data.csv")

# Print the first few rows of the DataFrame to verify that it was loaded correctly
print(df.head())
