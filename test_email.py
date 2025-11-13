import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

# ==================== CONFIGURATION ====================
# UPDATE THESE WITH YOUR DETAILS
EMAIL_TO = "siddheshd114@gmail.com"
EMAIL_FROM = "siddheshd114@gmail.com"  # ← UPDATE THIS
EMAIL_PASSWORD = "qrxd wbau rwbb qntu"  # ← UPDATE THIS (16 characters from Google)

# ==================== TEST EMAIL FUNCTION ====================

def test_email_connection():
    """Test email configuration and send a test email"""
    
    print("=" * 60)
    print("📧 EMAIL CONFIGURATION TEST")
    print("=" * 60)
    print(f"From: {EMAIL_FROM}")
    print(f"To: {EMAIL_TO}")
    print(f"Password length: {len(EMAIL_PASSWORD)} characters")
    print("=" * 60)
    
    # Validation
    if EMAIL_FROM == "your_email@gmail.com":
        print("\n❌ ERROR: Please update EMAIL_FROM with your Gmail address")
        return False
    
    if EMAIL_PASSWORD == "your_app_password_here" or len(EMAIL_PASSWORD) < 10:
        print("\n❌ ERROR: Please update EMAIL_PASSWORD with your Gmail App Password")
        print("\n📝 How to get Gmail App Password:")
        print("   1. Go to: https://myaccount.google.com/apppasswords")
        print("   2. Sign in to your Google Account")
        print("   3. Select 'Mail' and your device name")
        print("   4. Click 'Generate'")
        print("   5. Copy the 16-character password (remove spaces)")
        print("   6. Paste it in EMAIL_PASSWORD variable")
        return False
    
    try:
        print("\n🔄 Step 1: Connecting to Gmail SMTP server...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        print("   ✅ Connected to smtp.gmail.com:587")
        
        print("\n🔄 Step 2: Starting TLS encryption...")
        server.starttls()
        print("   ✅ TLS encryption enabled")
        
        print("\n🔄 Step 3: Logging in...")
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        print("   ✅ Login successful!")
        
        print("\n🔄 Step 4: Creating test email...")
        msg = MIMEMultipart()
        msg['From'] = EMAIL_FROM
        msg['To'] = EMAIL_TO
        msg['Subject'] = f"✅ Test Email - Internship Scraper Setup Complete - {datetime.now().strftime('%H:%M:%S')}"
        
        html_body = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; padding: 20px; }}
                .success-box {{ 
                    background-color: #4CAF50; 
                    color: white; 
                    padding: 30px; 
                    text-align: center; 
                    border-radius: 10px;
                    margin: 20px 0;
                }}
                .info-box {{
                    background-color: #f2f2f2;
                    padding: 20px;
                    border-radius: 5px;
                    margin: 20px 0;
                }}
                .check {{ font-size: 48px; }}
            </style>
        </head>
        <body>
            <div class="success-box">
                <div class="check">✅</div>
                <h1>Email Setup Successful!</h1>
                <p>Your internship scraper is now configured correctly</p>
            </div>
            
            <div class="info-box">
                <h2>📊 Configuration Details</h2>
                <p><strong>From:</strong> {EMAIL_FROM}</p>
                <p><strong>To:</strong> {EMAIL_TO}</p>
                <p><strong>Time:</strong> {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}</p>
            </div>
            
            <div class="info-box">
                <h2>🎯 Next Steps</h2>
                <ol>
                    <li>Run your internship scraper script</li>
                    <li>You'll receive daily emails with internship opportunities</li>
                    <li>Check spam folder if emails don't appear in inbox</li>
                    <li>Add {EMAIL_FROM} to your contacts to avoid spam</li>
                </ol>
            </div>
            
            <div class="info-box">
                <h2>💡 Tips</h2>
                <ul>
                    <li>Run the scraper daily for best results</li>
                    <li>Set up a scheduled task to automate it</li>
                    <li>Keep your App Password secure</li>
                    <li>Check the CSV attachment for full details</li>
                </ul>
            </div>
            
            <p style="text-align: center; color: #888; margin-top: 30px;">
                This is a test email from your Internship Auto-Scraper
            </p>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(html_body, 'html'))
        print("   ✅ Test email created")
        
        print("\n🔄 Step 5: Sending email...")
        server.send_message(msg)
        print("   ✅ Email sent successfully!")
        
        server.quit()
        
        print("\n" + "=" * 60)
        print("🎉 SUCCESS! Check your inbox at: " + EMAIL_TO)
        print("=" * 60)
        print("\n💡 If you don't see the email:")
        print("   1. Check your SPAM/Junk folder")
        print("   2. Wait 1-2 minutes for delivery")
        print("   3. Make sure email address is correct")
        print("   4. Try adding sender to contacts")
        print("\n✅ Your email configuration is working correctly!")
        print("   You can now run the main internship scraper script.")
        
        return True
        
    except smtplib.SMTPAuthenticationError:
        print("\n❌ AUTHENTICATION FAILED!")
        print("\n🔍 Common Issues:")
        print("   1. Wrong App Password - Did you use your regular Gmail password?")
        print("      ➜ You need a special 16-character 'App Password'")
        print("   2. App Password not generated yet")
        print("      ➜ Go to: https://myaccount.google.com/apppasswords")
        print("   3. Wrong email address")
        print("      ➜ Make sure EMAIL_FROM matches the Google account")
        print("\n📝 Steps to fix:")
        print("   1. Go to: https://myaccount.google.com/apppasswords")
        print("   2. You might need to enable 2-Step Verification first")
        print("   3. Select 'Mail' → 'Other' → Type 'Internship Scraper'")
        print("   4. Click 'Generate'")
        print("   5. Copy the 16-character password (it looks like: abcd efgh ijkl mnop)")
        print("   6. Remove spaces and paste in EMAIL_PASSWORD")
        return False
        
    except smtplib.SMTPException as e:
        print(f"\n❌ SMTP ERROR: {str(e)}")
        print("\n🔍 Possible Issues:")
        print("   1. Network/Firewall blocking SMTP")
        print("   2. Gmail SMTP temporarily unavailable")
        print("   3. Try again in a few minutes")
        return False
        
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {str(e)}")
        print("\n🔍 Debug Info:")
        import traceback
        traceback.print_exc()
        return False

# ==================== ALTERNATIVE: USING ENVIRONMENT VARIABLES ====================

def show_secure_setup():
    """Show how to use environment variables for security"""
    print("\n" + "=" * 60)
    print("🔒 SECURE SETUP (Recommended)")
    print("=" * 60)
    print("\nInstead of hardcoding credentials, use environment variables:")
    print("\n# Windows (Command Prompt):")
    print('setx GMAIL_ADDRESS "your_email@gmail.com"')
    print('setx GMAIL_APP_PASSWORD "your_16_char_password"')
    print("\n# Windows (PowerShell):")
    print('[Environment]::SetEnvironmentVariable("GMAIL_ADDRESS", "your_email@gmail.com", "User")')
    print('[Environment]::SetEnvironmentVariable("GMAIL_APP_PASSWORD", "your_16_char_password", "User")')
    print("\n# Mac/Linux (add to ~/.bashrc or ~/.zshrc):")
    print('export GMAIL_ADDRESS="your_email@gmail.com"')
    print('export GMAIL_APP_PASSWORD="your_16_char_password"')
    print("\nThen in your Python script:")
    print("""
import os
EMAIL_FROM = os.getenv('GMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('GMAIL_APP_PASSWORD')
    """)
    print("=" * 60)

# ==================== RUN TEST ====================

if __name__ == "__main__":
    print("\n🚀 Starting Email Configuration Test...\n")
    
    success = test_email_connection()
    
    if not success:
        print("\n" + "=" * 60)
        print("❌ EMAIL SETUP INCOMPLETE")
        print("=" * 60)
        print("\nPlease fix the errors above and run this script again.")
        show_secure_setup()
    else:
        print("\n🎊 Your email is configured and working!")
        print("   Run your main scraper script now to get daily internship emails.")