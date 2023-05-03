from bs4 import BeautifulSoup
import requests
from requests import get

def extract_remoteok_jobs(keyword):
    url = f"https://remoteok.com/remote-{keyword}-jobs"
    request = requests.get(url, headers={"User-Agent": "Kimchi"})
    results = []
    if request.status_code == 200:
        soup = BeautifulSoup(request.text, "html.parser", from_encoding="utf-8")
        jobs = soup.find_all("tr", class_="job")
        for job in jobs:
            link = job.find("a", class_="tooltip")["href"]
            company = job.find("h3", itemprop="name")
            position = job.find("h2", itemprop="title")
            location = job.find("div", class_="location")
            company = company.string.strip()
            position = position.string.strip()
            location = location.string.strip()

        logo = job.find("img", class_="logo")
        if logo:
            logo_url = logo.get("data-src")
        else:
            logo_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSGPEw64UGyIk9N-bsMo6Q68xtdYH0ZmBCbGATo2eZ3Q5Rm3RiFtPNpSgtl4GyuzIvachI&usqp=CAU"
        if company and position and location:
            job = {
            "logo": logo_url,
            "link": f"https://remoteok.com{link}",
            "company": company.replace(",", " "),
            "position": position.replace(",", " "),
            "location": location
            }
            results.append(job)
        
    return results