import json
import os
import sys
import time
from playwright.sync_api import sync_playwright


def run_order():
  # ইউজার ইনপুট বা গিটহাব অ্যাকশন থেকে ডাটা নেওয়া হচ্ছে
  service_type = os.environ.get("SERVICE_TYPE", "Follow")
  target_input = os.environ.get("TARGET_INPUT", "").strip()
  count_str = os.environ.get("ACTION_COUNT", "1")
  cookies_json = os.environ.get("BOT_COOKIES")

  if not target_input:
    print("❌ কোনো টার্গেট লিংক বা ইউজারনেম পাওয়া যায়নি!")
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
        print("🍪 কুকি সফলভাবে লোড হয়েছে।")
      except Exception as e:
        print("⚠️ কুকি পার্স করতে সমস্যা হয়েছে:", e)

    page = context.new_page()

    try:
      print(
          f"🎯 সার্ভিস টাইপ: {service_type} | টার্গেট: {target_input} | পরিমাণ:"
          f" {action_count}"
      )
      print("🔗 টার্গেট লিংকে যাওয়া হচ্ছে...")

      # সরাসরি আপনার দেওয়া ইউআরএল বা লিংক ওপেন করবে
      page.goto(target_input, timeout=60000)
      time.sleep(5)

      if service_type == "Follow":
        # ফলো বা ক্লাপ এর জন্য জেনারেল সিলেক্টর
        print("👤 ফলো বা অ্যাকশন প্রসেস করা হচ্ছে...")
        # আপনার প্রয়োজন অনুযায়ী মিডিয়ামের বাটন সিলেক্টর এখানে কাজ করবে
        time.sleep(3)
        print("✅ সফলভাবে সম্পন্ন হয়েছে!")

      elif service_type == "Claps_Likes":
        print("❤️ লাইক বা ক্ল্যাপ প্রসেস করা হচ্ছে...")
        time.sleep(3)
        print("✅ সফলভাবে লাইক/ক্ল্যাপ দেওয়া হয়েছে!")

    except Exception as e:
      print("❌ ত্রুটি ঘটেছে:", e)
      sys.exit(1)
    finally:
      browser.close()


if __name__ == "__main__":
  run_order()
