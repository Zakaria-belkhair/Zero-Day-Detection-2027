import streamlit as st
import pandas as pd
from sklearn.ensemble import IsolationForest

# إعدادات صفحة المنصة الأمنية
st.set_page_config(
    page_title="منصة الذكاء الاصطناعي لكشف الثغرات - 2027",
    page_icon="🛡️",
    layout="wide"
)

# نظام الحماية والنسخة الخاصة في الشريط الجانبي
st.sidebar.title("🔐 بوابة المصادقة الخاصة")
access_key = st.sidebar.text_input("أدخل مفتاح الترخيص أو كلمة المرور:", type="password")

CORRECT_KEY = "Zaki2027Secure"

if access_key != CORRECT_KEY:
    st.warning("⚠️ يرجى إدخال مفتاح الترخيص الصحيح في الشريط الجانبي لعرض لوحة التحكم وتحليل البيانات.")
    st.stop()

# واجهة المنصة بعد تسجيل الدخول بنجاح
st.title("🛡️ منصة الذكاء الاصطناعي للتحكم الأمني واكتشاف الثغرات غير المعروفة")
st.markdown("**النسخة التجارية الخاصة** - مخصصة لتحليل حركة مرور الشبكات وملفات الـ CSV عبر خوارزميات التعلم الآلي.")

uploaded_file = st.file_uploader("اختر ملف حركة المرور أو السجلات (CSV):", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("📊 معاينة البيانات المدخلة:")
    st.dataframe(df.head())
    
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    
    if len(numeric_cols) > 0:
        st.info("🔍 جاري فحص البيانات واكتشاف التهديدات والأنماط الشاذة عبر نموذج (Isolation Forest)...")
        model = IsolationForest(contamination=0.05, random_state=42)
        df['Anomaly'] = model.fit_predict(df[numeric_cols])
        
        df['Status'] = df['Anomaly'].apply(lambda x: "🚨 تهديد محتمل (Anomaly)" if x == -1 else "✅ آمن (Normal)")
        
        st.subheader("📈 تقرير النتائج والتهديدات المكتشفة:")
        st.dataframe(df)
        
        threats_count = (df['Anomaly'] == -1).sum()
        st.metric(label="إجمالي التهديدات غير المعروفة المكتشفة", value=threats_count)
    else:
        st.error("❌ الملف المدخل لا يحتوي على أعمدة رقمية كافية لتشغيل نموذج التحليل الأمني.")
else:
    st.info("📁 يرجى رفع ملف CSV يحتوي على سجلات الشبكة أو النظام لبدء الفحص الأمني.")
