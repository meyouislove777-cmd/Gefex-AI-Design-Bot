# 🎨 Gefex — AI Design Bot

> **خيالك، نصممه** | AI-Powered Discord Design Generator

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![Discord.py](https://img.shields.io/badge/discord.py-2.3%2B-blueviolet)](https://discordpy.readthedocs.io/)
[![OpenAI](https://img.shields.io/badge/OpenAI-DALL--E%203-green)](https://openai.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

---

## 📌 نبذة عن المشروع

**Gefex** هو بوت ديسكورد ذكي يستخدم قوة DALL·E 3 و GPT-4 لتحويل أفكارك إلى تصاميم احترافية وصور جميلة.

✨ **المميزات:**
- 🎨 توليد صور احترافية من أوصاف عادية
- 🔄 إعادة التوليد بدون حد للأزرار
- 🎭 10 أستايلات مختلفة (gaming, luxury, anime, cyberpunk...)
- 📊 حد يومي عادل (12 صورة افتراضياً)
- 🌍 واجهة باللغة العربية بالكامل
- 🚀 ملف واحد فقط - سهل الاستخدام والتطوير

---

## 🚀 البدء السريع

### المتطلبات
- Python 3.9+
- حساب Discord Developer
- مفتاح API من OpenAI
- pip أو poetry

### التثبيت

1. **استنسخ المستودع:**
```bash
git clone https://github.com/meyouislove777-cmd/Gefex-AI-Design-Bot.git
cd Gefex-AI-Design-Bot
```

2. **ثبت المكتبات:**
```bash
pip install -r requirements.txt
```

3. **أنشئ ملف `.env`:**
```bash
cp .env.example .env
```

4. **أملأ بيانات الإعدادات:**
```env
DISCORD_TOKEN=your_bot_token
CLIENT_ID=your_client_id
OPENAI_API_KEY=your_openai_api_key
DAILY_LIMIT=12
```

5. **شغّل البوت:**
```bash
python gefex.py
```

---

## 📖 الأوامر

### الأوامر الأساسية

| الأمر | الوصف | الاستخدام |
|------|-------|----------|
| `/تخيل` | توليد صورة من وصف عام | `/تخيل أسد ذهبي في الصحراء` |
| `/لوقو` | تصميم شعار احترافي | `/لوقو الاسم:MyBrand` |
| `/بنر` | بنر للسيرفر | `/بنر وصف البنر` |
| `/بروفايل` | صورة بروفايل | `/بروفايل وصف الصورة` |
| `/بوستر` | بوستر أو إعلان | `/بوستر عنوان الإعلان` |
| `/ثَمبنيل` | صورة مصغرة (YouTube) | `/ثَمبنيل وصف الفيديو` |
| `/خلفية` | خلفية جميلة | `/خلفية وصف الخلفية` |
| `/باك` | هوية بصرية كاملة (4 صور) | `/باك الاسم:MyBrand الالوان:gold الستايل:luxury` |
| `/مساعدة` | معلومات البوت والأوامر | `/مساعدة` |

---

## 🎨 الأستايلات المتاحة

```
🎮 Gaming - قيمنق
💎 Luxury - فخم
🌈 Anime - أنمي
🌃 Cyberpunk - سايبربانك
✨ Minimal - مينيمال
🚀 Futuristic - مستقبلي
🖤 Dark - داكن
🎬 Cartoon - كرتون
📸 Realistic - واقعي
🎥 Cinematic - سينمائي
```

---

## ⚙️ الإعدادات

### متغيرات البيئة (.env)

```env
# Token البوت من Discord Developer Portal
DISCORD_TOKEN=

# Client ID من إعدادات التطبيق
CLIENT_ID=

# معرّف السيرفر (اختياري) - للمزامنة السريعة
GUILD_ID=

# مفتاح API من OpenAI
OPENAI_API_KEY=

# الحد الأقصى من الصور يومياً
DAILY_LIMIT=12
```

---

## 📊 قاعدة البيانات

البوت يستخدم ملف JSON بسيط لتخزين البيانات:

```json
{
  "usage": {
    "123456789_2026-09-12": 5
  },
  "identity": {
    "guild_123456789_987654321": {
      "name": "MyBrand",
      "colors": "gold and black",
      "style": "luxury"
    }
  }
}
```

---

## 🔧 الميزات المتقدمة

### الأزرار التفاعلية
- **إعادة التوليد (🔄)** - توليد صورة جديدة بنفس الوصف
- **رابط الصورة (🔗)** - نسخ رابط الصورة الكامل

### الحفظ التلقائي للهوية
عند استخدام `/باك`، يحفظ البوت إعداداتك لاستخدامها في الأوامر المستقبلية.

### معالجة الأخطاء الذكية
- التحقق من الحد اليومي
- رسائل خطأ واضحة
- محاولة الاتصال من جديد تلقائياً

---

## 🐛 استكشاف الأخطاء

### "❌ حط DISCORD_TOKEN و OPENAI_API_KEY في ملف .env"
- تأكد من وجود ملف `.env` في نفس مجلد `gefex.py`
- تحقق من الـ tokens والمفاتيح

### "تم تجاوز حد OpenAI مؤقتاً"
- انتظر دقيقة ثم حاول مرة أخرى
- قد تكون قد تجاوزت حد الطلبات

### "الوصف غير مناسب"
- استخدم أوصاف أكثر وضوحاً
- تجنب الكلمات المحظورة
- جرب أستايل مختلف

---

## 📝 أمثلة الاستخدام

### مثال 1: تخيل
```
/تخيل أسد ملكي برتقالي وذهبي، نمط سينمائي، جودة عالية HD
```

### مثال 2: لوقو
```
/لوقو الاسم:TechCorp الوصف:شركة تكنولوجيا حديثة الستايل:futuristic الالوان:neon blue and purple
```

### مثال 3: باك
```
/باك الاسم:MyGaming الالوان:neon purple and black الستايل:gaming وصف_اضافي:esports team identity
```

---

## 🤝 المساهمة

نرحب بمساهماتك! يمكنك:
- الإبلاغ عن الأخطاء
- اقتراح ميزات جديدة
- تحسين الأداء
- ترجمة لغات أخرى

---

## 📄 الترخيص

هذا المشروع مرخص تحت [MIT License](LICENSE)

---

## 💬 التواصل والدعم

- **المشروع:** [Gefex on GitHub](https://github.com/meyouislove777-cmd/Gefex-AI-Design-Bot)
- **المطور:** [@meyouislove777-cmd](https://github.com/meyouislove777-cmd)

---

## ⭐ إذا أعجبك المشروع

ضع نجمة ⭐ على المستودع لدعمنا!

---

**صُنع بـ ❤️ من قبل Gefex Team**

*خيالك، نصممه. 🎨🤖*
