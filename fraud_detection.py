import streamlit as st 
import pandas as pd
import joblib

# --- Custom CSS for attractive UI ---
st.markdown("""
    <style>
    .stApp {background: linear-gradient(135deg, #e3f2fd 0%, #f7f9fa 100%);}
    .main-card {
        background-color: #ffffffcc;
        border-radius: 18px;
        box-shadow: 0 4px 24px rgba(0,0,0,0.07);
        padding: 2rem 2.5rem 2.5rem 2.5rem;
        margin: 2rem auto;
        max-width: 520px;
    }
    .stButton>button {
        background: linear-gradient(90deg, #0072ff 0%, #00c6ff 100%);
        color: white;
        border-radius: 10px;
        font-size: 18px;
        padding: 10px 30px;
        margin-top: 12px;
        border: none;
        box-shadow: 0 2px 6px #0072ff33;
        transition: background 0.2s;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #005bb5 0%, #0096c7 100%);
        color: #e3f2fd;
    }
    .stTextInput>div>input, .stNumberInput>div>input, .stSelectbox>div>div {
        background-color: #e3f2fd;
        border-radius: 8px;
        font-size: 17px;
    }
    .custom-title {
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 2.3rem;
        text-align: center;
        color: #0072ff;
        margin-bottom: 0.8rem;
        font-weight: 700;
        letter-spacing: -1px;
    }
    .custom-subtitle {
        text-align: center;
        font-size: 1.15rem;
        color: #343a40;
        margin-bottom: 1.7rem;
    }
    .avatar-img {
        display: block;
        margin-left: auto;
        margin-right: auto;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

model = joblib.load("fraud_detection_pipeline.pkl")

# --- Session state for users and login ---
if "users" not in st.session_state:
    st.session_state.users = {"admin": "password123"}
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "page" not in st.session_state:
    st.session_state.page = "login"

def signup_page():
    with st.container():
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.image("https://img.icons8.com/fluency/96/add-user-group-man-man.png", width=80, output_format="auto", use_container_width =False)
        st.markdown('<div class="custom-title">Create Account</div>', unsafe_allow_html=True)
        st.markdown('<div class="custom-subtitle">Sign up to start using the fraud detection app.</div>', unsafe_allow_html=True)
        new_username = st.text_input("New Username", key="signup_username")
        new_password = st.text_input("New Password", type="password", key="signup_password")
        if st.button("Register", key="register_btn"):
            if not new_username or not new_password:
                st.error("Please fill all fields.")
            elif new_username in st.session_state.users:
                st.error("Username already exists.")
            else:
                st.session_state.users[new_username] = new_password
                st.success("Registration successful! Please login.")
                st.session_state.page = "login"
        st.markdown("---")
        if st.button("Go to Login", key="login_nav_btn"):
            st.session_state.page = "login"
        st.markdown('</div>', unsafe_allow_html=True)

def login_page():
    with st.container():
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.image("https://img.icons8.com/fluency/96/lock.png", width=80, output_format="auto", use_container_width=False)
        st.markdown('<div class="custom-title">Login</div>', unsafe_allow_html=True)
        st.markdown('<div class="custom-subtitle">Welcome back! Please enter your credentials.</div>', unsafe_allow_html=True)
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login", key="login_btn"):
            if username in st.session_state.users and st.session_state.users[username] == password:
                st.session_state.logged_in = True
                st.session_state.current_user = username
                st.success("Login successful!")
                st.session_state.page = "main"
                st.rerun()
            else:
                st.error("Invalid username or password.")
        st.markdown("---")
        if st.button("Go to Register", key="register_nav_btn"):
            st.session_state.page = "signup"
        st.markdown('</div>', unsafe_allow_html=True)

def logout_page():
    with st.container():
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.image("https://img.icons8.com/fluency/96/logout-rounded-left.png", width=80, output_format="auto", use_container_width=False)
        st.markdown('<div class="custom-title">Logged Out</div>', unsafe_allow_html=True)
        st.markdown('<div class="custom-subtitle">You have been logged out. Thank you for using the app!</div>', unsafe_allow_html=True)
        if st.button("Return to Login", key="return_login_btn"):
            st.session_state.page = "login"
        st.markdown('</div>', unsafe_allow_html=True)

def main_page():
    with st.container():
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.image("https://img.freepik.com/free-vector/fraud-prevention-concept-illustration_114360-7887.jpg", width=250, output_format="auto", use_container_width=False)
        st.markdown(f'<div class="custom-title">Fraud Detection Prediction</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="custom-subtitle">Welcome, <span style="color:#0072ff;font-weight:600;">{st.session_state.current_user}</span>! Enter transaction details below and click <b>Predict</b>.</div>', unsafe_allow_html=True)
        if st.button("Logout", key="logout_btn"):
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.session_state.page = "logout"
            st.rerun()

        st.markdown("---")
        transaction_type = st.selectbox("Transaction Type", ["PAYMENT", "TRANSFER", "CASH_OUT", "DEPOSIT"])
        Amount = st.number_input("Amount", min_value=0.0, value=1000.0, step=100.0)
        oldbalanceOrg = st.number_input("Old Balance(Sender)", min_value=0.0, value=10000.0, step=500.0)
        newbalanceOrig = st.number_input("New Balance(Sender)", min_value=0.0, value=9000.0, step=500.0)
        oldbalanceDest = st.number_input("Old Balance(Receiver)", min_value=0.0, value=0.0, step=100.0)
        newbalanceDest = st.number_input("New Balance(Receiver)", min_value=0.0, value=0.00, step=100.0)

        if st.button("Predict", key="predict_btn"):
            input_data = pd.DataFrame([{
                "type": transaction_type,
                "amount": Amount,
                "oldbalanceOrg": oldbalanceOrg,
                "newbalanceOrig": newbalanceOrig,
                "oldbalanceDest": oldbalanceDest,
                "newbalanceDest": newbalanceDest
            }])                    
            prediction = model.predict(input_data)[0]
            st.subheader(f"Prediction: {'Fraud' if prediction == 0 else 'Not Fraud'}")
            if prediction == 0:
                st.error("⚠️ This transaction may be fraudulent!")
            else:
                st.success("✅ This transaction looks safe.")
        st.markdown('</div>', unsafe_allow_html=True)

# --- App logic ---
if not st.session_state.logged_in:
    if st.session_state.page == "login":
        login_page()
    elif st.session_state.page == "signup":
        signup_page()
    elif st.session_state.page == "logout":
        logout_page()
else:
    main_page()