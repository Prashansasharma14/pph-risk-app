import streamlit as st
import numpy as np
import pickle

# Page config
st.markdown("<h1 style='text-align: center;'>🩺 HemoraAI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>AI-powered PPH Risk Prediction</p>", unsafe_allow_html=True)

# Load model
model = pickle.load(open('pph_model.pkl', 'rb'))

# Header
st.markdown("<h1 style='text-align: center;'>🩺 PPH Risk Predictor AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Early Risk Detection for Postpartum Hemorrhage</p>", unsafe_allow_html=True)

st.markdown("---")

# Input Card
st.subheader("📋 Patient Information")
st.caption("Prediction based on clinical parameters including hemoglobin, parity, and labor characteristics.")

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

st.markdown("---")

st.subheader("Additional Risk Factors")

col3, col4 = st.columns(2)

with col3:
    bmi = st.number_input("BMI", 15.0, 40.0)
    prev_pph = st.selectbox("Previous PPH", ["No", "Yes"])

with col4:
    bp = st.selectbox("Hypertension / Preeclampsia", ["No", "Yes"])
    placenta = st.selectbox("Placenta Previa / Accreta", ["No", "Yes"])

# Convert inputs
prev_lscs = 1 if prev_lscs == "Yes" else 0
induction = 1 if induction == "Yes" else 0
prolonged = 1 if prolonged == "Yes" else 0
multiple = 1 if multiple == "Yes" else 0
prev_pph = 1 if prev_pph == "Yes" else 0
bp = 1 if bp == "Yes" else 0
placenta = 1 if placenta == "Yes" else 0

st.markdown("---")

# Predict button
if st.button("🔍 Predict Risk"):

    input_data = np.array([[age, parity, hb, prev_lscs, induction, prolonged, multiple]])

    # Prediction with spinner
    with st.spinner("Analyzing patient risk..."):
        prob = model.predict_proba(input_data)[0][1]
   st.markdown("### 🧾 Patient Summary")(f"""
Patient Summary:
- Age: {age}
- Hb: {hb}
- BMI: {bmi}
- Hypertension: {'Yes' if bp else 'No'}
- Previous PPH: {'Yes' if prev_pph else 'No'}
""") 
    # Clinical flags
    if hb < 7:
        st.warning("Severe anemia detected — high clinical concern.")

    if parity >= 4:
        st.warning("Grand multiparity — increased PPH risk.")

    st.markdown("---")
    st.subheader("📊 Risk Assessment")

    # Risk display
    st.subheader("Predicted Risk of Postpartum Hemorrhage")
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

    # Confidence line
    st.caption(f"Model confidence: {round(prob*100,1)}% probability of PPH")

# Footer
st.markdown(
    "<p style='text-align: center; font-size: 12px;'>⚠️ For clinical decision support only. Not a substitute for medical judgment.</p>",
    unsafe_allow_html=True
)

st.caption("Version 1.0 | HemoraAI")
st.markdown(
    "<p style='text-align: center;'>Developed by Dr. Prashansa Sharma</p>",
    unsafe_allow_html=True
)
