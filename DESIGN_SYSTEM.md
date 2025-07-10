# نظام التصميم الموحد - مساعد طبي ذكي
# Unified Design System - Medical Assistant

## نظرة عامة | Overview

تم تطوير نظام تصميم موحد شامل للموقع الطبي لضمان التناسق البصري وتحسين تجربة المستخدم عبر جميع الصفحات.

A comprehensive unified design system has been developed for the medical website to ensure visual consistency and improve user experience across all pages.

## الملفات الأساسية | Core Files

### 1. CSS Files
- `css/unified-theme.css` - النظام الأساسي الموحد | Core unified system
- `css/medical-enhancements.css` - تحسينات خاصة بالموقع الطبي | Medical-specific enhancements

### 2. JavaScript Files
- `js/common.js` - الوظائف المشتركة | Common functions

## نظام الألوان | Color System

### الألوان الأساسية | Primary Colors
```css
--primary-500: #3b82f6;  /* اللون الأساسي */
--primary-600: #2563eb;  /* اللون الأساسي الداكن */
--primary-700: #1d4ed8;  /* اللون الأساسي الأكثر قتامة */
```

### الألوان الثانوية | Secondary Colors
```css
--secondary-500: #f97316; /* البرتقالي */
--success-500: #10b981;   /* الأخضر */
--warning-500: #f59e0b;   /* الأصفر */
--danger-500: #ef4444;    /* الأحمر */
```

### الألوان المحايدة | Neutral Colors
```css
--gray-50: #f8fafc;   /* خلفية فاتحة */
--gray-100: #f1f5f9;  /* خلفية */
--gray-500: #64748b;  /* نص ثانوي */
--gray-800: #1e293b;  /* نص أساسي */
--gray-900: #0f172a;  /* نص داكن */
```

## نظام الخطوط | Typography System

### عائلات الخطوط | Font Families
- **Primary**: 'Cairo' - للنصوص العربية | For Arabic text
- **Secondary**: 'Plus Jakarta Sans' - للنصوص الإنجليزية | For English text

### أحجام الخطوط | Font Sizes
```css
--font-size-xs: 0.75rem;    /* 12px */
--font-size-sm: 0.875rem;   /* 14px */
--font-size-base: 1rem;     /* 16px */
--font-size-lg: 1.125rem;   /* 18px */
--font-size-xl: 1.25rem;    /* 20px */
--font-size-2xl: 1.5rem;    /* 24px */
--font-size-3xl: 1.875rem;  /* 30px */
--font-size-4xl: 2.25rem;   /* 36px */
--font-size-5xl: 3rem;      /* 48px */
```

### أوزان الخطوط | Font Weights
```css
--font-weight-normal: 400;
--font-weight-medium: 500;
--font-weight-semibold: 600;
--font-weight-bold: 700;
--font-weight-extrabold: 800;
```

## نظام المسافات | Spacing System

```css
--space-1: 0.25rem;   /* 4px */
--space-2: 0.5rem;    /* 8px */
--space-3: 0.75rem;   /* 12px */
--space-4: 1rem;      /* 16px */
--space-5: 1.25rem;   /* 20px */
--space-6: 1.5rem;    /* 24px */
--space-8: 2rem;      /* 32px */
--space-10: 2.5rem;   /* 40px */
--space-12: 3rem;     /* 48px */
--space-16: 4rem;     /* 64px */
--space-20: 5rem;     /* 80px */
--space-24: 6rem;     /* 96px */
```

## نظام الحدود المستديرة | Border Radius System

```css
--radius-sm: 0.25rem;   /* 4px */
--radius-md: 0.375rem;  /* 6px */
--radius-lg: 0.5rem;    /* 8px */
--radius-xl: 0.75rem;   /* 12px */
--radius-2xl: 1rem;     /* 16px */
--radius-3xl: 1.5rem;   /* 24px */
--radius-full: 9999px;  /* دائري كامل */
```

## نظام الظلال | Shadow System

```css
--shadow-xs: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
--shadow-sm: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.1);
--shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1);
--shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1);
--shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
--shadow-2xl: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
```

## المكونات الأساسية | Core Components

### 1. الأزرار | Buttons

#### الأنواع | Types
- `.btn-primary` - الزر الأساسي
- `.btn-secondary` - الزر الثانوي
- `.btn-outline-primary` - زر بحدود
- `.btn-success` - زر النجاح
- `.btn-warning` - زر التحذير
- `.btn-danger` - زر الخطر

#### الأحجام | Sizes
- `.btn-sm` - صغير
- `.btn` - عادي (افتراضي)
- `.btn-lg` - كبير
- `.btn-xl` - كبير جداً

### 2. البطاقات | Cards

```css
.card {
  background-color: white;
  border: 1px solid var(--gray-200);
  border-radius: var(--radius-2xl);
  box-shadow: var(--shadow-sm);
  overflow: hidden;
  transition: all var(--transition-normal);
}
```

#### أجزاء البطاقة | Card Parts
- `.card-header` - رأس البطاقة
- `.card-body` - محتوى البطاقة
- `.card-footer` - تذييل البطاقة

### 3. النماذج | Forms

#### عناصر النماذج | Form Elements
- `.form-control` - حقول الإدخال
- `.form-select` - قوائم الاختيار
- `.form-label` - تسميات الحقول
- `.form-group` - مجموعة الحقول

#### حالات التحقق | Validation States
- `.is-valid` - صحيح
- `.is-invalid` - خطأ
- `.valid-feedback` - رسالة النجاح
- `.invalid-feedback` - رسالة الخطأ

## المكونات الطبية المتخصصة | Medical-Specific Components

### 1. واجهة المحادثة الطبية | Medical Chat Interface

```css
.chat-container {
  background: white;
  border-radius: var(--radius-3xl);
  box-shadow: var(--shadow-2xl);
  overflow: hidden;
}
```

#### أجزاء المحادثة | Chat Parts
- `.chat-header` - رأس المحادثة
- `.chat-messages` - منطقة الرسائل
- `.chat-input` - منطقة الإدخال
- `.message` - الرسالة
- `.message.user` - رسالة المستخدم
- `.message.bot` - رسالة البوت

### 2. بطاقات الأطباء | Doctor Cards

```css
.doctor-selection-card {
  background: white;
  border-radius: var(--radius-2xl);
  transition: all var(--transition-normal);
  cursor: pointer;
}

.doctor-selection-card.selected {
  border-color: var(--primary-500);
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
}
```

### 3. بطاقات المواعيد | Appointment Cards

```css
.appointment-card {
  background: white;
  border-radius: var(--radius-2xl);
  transition: all var(--transition-normal);
}
```

#### شارات الحالة | Status Badges
- `.status-confirmed` - مؤكد
- `.status-pending` - في الانتظار
- `.status-completed` - مكتمل
- `.status-cancelled` - ملغي

## الحركات والتأثيرات | Animations & Effects

### الحركات الأساسية | Basic Animations
```css
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes slideInUp {
  from { opacity: 0; transform: translateY(100%); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes bounce {
  0%, 20%, 53%, 80%, 100% { transform: translate3d(0, 0, 0); }
  40%, 43% { transform: translate3d(0, -30px, 0); }
  70% { transform: translate3d(0, -15px, 0); }
  90% { transform: translate3d(0, -4px, 0); }
}
```

### فئات الحركة | Animation Classes
- `.animate-fadeIn` - ظهور تدريجي
- `.animate-slideInUp` - انزلاق من الأسفل
- `.animate-bounce` - ارتداد
- `.animate-pulse` - نبضة
- `.animate-spin` - دوران

## التصميم المتجاوب | Responsive Design

### نقاط التوقف | Breakpoints
```css
--breakpoint-sm: 576px;   /* الهواتف الكبيرة */
--breakpoint-md: 768px;   /* الأجهزة اللوحية */
--breakpoint-lg: 992px;   /* أجهزة الكمبيوتر المحمولة */
--breakpoint-xl: 1200px;  /* أجهزة سطح المكتب */
--breakpoint-xxl: 1400px; /* الشاشات الكبيرة */
```

### التحسينات للهواتف | Mobile Optimizations
```css
@media (max-width: 768px) {
  .message-content { max-width: 85%; }
  .quick-action-btn { padding: var(--space-3); }
  .doctor-image { width: 60px; height: 60px; }
}
```

## إمكانية الوصول | Accessibility

### دعم الحركة المقللة | Reduced Motion Support
```css
@media (prefers-reduced-motion: reduce) {
  .animate-fadeIn,
  .animate-slideInUp,
  .animate-bounce {
    animation: none;
  }
}
```

### دعم التباين العالي | High Contrast Support
```css
@media (prefers-contrast: high) {
  .card, .button {
    border-width: 2px;
    border-color: var(--gray-800);
  }
}
```

## الوظائف المشتركة | Common Functions

### إدارة المصادقة | Authentication Management
- `isAuthenticated()` - فحص حالة تسجيل الدخول
- `getCurrentUser()` - الحصول على بيانات المستخدم الحالي
- `setCurrentUser(userData)` - تعيين بيانات المستخدم
- `logout()` - تسجيل الخروج
- `updateAuthUI()` - تحديث واجهة المصادقة

### إدارة الواجهة | UI Management
- `showToast(message, type)` - عرض إشعار
- `showLoading(element)` - عرض حالة التحميل
- `hideLoading(element)` - إخفاء حالة التحميل
- `animateIn(element, animation)` - تحريك العنصر

### التحقق من النماذج | Form Validation
- `validateField(field, rules)` - التحقق من حقل
- `isValidEmail(email)` - التحقق من البريد الإلكتروني
- `isValidPhone(phone)` - التحقق من رقم الهاتف

## الاستخدام | Usage

### تطبيق النظام على صفحة جديدة | Applying System to New Page

1. **إضافة ملفات CSS**:
```html
<link rel="stylesheet" href="css/unified-theme.css">
<link rel="stylesheet" href="css/medical-enhancements.css">
```

2. **إضافة ملفات JavaScript**:
```html
<script src="js/common.js"></script>
```

3. **استخدام الفئات المحددة مسبقاً**:
```html
<button class="btn btn-primary btn-lg">
  <i class="fas fa-stethoscope me-2"></i>
  ابدأ التشخيص
</button>
```

## الصيانة والتطوير | Maintenance & Development

### إضافة مكون جديد | Adding New Component
1. إضافة الأنماط في `css/unified-theme.css` أو `css/medical-enhancements.css`
2. إضافة الوظائف في `js/common.js` إذا لزم الأمر
3. توثيق المكون في هذا الملف
4. اختبار المكون على جميع الصفحات

### تحديث الألوان | Updating Colors
1. تعديل المتغيرات في `:root` في `css/unified-theme.css`
2. التأكد من التباين المناسب للوصولية
3. اختبار التغييرات على جميع المكونات

---

## ملاحظات مهمة | Important Notes

- جميع المتغيرات معرفة في `:root` لسهولة التخصيص
- النظام يدعم الوضع المظلم (يمكن تطويره لاحقاً)
- جميع المكونات متجاوبة ومحسنة للهواتف
- النظام يدعم إمكانية الوصول والمعايير الحديثة
- الكود منظم ومعلق لسهولة الصيانة

تم تطوير هذا النظام لضمان تجربة مستخدم متسقة وعالية الجودة عبر جميع صفحات الموقع الطبي.
