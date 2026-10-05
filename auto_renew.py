import os
import time
from playwright.sync_api import sync_playwright

def renew_workspace():
    email = os.environ.get("PREPARE_EMAIL")
    password = os.environ.get("PREPARE_PASSWORD")

    with sync_playwright() as p:
        # ساخت مرورگر
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("Logging in to prepare.sh...")
        page.goto("https://prepare.sh/login")
        
        # ورود به حساب (براساس فرم لاگین سایت)
        page.fill('input[type="email"]', email)
        page.fill('input[type="password"]', password)
        page.click('button[type="submit"]')
        page.wait_for_timeout(5000)

        # رفتن به صفحه محیط‌ها
        page.goto("https://prepare.sh/profile/environments")
        page.wait_for_timeout(3000)

        # اگر سروری وجود دارد آن را پاک کن
        if page.locator("button:has-text('Delete')").is_visible():
            print("Deleting old environment...")
            page.click("button:has-text('Delete')")
            page.wait_for_timeout(2000)
            # تایید حذف در صورت وجود مدال
            if page.locator("button:has-text('Confirm')").is_visible():
                page.click("button:has-text('Confirm')")
            page.wait_for_timeout(5000)

        # ساخت سرور جدید
        print("Creating new environment...")
        page.click("text=New environment")
        page.wait_for_timeout(3000)
        
        # انتخاب اوبونتو و launch
        page.click("text=Ubuntu 24.04 LTS")
        page.wait_for_timeout(5000)

        print("New environment created successfully!")
        browser.close()

if __name__ == "__main__":
    renew_workspace()
