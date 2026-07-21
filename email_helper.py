import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
NOTIFY_EMAIL = os.getenv("NOTIFY_EMAIL")

def send_notification_email(student_name, support_type, urgency, description, neighborhood, phone, email):
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"🆕 New Support Request — {urgency} | {support_type}"
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = NOTIFY_EMAIL

        html = f"""
        <html>
        <body style="font-family: Inter, sans-serif; background: #f5f7fa; padding: 40px;">
            <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 16px; overflow: hidden; box-shadow: 0 4px 24px rgba(0,0,0,0.08);">
                
                <div style="background: linear-gradient(135deg, #1a1a1a, #2d6a4f); padding: 32px; text-align: center;">
                    <h1 style="color: white; margin: 0; font-size: 1.5em;">🎓 ChiEAC Support Portal</h1>
                    <p style="color: #a8d5b5; margin: 8px 0 0 0; font-size: 0.9em;">New Student Support Request</p>
                </div>

                <div style="padding: 32px;">
                    <div style="background: {'#fee2e2' if urgency == 'Critical - Need help today' else '#fef3c7' if urgency == 'High - Need help this week' else '#f0fdf4'}; 
                         border-radius: 8px; padding: 16px; margin-bottom: 24px; text-align: center;">
                        <span style="font-size: 1.1em; font-weight: 700; color: {'#dc2626' if urgency == 'Critical - Need help today' else '#d97706' if urgency == 'High - Need help this week' else '#2d6a4f'};">
                            {'🚨 CRITICAL' if urgency == 'Critical - Need help today' else '⚠️ HIGH PRIORITY' if urgency == 'High - Need help this week' else '📋 ' + urgency}
                        </span>
                    </div>

                    <table style="width: 100%; border-collapse: collapse;">
                        <tr style="border-bottom: 1px solid #f0f0f0;">
                            <td style="padding: 12px 0; color: #888; font-size: 0.9em; width: 140px;">Student Name</td>
                            <td style="padding: 12px 0; color: #1a1a1a; font-weight: 600;">{student_name}</td>
                        </tr>
                        <tr style="border-bottom: 1px solid #f0f0f0;">
                            <td style="padding: 12px 0; color: #888; font-size: 0.9em;">Email</td>
                            <td style="padding: 12px 0; color: #1a1a1a; font-weight: 600;">{email}</td>
                        </tr>
                        <tr style="border-bottom: 1px solid #f0f0f0;">
                            <td style="padding: 12px 0; color: #888; font-size: 0.9em;">Phone</td>
                            <td style="padding: 12px 0; color: #1a1a1a; font-weight: 600;">{phone if phone else 'Not provided'}</td>
                        </tr>
                        <tr style="border-bottom: 1px solid #f0f0f0;">
                            <td style="padding: 12px 0; color: #888; font-size: 0.9em;">Neighborhood</td>
                            <td style="padding: 12px 0; color: #1a1a1a; font-weight: 600;">{neighborhood if neighborhood else 'Not provided'}</td>
                        </tr>
                        <tr style="border-bottom: 1px solid #f0f0f0;">
                            <td style="padding: 12px 0; color: #888; font-size: 0.9em;">Support Type</td>
                            <td style="padding: 12px 0; color: #1a1a1a; font-weight: 600;">{support_type}</td>
                        </tr>
                        <tr style="border-bottom: 1px solid #f0f0f0;">
                            <td style="padding: 12px 0; color: #888; font-size: 0.9em;">Urgency</td>
                            <td style="padding: 12px 0; color: #1a1a1a; font-weight: 600;">{urgency}</td>
                        </tr>
                    </table>

                    <div style="margin-top: 24px; background: #fafafa; border-radius: 8px; padding: 16px;">
                        <div style="color: #888; font-size: 0.85em; margin-bottom: 8px;">Description</div>
                        <div style="color: #333; font-size: 0.95em; line-height: 1.7;">{description}</div>
                    </div>

                    <div style="margin-top: 24px; text-align: center;">
                        <a href="https://chieac-support-system-ntophmxj4oucyc79hkwsrp.streamlit.app" 
                           style="background: #2d6a4f; color: white; padding: 14px 32px; border-radius: 8px; 
                                  text-decoration: none; font-weight: 600; display: inline-block;">
                            View All Requests →
                        </a>
                    </div>
                </div>

                <div style="background: #f8f8f8; padding: 20px; text-align: center; border-top: 1px solid #f0f0f0;">
                    <p style="color: #888; font-size: 0.8em; margin: 0;">
                        Chicago Education Advocacy Cooperative (ChiEAC) | EIN: 84-4211875<br>
                        773-599-0267 | benjamin@chieac.org
                    </p>
                </div>
            </div>
        </body>
        </html>
        """

        msg.attach(MIMEText(html, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, NOTIFY_EMAIL, msg.as_string())

        return True

    except Exception as e:
        print(f"Email error: {e}")
        return False


def send_emergency_email(student_name, student_email):
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "🚨 EMERGENCY REQUEST — Immediate Action Required"
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = NOTIFY_EMAIL

        html = f"""
        <html>
        <body style="font-family: Inter, sans-serif; background: #f5f7fa; padding: 40px;">
            <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 16px; overflow: hidden; box-shadow: 0 4px 24px rgba(0,0,0,0.08);">
                
                <div style="background: linear-gradient(135deg, #dc2626, #b91c1c); padding: 32px; text-align: center;">
                    <h1 style="color: white; margin: 0; font-size: 1.8em;">🚨 EMERGENCY</h1>
                    <p style="color: #fca5a5; margin: 8px 0 0 0;">A student needs immediate help!</p>
                </div>

                <div style="padding: 32px; text-align: center;">
                    <div style="background: #fee2e2; border-radius: 12px; padding: 24px; margin-bottom: 24px;">
                        <div style="font-size: 1.2em; font-weight: 700; color: #dc2626; margin-bottom: 8px;">
                            {student_name}
                        </div>
                        <div style="color: #666; font-size: 0.9em;">{student_email}</div>
                    </div>

                    <p style="color: #333; font-size: 1em; line-height: 1.7;">
                        This student has triggered an emergency alert and needs
                        immediate assistance. Please contact them as soon as possible.
                    </p>

                    <div style="margin-top: 24px;">
                        <a href="https://chieac-support-system-ntophmxj4oucyc79hkwsrp.streamlit.app"
                           style="background: #dc2626; color: white; padding: 14px 32px; border-radius: 8px;
                                  text-decoration: none; font-weight: 600; display: inline-block;">
                            View Emergency Requests →
                        </a>
                    </div>
                </div>

                <div style="background: #f8f8f8; padding: 20px; text-align: center; border-top: 1px solid #f0f0f0;">
                    <p style="color: #888; font-size: 0.8em; margin: 0;">
                        Chicago Education Advocacy Cooperative (ChiEAC) | 773-599-0267
                    </p>
                </div>
            </div>
        </body>
        </html>
        """

        msg.attach(MIMEText(html, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, NOTIFY_EMAIL, msg.as_string())

        return True

    except Exception as e:
        print(f"Emergency email error: {e}")
        return False