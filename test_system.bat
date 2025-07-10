@echo off
title اختبار المساعد الطبي الذكي المحسن
color 0B

echo ========================================
echo    اختبار المساعد الطبي الذكي المحسن
echo    Enhanced Medical Chatbot Testing
echo ========================================
echo.

echo 🔍 جاري فحص حالة السيرفر...
timeout /t 2 >nul

echo 🧪 بدء اختبار المميزات المحسنة...
echo.

python test_enhanced_features.py

echo.
echo ========================================
echo 📋 تم الانتهاء من الاختبار
echo 
echo 💡 نصائح:
echo    • إذا فشلت الاختبارات، تأكد من تشغيل السيرفر أولاً
echo    • استخدم run_enhanced_chatbot.bat لتشغيل السيرفر
echo    • راجع ملف analytics.json للإحصائيات
echo ========================================
pause
