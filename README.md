# 🤖 آمِن - روبوت TikTok الذكي

## 🎯 الفكرة

**روبوت يشتغل على جهازك** يجلب فيديوهات آمنة من TikTok تلقائياً:

```
1️⃣ يسجّل دخول TikTok (كإنسان عادي)
        ↓
2️⃣ يبحث في 5 أقسام:
   • قرآن كريم
   • المذهب الجعفري (عزاء، مراثي)
   • أدعية شيعية
   • قصص شيوخ
   • تعليمي للأطفال
        ↓
3️⃣ يجمع روابط الفيديوهات (سكرول بطيء بشري)
        ↓
4️⃣ يحمّلها بـ yt-dlp
        ↓
5️⃣ يرفعها Cloudflare R2
        ↓
6️⃣ يحدّث الموقع تلقائياً
```

---

## ✅ المميزات

- 🆓 **مجاني 100%** (بدون اشتراكات API)
- 🤖 **ما ينكشف** (Playwright = متصفح حقيقي)
- 🐢 **بطيء عمداً** (3-8 ثانية بين كل فيديو)
- 🎯 **5 أقسام محددة** (قرآن، جعفري، دعاء، قصص، أطفال)
- 🔄 **يشتغل تلقائياً** (Task Scheduler / cron)
- 🔒 **آمن** (حد أقصى 15 فيديو/يوم)

---

## 🚀 التثبيت السريع (5 دقائق)

### **1️⃣ تحميل Python:**

🔗 https://www.python.org/downloads/

(✅ علّم على "Add to PATH" أثناء التثبيت)

### **2️⃣ تحميل الروبوت:**

```bash
git clone https://github.com/zuhair646-debug/amen-tiktok-bot.git
cd amen-tiktok-bot
```

(أو حمّل ZIP من GitHub → Extract)

### **3️⃣ تثبيت المكتبات:**

```bash
pip install -r requirements.txt
playwright install chromium
```

### **4️⃣ إعدادات `.env`:**

```bash
cp .env.example .env
```

**افتح `.env` بـ Notepad وأضف:**

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

### **5️⃣ تشغيل:**

```bash
python tiktok_bot.py
```

🎬 **المتصفح بيفتح تلقائياً**، بس خلّيه يشتغل.

---

## 📚 الأقسام الـ5

| القسم | كلمات البحث | الحد الأقصى |
|-------|-------------|-------------|
| **قرآن كريم** | قرآن كريم، تلاوة، تفسير، سورة البقرة، يس | 3/يوم |
| **المذهب الجعفري** | عزاء حسيني، مرثية، محرم، كربلاء، مجلس عزاء | 3/يوم |
| **أدعية** | دعاء شيعي، مناجاة، زيارة عاشوراء، دعاء كميل | 3/يوم |
| **قصص الشيوخ** | قصة شيخ، موعظة، حكمة، درس ديني | 3/يوم |
| **تعليمي للأطفال** | تعليم أطفال، قصص إسلامية، علوم، لغة عربية | 3/يوم |

**المجموع:** 15 فيديو/يوم

---

## 🔒 الحماية من الحظر

### **كيف نتجنب الكشف؟**

| الميزة | الشرح |
|--------|--------|
| ✅ **Playwright** | متصفح حقيقي (مو bot بسيط) |
| ✅ **سكرول عشوائي** | 800-1200 بكسل |
| ✅ **توقف عشوائي** | 2-4 ثانية بين كل فيديو |
| ✅ **حد أقصى** | 15 فيديو/يوم فقط |
| ✅ **User-Agent** | Chrome عادي |
| ✅ **Session محفوظ** | يسجّل دخول مرة واحدة فقط |

### **لو انحظر الحساب:**

1. سوي حساب TikTok جديد (3 دقائق)
2. غيّر `.env`:
   ```env
   TIKTOK_EMAIL=جديد@gmail.com
   TIKTOK_PASSWORD=كلمة_جديدة
   ```
3. احذف `tiktok_session.json`
4. شغّل الروبوت

**ما هو مهم** — الحساب عادي، مو مهم.

---

## ⏰ التشغيل التلقائي

### **على Windows:**

**Task Scheduler** (مدمج):

1. ابحث عن "Task Scheduler"
2. **Create Basic Task**
3. الاسم: `Amen TikTok Bot`
4. Trigger: **Daily** → **Repeat every 6 hours**
5. Action: **Start a program**
   ```
   Program: C:\Python311\python.exe
   Arguments: C:\path\to\tiktok_bot.py
   ```
6. **Finish**

### **على Mac/Linux:**

**cron** (مدمج):

```bash
crontab -e
```

أضف:

```
0 */6 * * * cd /path/to/amen-tiktok-bot && python tiktok_bot.py
```

(كل 6 ساعات)

---

## 🛠️ التخصيص

### **غيّر عدد الفيديوهات:**

في `tiktok_bot.py` → `SEARCH_CATEGORIES`:

```python
'quran': {
    ...
    'max_per_session': 5  # من 3 إلى 5
}
```

### **أضف كلمات بحث:**

```python
'keywords': [
    'قرآن كريم',
    'تلاوة',
    'سورة الملك',  # جديد
    'القرآن المجود'  # جديد
]
```

### **أضف قسم جديد:**

```python
'hadith': {
    'name': 'أحاديث نبوية',
    'keywords': ['حديث نبوي', 'أربعون نووية'],
    'max_per_session': 2
}
```

---

## 📊 السجلات

**مثال output:**

```
🚀 بدء روبوت TikTok...
⏰ 2025-01-15 14:30:00

🔐 تسجيل دخول TikTok...
✅ استخدام session محفوظ

📂 قسم: قرآن كريم
🔍 يبحث عن: تلاوة قرآن
✅ وُجد 3 فيديوهات
⬇️ يحمّل: 7234567890...
✅ تم التحميل (12.3 MB)
☁️ يرفع على R2: videos/quran/7234567890.mp4
✅ رابط عام: https://pub-xxx.r2.dev/videos/quran/7234567890.mp4

📂 قسم: المذهب الجعفري
🔍 يبحث عن: عزاء حسيني
✅ وُجد 3 فيديوهات
...

📝 يحدّث الموقع بـ 15 فيديو...
✅ تم تحديث الموقع: 15 فيديو
🎉 اكتمل! 15 فيديو
```

**المدة:** 10-15 دقيقة.

---

## 🔗 الروابط

| الرابط | الوصف |
|--------|--------|
| 🔗 [الموقع المباشر](https://zenrex.ai/s/amen-platform) | منصة آمِن |
| 📦 [الريبو](https://github.com/zuhair646-debug/amen-tiktok-bot) | الكود المصدري |
| 📖 [INSTALL.md](INSTALL.md) | تعليمات مفصّلة |

---

## 📞 الدعم

- 📧 افتح **Issue** على GitHub
- 🐙 الريبو: https://github.com/zuhair646-debug/amen-tiktok-bot

---

## 📜 الترخيص

**MIT License** — استخدمه بحرية ❤️

---

**بُني بـ ❤️ للعائلات العربية الشيعية.**

🛡️ **آمِن** - محتوى نظيف، قلوب مطمئنة.
