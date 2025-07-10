@echo off
echo ========================================
echo النظام الطبي الذكي المتكامل
echo Medical AI System
echo ========================================
echo.
echo تطوير: عمر أحمد فتحي & أحمد هاني النجار
echo.

REM التحقق من وجود Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python غير مثبت على النظام
    echo يرجى تثبيت Python من: https://python.org
    pause
    exit /b 1
)

echo ✅ Python مثبت بنجاح
echo.

REM التحقق من وجود pip
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip غير متاح
    echo يرجى تثبيت pip
    pause
    exit /b 1
)

echo ✅ pip متاح
echo.

REM تثبيت المتطلبات
echo 📦 تثبيت المكتبات المطلوبة...
pip install Flask Flask-CORS

if %errorlevel% neq 0 (
    echo ❌ فشل في تثبيت المكتبات
    echo جرب تشغيل الأمر كمدير
    pause
    exit /b 1
)

echo ✅ تم تثبيت المكتبات بنجاح
echo.

REM تشغيل الخادم
echo 🚀 بدء تشغيل الخادم الطبي...
echo.
echo 🌐 الخادم سيعمل على: http://localhost:5000
echo 📱 يمكنك الوصول للنظام من المتصفح
echo.
echo ⚠️  لإيقاف الخادم اضغط Ctrl+C
echo.

python medical_ai_backend.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ حدث خطأ في تشغيل الخادم
    echo تحقق من الملفات والمتطلبات
)

echo.
echo تم إيقاف الخادم
pause
