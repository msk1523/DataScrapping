import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib3

urllib3.disable_warnings()
def get_project_details(url):
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    details = {
        'GSTIN No': '',
        'PAN No': '',
        'Name': '',
        'Permanent Address': ''
    }
    
    details_table = soup.find('table', {'class': 'table table-striped table-bordered table-hover'})
    if details_table:
        rows = details_table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) == 2:
                key = cols[0].text.strip()
                value = cols[1].text.strip()
                if key in details:
                    details[key] = value
    
    return details

def scrape_projects():
    base_url = "https://hprera.nic.in"
    url = f"{base_url}/PublicDashboard"
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    projects = []
    registered_projects_section = soup.find('div', {'id': 'RegisteredProjects'})
    if registered_projects_section:
        project_rows = registered_projects_section.find_all('tr')[1:7]  # Skip header row and get first 6 projects
        for row in project_rows:
            cols = row.find_all('td')
            if len(cols) > 1:
                project_link = cols[1].find('a', href=True)
                if project_link:
                    project_url = f"{base_url}/{project_link['href']}"
                    project_details = get_project_details(project_url)
                    projects.append(project_details)
    
    return projects

def save_to_csv(projects, filename):
    df = pd.DataFrame(projects)
    df.to_csv(filename, index=False)

def main():
    projects = scrape_projects()
    print(projects)
    save_to_csv(projects, 'projects.csv')
    print("Data has been saved to projects.csv")

if __name__ == "__main__":
    main()
