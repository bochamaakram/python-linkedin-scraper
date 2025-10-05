import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from urllib.parse import urlencode
import re

class LinkedInJobScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.jobs_data = []

    def search_jobs(self, keywords, location="", max_pages=3):
        """Search for jobs on LinkedIn"""
        base_url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"

        for page in range(max_pages):
            try:
                params = {
                    'keywords': keywords,
                    'location': location,
                    'start': page * 25
                }

                url = f"{base_url}?{urlencode(params)}"
                print(f"Scraping page {page + 1}...")

                response = self.session.get(url)
                if response.status_code != 200:
                    print(f"Failed to fetch page {page + 1}")
                    break

                self.parse_job_listing(response.text)

                # Respectful delay
                time.sleep(random.uniform(2, 4))

            except Exception as e:
                print(f"Error on page {page}: {e}")
                break

    def parse_job_listing(self, html_content):
        """Parse job listings from HTML content"""
        soup = BeautifulSoup(html_content, 'html.parser')
        job_cards = soup.find_all('div', class_='base-search-card')

        for card in job_cards:
            try:
                job_data = self.extract_job_data(card)
                if job_data:
                    self.jobs_data.append(job_data)
                    print(f"Found: {job_data['title']} at {job_data['company']}")

            except Exception as e:
                print(f"Error parsing job card: {e}")
                continue

    def extract_job_data(self, card):
        """Extract individual job data from card"""
        # Extract basic info
        title_elem = card.find('h3', class_='base-search-card__title')
        company_elem = card.find('h4', class_='base-search-card__subtitle')
        location_elem = card.find('span', class_='job-search-card__location')
        date_elem = card.find('time')

        # Get job link
        link_elem = card.find('a', class_='base-card__full-link')

        if not all([title_elem, company_elem, link_elem]):
            return None

        job_data = {
            'title': title_elem.text.strip() if title_elem else 'N/A',
            'company': company_elem.text.strip() if company_elem else 'N/A',
            'location': location_elem.text.strip() if location_elem else 'N/A',
            'date_posted': date_elem.get('datetime') if date_elem else 'N/A',
            'job_url': link_elem.get('href') if link_elem else 'N/A',
        }

        # Try to get more detailed info from job page
        detailed_info = self.get_detailed_job_info(job_data['job_url'])
        job_data.update(detailed_info)

        return job_data

    def get_detailed_job_info(self, job_url):
        """Get detailed job information from individual job page"""
        detailed_data = {
            'description': 'N/A',
            'seniority_level': 'N/A',
            'employment_type': 'N/A',
            'job_function': 'N/A',
            'industries': 'N/A',
            'contact_info': 'N/A'
        }

        try:
            if not job_url or job_url == 'N/A':
                return detailed_data

            response = self.session.get(job_url)
            if response.status_code != 200:
                return detailed_data

            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract job description
            desc_elem = soup.find('div', class_='description__text')
            if desc_elem:
                detailed_data['description'] = desc_elem.get_text(strip=True)[:500] + "..."  # Limit length

            # Extract job criteria
            criteria_items = soup.find_all('li', class_='description__job-criteria-item')
            for item in criteria_items:
                subtitle = item.find('h3', class_='description__job-criteria-subheader')
                text = item.find('span', class_='description__job-criteria-text')

                if subtitle and text:
                    subtitle_text = subtitle.get_text(strip=True).lower()
                    if 'seniority level' in subtitle_text:
                        detailed_data['seniority_level'] = text.get_text(strip=True)
                    elif 'employment type' in subtitle_text:
                        detailed_data['employment_type'] = text.get_text(strip=True)
                    elif 'job function' in subtitle_text:
                        detailed_data['job_function'] = text.get_text(strip=True)
                    elif 'industries' in subtitle_text:
                        detailed_data['industries'] = text.get_text(strip=True)

            # Extract contact info (limited availability)
            contact_elem = soup.find('a', class_='message-the-recruiter')
            if contact_elem:
                detailed_data['contact_info'] = "Recruiter messaging available"

            # Respectful delay
            time.sleep(random.uniform(1, 3))

        except Exception as e:
            print(f"Error getting detailed info: {e}")

        return detailed_data

    def save_to_excel(self, filename="linkedin_jobs.xlsx"):
        """Save collected data to Excel file"""
        if not self.jobs_data:
            print("No data to save!")
            return

        df = pd.DataFrame(self.jobs_data)

        # Create Excel writer with auto-adjusted column widths
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='LinkedIn Jobs', index=False)

            # Auto-adjust column widths
            worksheet = writer.sheets['LinkedIn Jobs']
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width

        print(f"Data saved to {filename}")
        print(f"Total jobs collected: {len(self.jobs_data)}")

    def display_summary(self):
        """Display summary of collected data"""
        if not self.jobs_data:
            print("No data collected")
            return

        df = pd.DataFrame(self.jobs_data)
        print("\n=== COLLECTION SUMMARY ===")
        print(f"Total jobs: {len(self.jobs_data)}")
        print(f"Companies: {df['company'].nunique()}")
        print(f"Locations: {df['location'].nunique()}")
        print("\nSample data:")
        print(df[['title', 'company', 'location']].head())

def main():
    """Main function to run the scraper"""
    scraper = LinkedInJobScraper()

    # Get user input
    keywords = input("Enter job keywords (e.g., 'Python Developer'): ").strip()
    location = input("Enter location (press enter for any): ").strip()

    if not keywords:
        print("Keywords are required!")
        return

    try:
        # Search for jobs
        scraper.search_jobs(keywords=keywords, location=location, max_pages=2)

        # Display summary
        scraper.display_summary()

        # Save to Excel
        filename = f"linkedin_jobs_{keywords.replace(' ', '_')}.xlsx"
        scraper.save_to_excel(filename)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        print("\nScraping completed!")

if __name__ == "__main__":
    main()