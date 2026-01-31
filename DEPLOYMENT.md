# 🚀 نشر DailyQuest على Render

## الخطوات الأساسية للنشر على Render (المجاني)

### 1. إعداد Render
```bash
# تسجيل الدخول على Render
# https://render.com
# اربط حساب GitHub الخاص بك
```

### 2. إنشاء Web Service جديد
```
1. اذهب إلى Dashboard
2. اضغط "New +" 
3. اختر "Web Service"
4. اختر repository: Rid62/DailyQuest
5. استخدم الإعدادات التالية:
```

### 3. الإعدادات الضرورية:
```
Name: dailyquest
Runtime: Python 3.10
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
```

### 4. متغيرات البيئة (Environment Variables):
```
SECRET_KEY = (سيتم إنشاؤه تلقائياً)
OPENAI_API_KEY = (أضف مفتاح OpenAI الخاص بك)
DATABASE_URL = (سيتم إنشاؤه تلقائياً من قاعدة البيانات)
```

### 5. إضافة قاعدة بيانات PostgreSQL
```
1. اضغط "Add Database"
2. اختر PostgreSQL (مجاني)
3. سيتم إنشاء DATABASE_URL تلقائياً
```

---

## ⚠️ ملاحظة هامة: SQLite → PostgreSQL

**الفرق الأساسي:**
- **SQLite**: تُفقد البيانات عند إعادة تشغيل السيرفر (غير مناسب للإنتاج)
- **PostgreSQL**: قاعدة بيانات سحابية دائمة (مثالي للإنتاج)

**التحويل يتطلب فقط:**
1. تثبيت `psycopg2` في requirements.txt ✅ (مضافة بالفعل)
2. تغيير CONNECTION STRING في app.py ✅ (يتم تلقائياً عند اكتشاف DATABASE_URL)

---

## 📱 الميزات المضافة حديثاً (Anti-Cheating):

### ✅ نظام إثبات الإنجاز:
- **Modal popup** عند الضغط على "Complete"
- **الحد الأدنى 50 حرف** لوصف الإنجاز
- **عداد أحرف** فوري
- **التحقق من الصحة** قبل منح النقاط

### ✅ البيانات المخزنة:
```python
# كل completion يتضمن:
{
    'user_id': int,
    'challenge_id': int,
    'proof': str,  # النص المكتوب بواسطة المستخدم
    'completed_at': datetime
}
```

---

## 🔧 التثبيت المحلي للاختبار:

```bash
# تثبيت المتطلبات
pip install -r requirements.txt

# إعادة تعيين قاعدة البيانات
python init_db.py

# تشغيل التطبيق
python -m flask --app app run
```

---

## 🎯 خطوات ما بعد النشر:

1. **اختبر التطبيق:**
   - https://your-app-name.onrender.com
   - قم بإنشاء حساب وتسجيل الدخول
   - اختبر إكمال تحدٍ (يجب أن يطلب إثبات)

2. **أضف مفتاح OpenAI API:**
   - في Render Dashboard → Environment
   - أضف `OPENAI_API_KEY`

3. **راقب السجلات (Logs):**
   - اذهب إلى "Logs" لرؤية أي أخطاء

---

## 📊 خطة مجانية Render (الحدود):

| الميزة | الحد |
|--------|-----|
| CPU | 0.5 |
| RAM | 512 MB |
| Storage | 100 MB |
| Uptime | Limited (ينام بعد 15 دقيقة بدون نشاط) |
| PostgreSQL | 256 MB |

**ملاحظة:** السرعة قد تكون بطيئة قليلاً في الخطة المجانية!

---

## 💰 خيارات مدفوعة (خطة Pro):
- **Render Pro**: $7/شهر للـ Web Service (بدون ينام)
- **PostgreSQL**: $7/شهر لقاعدة بيانات خاصة

---

## 🐛 استكشاف الأخطاء:

إذا حدثت مشاكل:

```bash
# تحقق من الـ Logs في Render Dashboard
# ابحث عن الأخطاء الشائعة:

1. "ModuleNotFoundError": تأكد من requirements.txt
2. "DATABASE_URL not set": أضف PostgreSQL
3. "OPENAI_API_KEY missing": أضف المفتاح في Environment
```

---

## ✨ التحديثات المستقبلية:

- [ ] نظام التحقق من الصور (Gemini Vision API)
- [ ] مشاركة الإثبات مع الأصدقاء
- [ ] نظام التصويت على الإثباتات
- [ ] تحليلات إحصائية متقدمة
