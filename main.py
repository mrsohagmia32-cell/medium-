import json
import os
import sys
import time
from playwright.sync_api import sync_playwright


def run_order():
  service_type = os.environ.get("SERVICE_TYPE", "Followers")
  target_input = os.environ.get("TARGET_INPUT", "").strip()
  count_str = os.environ.get("ACTION_COUNT", "1")
  cookies_json = os.environ.get("BOT_COOKIES")

  if not target_input:
    print("❌ কোনো টার্গেট ইনপুট (ইউজারনেম বা লিংক) পাওয়া যায়নি!")
    sys.exit(1)

  try:
    action_count = int(count_str)
  except ValueError:
    action_count = 1

  with sync_playwright() as p:
    browser_args = [
        "--no-sandbox",
        "--disable-setuid-sandbox",
        "--disable-dev-shm-usage",
    ]
    launch_options = {
        "headless": True,
        "args": browser_args,
    }

    # নরমাল ব্রাউজার কানেকশন এবং সাধারণ ইউজার এজেন্ট ব্যবহার করা হচ্ছে
    browser = p.chromium.launch(**launch_options)
    context = browser.new_context(
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
            " like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ),
        viewport={"width": 1280, "height": 720},
    )

    if cookies_json:
      try:
        cookies = json.loads(cookies_json)
        context.add_cookies(cookies)
        print("🍪 অ্যাকাউন্ট কুকি সফলভাবে লোড হয়েছে।")
      except Exception as e:
        print("⚠️ কুকি পার্স করতে সমস্যা হয়েছে:", e)

    page = context.new_page()

    try:
      if service_type == "Followers":
        username = target_input.lstrip("@")
        target_url = f"https://www.instagram.com/{username}/"
        print(
            f"🎯 সার্ভিস: ফলোয়ার | টার্গেট: @{username} | পরিমাণ: {action_count}"
        )

        print("🔗 পেজে যাওয়া হচ্ছে...")
        page.goto(target_url, timeout=60000)
        time.sleep(5)

        follow_btn = page.locator(
            "button:has-text('Follow'), button:has-text('Follow Back')"
        ).first
        if follow_btn.is_visible():
          text = follow_btn.inner_text().strip()
          if "Follow" in text and "Following" not in text:
            follow_btn.click()
            time.sleep(3)
            print("✅ সফলভাবে ফলো করা হয়েছে!")
          else:
            print("⚠️ অ্যাকাউন্টটি ইতিমধ্যে ফলো করা আছে।")
        else:
          print("⚠️ ফলো বাটন পাওয়া যায়নি।")

      elif service_type == "Likes":
        target_url = target_input
        print(
            f"🎯 সার্ভিস: লাইক | পোস্ট লিংক: {target_url} | পরিমাণ: {action_count}"
        )

        print("🔗 পোস্ট পেজে যাওয়া হচ্ছে...")
        page.goto(target_url, timeout=60000)
        time.sleep(5)

        like_btn = page.locator(
            "svg[aria-label='Like'], svg[aria-label='Unlike']"
        ).first
        if like_btn.is_visible():
          like_btn.click()
          time.sleep(3)
          print("❤️ সফলভাবে পোস্টে লাইক দেওয়া হয়েছে!")
        else:
          print("⚠️ লাইক বাটন পাওয়া যায়নি।")

    except Exception as e:
      print("❌ ত্রুটি ঘটেছে:", e)
      sys.exit(1)
    finally:
      browser.close()


if __name__ == "__main__":
  run_order()
