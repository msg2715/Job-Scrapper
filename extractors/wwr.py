from bs4 import BeautifulSoup
import requests
from requests import get

def extract_wwr_jobs(keyword):
    url = f"https://weworkremotely.com/remote-jobs/search?term={keyword}"
    request = get(url)
    results = []
    if request.status_code == 200:
        soup = BeautifulSoup(request.text, "html.parser", from_encoding="utf-8")
        jobs = soup.find_all("section", class_="jobs")
        for job_section in jobs:
            job_posts = job_section.find_all('li')
            job_posts.pop(-1)
        for post in job_posts:
            anchors = post.find_all('a')
            anchor = anchors[1]
            link = anchor['href']
            company = anchor.find('span', class_="company")
            position = anchor.find('span', class_="title")
            location = anchor.find('span', class_="region")

            if company:
                company = company.string.strip()
            if position:
                position = position.string.strip()
            if location:
                location = location.string

            anchor_logo = anchors[0]
            logo = anchor_logo.find("div", class_="flag-logo")
            if logo == None:
                logo_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSGPEw64UGyIk9N-bsMo6Q68xtdYH0ZmBCbGATo2eZ3Q5Rm3RiFtPNpSgtl4GyuzIvachI&usqp=CAU"
            else:
                logo_url = logo["style"].replace("background-image:url(","").replace(")", "")
            
            job_data = {
            "logo": logo_url,
            "link": f"https://weworkemotely.com{link}",
            "company": company.replace(",", " "),
            "position": position.replace(",", " "),
            "location": location
            }
            results.append(job_data)
    return results