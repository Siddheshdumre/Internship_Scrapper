# Internship Auto-Scraper

A small Python toolkit to find internship listings (ML / Data Science / Web) from major job sites, save results to CSV, and email a daily report. It includes a more advanced script that optionally auto-applies and sends a styled email with top opportunities.

**Main files**
- `internships.py`: Original scraper with multiple site scrapers (Internshala, LinkedIn, Indeed, Naukri), deduplication and CSV saving.
- `internships_final.py`: Advanced scraper with broader search, auto-apply scaffolding, email report functionality and improved configuration.
- `internships_advanced.py`: Another advanced variant similar to `internships_final.py` (keeps experimental flags separate).
- `test_email.py`: Standalone script to validate Gmail SMTP / App Password configuration and send a test email.
- `internships_YYYY-MM-DD.csv`: Example output CSV(s) produced when running the scraper (auto-generated filename pattern).

**Repository purpose**
- Collect relevant internship listings for roles such as machine learning, data science, web development, and software engineering.
- Save results to CSV for tracking and optionally email the top opportunities daily.
- Provide a basis for automating applications (auto-apply functionality is experimental and must be used carefully).

**Requirements**
- Python 3.8+ recommended
- Chrome browser installed (used by Selenium)
- Packages (install with pip):

```powershell
pip install -r requirements.txt
# or directly
pip install selenium beautifulsoup4 pandas requests webdriver-manager
```

If you don't have a `requirements.txt`, the main packages used are: `selenium`, `beautifulsoup4`, `pandas`, `requests`, `webdriver-manager`.

**Important configuration & security notes**
- The scripts include email configuration variables: `EMAIL_FROM`, `EMAIL_PASSWORD`, and `EMAIL_TO` inside the scripts. Do NOT commit real credentials.
- Prefer using environment variables for credentials. Example (PowerShell):

```powershell
[Environment]::SetEnvironmentVariable("GMAIL_ADDRESS", "your_email@gmail.com", "User")
[Environment]::SetEnvironmentVariable("GMAIL_APP_PASSWORD", "your_16_char_app_password", "User")
```

Then in the script replace hardcoded values with `os.getenv('GMAIL_ADDRESS')` and `os.getenv('GMAIL_APP_PASSWORD')`.

- For Gmail sending, create an App Password (requires 2-Step Verification). See `test_email.py` for instructions and a helper to test your configuration.

**How to run**

1. (Optional) Create and activate a virtual environment:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install selenium beautifulsoup4 pandas requests webdriver-manager
```

2. Test email configuration:

```powershell
python test_email.py
```

3. Run the advanced scraper (recommended for interactive runs):

```powershell
python internships_final.py
```

4. Simple/original scraper:

```powershell
python internships.py
```

Output: each run saves a CSV named `internships_YYYY-MM-DD.csv` in the working directory. The advanced scripts also try to send an email with that CSV attached.

**Key options inside the scripts**
- `AUTO_APPLY_ENABLED` (in `internships_final.py` / `internships_advanced.py`): when `True`, the code attempts to auto-apply to internships where possible. Use after careful testing.
- `DAILY_TARGET`: number of top results to keep in the final output.
- `MIN_DURATION_MONTHS`: filter internships shorter than this.

**ChromeDriver / Selenium**
- The scripts use `webdriver-manager` to automatically download a matching ChromeDriver. Ensure your Chrome version is up to date for best compatibility.
- If you prefer manual driver management, install a compatible ChromeDriver and adjust the `Service` initialization inside the `get_driver()` function.

**Automation / Scheduling**
- On Windows you can create a Task Scheduler entry to run `internships_final.py` daily. Make sure the environment and Chrome are available to the scheduled task.

**Troubleshooting**
- If Selenium fails to start, check that Chrome is installed and `webdriver-manager` can download the driver. Run `python -c "from webdriver_manager.chrome import ChromeDriverManager; print(ChromeDriverManager().install())"` to test.
- If emails fail: run `test_email.py` and follow its printed troubleshooting steps. Use App Passwords.
- If scrapers return few results, the target sites may have updated their HTML; selectors are in the scripts — update `BeautifulSoup` selectors accordingly.

**Contributing / Next steps**
- Add a `requirements.txt` and `.gitignore` (recommended: ignore `.venv/`, any `*.csv`, credentials files).
- Add GitHub Actions to run linting and optionally nightly runs (careful with secrets and scheduling).
- Improve auto-apply logic and add robust login/session handling for sites that require authentication.

**License**
- Add a license file if you plan to share this publicly.

---

If you want, I can: add a `requirements.txt`, create a `.gitignore` tuned for Python, or commit + push these changes for you. Which should I do next?
# Internship_Scrapper
