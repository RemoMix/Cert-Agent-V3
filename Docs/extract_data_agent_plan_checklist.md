# Cert Agent V3 – Master Plan Checklist

> الهدف من الملف ده: يبقى **مرجع واحد** للشغل كله، نبعته في أي شات جديد علشان نكمّل من غير ما نعيد شرح.

---

## 🧭 Vision
- Agent محلي
- قراءة شهادات معملية (PDF)
- استخراج بيانات **بدقة عالية + قابلية مراجعة**
- بدون AI تخمين، كله Rules + OCR + Validation

---

## 📦 Core Pipeline (High Level)

- [x] PDF → PNG (page by page)
- [x] Image preprocessing
- [x] OCR (JSON output per page)
- [x] Independent Extract Agents
- [x] Aggregator / ExtractDataAgent
- [x] CSV Output (1 cert = 1 row)

---

## 🧠 Agents Architecture (Agreed – لا زيادة)

### 1️⃣ CertNumberExtractAgent
- [x] استخراج Certificate Number من OCR
- [x] Regex ثابت: `Dokki-xxxxxx`
- [x] غير مرتبط باسم الملف
- [x] Handling تعدد ظهور Certificate Number
- [ ] اختبارات على عينات جديدة

---

### 2️⃣ ProductNameExtractAgent
- [x] استخراج اسم المنتج من OCR
- [x] الاعتماد على Context (Sample / Sample : / Sample -)
- [x] دعم `:ProductName`
- [x] Ignore noise tokens
- [x] عدم كسر حالات شغالة (Anise / Fennel / Marjoram / Dry Mint)
- [ ] تحسين fallback باستخدام product_list.csv (اختياري – لم يُنفّذ)

---

### 3️⃣ LotNumberExtractAgent
- [x] استخراج Lot Number
- [x] دعم Single lot (139385)
- [x] دعم Multi lot (139912-139913)
- [x] عدم الخلط مع Weight أو IDs
- [ ] اختبارات إضافية على شهادات جديدة

---

### 4️⃣ LotSize / Weight Extract Agent
- [x] استخراج الوزن الكلي
- [x] دعم KG
- [x] منع قراءة Lot بدل Weight
- [x] التعامل مع أخطاء OCR (5 ↔ 6 / 9 ↔ 0)
- [ ] تحسين دقة الأرقام (جزئي)

---

### 5️⃣ AnalysisResultExtractAgent
- [x] استخراج نتائج المبيدات
- [x] دعم حالات وجود مبيدات
- [x] دعم حالة `Not Detected`
- [x] كتابة `Not Detected` صريحة
- [x] تمهيد لتصنيف Organic
- [ ] مراجعة شاملة للدقة (مؤجل)

---

## 🖼️ Image Preprocessing

- [x] Grayscale
- [x] Gaussian Blur
- [x] Adaptive Threshold
- [x] Sharpening خفيف
- [x] Stable – لا يكسر OCR
- [ ] تحسين إضافي للأرقام فقط (مؤجل)
- [ ] Auto-CLAHE للصور الباهتة (مؤجل)

---

## 🧩 ExtractDataAgent (Orchestrator)

- [x] ينادي كل Agent بشكل مستقل
- [x] لا يحتوي Logic استخراج
- [x] Aggregation فقط
- [x] Logging للنتائج
- [x] CSV final output

---

## 📄 Outputs

- [x] PNG per page
- [x] OCR JSON per page
- [x] CSV per certificate
- [x] All Certs CSV

---

## 🧪 Testing & Validation

- [x] Tests على 9 شهادات أساسية
- [x] مقارنة OCR vs CSV vs PDF
- [ ] Test set أوسع (شهادات مختلفة)
- [ ] Regression tests قبل أي تعديل

---

## 🚫 Explicitly NOT In Scope

- ❌ LLM-based guessing
- ❌ Auto correction بدون OCR evidence
- ❌ دمج Agents أو تداخل مسؤوليات
- ❌ كسر كود شغّال لحالة واحدة

---

## 🔒 Design Rules (لازم تفضل ثابتة)

- كل Agent مستقل
- أي تعديل = حالة جديدة فقط
- ممنوع تعديل يكسر حالة قديمة
- OCR هو المصدر الوحيد للحقيقة

---

## 📌 Next Steps (بعد فتح شات جديد)

- [ ] إضافة الشهادات الجديدة كـ Test Set
- [ ] تحسين الأرقام بحذر
- [ ] توثيق Known Failure Cases
- [ ] Final stabilization

---

> ✅ الملف ده هو **Baseline رسمي** لـ Cert Agent V3

