import os
import sys
import time
import threading
from pathlib import Path
from datetime import datetime

class OutlookAgent:
    """Agent for monitoring Outlook emails and saving certificates"""
    
    def __init__(self, scan_interval=30):
        """
        Initialize Outlook Agent
        
        Args:
            scan_interval: Seconds between each inbox scan (default: 30)
        """
        self.scan_interval = scan_interval
        self.is_running = False
        self.processed_emails = set()
        
        # Try to import win32com
        try:
            import win32com.client
            import pythoncom
            self.win32com = win32com.client
            self.pythoncom = pythoncom
            self.HAS_WIN32 = True
        except ImportError:
            self.HAS_WIN32 = False
            print("⚠ Warning: pywin32 not installed. Outlook Agent will not work.")
        
        # Create necessary folders
        self.create_folders()
        
        # Outlook application reference
        self.outlook = None
        
        # Certificate keywords to look for
        self.cert_keywords = [
            'cert', 'certificate', 'analysis', 'report', 'test',
            'شهادة', 'تحليل', 'فحص', 'تقرير', 'نتيجة'
        ]
        
        # Supported attachment extensions
        self.supported_extensions = [
            '.pdf', '.xlsx', '.xls', '.doc', '.docx',
            '.jpg', '.jpeg', '.png', '.tif', '.tiff'
        ]
    
    def create_folders(self):
        """Create necessary folders if they don't exist"""
        from Config.paths import GETCERT_INBOX, MY_EMAILS_FOLDER
        GETCERT_INBOX.mkdir(parents=True, exist_ok=True)
        MY_EMAILS_FOLDER.mkdir(parents=True, exist_ok=True)
        print(f"✓ Certificates folder: {GETCERT_INBOX}")
        print(f"✓ Emails folder: {MY_EMAILS_FOLDER}")
    
    def start(self):
        """Start the Outlook monitoring agent"""
        if not self.HAS_WIN32:
            print("❌ Cannot start Outlook Agent: pywin32 not installed.")
            print("   Please install with: pip install pywin32")
            return False
        
        try:
            self.connect_to_outlook()
            self.is_running = True
            
            # Start monitoring in a separate thread
            monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
            monitor_thread.start()
            
            print("✅ Outlook Agent started successfully")
            print(f"📧 Monitoring emails every {self.scan_interval} seconds")
            print("🛑 Press Ctrl+C in main program to stop")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to start Outlook Agent: {e}")
            return False
    
    def connect_to_outlook(self):
        """Connect to Outlook application"""
        try:
            # Try to get existing Outlook instance
            self.outlook = self.win32com.Dispatch("Outlook.Application")
            print("✓ Connected to Outlook")
        except:
            # Start Outlook if not running
            print("⚠ Outlook not running, attempting to start...")
            try:
                os.startfile("outlook")
                time.sleep(10)  # Wait for Outlook to start
                self.outlook = self.win32com.Dispatch("Outlook.Application")
                print("✓ Outlook started and connected")
            except Exception as e:
                raise Exception(f"Failed to start Outlook: {e}")
    
    # باقي الدوال تبقى كما هي بدون تغيير...
    # فقط استبدل win32com.client بـ self.win32com
    # واستبدل pythoncom بـ self.pythoncom
    
    def monitor_loop(self):
        """Main monitoring loop"""
        try:
            namespace = self.outlook.GetNamespace("MAPI")
            inbox = namespace.GetDefaultFolder(6)  # Inbox
            
            print("\n🔍 Monitoring Outlook inbox...")
            
            while self.is_running:
                try:
                    # Get all messages
                    messages = inbox.Items
                    messages.Sort("[ReceivedTime]", True)
                    
                    new_count = 0
                    
                    # Process each message
                    for message in messages:
                        if (hasattr(message, 'Class') and 
                            message.Class == 43 and  # MailItem
                            hasattr(message, 'EntryID')):
                            
                            certificates = self.process_email(message)
                            if certificates:
                                new_count += 1
                    
                    # Report status
                    if new_count > 0:
                        print(f"\n📬 Processed {new_count} new email(s) with certificates")
                    
                    # Wait for next scan
                    for _ in range(self.scan_interval):
                        if not self.is_running:
                            break
                        time.sleep(1)
                        self.pythoncom.PumpWaitingMessages()
                        
                except Exception as e:
                    print(f"⚠ Monitoring error: {e}")
                    time.sleep(5)
                    
        except Exception as e:
            print(f"❌ Fatal error in monitor loop: {e}")