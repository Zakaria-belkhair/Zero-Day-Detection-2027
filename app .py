# Zero-Day-Detection-2027
منصة ذكاء اصطناعي لاكتشاف الثغرات الصفرية وتحليل السلوك الشبكي
import streamlit as st
import pandas as pd
from sklearn.ensemble import IsolationForest

# --- 1. إعدادات الصفحة ونظام الحماية ---
st.set_page_config(page_title="Zero-Day Detection SaaS", page_icon="🛡️", layout="wide")

# قائمة العملاء أو الأصدقاء المسموح لهم بالدخول (يمكنك إضافة أي إيميل جديد هنا)
ALLOWED_EMAILS = [
    "zakaria@example.com", 
    "friend@example.com"  # استبدل هذا بإيميل صديقك الفعلي
]

st.sidebar.title("🔐 Client Portal")
user_email = st.sidebar.text_input("Enter your registered email:")

# --- 2. التحقق من صلاحيات الوصول ---
if user_email in ALLOWED_EMAILS:
    st.sidebar.success("✅ Access verified successfully!")
    
    # واجهة المنصة الاحترافية
    st.title("🛡️ Zero-Day Detection & Threat Analysis Platform")
    st.write("Welcome to the professional SaaS platform for advanced security analysis.")
    
    # قسم رفع الملفات
    uploaded_file = st.file_uploader("Upload log file (CSV) for analysis", type=["csv"])
    
    if uploaded_file is not None:
        try:
            # قراءة البيانات
            df = pd.read_csv(uploaded_file)
            st.write("### 📊 Dataset Preview")
            st.dataframe(df.head())
            
            # تحليل البيانات واكتشاف الشذوذ باستخدام Isolation Forest
            st.write("---")
            st.write("🔄 Running Machine Learning Threat Analysis...")
            
            # استخراج الأعمدة الرقمية فقط للتحليل
            numeric_df = df.select_dtypes(include=['float64', 'int64'])
            
            if not numeric_df.empty:
                model = IsolationForest(contamination=0.05, random_state=42)
                preds = model.fit_predict(numeric_df)
                
                df['Anomalies'] = preds
                # اعتبار القيم التي تم التنبؤ بـ -1 كتهديدات محتملة
                anomalies = df[df['Anomalies'] == -1]
                
                st.warning(f"⚠️ Detected {len(anomalies)} potential zero-day or anomalous events!")
                if not anomalies.empty:
                    st.dataframe(anomalies)
            else:
                st.info("The uploaded CSV does not contain sufficient numerical columns for isolation forest analysis.")
                
        except Exception as e:
            st.error(f"An error occurred while processing the file: {e}")
            
else:
    if user_email:
        st.sidebar.error("❌ This email is not registered or has not purchased access.")
    
    st.warning("⚠️ Please enter your correct registered email in the sidebar to unlock the platform.")
    st.stop()
