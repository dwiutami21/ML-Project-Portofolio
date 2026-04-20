import streamlit as st
import pickle
import pandas as pd 
import time

st.set_page_config(page_title="ML Portfolio", page_icon="🌸", layout="wide", initial_sidebar_state="expanded")
st.write("Welcome to my ML Portfolio!")

select_var = st.sidebar.selectbox("Select page", ["Home", "Iris Species", "Heart Disease"])

if select_var == "Home":
    st.title("🌸 Welcome to ML Portfolio")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("About This App")
        st.write("""
        Selamat datang di **ML Portfolio** saya! 
        
        Aplikasi ini mendemonstrasikan penggunaan **Machine Learning** 
        untuk klasifikasi data real-world menggunakan dataset terkenal seperti Iris.
        """)
    
    with col2:
        st.image("https://s3.amazonaws.com/assets.datacamp.com/blog_assets/Machine+Learning+R/iris-machinelearning.png", width=300)
    
    st.markdown("---")
    
    st.subheader("📊 Available Features")
    
    features = {
        "🔍 Iris Species Prediction": "Prediksi jenis Iris berdasarkan karakteristik bunga (Sepal & Petal measurements)",
        "❤️ Heart Disease Prediction": "Prediksi risiko penyakit jantung berdasarkan parameter kesehatan",
        "📤 CSV Upload Support": "Upload file CSV dengan data Anda sendiri untuk batch prediction",
        "🎚️ Interactive Sliders": "Gunakan slider untuk input data secara manual",
        "⚡ Real-time Results": "Dapatkan hasil prediksi secara instant"
    }
    
    for feature, description in features.items():
        st.write(f"**{feature}**")
        st.write(f"→ {description}")
        st.write("")
    
    st.markdown("---")
    
    st.subheader("🚀 Getting Started")
    st.write("""
    1. Pilih model dari menu sidebar
    2. Input data Anda:
       - **Upload CSV**: Upload file dataset Anda
       - **Manual Input**: Gunakan slider untuk input data
    3. Klik tombol **"Submit"** untuk prediksi
    4. Lihat hasil prediksi secara instant!
    """)
    
    st.markdown("---")
    
    st.info("💡 Tips: Setiap model telah dilatih dengan dataset yang relevan untuk memberikan prediksi akurat")

elif select_var == "Iris Species":
    st.write("""
    This app predicts the **Iris Species**

    Data obtained from the [iris dataset](https://www.kaggle.com/uciml/iris) by UCIML. 
    """)

    st.sidebar.header('User Input Features:')
    uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"])
    if uploaded_file is not None:
            input_df = pd.read_csv(uploaded_file) ## convert to dataframe
    else:
        def user_input_features():
            st.sidebar.header('Input Manual')
            SepalLengthCm = st.sidebar.slider('Sepal Length (cm)', min_value=4.3, value=6.5, max_value=10.0)
            SepalWidthCm = st.sidebar.slider('Sepal Width (cm)', min_value=2.0, value=3.3, max_value=5.0)
            PetalLengthCm = st.sidebar.slider('Petal Length (cm)',min_value= 1.0, value=4.5, max_value=9.0)
            PetalWidthCm = st.sidebar.slider('Petal Width (cm)',min_value= 0.1, value=1.4, max_value=5.0)
            data = {'SepalLengthCm': SepalLengthCm,
                    'SepalWidthCm': SepalWidthCm,
                    'PetalLengthCm': PetalLengthCm,
                    'PetalWidthCm': PetalWidthCm}
            features = pd.DataFrame(data, index=[0]) #convert to dataframe
            return features
        input_df = user_input_features()

    button_var = st.sidebar.button('Submit')

    st.image("https://s3.amazonaws.com/assets.datacamp.com/blog_assets/Machine+Learning+R/iris-machinelearning.png", width=500)

    if button_var:
        df = input_df
        st.write(df) # show the input data

        with open("generate_iris.pkl", 'rb') as file:  
            loaded_model = pickle.load(file) # load previous trained model
            prediction = loaded_model.predict(df) # do prediction according to input value
            result = ['Iris-setosa' if prediction == 0 else ('Iris-versicolor' if prediction == 1 else 'Iris-virginica')]
            output = result[0]  
            st.subheader('Prediction: ')
            with st.spinner('Wait for it...'):
                time.sleep(4)
                st.success(f"Prediction of this app is {output}")

if select_var == "Heart Disease":   
    st.write("""
    This app predicts the **Heart Disease**

    Data obtained from the [heart disease dataset](https://www.kaggle.com/ronitf/heart-disease-uci) by Ronit Fartaria. 
    """)
    st.sidebar.header('User Input Features:')
    uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"])
    if uploaded_file is not None:
            input_df = pd.read_csv(uploaded_file) ## convert to dataframe
    else:
        def user_input_features():
            st.sidebar.header('Input Manual')
            chest_pain_map = {
                "Typical Angina": 0,
                "Atypical Angina": 1,
                "Non-Anginal Pain": 2,
                "Asymptomatic": 3
            }
            wcp = st.sidebar.selectbox('Chest pain type', options=list(chest_pain_map.keys()), help="Type of chest pain experienced")
            cp = chest_pain_map[wcp]

            thalach = st.sidebar.number_input('Maximum Heart Rate Achieved', min_value=60, value=150, max_value=220, step=1, help="Maximum heart rate achieved during exercise")
            slope = st.sidebar.selectbox('Slope of ST Segment', options=[0, 1, 2], index=0, help="Slope of the peak exercise ST segment")
            oldpeak = st.sidebar.number_input('Oldpeak', min_value=0.0, value=1.0, max_value=6.2, step=0.1, help="ST depression induced by exercise relative to rest")
            exang = st.sidebar.radio('Exercise Induced Angina', options=['Yes', 'No'], index=0, help="Whether exercise induced angina is present")
            if exang == 'Yes':
                exang = 1
            else:
                exang = 0
            ca = st.sidebar.selectbox('Number of Major Vessels', options=[0, 1, 2, 3], index=0, help="Number of major vessels colored by fluoroscopy")
            thal = st.sidebar.selectbox('Thalassemia', options=[1, 2, 3], index=0, help="Thalassemia result")
            sex= st.sidebar.radio('Sex', options=['Male', 'Female'], index=0)
            if sex=="Female":
                sex=0
            else :
                sex=1
            age = st.sidebar.number_input('Age', min_value=29, max_value=77, value=30, step=1, help="Age of the patient in years")
            
            data = {'sex': sex,
                    'age': age,
                    'cp': cp,
                    'thalach': thalach,
                    'slope': slope,
                    'exang': exang,
                    'ca': ca,
                    'thal': thal,
                    'oldpeak': oldpeak}
            
            # Create a DataFrame from the input data
            features = pd.DataFrame(data, index=[0])
            return features
        
        input_df = user_input_features()
        st.image("https://drramjimehrotra.com/wp-content/uploads/2022/09/Women-Heart-Disease-min-resize.png", width=300)

        if st.sidebar.button('Predict!'):
            df= input_df
            st.write(df)
            with open("full_heart_disease_pipeline.pkl", 'rb') as file:  
                loaded_model = pickle.load(file)

            prediction_proba = loaded_model.predict_proba(df)
            if prediction_proba[:,1] >= 0.4:
                prediction = 1
            else: 
                prediction = 0
            
            result = ['No Heart Disease Risk' if prediction == 0 else 'Heart Disease Risk Detected']
            
            # Print the prediction result
            st.subheader('Prediction: ')
            output = str(result[0])
            with st.spinner('Wait for it...'):
                time.sleep(4)
                if output == "No Heart Disease Risk":
                    st.success(f"Prediction : {output}")
                if output == "Heart Disease Risk Detected":
                    st.error(f"Prediction : {output}")
                    st.info("Please consult a doctor for further evaluation and advice.")
                st.write("Probability of Heart Disease Risk: {:.2f}%".format(prediction_proba[:,1][0] * 100))
