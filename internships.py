import time
import pandas as pd
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re

# Keywords based on your resume
KEYWORDS = [
    "machine learning", "deep learning", "artificial intelligence", "AI", "NLP",
    "data science", "python", "tensorflow", "keras", "react", "node", "mern",
    "full stack", "web development", "backend", "frontend", "software developer",
    "data analyst", "computer vision", "neural network"
]

MIN_DURATION_MONTHS = 3
DAILY_TARGET = 15
MAX_RETRIES = 3

def get_driver():
    """Initialize Chrome driver with anti-detection settings"""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--log-level=3")
    
    # Anti-detection measures
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
    })
    return driver

def match_keywords(text):
    """Check if text matches any keywords"""
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in KEYWORDS)

def parse_duration(duration_text):
    """Extract duration in months"""
    try:
        duration_text = duration_text.lower()
        if 'month' in duration_text:
            months = re.findall(r'(\d+)', duration_text)
            return int(months[0]) if months else 0
        elif 'week' in duration_text:
            weeks = re.findall(r'(\d+)', duration_text)
            return int(weeks[0]) // 4 if weeks else 0
    except:
        pass
    return 0

def scrape_internshala_improved(driver):
    """Improved Internshala scraper with better selectors"""
    print("🔹 Scraping Internshala...")
    jobs = []
    
    try:
        # Direct link to tech internships
        url = "https://internshala.com/internships/computer-science,web-development,data-science,machine-learning-internship/work-from-home-internship"
        driver.get(url)
        time.sleep(5)
        
        # Try to close any popups
        try:
            close_buttons = driver.find_elements(By.CSS_SELECTOR, "button.close, .modal-close, [aria-label='Close']")
            for btn in close_buttons:
                try:
                    btn.click()
                    time.sleep(1)
                except:
                    pass
        except:
            pass
        
        # Scroll to load more content
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
        time.sleep(2)
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        # Try multiple selector patterns
        cards = soup.find_all("div", class_="individual_internship") or \
                soup.find_all("div", class_="internship_meta") or \
                soup.find_all("div", {"data-internship-id": True})
        
        print(f"   Found {len(cards)} cards")
        
        for card in cards[:30]:  # Check more cards
            try:
                # Title extraction with multiple fallbacks
                title = None
                title_selectors = [
                    card.find("h3", class_="heading_4_5"),
                    card.find("h4", class_="heading"),
                    card.find("a", class_="view_detail_button")
                ]
                
                for selector in title_selectors:
                    if selector:
                        title = selector.text.strip()
                        break
                
                if not title or not match_keywords(title):
                    continue
                
                # Company
                company = "Unknown"
                company_tag = card.find("a", class_="link_display_like_text") or \
                             card.find("p", class_="company-name")
                if company_tag:
                    company = company_tag.text.strip()
                
                # Duration
                duration = "Not specified"
                duration_patterns = card.find_all(string=re.compile(r'(\d+)\s*(month|week)', re.I))
                if duration_patterns:
                    duration = duration_patterns[0].strip()
                
                # Posted date
                posted = "recently"
                posted_tag = card.find("div", class_="status-container") or \
                            card.find(string=re.compile(r'(posted|ago)', re.I))
                if posted_tag:
                    posted = posted_tag.text.strip() if hasattr(posted_tag, 'text') else str(posted_tag).strip()
                
                # Link
                link = ""
                link_tag = card.find("a", href=True)
                if link_tag:
                    href = link_tag["href"]
                    link = f"https://internshala.com{href}" if not href.startswith("http") else href
                
                # Duration filter
                duration_months = parse_duration(duration)
                if duration_months > 0 and duration_months < MIN_DURATION_MONTHS:
                    continue
                
                jobs.append({
                    "Source": "Internshala",
                    "Title": title,
                    "Company": company,
                    "Duration": duration,
                    "Posted": posted,
                    "Link": link,
                    "Skills": "Multiple (check listing)"
                })
                
            except Exception as e:
                print(f"   Error parsing card: {str(e)[:50]}")
                continue
    
    except Exception as e:
        print(f"   ❌ Internshala error: {str(e)[:100]}")
    
    print(f"   ✅ Found {len(jobs)} matching internships")
    return jobs

def scrape_linkedin_lite(driver):
    """Scrape LinkedIn without login"""
    print("🔹 Scraping LinkedIn Jobs...")
    jobs = []
    
    try:
        # LinkedIn job search URL (no login required)
        keywords = "machine learning OR data science OR software developer"
        url = f"https://www.linkedin.com/jobs/search?keywords={keywords}&location=India&f_TP=1%2C2&f_E=1&position=1&pageNum=0"
        
        driver.get(url)
        time.sleep(5)
        
        # Scroll to load jobs
        for _ in range(3):
            driver.execute_script("window.scrollBy(0, 500);")
            time.sleep(1)
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        cards = soup.find_all("div", class_="base-card") or \
                soup.find_all("li", class_="jobs-search__results-list")
        
        print(f"   Found {len(cards)} cards")
        
        for card in cards[:20]:
            try:
                title_tag = card.find("h3", class_="base-search-card__title") or \
                           card.find("a", class_="job-card-list__title")
                if not title_tag:
                    continue
                
                title = title_tag.text.strip()
                if not match_keywords(title):
                    continue
                
                company_tag = card.find("h4", class_="base-search-card__subtitle") or \
                             card.find("a", class_="job-card-container__company-name")
                company = company_tag.text.strip() if company_tag else "Unknown"
                
                link_tag = card.find("a", href=True)
                link = link_tag["href"] if link_tag else ""
                
                jobs.append({
                    "Source": "LinkedIn",
                    "Title": title,
                    "Company": company,
                    "Duration": "3-6 months (typical)",
                    "Posted": "recent",
                    "Link": link,
                    "Skills": "Check listing"
                })
                
            except Exception as e:
                continue
    
    except Exception as e:
        print(f"   ❌ LinkedIn error: {str(e)[:100]}")
    
    print(f"   ✅ Found {len(jobs)} matching internships")
    return jobs

def scrape_indeed_improved(driver):
    """Improved Indeed scraper"""
    print("🔹 Scraping Indeed India...")
    jobs = []
    
    try:
        # India-specific Indeed URL
        url = "https://in.indeed.com/jobs?q=internship+(machine+learning+OR+data+science+OR+software+developer)&l=India&fromage=3"
        driver.get(url)
        time.sleep(4)
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        # Multiple selector attempts
        cards = soup.find_all("div", class_="job_seen_beacon") or \
                soup.find_all("div", class_="jobsearch-SerpJobCard") or \
                soup.find_all("a", class_="jcs-JobTitle")
        
        print(f"   Found {len(cards)} cards")
        
        for card in cards[:25]:
            try:
                title = None
                title_selectors = [
                    card.find("h2", class_="jobTitle"),
                    card.find("a", class_="jcs-JobTitle"),
                    card.find("span", title=True)
                ]
                
                for selector in title_selectors:
                    if selector:
                        title = selector.text.strip() if hasattr(selector, 'text') else selector.get('title', '')
                        break
                
                if not title or not match_keywords(title):
                    continue
                
                company_tag = card.find("span", class_="companyName") or \
                             card.find("span", {"data-testid": "company-name"})
                company = company_tag.text.strip() if company_tag else "Unknown"
                
                link = ""
                link_tag = card.find("a", href=True)
                if link_tag:
                    href = link_tag["href"]
                    link = f"https://in.indeed.com{href}" if not href.startswith("http") else href
                
                jobs.append({
                    "Source": "Indeed",
                    "Title": title,
                    "Company": company,
                    "Duration": "3-6 months",
                    "Posted": "Last 3 days",
                    "Link": link,
                    "Skills": "Multiple (see listing)"
                })
                
            except Exception as e:
                continue
    
    except Exception as e:
        print(f"   ❌ Indeed error: {str(e)[:100]}")
    
    print(f"   ✅ Found {len(jobs)} matching internships")
    return jobs

def scrape_naukri_internships(driver):
    """Scrape Naukri.com internships"""
    print("🔹 Scraping Naukri.com...")
    jobs = []
    
    try:
        url = "https://www.naukri.com/internship-jobs"
        driver.get(url)
        time.sleep(5)
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        cards = soup.find_all("article", class_="jobTuple") or \
                soup.find_all("div", class_="srp-jobtuple-wrapper")
        
        print(f"   Found {len(cards)} cards")
        
        for card in cards[:20]:
            try:
                title_tag = card.find("a", class_="title") or card.find("a", class_="jobTitle")
                if not title_tag:
                    continue
                
                title = title_tag.text.strip()
                if not match_keywords(title):
                    continue
                
                company_tag = card.find("a", class_="subTitle")
                company = company_tag.text.strip() if company_tag else "Unknown"
                
                link = title_tag.get("href", "")
                
                jobs.append({
                    "Source": "Naukri",
                    "Title": title,
                    "Company": company,
                    "Duration": "3-6 months",
                    "Posted": "recent",
                    "Link": link,
                    "Skills": "Check listing"
                })
                
            except:
                continue
    
    except Exception as e:
        print(f"   ❌ Naukri error: {str(e)[:100]}")
    
    print(f"   ✅ Found {len(jobs)} matching internships")
    return jobs

def deduplicate_jobs(jobs):
    """Remove duplicate internships"""
    seen = set()
    unique_jobs = []
    
    for job in jobs:
        # Create identifier from title and company
        identifier = f"{job['Title'].lower()}_{job['Company'].lower()}"
        if identifier not in seen:
            seen.add(identifier)
            unique_jobs.append(job)
    
    return unique_jobs

def save_results(all_jobs):
    """Save results to CSV with timestamp"""
    if not all_jobs:
        print("⚠️ No internships found today.")
        return
    
    df = pd.DataFrame(all_jobs)
    
    # Add application tracking columns
    df['Applied'] = 'No'
    df['Status'] = 'Not Applied'
    df['Notes'] = ''
    df['Scraped_Date'] = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"internships_{date_str}.csv"
    
    df.to_csv(filename, index=False)
    print(f"\n✅ Saved {len(df)} internships to {filename}")
    print(f"\n📊 Summary by Source:")
    print(df['Source'].value_counts())
    
    # Show sample
    print(f"\n🎯 Sample Internships:")
    print(df[['Title', 'Company', 'Source']].head(5).to_string(index=False))

def main():
    """Main execution function"""
    print("=" * 60)
    print("🚀 INTERNSHIP SCRAPER - STARTING")
    print("=" * 60)
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"🎯 Target: {DAILY_TARGET} internships")
    print(f"💼 Focus: ML, AI, Data Science, Web Development")
    print("=" * 60)
    
    driver = get_driver()
    all_jobs = []
    
    try:
        # Scrape from multiple sources
        scrapers = [
            scrape_internshala_improved,
            scrape_linkedin_lite,
            scrape_indeed_improved,
            scrape_naukri_internships
        ]
        
        for scraper in scrapers:
            try:
                jobs = scraper(driver)
                all_jobs.extend(jobs)
                time.sleep(2)  # Respectful delay between sites
            except Exception as e:
                print(f"   ❌ Scraper failed: {str(e)[:100]}")
                continue
        
        # Deduplicate
        all_jobs = deduplicate_jobs(all_jobs)
        
        # Filter to get best matches
        if len(all_jobs) > DAILY_TARGET:
            # Prioritize by keyword matches
            all_jobs = sorted(all_jobs, key=lambda x: sum(
                1 for kw in ["machine learning", "deep learning", "AI", "data science", "python"] 
                if kw in x['Title'].lower()
            ), reverse=True)[:DAILY_TARGET]
        
        print("\n" + "=" * 60)
        save_results(all_jobs)
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
    
    finally:
        driver.quit()
        print("\n✅ Scraping completed!")

if __name__ == "__main__":
    main()