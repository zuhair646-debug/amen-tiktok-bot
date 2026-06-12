# 🚀 تعليمات التثبيت على جهازك

## ✅ المتطلبات:

1. **Python 3.9+** → تحميل من https://www.python.org/downloads/
2. **Git** → تحميل من https://git-scm.com/downloads

---

## 📥 التثبيت (5 دقائق):

### **1️⃣ حمّل المشروع:**

```bash
git clone https://github.com/zuhair646-debug/amen-tiktok-bot.git
cd amen-tiktok-bot
```

### **2️⃣ ثبّت المكتبات:**

```bash
pip install -r requirements.txt
playwright install chromium
```

> **💡 ملاحظة:** `playwright install` يحمّل متصفح Chromium (~300 MB)

### **3️⃣ اضبط المتغيرات البيئية:**

انسخ `.env.example` إلى `.env`:

```bash
cp .env.example .env
```

**افتح `.env` وأضف بياناتك:**

```env
TIKTOK_EMAIL=zuhair770000@gmail.com
TIKTOK_PASSWORD=4566421050ZaZ**

R2_ACCESS_KEY=<من Cloudflare>
R2_SECRET_KEY=<من Cloudflare>
R2_ENDPOINT=https://xxx.r2.cloudflarestorage.com
R2_BUCKET=amen-videos
R2_PUBLIC_URL=https://pub-xxx.r2.dev

GITHUB_TOKEN=<من GitHub>
GITHUB_REPO=zuhair646-debug/amen-videos
```

### **4️⃣ شغّل الروبوت:**

```bash
python tiktok_bot.py
```

---

## 🎬 ماذا سيحدث؟

```
🔐 تسجيل دخول TikTok...
✅ تم حفظ session

📂 قسم: قرآن كريم
🔍 يبحث عن: قرآن كريم
✅ وُجد 3 فيديوهات
⬇️ يحمّل: 7234567890...
✅ تم التحميل (12.3 MB)
☁️ يرفع على R2...
✅ رابط عام: https://pub-xxx.r2.dev/videos/quran/7234567890.mp4

📂 قسم: المذهب الجعفري
🔍 يبحث عن: عزاء حسيني
...

📝 يحدّث الموقع بـ 15 فيديو...
✅ تم تحديث الموقع
🎉 اكتمل! 15 فيديو
```

**المدة:** 10-15 دقيقة.

---

## ⏰ التشغيل التلقائي (كل 6 ساعات):

### **على Windows:**

استخدم **Task Scheduler**:

1. افتح Task Scheduler
2. **Create Basic Task**
3. الاسم: `Amen TikTok Bot`
4. Trigger: **Daily** → Repeat every **6 hours**
5. Action: **Start a program**
   - Program: `python`
   - Arguments: `C:\path\to\amen-tiktok-bot\tiktok_bot.py`
6. **Finish**

### **على Mac/Linux:**

استخدم **cron**:

```bash
crontab -e
```

أضف السطر:

```
0 */6 * * * cd /path/to/amen-tiktok-bot && python tiktok_bot.py
```

(يشتغل كل 6 ساعات)

---

## 🔒 الأمان:

- ✅ الروبوت **بطيء عمداً** (2-4 ثانية بين كل فيديو)
- ✅ **سكرول عشوائي** (800-1200 بكسل)
- ✅ **حد أقصى 15 فيديو/يوم** (3 لكل قسم)
- ✅ **User-Agent حقيقي**

**لو انحظر الحساب:** سوي حساب جديد وغيّر `.env`

---

## 🛠️ التخصيص:

### **غيّر عدد الفيديوهات:**

في `tiktok_bot.py` → `SEARCH_CATEGORIES`:

```python
'max_per_session': 5  # غيّر من 3 إلى 5
```

### **أضف قسم جديد:**

```python
'dua': {
    'name': 'أدعية خاصة',
    'keywords': ['دعاء الفرج', 'دعاء الصباح'],
    'max_per_session': 2
}
```

---

## ❓ الدعم:

- 📧 افتح Issue على GitHub
- 🔗 الريبو: https://github.com/zuhair646-debug/amen-tiktok-bot

---

**بُني بـ ❤️ للعائلات العربية.**
