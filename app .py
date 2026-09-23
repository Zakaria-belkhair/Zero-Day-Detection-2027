import streamlit as st

# --- نظام المصادقة بالبريد الإلكتروني للعملاء المشتركين ---
ALLOWED_EMAILS = [
    "zakaria@example.com", 
    "friend@example.com"  # أضف هنا إيميل صديقك أو عملائك
]

st.sidebar.title("🔐 Client Portal")
user_email = st.sidebar.text_input("Enter your registered email:")

# التحقق مما إذا كان الإيميل المدخل موجوداً في القائمة المسموحة
if user_email in ALLOWED_EMAILS:
    st.sidebar.success("✅ Access verified successfully!")
    
    st.title("🛡️ Zero-Day Detection SaaS Platform")
    st.write("Welcome to the professional version of the platform.")
    
    uploaded_file = st.file_uploader("Upload log file (CSV) for analysis", type=["csv"])
    if uploaded_file is not None:
        st.write("Analyzing data and detecting threats...")

else:
    if user_email:
        st.sidebar.error("❌ This email is not registered or has not purchased access.")
    
    st.warning("⚠️ Please enter your correct email in the sidebar to access the platform.")
    st.stop()
