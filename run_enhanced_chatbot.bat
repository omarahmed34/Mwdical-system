@echo off
title المساعد الطبي الذكي المحسن - Enhanced Medical Chatbot v2.0
color 0A

echo ========================================
echo    المساعد الطبي الذكي المحسن
echo    Enhanced Medical Chatbot v2.0
echo ========================================
echo.

echo [1/4] جاري فحص المتطلبات...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python غير مثبت! يرجى تثبيت Python أولاً
    echo    تحميل Python من: https://python.org
    pause
    exit /b 1
)
echo ✅ Python مثبت

echo.
echo [2/4] جاري فحص المكتبات المطلوبة...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Flask غير مثبت، جاري التثبيت...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ فشل في تثبيت المكتبات
        pause
        exit /b 1
    )
)
echo ✅ المكتبات جاهزة

echo.
echo [3/4] جاري تحضير النظام...
if not exist "analytics.json" echo [] > analytics.json
if not exist "response_cache.json" echo {} > response_cache.json
if not exist "history.json" echo [] > history.json
if not exist "memory.json" echo {} > memory.json
echo ✅ ملفات النظام جاهزة

echo.
echo [4/4] جاري تشغيل السيرفر المحسن...
echo.
echo 🚀 المساعد الطبي الذكي يعمل الآن!
echo 🌐 افتح المتصفح واذهب إلى: http://localhost:5000
echo 📱 للوصول من الهاتف: http://[IP-ADDRESS]:5000
echo.
echo ⭐ المميزات الجديدة في الإصدار 2.0:
echo    • 🧠 تحليل الأعراض الذكي
echo    • 👨‍⚕️ اقتراح الأطباء المناسبين (17 طبيب)
echo    • ⚠️  تقييم مستوى الخطورة
echo    • 💾 نظام التخزين المؤقت للأداء
echo    • 📊 تحليلات متقدمة ومراقبة
echo    • 🔍 8 تخصصات طبية متاحة
echo    • 🚨 كشف حالات الطوارئ
echo.
echo 📋 API Endpoints الجديدة:
echo    • /doctors/^<specialty^> - قائمة الأطباء
echo    • /doctors/recommend - اقتراح أطباء
echo    • /analytics - إحصائيات النظام
echo    • /specialties - التخصصات المتاحة
echo    • /health - حالة النظام
echo.
echo 🛑 لإيقاف السيرفر: اضغط Ctrl+C
echo ========================================
echo.

python app.py

echo.
echo 👋 تم إيقاف السيرفر المحسن
echo 📊 تحقق من ملف analytics.json للإحصائيات
pause
