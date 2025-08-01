import streamlit as st
from datetime import datetime
import pandas as pd
import uuid

# Initialize session state
if "appointments" not in st.session_state:
    st.session_state.appointments = []

if "feedbacks" not in st.session_state:
    st.session_state.feedbacks = []

# Title
st.title("🩺 Orthopedic Doctor Online Appointment System")

# Sidebar: Stats and Payment
st.sidebar.header("Doctor Dashboard")

total_patients = len(st.session_state.appointments)
st.sidebar.metric("👨‍⚕️ Patients Treated", total_patients)

st.sidebar.subheader("💳 Make a Payment")
payment_link = "https://razorpay.com/payment-link/replace-this-link"
st.sidebar.markdown(f"[Pay Consultation Fee ₹500]({payment_link})", unsafe_allow_html=True)

st.sidebar.info("Secure payment via Razorpay or UPI")

# Main Tab Layout
tab1, tab2, tab3 = st.tabs(["📅 Book Appointment", "💬 Feedback", "🗓️ View Bookings"])

# --- TAB 1: Book Appointment ---
with tab1:
    st.subheader("📅 Book an Appointment")
    with st.form("appointment_form"):
        name = st.text_input("Full Name")
        age = st.number_input("Age", min_value=0, max_value=120, step=1)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        contact = st.text_input("Contact Number")
        reason = st.text_area("Reason for Appointment")
        date = st.date_input("Preferred Date", min_value=datetime.today())
        time = st.time_input("Preferred Time")
        submit = st.form_submit_button("Book Appointment")

        if submit:
            appointment_id = str(uuid.uuid4())[:8]
            st.session_state.appointments.append({
                "ID": appointment_id,
                "Name": name,
                "Age": age,
                "Gender": gender,
                "Contact": contact,
                "Reason": reason,
                "Date": date.strftime("%Y-%m-%d"),
                "Time": time.strftime("%H:%M"),
                "Status": "Pending"
            })
            st.success(f"Appointment Booked Successfully! Your ID: {appointment_id}")
            st.balloons()

# --- TAB 2: Feedback ---
with tab2:
    st.subheader("💬 Share Your Feedback")
    with st.form("feedback_form"):
        patient_name = st.text_input("Your Name")
        rating = st.slider("Rate the Doctor", 1, 5)
        feedback = st.text_area("Write your feedback")
        submit_feedback = st.form_submit_button("Submit Feedback")

        if submit_feedback:
            st.session_state.feedbacks.append({
                "Name": patient_name,
                "Rating": rating,
                "Feedback": feedback
            })
            st.success("Thank you for your feedback!")

    if st.session_state.feedbacks:
        st.markdown("### ⭐ Previous Patient Feedback")
        for fb in st.session_state.feedbacks[::-1]:
            st.write(f"**{fb['Name']}** (⭐ {fb['Rating']}/5)")
            st.info(fb["Feedback"])

# --- TAB 3: View Appointments (For Doctor/Admin) ---
with tab3:
    st.subheader("🗓️ All Appointments")
    if st.session_state.appointments:
        df = pd.DataFrame(st.session_state.appointments)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No appointments booked yet.")
