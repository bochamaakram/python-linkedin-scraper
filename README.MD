# LinkedIn Job Scraper

A Python web scraper that extracts job listings from LinkedIn and saves the information to an Excel file.

## ⚠️ Important Disclaimer

**Please read this carefully before using this tool:**

- LinkedIn's Terms of Service prohibit unauthorized scraping
- This tool is for **educational purposes only**
- LinkedIn has strong anti-scraping measures and may block your IP
- Always respect `robots.txt` and implement proper rate limiting
- Consider using LinkedIn's official API for production use
- The author is not responsible for any misuse of this tool

## Features

- Search jobs by keywords and location
- Extract comprehensive job information:
  - Job title
  - Company name
  - Location
  - Posting date
  - Job description
  - Seniority level
  - Employment type
  - Job function
  - Industries
  - Contact information (when available)
- Save data to Excel with auto-formatted columns
- Respectful rate limiting to avoid overloading servers
- Comprehensive error handling

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd linkedin-job-scraper

2. **Install required packages**:
- **For Windows**:
   ```bash
    pip install requests beautifulsoup4 pandas openpyxl lxml
- **For macOS/Linux**:
   ```bash
    pip install requests beautifulsoup4 pandas openpyxl lxml
##
### run scraper:
    python main.py
**The script will prompt you for**:

Job keywords (e.g., "Python Developer")

Location (optional, press Enter for any location)
##
## Ethical Scraping Guidelines
When using this tool, please follow these best practices:

- Respect robots.txt: Check https://www.linkedin.com/robots.txt
- Implement delays: Avoid rapid, consecutive requests
- Limit data collection: Only collect what you need
- Cache responses: Avoid re-scraping the same content
- Monitor for blocks: Stop if you receive 429/403 errors
- Use official APIs: Prefer LinkedIn's API when possible
##
**Legal Considerations**:
- Terms of Service: Violating ToS may result in account suspension
- Data Protection Laws: Be aware of GDPR, CCPA, and other privacy regulations
- Intellectual Property: Respect copyright and intellectual property rights
- Commercial Use: Commercial scraping may require explicit permission
##
**Remember: Always scrape responsibly and respect website terms of service.**