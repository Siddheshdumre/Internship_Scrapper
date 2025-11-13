import time
import pandas as pd
import requests
import smtplib
import os
import sys
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import re

print("=" * 60)
print("🚀 SCRIPT STARTING - IMPORTS SUCCESSFUL")
print("=" * 60)

# ==================== CONFIGURATION ====================
EMAIL_TO = "siddheshd114@gmail.com"
EMAIL_FROM = "siddheshd114@gmail.com"  # UPDATE THIS
EMAIL_PASSWORD = "odza obsf qces owen"  # UPDATE THIS

# Auto-apply settings
AUTO_APPLY_ENABLED = False  # Set to True after testing
RESUME_PATH = "Siddhesh_Dumre_ML_AI_SDE.pdf"
COVER_LETTER_TEMPLATE = """
Dear Hiring Manager,

I am writing to express my interest in the {position} position at {company}. As a Computer Science student at MIT World Peace University with 2+ years of experience in Machine Learning, Deep Learning, and Web Development, I believe I would be a valuable addition to your team.

My technical expertise includes:
- ML/AI: TensorFlow, Keras, NLP, Computer Vision (85-89% accuracy in deepfake detection)
- Web Development: MERN Stack, Node.js, React.js (30% performance improvement)
- Leadership: Led teams to victory in Smart India Hackathon, delivered 7+ client projects

I am particularly excited about this opportunity because it aligns with my skills in {key_skills}. I am eager to contribute to your team and learn from experienced professionals.

Thank you for considering my application. I look forward to discussing how I can contribute to {company}.

Best regards,
Siddhesh Dumre
8767705996 | siddheshd114@gmail.com
"""

KEYWORDS = [
    "machine learning", "deep learning", "artificial intelligence", "AI", "NLP",
    "data science", "python", "tensorflow", "keras", "react", "node", "mern",
    "full stack", "web development", "backend", "frontend", "software developer",
    "data analyst", "computer vision", "neural network"
]

MIN_DURATION_MONTHS = 3
DAILY_TARGET = 15

INTERNSHALA_EMAIL = ""
INTERNSHALA_PASSWORD = ""

print("✅ Configuration loaded")
print(f"   Email to: {EMAIL_TO}")
print(f"   Auto-apply: {AUTO_APPLY_ENABLED}")
print(f"   Target: {DAILY_TARGET} internships")

# ==================== UTILITIES ====================

def get_driver(headless=False):
    """Initialize Chrome driver"""
    try:
        print("\n🔧 Initializing Chrome driver...")
        
        # Try to import webdriver_manager
        try:
            from webdriver_manager.chrome import ChromeDriverManager
            print("   ✅ webdriver_manager imported")
        except ImportError:
            print("   ❌ webdriver_manager not found!")
            print("   Installing webdriver_manager...")
            os.system("pip install webdriver_manager")
            from webdriver_manager.chrome import ChromeDriverManager
        
        options = Options()
        if headless:
            options.add_argument("--headless")
            print("   Running in headless mode")
        else:
            print("   Running with visible browser")
            
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--log-level=3")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        prefs = {
            "download.default_directory": os.getcwd(),
            "download.prompt_for_download": False,
        }
        options.add_experimental_option("prefs", prefs)
        
        print("   Installing ChromeDriver...")
        service = Service(ChromeDriverManager().install())
        
        print("   Creating driver instance...")
        driver = webdriver.Chrome(service=service, options=options)
        
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
        })
        
        print("   ✅ Chrome driver initialized successfully!")
        return driver
        
    except Exception as e:
        print(f"   ❌ Error initializing driver: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

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

def generate_cover_letter(position, company):
    """Generate personalized cover letter"""
    key_skills = "machine learning, web development, and data science"
    if "machine learning" in position.lower() or "ml" in position.lower():
        key_skills = "machine learning, deep learning, and NLP"
    elif "web" in position.lower() or "full stack" in position.lower():
        key_skills = "MERN stack and full-stack web development"
    elif "data" in position.lower():
        key_skills = "data science, Python, and data visualization"
    
    return COVER_LETTER_TEMPLATE.format(
        position=position,
        company=company,
        key_skills=key_skills
    )

# ==================== SCRAPERS ====================

def scrape_internshala_improved(driver):
    """Improved Internshala scraper"""
    print("\n🔹 Scraping Internshala...")
    jobs = []
    
    try:
        url = "https://internshala.com/internships/computer-science,web-development,data-science,machine-learning-internship/work-from-home-internship"
        print(f"   Navigating to: {url[:50]}...")
        driver.get(url)
        print("   Waiting for page load...")
        time.sleep(5)
        
        # Close popups
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
        
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
        time.sleep(2)
        
        print("   Parsing HTML...")
        soup = BeautifulSoup(driver.page_source, "html.parser")
        cards = soup.find_all("div", class_="individual_internship") or \
                soup.find_all("div", class_="internship_meta") or \
                soup.find_all("div", {"data-internship-id": True})
        
        print(f"   Found {len(cards)} internship cards")
        
        for idx, card in enumerate(cards[:30]):
            try:
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
                
                if not title:
                    continue
                    
                if not match_keywords(title):
                    continue
                
                company = "Unknown"
                company_tag = card.find("a", class_="link_display_like_text") or \
                             card.find("p", class_="company-name")
                if company_tag:
                    company = company_tag.text.strip()
                
                duration = "Not specified"
                duration_patterns = card.find_all(string=re.compile(r'(\d+)\s*(month|week)', re.I))
                if duration_patterns:
                    duration = duration_patterns[0].strip()
                
                posted = "recently"
                posted_tag = card.find("div", class_="status-container") or \
                            card.find(string=re.compile(r'(posted|ago)', re.I))
                if posted_tag:
                    posted = posted_tag.text.strip() if hasattr(posted_tag, 'text') else str(posted_tag).strip()
                
                link = ""
                internship_id = ""
                link_tag = card.find("a", href=True)
                if link_tag:
                    href = link_tag["href"]
                    link = f"https://internshala.com{href}" if not href.startswith("http") else href
                    id_match = re.search(r'/internship/detail/([^/]+)', href)
                    if id_match:
                        internship_id = id_match.group(1)
                
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
                    "InternshipID": internship_id,
                    "Skills": "Multiple (check listing)",
                    "CanAutoApply": "Yes" if internship_id else "No",
                    "Applied": "No",
                    "Status": "Not Applied"
                })
                
                if idx % 5 == 0:
                    print(f"   Processed {idx+1} cards, found {len(jobs)} matches...")
                
            except Exception as e:
                print(f"   Warning: Error parsing card {idx}: {str(e)[:50]}")
                continue
    
    except Exception as e:
        print(f"   ❌ Internshala error: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print(f"   ✅ Found {len(jobs)} matching internships from Internshala")
    return jobs

def scrape_linkedin_lite(driver):
    """Scrape LinkedIn without login"""
    print("\n🔹 Scraping LinkedIn Jobs...")
    jobs = []
    
    try:
        keywords = "machine learning OR data science OR software developer"
        url = f"https://www.linkedin.com/jobs/search?keywords={keywords}&location=India&f_TP=1%2C2&f_E=1&position=1&pageNum=0"
        
        print(f"   Navigating to LinkedIn...")
        driver.get(url)
        time.sleep(5)
        
        for _ in range(3):
            driver.execute_script("window.scrollBy(0, 500);")
            time.sleep(1)
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        cards = soup.find_all("div", class_="base-card") or \
                soup.find_all("li")[:20]  # Fallback
        
        print(f"   Found {len(cards)} cards")
        
        for card in cards[:20]:
            try:
                title_tag = card.find("h3") or card.find("a")
                if not title_tag:
                    continue
                
                title = title_tag.text.strip()
                if not match_keywords(title):
                    continue
                
                company_tag = card.find("h4") or card.find("span", class_="company")
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
                    "InternshipID": "",
                    "Skills": "Check listing",
                    "CanAutoApply": "LinkedIn Easy Apply",
                    "Applied": "Manual Required",
                    "Status": "Not Applied"
                })
                
            except Exception as e:
                continue
    
    except Exception as e:
        print(f"   ❌ LinkedIn error: {str(e)[:100]}")
    
    print(f"   ✅ Found {len(jobs)} matching internships from LinkedIn")
    return jobs

def scrape_indeed_improved(driver):
    """Improved Indeed scraper"""
    print("\n🔹 Scraping Indeed India...")
    jobs = []
    
    try:
        url = "https://in.indeed.com/jobs?q=internship+(machine+learning+OR+data+science+OR+software+developer)&l=India&fromage=3"
        print(f"   Navigating to Indeed...")
        driver.get(url)
        time.sleep(4)
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        cards = soup.find_all("div", class_="job_seen_beacon") or \
                soup.find_all("td", class_="resultContent")
        
        print(f"   Found {len(cards)} cards")
        
        for card in cards[:25]:
            try:
                title = None
                title_tag = card.find("h2") or card.find("a", class_="jcs-JobTitle")
                if title_tag:
                    title = title_tag.text.strip()
                
                if not title or not match_keywords(title):
                    continue
                
                company_tag = card.find("span", class_="companyName")
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
                    "InternshipID": "",
                    "Skills": "Multiple (see listing)",
                    "CanAutoApply": "Manual",
                    "Applied": "Manual Required",
                    "Status": "Not Applied"
                })
                
            except Exception as e:
                continue
    
    except Exception as e:
        print(f"   ❌ Indeed error: {str(e)[:100]}")
    
    print(f"   ✅ Found {len(jobs)} matching internships from Indeed")
    return jobs

# ==================== EMAIL FUNCTIONALITY ====================

def send_email(jobs_df, csv_filename):
    """Send email with internship results"""
    try:
        print("\n📧 Preparing to send email...")
        
        if EMAIL_FROM == "your_email@gmail.com" or EMAIL_PASSWORD == "your_app_password":
            print("   ⚠️ Email credentials not configured!")
            print("   Please update EMAIL_FROM and EMAIL_PASSWORD in the script")
            return False
        
        msg = MIMEMultipart()
        msg['From'] = EMAIL_FROM
        msg['To'] = EMAIL_TO
        msg['Subject'] = f"Daily Internship Report - {datetime.now().strftime('%B %d, %Y')} - {len(jobs_df)} Opportunities"
        
        html_body = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .header {{ background-color: #4CAF50; color: white; padding: 20px; text-align: center; }}
                .summary {{ background-color: #f2f2f2; padding: 15px; margin: 20px 0; border-radius: 5px; }}
                .job-card {{ border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }}
                .job-title {{ color: #2196F3; font-size: 18px; font-weight: bold; }}
                .company {{ color: #555; font-size: 16px; }}
                .apply-btn {{ background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 10px; }}
                .stats {{ display: inline-block; margin: 10px 20px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🎯 Your Daily Internship Report</h1>
                <p>{datetime.now().strftime('%B %d, %Y')}</p>
            </div>
            
            <div class="summary">
                <h2>📊 Summary</h2>
                <div class="stats"><strong>Total Found:</strong> {len(jobs_df)}</div>
                <div class="stats"><strong>Auto-Applied:</strong> {len(jobs_df[jobs_df['Applied'] == 'Yes'])}</div>
                <div class="stats"><strong>Manual Required:</strong> {len(jobs_df[jobs_df['Applied'].str.contains('Manual|Login', na=False)])}</div>
            </div>
            
            <h2>🔥 Top Opportunities</h2>
        """
        
        for idx, row in jobs_df.head(10).iterrows():
            html_body += f"""
            <div class="job-card">
                <div class="job-title">{row['Title']}</div>
                <div class="company">🏢 {row['Company']} | 📍 {row['Source']}</div>
                <p>⏰ Duration: {row['Duration']} | 📅 Posted: {row['Posted']}</p>
                <p>Status: {row['Applied']}</p>
                <a href="{row['Link']}" class="apply-btn" target="_blank">View & Apply</a>
            </div>
            """
        
        html_body += """
            <div style="text-align: center; margin-top: 30px; color: #888;">
                <p>Full details attached as CSV | Generated by Internship Auto-Scraper</p>
            </div>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(html_body, 'html'))
        
        # Attach CSV
        with open(csv_filename, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={csv_filename}')
            msg.attach(part)
        
        print("   Connecting to Gmail SMTP...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        print("   Sending email...")
        server.send_message(msg)
        server.quit()
        
        print("   ✅ Email sent successfully!")
        return True
        
    except Exception as e:
        print(f"   ❌ Email error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

# ==================== MAIN ====================

def deduplicate_jobs(jobs):
    """Remove duplicate internships"""
    seen = set()
    unique_jobs = []
    
    for job in jobs:
        identifier = f"{job['Title'].lower()}_{job['Company'].lower()}"
        if identifier not in seen:
            seen.add(identifier)
            unique_jobs.append(job)
    
    return unique_jobs

def save_results(all_jobs):
    """Save results to CSV"""
    if not all_jobs:
        print("\n⚠️ No internships found today.")
        return None
    
    print(f"\n💾 Saving {len(all_jobs)} internships to CSV...")
    df = pd.DataFrame(all_jobs)
    
    df['Scraped_Date'] = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"internships_{date_str}.csv"
    
    df.to_csv(filename, index=False)
    print(f"   ✅ Saved to {filename}")
    print(f"\n📊 Summary by Source:")
    print(df['Source'].value_counts().to_string())
    
    return filename

def main():
    """Main execution function"""
    print("\n" + "=" * 60)
    print("🚀 ADVANCED INTERNSHIP SCRAPER")
    print("=" * 60)
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"🎯 Target: {DAILY_TARGET} internships")
    print(f"💼 Focus: ML, AI, Data Science, Web Development")
    print(f"🤖 Auto-Apply: {'Enabled' if AUTO_APPLY_ENABLED else 'Disabled'}")
    print(f"📧 Email: {EMAIL_TO}")
    print("=" * 60)
    
    driver = None
    all_jobs = []
    
    try:
        driver = get_driver(headless=False)
        
        # Scrape from multiple sources
        print("\n📊 Starting scraping process...")
        scrapers = [
            ("Internshala", scrape_internshala_improved),
            ("LinkedIn", scrape_linkedin_lite),
            ("Indeed", scrape_indeed_improved),
        ]
        
        for name, scraper in scrapers:
            try:
                print(f"\n{'='*40}")
                jobs = scraper(driver)
                all_jobs.extend(jobs)
                print(f"Running total: {len(all_jobs)} internships")
                time.sleep(2)
            except Exception as e:
                print(f"❌ {name} scraper failed: {str(e)[:100]}")
                import traceback
                traceback.print_exc()
                continue
        
        print("\n" + "=" * 60)
        print(f"📊 SCRAPING COMPLETE: Found {len(all_jobs)} total internships")
        print("=" * 60)
        
        # Deduplicate
        print("\n🔄 Removing duplicates...")
        all_jobs = deduplicate_jobs(all_jobs)
        print(f"   After deduplication: {len(all_jobs)} unique internships")
        
        # Filter to target
        if len(all_jobs) > DAILY_TARGET:
            print(f"\n🎯 Filtering to top {DAILY_TARGET} matches...")
            all_jobs = sorted(all_jobs, key=lambda x: sum(
                1 for kw in ["machine learning", "deep learning", "AI", "data science", "python"] 
                if kw in x['Title'].lower()
            ), reverse=True)[:DAILY_TARGET]
        
        # Save results
        csv_filename = save_results(all_jobs)
        
        # Send email
        if csv_filename:
            df = pd.DataFrame(all_jobs)
            send_email(df, csv_filename)
        
        print("\n" + "=" * 60)
        print("🎉 PROCESS COMPLETED SUCCESSFULLY!")
        print(f"   📊 Total internships: {len(all_jobs)}")
        print(f"   📧 Email sent to: {EMAIL_TO}")
        print(f"   💾 CSV saved: {csv_filename}")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        if driver:
            print("\n🔒 Closing browser...")
            driver.quit()
        print("\n✅ Script execution completed!\n")

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🎬 SCRIPT EXECUTION STARTING")
    print("=" * 60)
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Script interrupted by user (Ctrl+C)")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n" + "=" * 60)
        print("👋 SCRIPT FINISHED")
        print("=" * 60)