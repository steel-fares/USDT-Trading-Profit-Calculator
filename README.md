# USDT Trading Profit Calculator

حاسبة أرباح تداول USDT تعمل على GitHub Pages.

## المميزات
- حساب الربح تلقائيًا بدون الضغط على زر
- دعم عدة عملات
- تحليل أفضل عملة
- جلب أسعار Binance P2P من الملف المحدث تلقائيًا
- عمولة ثابتة 0.08 USDT لكل عملية
- حفظ البيانات داخل المتصفح
- نسخ النتائج

## الملفات
- `index.html`
- `scripts/fetch_p2p_prices.py`
- `.github/workflows/update-p2p.yml`

## ملاحظات
- GitHub Pages لا يشغّل Python مباشرة، لذلك يتم تشغيل Python عبر GitHub Actions.
- يتم تحديث ملف الأسعار كل 5 دقائق تقريبًا.
