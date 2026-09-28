import streamlit as st
import joblib

model = joblib.load("titanic_model.pkl")
scaler = joblib.load("titanic_scaler.pkl")

st.set_page_config(
    page_title="Titanic Survival Dashboard",
    page_icon="🚢",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #f4f7fb;
}

.header {
    background: white;
    padding: 25px 35px;
    border-radius: 16px;
    margin-bottom: 25px;
    border: 1px solid #e3e8ef;
}

.title {
    color: #17365d;
    font-size: 36px;
    font-weight: 700;
}

.subtitle {
    color: #718096;
    font-size: 16px;
}

.card {
    background: white;
    padding: 22px;
    border-radius: 15px;
    border: 1px solid #e3e8ef;
    margin-bottom: 20px;
}

.card-title {
    color: #17365d;
    font-size: 20px;
    font-weight: 600;
}

.stButton button {
    background-color: #2563eb;
    color: white;
    width: 100%;
    border-radius: 10px;
    height: 45px;
    font-weight: 600;
}

.result {
    text-align: center;
    padding: 30px;
    border-radius: 15px;
    background: white;
    border: 1px solid #e3e8ef;
}
</style>
""", unsafe_allow_html=True)


# HEADER

st.markdown("""
<div class="header">
    <div class="title">🚢 Titanic Survival Model</div>
    <div class="subtitle">
        Machine Learning Based Passenger Survival Prediction
    </div>
</div>
""", unsafe_allow_html=True)


# PASSENGER INFORMATION

st.markdown("""
<div class="card">
    <div class="card-title">👤 Passenger Information</div>
</div>
""", unsafe_allow_html=True)

left, right = st.columns(2)

with left:

    pclass = st.selectbox(
        "Passenger Class",
        [1, 2, 3]
    )

    age = st.number_input(
        "Age",
        min_value=0,
        max_value=100,
        value=25
    )

    sibsp = st.number_input(
        "Siblings / Spouses",
        min_value=0,
        max_value=10,
        value=0
    )

    parch = st.number_input(
        "Parents / Children",
        min_value=0,
        max_value=10,
        value=0
    )


with right:

    fare = st.number_input(
        "Fare",
        min_value=0.0,
        max_value=600.0,
        value=30.0
    )

    gender = st.selectbox(
        "Gender",
        ["Female", "Male"]
    )

    embarked = st.selectbox(
        "Embarked",
        ["Southampton", "Cherbourg", "Queenstown"]
    )


# FAMILY CALCULATION

family_size = sibsp + parch + 1
is_alone = 1 if family_size == 1 else 0


# SUMMARY CARDS

st.write("")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Passenger Class", pclass)
c2.metric("Age", age)
c3.metric("Family Size", family_size)
c4.metric("Fare", f"{fare:.2f}")


# PREDICTION

st.write("")

st.markdown("""
<div class="card">
    <div class="card-title">🔮 Survival Prediction</div>
</div>
""", unsafe_allow_html=True)

predict = st.button(
    "🔮 Predict Passenger Survival",
    use_container_width=True
)

if predict:

    female = 1 if gender == "Female" else 0
    male = 1 if gender == "Male" else 0

    C = 1 if embarked == "Cherbourg" else 0
    Q = 1 if embarked == "Queenstown" else 0
    S = 1 if embarked == "Southampton" else 0

    data = [[
        pclass,
        age,
        sibsp,
        parch,
        fare,
        family_size,
        is_alone,
        female,
        male,
        C,
        Q,
        S
    ]]

    data = scaler.transform(data)

    prediction = model.predict(data)

    st.write("")

    if prediction[0] == 1:

        st.markdown("""
        <div class="result">
            <h2 style="color:#16a34a;">🟢 Passenger Survived</h2>
            <p>The machine learning model predicts survival.</p>
        </div>
        """, unsafe_allow_html=True)

    else:

        st.markdown("""
        <div class="result">
            <h2 style="color:#dc2626;">🔴 Passenger Did Not Survive</h2>
            <p>The machine learning model predicts non-survival.</p>
        </div>
        """, unsafe_allow_html=True)


# PASSENGER SUMMARY

st.write("")

st.markdown("""
<div class="card">
    <div class="card-title">📋 Passenger Summary</div>
</div>
""", unsafe_allow_html=True)

s1, s2, s3 = st.columns(3)

with s1:
    st.write("**Gender:**", gender)
    st.write("**Embarked:**", embarked)

with s2:
    st.write("**Siblings / Spouses:**", sibsp)
    st.write("**Parents / Children:**", parch)

with s3:
    st.write("**Family Size:**", family_size)
    st.write(
        "**Travelling Alone:**",
        "Yes" if is_alone else "No"
    )