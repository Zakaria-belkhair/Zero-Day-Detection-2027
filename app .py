import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

st.set_page_config(page_title="Zero-Day Detection SaaS", page_icon="🛡️", layout="wide")

ALLOWED_EMAILS = [
    "Zaki.nexura@gmail.com", 
    "friend@example.com"
]

st.sidebar.title("🔐 Client Portal")
user_email = st.sidebar.text_input("Enter your registered email:")

if user_email in ALLOWED_EMAILS:
    st.sidebar.success("✅ Access verified successfully!")
    
    st.title("🛡️ Zero-Day Detection & Threat Analysis Platform")
    st.write("Welcome to the professional SaaS platform for advanced security analysis.")
    
    option = st.sidebar.selectbox("Choose Mode", ["Upload CSV File", "Generate Sample Data"])
    
    if option == "Generate Sample Data":
        st.subheader("📊 Generate Sample Network Logs")
        num_rows = st.slider("Select number of rows to generate", 100, 1000, 500)
        
        if st.button("Generate Data Now"):
            np.random.seed(2027)
            normal_data = np.random.normal(loc=50, scale=10, size=(num_rows, 3))
            df_generated = pd.DataFrame(normal_data, columns=["Packet_Size", "Response_Time", "Connection_Count"])
            
            st.success(f"Successfully generated {len(df_generated)} rows of sample data!")
            st.dataframe(df_generated.head(10))
            
            csv_data = df_generated.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Generated CSV",
                data=csv_data,
                file_name="Generated_Network_Traffic.csv",
                mime="text/csv"
            )
            
    elif option == "Upload CSV File":
        st.subheader("📂 Upload Custom CSV Logs")
        uploaded_file = st.file_uploader("Upload your log file for AI analysis", type=["csv"])
        
        if uploaded_file is not None:
            try:
                df_user = pd.read_csv(uploaded_file)
                st.write("### Dataset Preview")
                st.dataframe(df_user.head())
                
                numeric_df = df_user.select_dtypes(include=['float64', 'int64'])
                
                if numeric_df.empty:
                    st.error("No numerical columns found for analysis.")
                else:
                    ai_model = IsolationForest(contamination=0.05, random_state=42)
                    predictions = ai_model.fit_predict(numeric_df)
                    
                    df_user['Security_Status'] = predictions
                    threats_count = np.sum(predictions == -1)
                    
                    col1, col2 = st.columns(2)
                    col1.metric("Total Analyzed Rows", len(df_user))
                    col2.metric("Detected Threats", int(threats_count))
                    
                    st.dataframe(df_user)
                    
                    result_csv = df_user.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Download Final Analysis Report",
                        data=result_csv,
                        file_name="Analyzed_Security_Report.csv",
                        mime="text/csv"
                    )
            except Exception as e:
                st.error(f"Error processing file: {e}")
                
else:
    if user_email:
        st.sidebar.error("❌ This email is not registered.")
    st.warning("⚠️ Please enter your correct registered email in the sidebar to access the platform.")
    st.stop()
