import streamlit as st
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

st.set_page_config(page_title="منصة الأمن الاستباقي ومولد البيانات 2027", page_icon="🛡️", layout="wide")

st.title("🛡️ منصة الأمن الاستباقي ومولد ملفات البيانات (نظام 2027)")
st.write("أداة متكاملة لتوليد بيانات الشبكة، حفظها بصيغة CSV، وفحصها بحثاً عن الثغرات الصفرية.")

# القائمة الجانبية للتحكم
st.sidebar.header("⚙️ خيارات المنصة")
option = st.sidebar.selectbox("اختر القسم المطلوب:", ["مولد ملفات CSV الذكي", "فحص ورفع ملف CSV خارجي"])

if option == "مولد ملفات CSV الذكي":
    st.subheader("📥 قسم توليد وتصدير ملفات حركة الشبكة (CSV Generator)")
    st.write("قم بتحديد عدد السجلات المطلوبة، وسيقوم النظام بتوليد ملف بيانات افتراضي يحتوي على سلوك طبيعي وهجمات محتملة جاهز للتحميل.")
    
    num_rows = st.slider("عدد السجلات المراد توليدها في الملف", min_value=50, max_value=1000, value=200, step=50)
    
    if st.button("توليد ملف البيانات الآن"):
        np.random.seed(2027)
        normal_data = np.random.normal(loc=100, scale=10, size=(int(num_rows * 0.95), 3))
        anomaly_data = np.random.normal(loc=170, scale=25, size=(int(num_rows * 0.05), 3))
        combined_data = np.vstack([normal_data, anomaly_data])
        
        df_generated = pd.DataFrame(combined_data, columns=["معدل الحزم (Rate)", "زمن الاستجابة (Latency)", "حجم البيانات (Size)"])
        df_generated = df_generated.sample(frac=1).reset_index(drop=True)
        
        st.success(f"تم بنجاح توليد {len(df_generated)} سجل شبكي افتراضي!")
        st.dataframe(df_generated.head(10), use_container_width=True)
        
        csv_data = df_generated.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="💾 اضغط هنا لتحميل ملف الـ CSV المنشأ على جهازك",
            data=csv_data,
            file_name="Generated_Network_Traffic_2027.csv",
            mime="text/csv"
        )

elif option == "فحص ورفع ملف CSV خارجي":
    st.subheader("🔍 قسم الفحص الحي لملفات CSV الخاصة بك")
    st.write("قم برفع أي ملف CSV (سواء قمت بتوليده بالخيار السابق أو ملف خاص بك) ليفحصه الذكاء الاصطناعي لحظياً.")
    
    uploaded_file = st.file_uploader("اختر ملف CSV للرفع", type=["csv"])
    
    if uploaded_file is not None:
        df_user = pd.read_csv(uploaded_file)
        numeric_df = df_user.select_dtypes(include=[np.number])
        
        if numeric_df.empty:
            st.error("الملف المرفوع لا يحتوي على أعمدة رقمية كافية للتحليل.")
        else:
            ai_model = IsolationForest(contamination=0.05, random_state=2027)
            predictions = ai_model.fit_predict(numeric_df.values)
            
            df_user['حالة الأمان الاستباقي'] = ["🚨 تهديد حرج (شذوذ)" if p == -1 else "✅ آمن ومستقر" for p in predictions]
            threats_count = np.sum(predictions == -1)
            
            col1, col2 = st.columns(2)
            col1.metric("إجمالي السجلات المفحوصة", len(df_user))
            col2.metric("التهديدات المكتشفة", threats_count)
            
            st.dataframe(df_user, use_container_width=True)
            
            result_csv = df_user.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 تحميل تقرير النتائج النهائي (CSV)",
                data=result_csv,
                file_name="Analyzed_Security_Report.csv",
                mime="text/csv"
            )
