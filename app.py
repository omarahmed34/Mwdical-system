from flask import Flask, request, jsonify, send_from_directory
import os
import json
import logging
from google import genai
from google.genai import types
from datetime import datetime, timedelta
from config import config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Load configuration
config_name = os.environ.get('FLASK_CONFIG', 'default')
app.config.from_object(config[config_name])

# Configuration variables
MEMORY_FILE = app.config['MEMORY_FILE']
HISTORY_FILE = app.config['HISTORY_FILE']
API_KEY = app.config['GOOGLE_API_KEY']

# Doctors database
DOCTORS_DATA = {
    'cardiology': [
        {'id': 1, 'name': 'د. أحمد محمد', 'rating': 4.8, 'experience': 15, 'price': 300, 'availability': 'متاح اليوم', 'specialties': ['أمراض القلب', 'قسطرة القلب', 'جراحة القلب']},
        {'id': 2, 'name': 'د. فاطمة علي', 'rating': 4.9, 'experience': 12, 'price': 350, 'availability': 'متاح غداً', 'specialties': ['أمراض القلب', 'ضغط الدم', 'عدم انتظام ضربات القلب']},
        {'id': 3, 'name': 'د. محمد حسن', 'rating': 4.7, 'experience': 18, 'price': 400, 'availability': 'متاح اليوم', 'specialties': ['أمراض القلب', 'قصور القلب', 'الذبحة الصدرية']}
    ],
    'neurology': [
        {'id': 4, 'name': 'د. سارة أحمد', 'rating': 4.9, 'experience': 20, 'price': 450, 'availability': 'متاح غداً', 'specialties': ['أمراض الأعصاب', 'الصرع', 'الصداع النصفي']},
        {'id': 5, 'name': 'د. عمر محمود', 'rating': 4.6, 'experience': 14, 'price': 380, 'availability': 'متاح اليوم', 'specialties': ['أمراض الأعصاب', 'السكتة الدماغية', 'الزهايمر']}
    ],
    'orthopedics': [
        {'id': 6, 'name': 'د. ليلى حسام', 'rating': 4.8, 'experience': 16, 'price': 320, 'availability': 'متاح اليوم', 'specialties': ['العظام', 'إصابات الملاعب', 'جراحة العمود الفقري']},
        {'id': 7, 'name': 'د. كريم فؤاد', 'rating': 4.7, 'experience': 11, 'price': 280, 'availability': 'متاح غداً', 'specialties': ['العظام', 'كسور العظام', 'التهاب المفاصل']}
    ],
    'dermatology': [
        {'id': 8, 'name': 'د. نور الهدى', 'rating': 4.9, 'experience': 13, 'price': 250, 'availability': 'متاح اليوم', 'specialties': ['الجلدية', 'الأكزيما', 'حب الشباب']},
        {'id': 9, 'name': 'د. حسام الدين', 'rating': 4.5, 'experience': 9, 'price': 220, 'availability': 'متاح غداً', 'specialties': ['الجلدية', 'الصدفية', 'الفطريات']}
    ],
    'pediatrics': [
        {'id': 10, 'name': 'د. منى سالم', 'rating': 4.8, 'experience': 17, 'price': 200, 'availability': 'متاح اليوم', 'specialties': ['طب الأطفال', 'التطعيمات', 'نمو الأطفال']},
        {'id': 11, 'name': 'د. يوسف عادل', 'rating': 4.6, 'experience': 8, 'price': 180, 'availability': 'متاح غداً', 'specialties': ['طب الأطفال', 'أمراض الجهاز التنفسي', 'الحساسية']}
    ],
    'general': [
        {'id': 12, 'name': 'د. رانيا طارق', 'rating': 4.7, 'experience': 10, 'price': 150, 'availability': 'متاح اليوم', 'specialties': ['طب عام', 'الفحص الشامل', 'الأمراض المزمنة']},
        {'id': 13, 'name': 'د. خالد نبيل', 'rating': 4.4, 'experience': 7, 'price': 120, 'availability': 'متاح غداً', 'specialties': ['طب عام', 'السكري', 'ضغط الدم']}
    ],
    'gastroenterology': [
        {'id': 14, 'name': 'د. هالة محمد', 'rating': 4.8, 'experience': 14, 'price': 350, 'availability': 'متاح اليوم', 'specialties': ['الجهاز الهضمي', 'القولون', 'قرحة المعدة']},
        {'id': 15, 'name': 'د. طارق سعد', 'rating': 4.6, 'experience': 12, 'price': 300, 'availability': 'متاح غداً', 'specialties': ['الجهاز الهضمي', 'الكبد', 'المرارة']}
    ],
    'psychiatry': [
        {'id': 16, 'name': 'د. ياسمين أحمد', 'rating': 4.9, 'experience': 15, 'price': 400, 'availability': 'متاح اليوم', 'specialties': ['الطب النفسي', 'الاكتئاب', 'القلق']},
        {'id': 17, 'name': 'د. محمود علي', 'rating': 4.7, 'experience': 18, 'price': 450, 'availability': 'متاح غداً', 'specialties': ['الطب النفسي', 'اضطرابات النوم', 'الوسواس القهري']}
    ]
}

# Symptom to specialty mapping
SYMPTOM_SPECIALTY_MAP = {
    'صداع': ['neurology', 'general'],
    'دوخة': ['neurology', 'cardiology', 'general'],
    'ألم صدر': ['cardiology', 'general'],
    'خفقان': ['cardiology', 'general'],
    'ضيق تنفس': ['cardiology', 'general'],
    'ألم بطن': ['gastroenterology', 'general'],
    'غثيان': ['gastroenterology', 'general'],
    'إسهال': ['gastroenterology', 'general'],
    'إمساك': ['gastroenterology', 'general'],
    'ألم ظهر': ['orthopedics', 'general'],
    'ألم مفاصل': ['orthopedics', 'general'],
    'طفح جلدي': ['dermatology', 'general'],
    'حكة': ['dermatology', 'general'],
    'حمى': ['general', 'pediatrics'],
    'سعال': ['general', 'pediatrics'],
    'قلق': ['psychiatry', 'general'],
    'اكتئاب': ['psychiatry', 'general'],
    'أرق': ['psychiatry', 'neurology', 'general'],
    'نسيان': ['neurology', 'psychiatry', 'general']
}

# Emotional triggers
emotional_triggers = [
    "مرعوب", "خايف", "قلقان", "متوتر", "هموت", "بحس بضيق", 
    "زعلان", "حزين", "مخنوق", "مجنون", "حاسس بضيق"
]

# First aid guides
first_aid_guides = {
    "حروق": "🔥 في حالة الحروق:\n1. بعدّي المياه الباردة على مكان الحرق لمدة 10 دقايق.\n2. متحطش ثلج أو معجون أسنان.\n3. لو الحرق شديد أو فيه فقاعات، لازم تروح طوارئ.\n\n⚠️ ده مش تشخيص طبي، لو الأعراض مستمرة أو زادت، لازم تروح لدكتور متخصص.",
    "غرق": "🌊 في حالة الغرق:\n1. طلع الشخص من المية فورًا.\n2. لو مش بيتنفس، ابتدي **الإنعاش القلبي الرئوي (CPR)**.\n3. كلم الإسعاف فورًا.\n\n⚠️ ده مش تشخيص طبي، لو الأعراض مستمرة أو زادت، لازم تروح لدكتور متخصص.",
    "إغماء": "😵 في حالة الإغماء:\n1. مدد الشخص على الأرض.\n2. ارفع رجله شوية.\n3. لو ما فاقش خلال دقيقة، اتصل بالإسعاف.\n\n⚠️ ده مش تشخيص طبي، لو الأعراض مستمرة أو زادت، لازم تروح لدكتور متخصص.",
    "اختناق": "😮‍💨 في حالة الاختناق:\n1. اسأل الشخص لو يقدر يتكلم أو يسعل.\n2. لو مش قادر، ابتدي **مناورة هيمليخ**.\n3. لو فقد الوعي، ابتدي **الإنعاش القلبي الرئوي (CPR)** واتصل بالإسعاف.\n\n⚠️ ده مش تشخيص طبي، لو الأعراض مستمرة أو زادت، لازم تروح لدكتور متخصص.",
    "جروح": "🩸 في حالة الجروح:\n1. نظّف الجرح بمياه جارية.\n2. حط شاش معقم واضغط عليه.\n3. لو الجرح عميق أو بينزف كتير، لازم تروح طوارئ.\n\n⚠️ ده مش تشخيص طبي، لو الأعراض مستمرة أو زادت، لازم تروح لدكتور متخصص.",
    "تسمم": "☠️ في حالة التسمم:\n1. متحاولش تخلي الشخص يرجع.\n2. اتصل بمركز السموم فورًا.\n3. اعرف نوع المادة اللي اتسمم منها لو أمكن.\n\n⚠️ ده مش تشخيص طبي، لو الأعراض مستمرة أو زادت، لازم تروح لدكتور متخصص.",
    "صرع": "⚡ في حالة نوبة صرع:\n1. ابعد أي حاجة ممكن تأذيه.\n2. متقيدهوش، وسيبه لحد ما النوبة تخلص.\n3. لو النوبة استمرت أكتر من ٥ دقايق، اتصل بالإسعاف.\n\n⚠️ ده مش تشخيص طبي، لو الأعراض مستمرة أو زادت، لازم تروح لدكتور متخصص.",
    "ضربات الرأس": "🧠 في حالة ضربة رأس:\n1. راقب الشخص لو فيه قيء، فقدان وعي، أو صداع شديد.\n2. لو فيه أي من دول، لازم يروح طوارئ.\n3. متديهش أدوية بدون استشارة طبيب.\n\n⚠️ ده مش تشخيص طبي، لو الأعراض مستمرة أو زادت، لازم تروح لدكتور متخصص.",
    "cpr": "❤️ إزاي تعمل الإنعاش القلبي الرئوي (CPR):\n1. تأكد إن المكان آمن، وان الشخص مش بيتنفس أو مش بيستجيب.\n2. اطلب المساعدة فورًا (اتصل بالإسعاف).\n3. حط إيد على إيد في نص صدر الشخص.\n4. اضغط بقوة وسرعة (حوالي 100-120 ضغطة في الدقيقة) بعمق 5-6 سم.\n5. بعد كل 30 ضغطة، ممكن تعمل نفسين إنقاذ لو مدرب على كده، أو استمر في الضغطات بس.\n6. استمر لحد ما يوصل الإسعاف أو الشخص يستجيب.\n\n⚠️ ده شرح مبسط ومبيغنيش عن التدريب العملي على الـ CPR.",
    "مناورة هيمليخ": "👐 إزاي تعمل مناورة هيمليخ (لشخص واعي بيختنق):\n1. اقف ورا الشخص، وحاوط وسطه بإيديك.\n2. حط قبضة إيدك فوق سرة الشخص بشوية، وإيدك التانية فوقها.\n3. اضغط بقوة وسرعة للداخل وللأعلى في نفس الوقت، زي ما تكون عايز ترفع الشخص.\n4. كرر الضغطات دي لحد ما الجسم الغريب يطلع أو الشخص يفقد الوعي.\n5. لو فقد الوعي، مدد الشخص على الأرض وابتدي CPR.\n\n⚠️ ده شرح مبسط ومبيغنيش عن التدريب العملي على الإسعافات الأولية."
}

def analyze_symptoms(text):
    """Analyze symptoms in text and return relevant specialties"""
    text_lower = text.lower()
    relevant_specialties = set()
    detected_symptoms = []

    for symptom, specialties in SYMPTOM_SPECIALTY_MAP.items():
        if symptom in text_lower:
            detected_symptoms.append(symptom)
            relevant_specialties.update(specialties)

    return list(relevant_specialties), detected_symptoms

def get_doctor_recommendations(specialties, limit=3):
    """Get doctor recommendations based on specialties"""
    recommendations = []

    for specialty in specialties:
        if specialty in DOCTORS_DATA:
            doctors = DOCTORS_DATA[specialty]
            # Sort by rating and availability
            sorted_doctors = sorted(doctors, key=lambda x: (x['rating'], x['availability'] == 'متاح اليوم'), reverse=True)
            recommendations.extend(sorted_doctors[:2])  # Top 2 from each specialty

    # Remove duplicates and limit results
    seen_ids = set()
    unique_recommendations = []
    for doctor in recommendations:
        if doctor['id'] not in seen_ids:
            unique_recommendations.append(doctor)
            seen_ids.add(doctor['id'])

    return unique_recommendations[:limit]

def format_doctor_recommendation(doctors, symptoms):
    """Format doctor recommendations as a response"""
    if not doctors:
        return ""

    response = f"\n\n👨‍⚕️ **اقتراحات أطباء بناءً على الأعراض:**\n"

    if symptoms:
        response += f"**الأعراض المكتشفة:** {', '.join(symptoms)}\n\n"

    for i, doctor in enumerate(doctors, 1):
        availability_icon = "🟢" if doctor['availability'] == 'متاح اليوم' else "🟡"
        response += f"**{i}. {doctor['name']}**\n"
        response += f"   • التقييم: {'⭐' * int(doctor['rating'])} ({doctor['rating']})\n"
        response += f"   • الخبرة: {doctor['experience']} سنة\n"
        response += f"   • السعر: {doctor['price']} جنيه\n"
        response += f"   • التوفر: {availability_icon} {doctor['availability']}\n"
        response += f"   • التخصصات: {', '.join(doctor['specialties'][:2])}\n\n"

    response += "💡 **لحجز موعد:** اذهب لصفحة حجز المواعيد واختر التخصص المناسب.\n"
    response += "🔗 **رابط الحجز:** [احجز موعدك الآن](appointments.html)"

    return response

def handle_first_aid(text):
    """Check if the text contains first aid keywords and return appropriate guide"""
    text_lower = text.lower()
    for keyword, guide in first_aid_guides.items():
        if keyword in text_lower:
            return guide
    return None

def is_arabic(text):
    """Check if text contains Arabic characters"""
    for ch in text:
        if '\u0600' <= ch <= '\u06FF' or '\u0750' <= ch <= '\u077F':
            return True
    return False

def save_last_question(question):
    """Save the last question to memory file"""
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump({"last_question": question}, f, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Error saving last question: {e}")

def load_last_question():
    """Load the last question from memory file"""
    try:
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("last_question", "")
    except Exception as e:
        logger.error(f"Error loading last question: {e}")
    return ""

def log_conversation(question, answer):
    """Log conversation to history file"""
    try:
        data = []
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        
        data.append({
            "q": question, 
            "a": answer,
            "timestamp": datetime.now().isoformat()
        })
        
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Error logging conversation: {e}")

def is_emotional(text):
    """Check if text contains emotional triggers"""
    text_lower = text.lower()
    return any(trigger in text_lower for trigger in emotional_triggers)

def get_severity_level(text):
    """Determine severity level of symptoms"""
    text_lower = text.lower()

    # High severity indicators
    high_severity = ['شديد', 'قوي', 'مؤلم جداً', 'لا أستطيع', 'طوارئ', 'نزيف', 'فقدان وعي', 'صعوبة تنفس']
    medium_severity = ['متوسط', 'مؤلم', 'مزعج', 'يؤثر على', 'صعوبة في']
    low_severity = ['خفيف', 'بسيط', 'أحياناً', 'قليل', 'نادراً']

    if any(indicator in text_lower for indicator in high_severity):
        return 'high'
    elif any(indicator in text_lower for indicator in medium_severity):
        return 'medium'
    elif any(indicator in text_lower for indicator in low_severity):
        return 'low'
    else:
        return 'medium'  # Default

def get_urgency_message(severity):
    """Get urgency message based on severity"""
    if severity == 'high':
        return "🚨 **تحذير:** الأعراض تبدو شديدة. يُنصح بمراجعة الطبيب فوراً أو الذهاب للطوارئ."
    elif severity == 'medium':
        return "⚠️ **تنبيه:** يُنصح بمراجعة الطبيب في أقرب وقت ممكن."
    else:
        return "💡 **نصيحة:** يمكن مراجعة الطبيب عند الحاجة أو للاطمئنان."

def enhance_ai_prompt(user_input, symptoms, severity):
    """Enhance AI prompt with context"""
    enhanced_prompt = f"""
المريض يشكو من: {user_input}

الأعراض المكتشفة: {', '.join(symptoms) if symptoms else 'غير محددة'}
مستوى الخطورة: {severity}

يرجى تقديم:
1. تحليل مبدئي للأعراض
2. نصائح للتعامل الفوري
3. متى يجب مراجعة الطبيب
4. نصائح وقائية

تذكر: هذا لا يغني عن استشارة الطبيب المختص.
"""
    return enhanced_prompt

def filter_medical_question(text):
    """Enhanced medical question filter"""
    text_lower = text.lower()

    # Non-medical keywords
    non_medical_keywords = ["سياسة", "رياضة", "فيلم", "موسيقى", "برمجة", "تعليم", "ترفيه", "طبخ", "سفر"]

    # Medical keywords
    medical_keywords = ["ألم", "وجع", "مرض", "دواء", "طبيب", "مستشفى", "أعراض", "صحة", "علاج", "فحص", "تحليل"]

    # Check for non-medical content
    if any(word in text_lower for word in non_medical_keywords):
        return False

    # Check for medical content
    if any(word in text_lower for word in medical_keywords):
        return True

    # Check for symptoms
    if any(symptom in text_lower for symptom in SYMPTOM_SPECIALTY_MAP.keys()):
        return True

    # Default to medical if uncertain
    return True

def cache_response(user_input, response):
    """Cache responses for better performance"""
    try:
        cache_file = 'response_cache.json'
        cache = {}

        if os.path.exists(cache_file):
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache = json.load(f)

        # Simple hash for caching
        input_hash = str(hash(user_input.lower().strip()))
        cache[input_hash] = {
            'response': response,
            'timestamp': datetime.now().isoformat()
        }

        # Keep only recent entries (last 1000)
        if len(cache) > 1000:
            sorted_cache = sorted(cache.items(), key=lambda x: x[1]['timestamp'], reverse=True)
            cache = dict(sorted_cache[:1000])

        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Error caching response: {e}")

def get_cached_response(user_input):
    """Get cached response if available"""
    try:
        cache_file = 'response_cache.json'
        if not os.path.exists(cache_file):
            return None

        with open(cache_file, 'r', encoding='utf-8') as f:
            cache = json.load(f)

        input_hash = str(hash(user_input.lower().strip()))
        if input_hash in cache:
            cached_entry = cache[input_hash]
            # Check if cache is not too old (24 hours)
            cached_time = datetime.fromisoformat(cached_entry['timestamp'])
            if datetime.now() - cached_time < timedelta(hours=24):
                return cached_entry['response']

        return None
    except Exception as e:
        logger.error(f"Error getting cached response: {e}")
        return None

def log_analytics(conversation_data):
    """Log detailed analytics for performance monitoring"""
    try:
        analytics_file = 'analytics.json'
        analytics = []

        if os.path.exists(analytics_file):
            with open(analytics_file, 'r', encoding='utf-8') as f:
                analytics = json.load(f)

        analytics.append(conversation_data)

        # Keep only recent entries (last 5000)
        if len(analytics) > 5000:
            analytics = analytics[-5000:]

        with open(analytics_file, 'w', encoding='utf-8') as f:
            json.dump(analytics, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Error logging analytics: {e}")

def get_analytics_summary():
    """Get analytics summary"""
    try:
        analytics_file = 'analytics.json'
        if not os.path.exists(analytics_file):
            return {}

        with open(analytics_file, 'r', encoding='utf-8') as f:
            analytics = json.load(f)

        # Calculate statistics
        total_conversations = len(analytics)
        symptom_frequency = {}
        severity_distribution = {'high': 0, 'medium': 0, 'low': 0}
        specialty_requests = {}

        for entry in analytics:
            # Count symptoms
            for symptom in entry.get('symptoms', []):
                symptom_frequency[symptom] = symptom_frequency.get(symptom, 0) + 1

            # Count severity
            severity = entry.get('severity', 'medium')
            severity_distribution[severity] = severity_distribution.get(severity, 0) + 1

            # Count specialties
            for specialty in entry.get('specialties', []):
                specialty_requests[specialty] = specialty_requests.get(specialty, 0) + 1

        return {
            'total_conversations': total_conversations,
            'most_common_symptoms': sorted(symptom_frequency.items(), key=lambda x: x[1], reverse=True)[:10],
            'severity_distribution': severity_distribution,
            'most_requested_specialties': sorted(specialty_requests.items(), key=lambda x: x[1], reverse=True)[:10]
        }
    except Exception as e:
        logger.error(f"Error getting analytics summary: {e}")
        return {}

def get_ai_response(user_input, symptoms=None, severity='medium'):
    """Enhanced AI response with context"""
    try:
        # Check cache first
        cached_response = get_cached_response(user_input)
        if cached_response:
            logger.info("Using cached response")
            return cached_response

        client = genai.Client(api_key=API_KEY)
        model = app.config['GOOGLE_MODEL']

        # Enhance prompt with context
        enhanced_input = enhance_ai_prompt(user_input, symptoms or [], severity)

        generate_content_config = types.GenerateContentConfig(
            safety_settings=[
                types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_ONLY_HIGH"),
                types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_ONLY_HIGH"),
                types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="BLOCK_ONLY_HIGH"),
                types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_ONLY_HIGH"),
            ],
            response_mime_type="text/plain",
            system_instruction=[
                types.Part.from_text(text=app.config['SYSTEM_INSTRUCTION']),
            ],
        )

        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=enhanced_input),
                ],
            ),
        ]

        response = client.models.generate_content(
            model=model,
            contents=contents,
            config=generate_content_config,
        )

        ai_response = response.text

        # Cache the response
        cache_response(user_input, ai_response)

        return ai_response

    except Exception as e:
        logger.error(f"Error getting AI response: {e}")
        return "عذراً، حدث خطأ في الحصول على الرد. يرجى المحاولة مرة أخرى."

@app.route('/')
def index():
    """Serve the main HTML page"""
    try:
        with open('diagnosis.html', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "HTML file not found", 404

@app.route('/favicon.ico')
def favicon():
    """Serve favicon"""
    return send_from_directory('.', 'favicon.svg', mimetype='image/svg+xml')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory('.', filename)

@app.route('/chat', methods=['POST'])
def chat():
    """Enhanced chat handler with symptom analysis and doctor recommendations"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()

        if not user_message:
            return jsonify({'error': 'Empty message'}), 400

        # Check if it's a medical question
        if not filter_medical_question(user_message):
            response = "⚠️ عذرًا، يبدو أن سؤالك غير طبي. أنا متخصص في الأسئلة الطبية والصحية. يمكنك سؤالي عن الأعراض، الأدوية، أو أي استفسارات صحية."
            return jsonify({'response': response})

        # Analyze symptoms and severity
        relevant_specialties, detected_symptoms = analyze_symptoms(user_message)
        severity = get_severity_level(user_message)

        # Check for emotional content
        emotional_response = ""
        if is_emotional(user_message):
            emotional_response = "🤗 أفهم أنك قلقان، وهذا طبيعي. دعني أساعدك بأفضل ما أستطيع.\n\n"

        # Check for first aid keywords
        first_aid_response = handle_first_aid(user_message)
        if first_aid_response:
            response = emotional_response + first_aid_response
        else:
            # Get enhanced AI response
            ai_response = get_ai_response(user_message, detected_symptoms, severity)
            response = emotional_response + ai_response

            # Add urgency message based on severity
            urgency_message = get_urgency_message(severity)
            response += f"\n\n{urgency_message}"

            # Add doctor recommendations if symptoms detected
            if detected_symptoms and relevant_specialties:
                recommended_doctors = get_doctor_recommendations(relevant_specialties)
                if recommended_doctors:
                    doctor_recommendations = format_doctor_recommendation(recommended_doctors, detected_symptoms)
                    response += doctor_recommendations

        # Save conversation with metadata
        conversation_data = {
            'question': user_message,
            'response': response,
            'symptoms': detected_symptoms,
            'severity': severity,
            'specialties': relevant_specialties,
            'timestamp': datetime.now().isoformat()
        }

        save_last_question(user_message)
        log_conversation(user_message, response)

        # Log detailed analytics
        log_analytics(conversation_data)

        return jsonify({
            'response': response,
            'symptoms': detected_symptoms,
            'severity': severity,
            'recommended_specialties': relevant_specialties
        })

    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        return jsonify({'error': 'حدث خطأ في النظام. يرجى المحاولة مرة أخرى.'}), 500

@app.route('/history')
def get_history():
    """Get chat history"""
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            return jsonify({'history': data})
        else:
            return jsonify({'history': []})
    except Exception as e:
        logger.error(f"Error getting history: {e}")
        return jsonify({'error': 'Error retrieving history'}), 500

@app.route('/clear-history', methods=['POST'])
def clear_history():
    """Clear chat history"""
    try:
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)
        if os.path.exists(MEMORY_FILE):
            os.remove(MEMORY_FILE)
        return jsonify({'success': True})
    except Exception as e:
        logger.error(f"Error clearing history: {e}")
        return jsonify({'error': 'Error clearing history'}), 500

@app.route('/doctors/<specialty>')
def get_doctors_by_specialty(specialty):
    """Get doctors by specialty"""
    try:
        if specialty not in DOCTORS_DATA:
            return jsonify({'error': 'Specialty not found'}), 404

        doctors = DOCTORS_DATA[specialty]
        return jsonify({'doctors': doctors, 'specialty': specialty})
    except Exception as e:
        logger.error(f"Error getting doctors: {e}")
        return jsonify({'error': 'Error retrieving doctors'}), 500

@app.route('/doctors/recommend', methods=['POST'])
def recommend_doctors():
    """Recommend doctors based on symptoms"""
    try:
        data = request.get_json()
        symptoms_text = data.get('symptoms', '').strip()

        if not symptoms_text:
            return jsonify({'error': 'No symptoms provided'}), 400

        relevant_specialties, detected_symptoms = analyze_symptoms(symptoms_text)
        recommended_doctors = get_doctor_recommendations(relevant_specialties)

        return jsonify({
            'recommended_doctors': recommended_doctors,
            'detected_symptoms': detected_symptoms,
            'relevant_specialties': relevant_specialties
        })
    except Exception as e:
        logger.error(f"Error recommending doctors: {e}")
        return jsonify({'error': 'Error getting recommendations'}), 500

@app.route('/analytics')
def get_analytics():
    """Get system analytics"""
    try:
        summary = get_analytics_summary()
        return jsonify(summary)
    except Exception as e:
        logger.error(f"Error getting analytics: {e}")
        return jsonify({'error': 'Error retrieving analytics'}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '2.0.0',
        'features': [
            'symptom_analysis',
            'doctor_recommendations',
            'severity_assessment',
            'response_caching',
            'analytics'
        ]
    })

@app.route('/specialties')
def get_specialties():
    """Get all available specialties"""
    try:
        specialties = []
        for specialty, doctors in DOCTORS_DATA.items():
            specialties.append({
                'id': specialty,
                'name': {
                    'cardiology': 'أمراض القلب',
                    'neurology': 'أمراض الأعصاب',
                    'orthopedics': 'العظام',
                    'dermatology': 'الجلدية',
                    'pediatrics': 'طب الأطفال',
                    'general': 'طب عام',
                    'gastroenterology': 'الجهاز الهضمي',
                    'psychiatry': 'الطب النفسي'
                }.get(specialty, specialty),
                'doctor_count': len(doctors),
                'available_today': len([d for d in doctors if d['availability'] == 'متاح اليوم'])
            })

        return jsonify({'specialties': specialties})
    except Exception as e:
        logger.error(f"Error getting specialties: {e}")
        return jsonify({'error': 'Error retrieving specialties'}), 500

if __name__ == '__main__':
    # Create necessary directories and files
    os.makedirs('static', exist_ok=True)

    # Initialize analytics file if not exists
    if not os.path.exists('analytics.json'):
        with open('analytics.json', 'w', encoding='utf-8') as f:
            json.dump([], f)

    # Initialize cache file if not exists
    if not os.path.exists('response_cache.json'):
        with open('response_cache.json', 'w', encoding='utf-8') as f:
            json.dump({}, f)

    logger.info("🚀 Medical Chatbot Server Starting...")
    logger.info("✅ Enhanced features enabled:")
    logger.info("   - Symptom Analysis")
    logger.info("   - Doctor Recommendations")
    logger.info("   - Severity Assessment")
    logger.info("   - Response Caching")
    logger.info("   - Analytics Tracking")
    logger.info("   - Performance Monitoring")

    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
