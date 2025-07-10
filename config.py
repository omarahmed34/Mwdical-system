"""
Configuration file for Medical Chatbot
"""

import os
from datetime import timedelta

class Config:
    """Base configuration class"""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'medical-chatbot-secret-key-2024'
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Google AI Configuration
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY') or 'AIzaSyBPs9sNSu0-4Z33TUEvHrVF6Mx1CKLj9zQ'
    GOOGLE_MODEL = os.environ.get('GOOGLE_MODEL') or 'gemini-2.5-flash-preview-05-20'
    
    # File Configuration
    MEMORY_FILE = 'memory.json'
    HISTORY_FILE = 'history.json'
    MAX_HISTORY_SIZE = 1000  # Maximum number of conversations to keep
    
    # Chat Configuration
    MAX_MESSAGE_LENGTH = 2000
    TYPING_DELAY = 1.0  # Seconds to simulate typing
    
    # Emergency Configuration
    EMERGENCY_KEYWORDS = [
        'طوارئ', 'emergency', 'نزيف', 'bleeding', 'اختناق', 'choking',
        'توقف القلب', 'cardiac arrest', 'فقدان الوعي', 'unconscious',
        'حادث', 'accident', 'سكتة', 'stroke', 'نوبة قلبية', 'heart attack',
        'تسمم', 'poisoning', 'حريق', 'fire', 'غرق', 'drowning'
    ]
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE = 30
    RATE_LIMIT_PER_HOUR = 200
    
    # Session Configuration
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # Logging Configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = 'medical_chatbot.log'
    
    # Security Configuration
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']
    
    # Medical Disclaimer
    MEDICAL_DISCLAIMER = "⚠️ ده مش تشخيص طبي، لو الأعراض مستمرة أو زادت، لازم تروح لدكتور متخصص."
    
    # System Instructions for AI
    SYSTEM_INSTRUCTION = """
أنت مساعد طبي ذكي ومتخصص. دورك هو:

🎯 **المهام الأساسية:**
- تقديم معلومات طبية دقيقة وواضحة
- الرد باللغة العربية والعامية المصرية
- تحليل الأعراض وتقديم نصائح مفيدة
- توجيه المرضى للتخصص الطبي المناسب

📋 **إرشادات الرد:**
- كن ودود ومتفهم ومطمئن
- استخدم الرموز التعبيرية المناسبة
- قسم الإجابة لنقاط واضحة
- اذكر متى يجب مراجعة الطبيب فوراً

🔍 **التحليل المطلوب:**
- حلل الأعراض المذكورة
- حدد مستوى الخطورة (خفيف/متوسط/شديد)
- اقترح الإسعافات الأولية إن أمكن
- قدم نصائح وقائية

💊 **المواضيع المتخصصة:**
- إذا سُئلت عن نظام غذائي، اسأل عن الهدف الصحي والتفضيلات
- إذا شُورك تحليل طبي، اشرح النتائج ببساطة
- إذا ذُكرت أدوية، قدم معلومات عامة فقط

⚠️ **تحذير إجباري:** أضف دائماً في نهاية كل رد:
"⚠️ هذا لا يغني عن استشارة الطبيب المختص، خاصة إذا استمرت الأعراض أو ازدادت سوءاً."

🚨 **حالات الطوارئ:** إذا كانت الأعراض خطيرة، أكد على ضرورة الذهاب للطوارئ فوراً.
"""

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    
    # Use environment variables for sensitive data in production
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # Enhanced security for production
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    GOOGLE_API_KEY = 'test-api-key'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
