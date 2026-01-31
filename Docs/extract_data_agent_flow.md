# ExtractDataAgent – Current Working Flow (Agreed Scope)

> **Scope note**  
> هذا الملف يشرح *الفلو الحقيقي الحالي* للنظام كما هو متفق عليه فعليًا، بدون أي Agents إضافية أو مستقبلية.

---

## Overall Pipeline

```
PDF
 ↓
PDF → PNG
 ↓
image_preprocess
 ↓
OCR (single pass)
 ↓
CertNumberExtractAgent
ProductNameExtractAgent
LotNumberExtractAgent
LotSizeExtractAgent
AnalysisResultExtractAgent
 ↓
Aggregator → CSV
```

- OCR يتم **مرة واحدة فقط**
- كل Agent يعمل بشكل مستقل
- لا يوجد تبادل منطق بين Agents
- أي قيمة غير مؤكدة تُترك فارغة

---

## 1. CertNumberExtractAgent

### Responsibility
استخراج **رقم الشهادة فقط**.

### Inputs
- OCR lines / tokens

### Extraction Logic
1. البحث عن الكلمات المفتاحية:
   - `Certificate`
   - `Certificate Number`
2. تثبيت Anchor:
   ```
   Certificate Number :
   ```
3. قراءة التوكن الذي يلي النقطتين مباشرة.
4. التحقق من الشكل:
   ```
   Dokki-XXXXXX
   ```

### Output
- `certificate_number` (string)
- أو قيمة فارغة إذا لم يتم التأكد.

### Explicit Non-Responsibilities
- لا يعتمد على اسم الملف
- لا يقرأ Sample ID
- لا يتعامل مع أي رقم آخر

### Design Principle
**Anchor-based extraction – no guessing**

---

## 2. ProductNameExtractAgent

### Responsibility
استخراج **اسم المنتج** كما هو مكتوب في الشهادة.

### Inputs
- OCR lines (normalized)
- line order

### Extraction Logic
1. البحث عن Anchor:
   ```
   Sample :
   ```
2. القراءة من:
   - نفس السطر
   - أو السطر الذي يليه
3. استبعاد التوكنات غير الصالحة:
   - `: ~ = . Fax Phone N/A`
4. اختيار:
   - أول كلمة alphabetic
   - أو كلمتين في حالة الاسم المركب (مثل: Dry Mint)
5. Normalization بسيط لأخطاء OCR الشائعة:
   - `Bail → Basil`

### Supported Edge Cases
- `Sample : Fennel Fax`
- `:Marjoram`
- `Sample : Dry Mint`

### Output
- `product_name` (string)

### Explicit Non-Responsibilities
- لا يستخدم product list خارجي
- لا يخمّن في حالة الغياب

### Design Principle
**Context-aware extraction, not dictionary lookup**

---

## 3. LotNumberExtractAgent

### Responsibility
استخراج **رقم اللوط** فقط.

### Inputs
- OCR lines

### Extraction Logic
1. البحث عن:
   ```
   Lot Number :
   ```
2. قراءة القيمة التي تلي الـ anchor.
3. دعم الحالات:
   - رقم واحد: `139385`
   - رقمين: `139912 / 139913`

### Output
- `lot_number` (string أو list حسب التنفيذ)

### Explicit Non-Responsibilities
- لا يستخرج وزن
- لا يقوم بتصحيح أرقام

### Design Principle
**Keyword + numeric value only**

---

## 4. LotSizeExtractAgent (Total Weight)

### Responsibility
استخراج **الوزن الكلي للشحنة**.

### Inputs
- OCR lines

### Extraction Logic
1. البحث عن:
   ```
   Total Weight
   ```
2. استخراج:
   - القيمة الرقمية
   - وحدة القياس (Kg)
3. تطبيق digit normalization (بعد OCR):
   - `I615 → 1615`
   - `857O → 8570`
4. التحقق من منطقية الوزن.
   - القيم غير المنطقية تُترك فارغة

### Output
- `total_weight_kg` (string / int)

### Known OCR Issues
- `9 ↔ 0`
- `5 ↔ 6`
- `I ↔ 1`

### Design Principle
**Numeric extraction + post-OCR cleanup**

---

## 5. AnalysisResultExtractAgent

### Responsibility
تحديد **نتيجة التحليل الكيميائي**.

### Inputs
- OCR lines (غالبًا في الجزء السفلي من الصفحة)

### Extraction Logic
1. البحث عن أي من الكلمات:
   - `Not detected`
   - `ND`
   - `<LOQ`
2. في حالة وجودها:
   - النتيجة = CLEAN
3. في حالة وجود أسماء مبيدات:
   - تسجيل الأسماء كما هي

### Output
- `analysis_status` (CLEAN / DETECTED)
- optional list of detected pesticides

### Explicit Non-Responsibilities
- لا يقارن مع MRL
- لا يقرر compliance

### Design Principle
**Presence-based logic, not calculation**

---

## 6. Aggregator / CSV Writer

### Responsibility
تجميع مخرجات كل Agents في **صف CSV واحد**.

### Inputs
- Outputs من جميع Agents:
  - Certificate Number
  - Product Name
  - Lot Number
  - Total Weight
  - Analysis Result

### Aggregation Logic
1. وضع كل قيمة في عمودها المحدد.
2. القيم غير المتاحة تبقى فارغة.
3. لا يوجد أي تعديل أو تخمين.

### Output
- CSV file (single row per certificate)

### Design Principle
**Dumb by design – aggregation only**

---

## Final Notes

- كل Agent مسؤول عن **حقل واحد فقط**
- لا يوجد Agent يصحّح أو يكمّل عمل Agent آخر
- أي تحسين أو bug fix يتم داخل Agent واحد فقط
- هذا الفصل هو سبب استقرار النظام

> هذا الملف يمثل **baseline معماري**، وأي إضافة مستقبلية يجب أن تكون صريحة ومحددة النطاق.

