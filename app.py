import streamlit as st
import numpy as np
import pickle

# Load model
model = pickle.load(open('pph_model.pkl', 'rb'))

st.title("PPH Risk Predictor")

st.write("Enter patient details:")

age = st.number_input("Age")
parity = st.number_input("Parity")
hb = st.number_input("Hemoglobin")
prev_lscs = st.selectbox("Previous LSCS", [0,1])
induction = st.selectbox("Induction of Labor", [0,1])
prolonged = st.selectbox("Prolonged Labor", [0,1])
multiple = st.selectbox("Multiple Pregnancy", [0,1])

if st.button("Predict Risk"):
    input_data = np.array([[age, parity, hb, prev_lscs, induction, prolonged, multiple]])

    prob = model.predict_proba(input_data)[0][1]
    prediction = 1 if prob > 0.5 else 0

    st.subheader(f"Risk Score: {round(prob*100,2)} %")

    if prediction == 1:
        st.error("⚠️ High Risk of PPH")
        st.warning("Consider: Active management of third stage, blood availability, senior supervision.")
    else:
        st.success("✅ Low Risk of PPH")
        st.info("Routine monitoring recommended.")
