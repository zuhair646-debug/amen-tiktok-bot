#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 آمِن - روبوت TikTok الذكي
يبحث في TikTok، يجمع روابط، يحمّل فيديوهات آمنة، يرفعها R2
"""

import os
import json
import time
import random
from datetime import datetime
from pathlib import Path
import subprocess
import boto3
from botocore.client import Config
from playwright.sync_api import sync_playwright
import requests

# ═══════════════════════════════════════════════════════════
# ⚙️ الإعدادات
# ═══════════════════════════════════════════════════════════

TIKTOK_EMAIL = os.getenv('TIKTOK_EMAIL')
TIKTOK_PASSWORD = os.getenv('TIKTOK_PASSWORD')
R2_ACCESS_KEY = os.getenv('R2_ACCESS_KEY')
R2_SECRET_KEY = os.getenv('R2_SECRET_KEY')
R2_ENDPOINT = os.getenv('R2_ENDPOINT')
R2_BUCKET = os.getenv('R2_BUCKET', 'amen-videos')
R2_PUBLIC_URL = os.getenv('R2_PUBLIC_URL')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_REPO = os.getenv('GITHUB_REPO', 'zuhair646-debug/amen-videos')

# ═══════════════════════════════════════════════════════════
# 📚 قوائم البحث (5 أقسام)
# ═══════════════════════════════════════════════════════════

SEARCH_CATEGORIES = {
    'quran': {
        'name': 'قرآن كريم',
        'keywords': [
            'قرآن كريم',
            'تلاوة قرآن',
            'تفسير قرآن',
            'سورة البقرة',
            'سورة يس'
        ],
        'max_per_session': 3
    },
    'jafari': {
        'name': 'المذهب الجعفري',
        'keywords': [
            'عزاء حسيني',
            'مرثية الحسين',
            'محرم',
            'كربلاء',
            'مجلس عزاء'
        ],
        'max_per_session': 3
    },
    'duaa': {
        'name': 'أدعية',
        'keywords': [
            'دعاء شيعي',
            'مناجاة',
            'زيارة عاشوراء',
            'دعاء كميل',
            'أدعية أهل البيت'
        ],
        'max_per_session': 3
    },
    'stories': {
        'name': 'قصص الشيوخ',
        'keywords': [
            'قصة شيخ',
            'موعظة',
            'حكمة شيخ',
            'درس ديني',
            'قصة إسلامية'
        ],
        'max_per_session': 3
    },
    'kids': {
        'name': 'تعليمي للأطفال',
        'keywords': [
            'تعليم أطفال',
            'قصص أطفال إسلامية',
            'علوم للأطفال',
            'لغة عربية للأطفال',
            'تعليم دين للأطفال'
        ],
        'max_per_session': 3
    }
}

# ═══════════════════════════════════════════════════════════
# 🎭 Playwright: تسجيل دخول TikTok
# ═══════════════════════════════════════════════════════════

def login_tiktok(page):
    """
    تسجيل دخول TikTok (مرة واحدة، يحفظ cookies)
    """
    session_file = Path("tiktok_session.json")
    
    # لو موجود session قديم، استخدمه
    if session_file.exists():
        print("✅ استخدام session محفوظ...")
        page.context.add_cookies(json.loads(session_file.read_text()))
        return True
    
    # تسجيل دخول جديد
    print("🔐 تسجيل دخول TikTok...")
    try:
        page.goto("https://www.tiktok.com/login/phone-or-email/email")
        page.wait_for_timeout(2000)
        
        # أدخل البريد
        page.fill('input[name="username"]', TIKTOK_EMAIL)
        page.wait_for_timeout(1000)
        
        # أدخل كلمة المرور
        page.fill('input[type="password"]', TIKTOK_PASSWORD)
        page.wait_for_timeout(1000)
        
        # اضغط دخول
        page.click('button[type="submit"]')
        page.wait_for_timeout(5000)
        
        # انتظر حتى يكتمل التحميل
        page.wait_for_selector('input[placeholder*="Search"]', timeout=15000)
        
        # احفظ الـ cookies
        cookies = page.context.cookies()
        session_file.write_text(json.dumps(cookies, indent=2))
        print("✅ تم حفظ session بنجاح!")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في تسجيل الدخول: {e}")
        return False

# ═══════════════════════════════════════════════════════════
# 🔍 البحث وجمع الروابط
# ═══════════════════════════════════════════════════════════

def search_tiktok(page, keyword, max_videos=5):
    """
    يبحث عن كلمة في TikTok ويجمع روابط الفيديوهات
    """
    print(f"🔍 يبحث عن: {keyword}")
    
    try:
        # اذهب لصفحة البحث
        search_url = f"https://www.tiktok.com/search?q={keyword.replace(' ', '%20')}"
        page.goto(search_url)
        page.wait_for_timeout(3000)
        
        # سكرول بطيء لتحميل الفيديوهات
        links = set()
        for i in range(5):  # سكرول 5 مرات
            # سكرول
            page.mouse.wheel(0, random.randint(800, 1200))
            page.wait_for_timeout(random.randint(2000, 4000))  # توقف عشوائي
            
            # جمع الروابط
            video_elements = page.query_selector_all('a[href*="/video/"]')
            for elem in video_elements:
                href = elem.get_attribute('href')
                if href and '/video/' in href:
                    # استخرج الرابط الكامل
                    if href.startswith('/'):
                        href = f"https://www.tiktok.com{href}"
                    links.add(href)
            
            # لو وصلنا للحد المطلوب، توقف
            if len(links) >= max_videos:
                break
        
        result = list(links)[:max_videos]
        print(f"✅ وُجد {len(result)} فيديو لـ '{keyword}'")
        return result
        
    except Exception as e:
        print(f"❌ خطأ في البحث '{keyword}': {e}")
        return []

# ═══════════════════════════════════════════════════════════
# ⬇️ تحميل الفيديو
# ═══════════════════════════════════════════════════════════

def download_video(url):
    """
    يحمّل فيديو TikTok بـ yt-dlp
    """
    output_dir = Path("downloads")
    output_dir.mkdir(exist_ok=True)
    
    # اسم فريد من الرابط
    video_id = url.split('/video/')[-1].split('?')[0]
    output_file = output_dir / f"{video_id}.mp4"
    
    # لو محمّل مسبقاً، تخطى
    if output_file.exists():
        print(f"⏩ موجود مسبقاً: {video_id}")
        return output_file
    
    cmd = [
        'yt-dlp',
        '--format', 'best',
        '--output', str(output_file),
        '--no-playlist',
        '--quiet',
        '--no-warnings',
        url
    ]
    
    try:
        print(f"⬇️ يحمّل: {video_id}...")
        subprocess.run(cmd, check=True, timeout=180)
        
        if output_file.exists():
            size_mb = output_file.stat().st_size / (1024 * 1024)
            print(f"✅ تم التحميل ({size_mb:.1f} MB)")
            return output_file
        else:
            print(f"❌ فشل التحميل: {video_id}")
            return None
            
    except subprocess.TimeoutExpired:
        print(f"⏱️ انتهى الوقت: {video_id}")
        return None
    except Exception as e:
        print(f"❌ خطأ في التحميل: {e}")
        return None

# ═══════════════════════════════════════════════════════════
# ☁️ رفع على R2
# ═══════════════════════════════════════════════════════════

def upload_to_r2(file_path, category):
    """
    يرفع الفيديو على Cloudflare R2
    """
    try:
        s3 = boto3.client(
            's3',
            endpoint_url=R2_ENDPOINT,
            aws_access_key_id=R2_ACCESS_KEY,
            aws_secret_access_key=R2_SECRET_KEY,
            config=Config(signature_version='s3v4')
        )
        
        # مسار داخل R2
        key = f"videos/{category}/{file_path.name}"
        
        print(f"☁️ يرفع على R2: {key}...")
        s3.upload_file(
            str(file_path),
            R2_BUCKET,
            key,
            ExtraArgs={'ContentType': 'video/mp4'}
        )
        
        # رابط عام
        public_url = f"{R2_PUBLIC_URL}/{key}"
        print(f"✅ رابط عام: {public_url}")
        
        return {
            'url': public_url,
            'size': file_path.stat().st_size,
            'category': category,
            'filename': file_path.name
        }
        
    except Exception as e:
        print(f"❌ خطأ في الرفع: {e}")
        return None

# ═══════════════════════════════════════════════════════════
# 📝 تحديث الموقع
# ═══════════════════════════════════════════════════════════

def update_website(videos_data):
    """
    يحدّث index.html بالفيديوهات الجديدة
    """
    try:
        # جلب index.html الحالي
        url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/index.html"
        headers = {
            'Authorization': f'token {GITHUB_TOKEN}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"❌ خطأ في جلب index.html: {response.status_code}")
            return False
        
        file_data = response.json()
        current_html = requests.get(file_data['download_url']).text
        
        # أضف الفيديوهات الجديدة
        # (منطق بسيط: نضيف قبل </body>)
        new_videos_html = "\n<!-- 🆕 فيديوهات TikTok الجديدة -->\n"
        
        for video in videos_data:
            new_videos_html += f"""
<div class="video-card" data-category="{video['category']}">
    <video controls>
        <source src="{video['url']}" type="video/mp4">
    </video>
    <p>من TikTok - {SEARCH_CATEGORIES[video['category']]['name']}</p>
</div>
"""
        
        updated_html = current_html.replace('</body>', new_videos_html + '\n</body>')
        
        # رفع على GitHub
        import base64
        content_encoded = base64.b64encode(updated_html.encode()).decode()
        
        update_data = {
            'message': f'🤖 تحديث تلقائي: {len(videos_data)} فيديو من TikTok',
            'content': content_encoded,
            'sha': file_data['sha']
        }
        
        response = requests.put(url, headers=headers, json=update_data)
        if response.status_code == 200:
            print(f"✅ تم تحديث الموقع: {len(videos_data)} فيديو")
            return True
        else:
            print(f"❌ خطأ في التحديث: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في update_website: {e}")
        return False

# ═══════════════════════════════════════════════════════════
# 🚀 البرنامج الرئيسي
# ═══════════════════════════════════════════════════════════

def main():
    print("🚀 بدء روبوت TikTok...")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    all_videos = []
    
    with sync_playwright() as p:
        # افتح متصفح (headless=False للتطوير، True للإنتاج)
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            viewport={'width': 1920, 'height': 1080}
        )
        page = context.new_page()
        
        # تسجيل دخول
        if not login_tiktok(page):
            print("❌ فشل تسجيل الدخول!")
            browser.close()
            return
        
        # ابحث في كل قسم
        for category_id, category_data in SEARCH_CATEGORIES.items():
            print(f"\n📂 قسم: {category_data['name']}")
            
            # اختر كلمة بحث عشوائية
            keyword = random.choice(category_data['keywords'])
            
            # ابحث
            links = search_tiktok(page, keyword, max_videos=category_data['max_per_session'])
            
            # حمّل كل فيديو
            for link in links:
                video_file = download_video(link)
                if video_file:
                    # ارفع على R2
                    video_data = upload_to_r2(video_file, category_id)
                    if video_data:
                        all_videos.append(video_data)
                
                # توقف عشوائي (سلوك بشري)
                time.sleep(random.randint(3, 8))
        
        browser.close()
    
    # حدّث الموقع
    if all_videos:
        print(f"\n📝 يحدّث الموقع بـ {len(all_videos)} فيديو...")
        update_website(all_videos)
    else:
        print("\n⚠️ لم يتم تحميل أي فيديو")
    
    print(f"\n🎉 اكتمل! {len(all_videos)} فيديو")

if __name__ == '__main__':
    main()
