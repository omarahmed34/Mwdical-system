#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار المميزات المحسنة للمساعد الطبي الذكي
Enhanced Medical Chatbot Features Test
"""

import requests
import json
import time
from datetime import datetime

# إعدادات الاختبار
BASE_URL = "http://localhost:5000"
TEST_SYMPTOMS = [
    "عندي صداع شديد ودوخة",
    "ألم في الصدر وضيق تنفس",
    "ألم في البطن وغثيان",
    "طفح جلدي وحكة",
    "قلق واكتئاب وأرق",
    "ألم في الظهر والمفاصل"
]

def test_health_endpoint():
    """اختبار endpoint الصحة"""
    print("🔍 اختبار حالة النظام...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ النظام يعمل - الإصدار: {data.get('version', 'غير محدد')}")
            print(f"📋 المميزات: {', '.join(data.get('features', []))}")
            return True
        else:
            print(f"❌ خطأ في الاتصال: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ خطأ في الاتصال: {e}")
        return False

def test_specialties_endpoint():
    """اختبار endpoint التخصصات"""
    print("\n🏥 اختبار التخصصات المتاحة...")
    try:
        response = requests.get(f"{BASE_URL}/specialties")
        if response.status_code == 200:
            data = response.json()
            specialties = data.get('specialties', [])
            print(f"✅ عدد التخصصات: {len(specialties)}")
            for spec in specialties[:3]:  # عرض أول 3 تخصصات
                print(f"   • {spec['name']}: {spec['doctor_count']} أطباء")
            return True
        else:
            print(f"❌ خطأ: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ خطأ: {e}")
        return False

def test_doctor_recommendations():
    """اختبار اقتراح الأطباء"""
    print("\n👨‍⚕️ اختبار اقتراح الأطباء...")
    test_symptoms = "عندي صداع شديد ودوخة"
    
    try:
        response = requests.post(f"{BASE_URL}/doctors/recommend", 
                               json={"symptoms": test_symptoms})
        if response.status_code == 200:
            data = response.json()
            doctors = data.get('recommended_doctors', [])
            symptoms = data.get('detected_symptoms', [])
            specialties = data.get('relevant_specialties', [])
            
            print(f"✅ الأعراض المكتشفة: {', '.join(symptoms)}")
            print(f"✅ التخصصات المقترحة: {', '.join(specialties)}")
            print(f"✅ عدد الأطباء المقترحين: {len(doctors)}")
            
            if doctors:
                doctor = doctors[0]
                print(f"   🥇 أفضل طبيب: {doctor['name']} - تقييم {doctor['rating']}")
            
            return True
        else:
            print(f"❌ خطأ: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ خطأ: {e}")
        return False

def test_chat_enhancement():
    """اختبار تحسينات الشات"""
    print("\n💬 اختبار تحسينات الشات...")
    
    for i, symptom in enumerate(TEST_SYMPTOMS[:3], 1):
        print(f"\n[{i}/3] اختبار: {symptom}")
        try:
            response = requests.post(f"{BASE_URL}/chat", 
                                   json={"message": symptom})
            if response.status_code == 200:
                data = response.json()
                
                # فحص البيانات المحسنة
                symptoms = data.get('symptoms', [])
                severity = data.get('severity', 'غير محدد')
                specialties = data.get('recommended_specialties', [])
                
                print(f"   ✅ الأعراض: {symptoms}")
                print(f"   ⚠️  الخطورة: {severity}")
                print(f"   🏥 التخصصات: {specialties}")
                
                # فحص طول الرد
                response_text = data.get('response', '')
                if len(response_text) > 100:
                    print(f"   📝 رد مفصل ({len(response_text)} حرف)")
                else:
                    print(f"   📝 رد مختصر ({len(response_text)} حرف)")
                    
            else:
                print(f"   ❌ خطأ: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ خطأ: {e}")
        
        time.sleep(1)  # توقف قصير بين الطلبات

def test_analytics():
    """اختبار التحليلات"""
    print("\n📊 اختبار التحليلات...")
    try:
        response = requests.get(f"{BASE_URL}/analytics")
        if response.status_code == 200:
            data = response.json()
            
            total = data.get('total_conversations', 0)
            symptoms = data.get('most_common_symptoms', [])
            severity = data.get('severity_distribution', {})
            
            print(f"✅ إجمالي المحادثات: {total}")
            
            if symptoms:
                print("✅ أكثر الأعراض شيوعاً:")
                for symptom, count in symptoms[:3]:
                    print(f"   • {symptom}: {count} مرة")
            
            if severity:
                print("✅ توزيع الخطورة:")
                for level, count in severity.items():
                    print(f"   • {level}: {count}")
            
            return True
        else:
            print(f"❌ خطأ: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ خطأ: {e}")
        return False

def test_caching():
    """اختبار نظام التخزين المؤقت"""
    print("\n💾 اختبار نظام التخزين المؤقت...")
    test_message = "صداع خفيف"
    
    try:
        # الطلب الأول
        start_time = time.time()
        response1 = requests.post(f"{BASE_URL}/chat", 
                                json={"message": test_message})
        time1 = time.time() - start_time
        
        # الطلب الثاني (يجب أن يكون أسرع)
        start_time = time.time()
        response2 = requests.post(f"{BASE_URL}/chat", 
                                json={"message": test_message})
        time2 = time.time() - start_time
        
        if response1.status_code == 200 and response2.status_code == 200:
            print(f"✅ الطلب الأول: {time1:.2f} ثانية")
            print(f"✅ الطلب الثاني: {time2:.2f} ثانية")
            
            if time2 < time1 * 0.8:  # إذا كان الثاني أسرع بـ 20%
                print("🚀 التخزين المؤقت يعمل بكفاءة!")
            else:
                print("⚠️  التخزين المؤقت قد لا يعمل بالشكل المطلوب")
            
            return True
        else:
            print("❌ خطأ في الطلبات")
            return False
            
    except Exception as e:
        print(f"❌ خطأ: {e}")
        return False

def main():
    """تشغيل جميع الاختبارات"""
    print("🧪 بدء اختبار المميزات المحسنة للمساعد الطبي الذكي")
    print("=" * 60)
    
    tests = [
        ("حالة النظام", test_health_endpoint),
        ("التخصصات", test_specialties_endpoint),
        ("اقتراح الأطباء", test_doctor_recommendations),
        ("تحسينات الشات", test_chat_enhancement),
        ("التحليلات", test_analytics),
        ("التخزين المؤقت", test_caching)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name}: نجح")
            else:
                print(f"❌ {test_name}: فشل")
        except Exception as e:
            print(f"❌ {test_name}: خطأ - {e}")
    
    print("\n" + "="*60)
    print(f"📊 نتائج الاختبار: {passed}/{total} نجح")
    
    if passed == total:
        print("🎉 جميع الاختبارات نجحت! النظام يعمل بشكل مثالي")
    elif passed >= total * 0.8:
        print("✅ معظم الاختبارات نجحت. النظام يعمل بشكل جيد")
    else:
        print("⚠️  بعض الاختبارات فشلت. يرجى مراجعة النظام")
    
    print(f"\n⏰ وقت الاختبار: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
