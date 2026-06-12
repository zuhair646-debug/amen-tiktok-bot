# 🤖 آمِن - روبوت TikTok الذكي

<div dir="rtl">

## 📖 الوصف

روبوت ذكي يجلب محتوى آمن ومناسب للعائلات من TikTok بشكل تلقائي، يحمّله، ويرفعه إلى Cloudflare R2.

### 🎯 الأقسام المدعومة:

1. **📖 قرآن كريم** - تلاوات وتفسير
2. **🕌 المذهب الجعفري** - عزاء حسيني ومجالس
3. **🤲 أدعية** - أدعية وأذكار
4. **📚 قصص الشيوخ** - مواعظ وحكم
5. **👶 تعليمي للأطفال** - محتوى آمن للأطفال

---

## 🚀 النشر على Railway

### 1️⃣ **إنشاء حساب Railway**
- اذهب إلى [railway.app](https://railway.app)
- سجّل دخول بـ GitHub

### 2️⃣ **ربط المستودع**
- اضغط **"New Project"**
- اختر **"Deploy from GitHub repo"**
- اختر `amen-tiktok-bot`

### 3️⃣ **إضافة المتغيرات البيئية**

في إعدادات المشروع → **Variables**، أضف:

```env
# TikTok (اختياري - للتحميل المباشر)
TIKTOK_EMAIL=your-email@example.com
TIKTOK_PASSWORD=your-password

# Cloudflare R2
R2_ACCESS_KEY=your-r2-access-key
R2_SECRET_KEY=your-r2-secret-key
R2_ENDPOINT=https://your-account-id.r2.cloudflarestorage.com
R2_BUCKET=amen-videos
R2_PUBLIC_URL=https://your-r2-public-domain.com

# GitHub (للنسخ الاحتياطي)
GITHUB_TOKEN=ghp_xxxxxxxxxxxxx
GITHUB_REPO=zuhair646-debug/amen-videos
```

### 4️⃣ **النشر**
- اضغط **"Deploy"**
- انتظر حتى يكتمل البناء (3-5 دقائق)
- ستحصل على رابط مثل: `https://amen-bot.up.railway.app`

---

## 🌐 API Endpoints

بعد النشر، يمكنك الوصول إلى:

### 📡 **جلب جميع الفيديوهات**
```
GET https://your-app.railway.app/api/videos
```

**مثال الاستجابة:**
```json
{
  "success": true,
  "count": 20,
  "videos": [
    {
      "id": "quran_video_001.mp4",
      "title": "quran video 001",
      "category": "quran",
      "url": "https://r2.../quran_video_001.mp4",
      "thumbnail": "https://r2.../quran_video_001.mp4?poster",
      "size": 5242880,
      "uploaded_at": "2026-06-12T15:30:00Z"
    }
  ]
}
```

### 🎯 **جلب فيديوهات حسب القسم**
```
GET https://your-app.railway.app/api/videos/quran
GET https://your-app.railway.app/api/videos/jafari
GET https://your-app.railway.app/api/videos/kids
```

### 📊 **الإحصائيات**
```
GET https://your-app.railway.app/api/stats
```

---

## 🔧 التشغيل المحلي

### 1️⃣ **المتطلبات**
```bash
python 3.11+
```

### 2️⃣ **التثبيت**
```bash
git clone https://github.com/zuhair646-debug/amen-tiktok-bot.git
cd amen-tiktok-bot
pip install -r requirements.txt
playwright install chromium
```

### 3️⃣ **الإعدادات**
```bash
cp .env.example .env
nano .env
```

### 4️⃣ **التشغيل**

**تشغيل الروبوت (مرة واحدة):**
```bash
python tiktok_bot.py
```

**تشغيل الـ API:**
```bash
python api.py
```

---

## 📝 الترخيص

MIT License - مفتوح المصدر ❤️

---

## 🤝 المساهمة

المساهمات مرحب بها! افتح issue أو pull request.

---

## 📧 التواصل

لأي استفسارات: [GitHub Issues](https://github.com/zuhair646-debug/amen-tiktok-bot/issues)

</div>
