import streamlit as st
import numpy as np
import pickle

# Page config
st.markdown("<h1 style='text-align: center;'>🩺 HemoraAI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>AI-powered PPH Risk Prediction</p>", unsafe_allow_html=True)
st.info("Designed to assist early identification of postpartum hemorrhage risk in resource-limited settings.")

# Load model
model = pickle.load(open('pph_model.pkl', 'rb'))

# Header
st.markdown("<h1 style='text-align: center;'>🩺 PPH Risk Predictor AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Early Risk Detection for Postpartum Hemorrhage</p>", unsafe_allow_html=True)

st.markdown("---")

# Input Card
st.subheader("📋 Patient Information")

col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age", 15, 50)
    parity = st.number_input("Parity", 0, 10)
    hb = st.number_input("Hemoglobin (g/dL)", 5.0, 15.0)

with col2:
    prev_lscs = st.selectbox("Previous LSCS", ["No", "Yes"])
    induction = st.selectbox("Induction of Labor", ["No", "Yes"])
    prolonged = st.selectbox("Prolonged Labor", ["No", "Yes"])
    multiple = st.selectbox("Multiple Pregnancy", ["No", "Yes"])

# Convert inputs
prev_lscs = 1 if prev_lscs == "Yes" else 0
induction = 1 if induction == "Yes" else 0
prolonged = 1 if prolonged == "Yes" else 0
multiple = 1 if multiple == "Yes" else 0

st.markdown("---")

# Predict button
if st.button("🔍 Predict Risk"):

    input_data = np.array([[age, parity, hb, prev_lscs, induction, prolonged, multiple]])
    
   with st.spinner("Analyzing patient risk..."):
    prob = model.predict_proba(input_data)[0][1]
       if hb < 7:
    st.warning("Severe anemia detected — high clinical concern.")
if parity >= 4:
    st.warning("Grand multiparity — increased PPH risk.")

    st.markdown("---")

    # Risk display
    st.markdown("## 📊 Risk Assessment")

    if prob < 0.3:
        st.success(f"🟢 Low Risk ({round(prob*100,1)}%)")
        st.info("Routine monitoring recommended.")

    elif prob < 0.7:
        st.warning(f"🟡 Moderate Risk ({round(prob*100,1)}%)")
        st.warning("Consider closer observation and preparedness.")

    else:
        st.error(f"🔴 High Risk ({round(prob*100,1)}%)")
        st.error("""
        Immediate Actions:
        • Active management of third stage  
        • Ensure blood availability  
        • Senior supervision  
        • Monitor closely postpartum  
        """)

    st.markdown("---")

# Footer
st.markdown(
    "<p style='text-align: center; font-size: 12px;'>⚠️ For clinical decision support only. Not a substitute for medical judgment.</p>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align: center;'>Developed by Dr. Prashansa Sharma</p>",
    unsafe_allow_html=True
)
