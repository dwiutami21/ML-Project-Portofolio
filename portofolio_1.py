import streamlit as st
import pickle
import pandas as pd 
import time

st.set_page_config(page_title="ML Portfolio", page_icon="🌸", layout="wide", initial_sidebar_state="expanded")
st.write("Welcome to my ML Portfolio!")

select_var = st.sidebar.selectbox("Select page", ["Home", "Iris Species", "Heart Disease","Obesity Level","Fruit Classification"])

if select_var == "Home":
    st.title("🌸 Welcome to ML Portfolio")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("About This App")
        st.write("""
        Selamat datang di **ML Portfolio** saya! 
        
      Aplikasi ini menyajikan berbagai proyek Machine Learning  
      yang mengimplementasikan model klasifikasi pada dataset real‑world, termasuk dataset populer seperti Iris.
        """)
    
    with col2:
        st.image("https://s3.amazonaws.com/assets.datacamp.com/blog_assets/Machine+Learning+R/iris-machinelearning.png", width=300)
    
    st.markdown("---")
    
    st.subheader("📊 Available Features")
    
    features = {
        "🔍 Iris Species Prediction": "Prediksi jenis Iris berdasarkan karakteristik bunga (Sepal & Petal measurements)",
        "❤️ Heart Disease Prediction": "Prediksi risiko penyakit jantung berdasarkan parameter kesehatan",
        "🍔 Obesity Level Prediction": "Prediksi tingkat obesitas berdasarkan gaya hidup dan metrik tubuh",
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

elif select_var == "Obesity Level":

    st.title("🍔 Obesity Level Prediction")
    st.write("""
    This app predicts **Obesity Level** based on lifestyle and body metrics.
    
    Model trained on Obesity Dataset (7 classes).
    """)

    st.sidebar.header("User Input Features")

    # ===============================
    # Upload CSV
    # ===============================
    uploaded_file = st.sidebar.file_uploader(
        "Upload CSV file",
        type=["csv"]
    )

    if uploaded_file is not None:
        input_df = pd.read_csv(uploaded_file)

    else:
        # ===============================
        # Manual Input
        # ===============================
        def user_input_features():
            weight = st.sidebar.number_input(
                "Weight (kg)", min_value=30.0, max_value=200.0, value=70.0
            )
            age = st.sidebar.number_input(
                "Age", min_value=5, max_value=80, value=25
            )

            family_history = st.sidebar.radio(
                "Family history with overweight",
                ["Yes", "No"]
            )
            family_history = 1 if family_history == "Yes" else 0

            favc = st.sidebar.radio(
                "Frequent High Calorie Food (FAVC)",
                ["Yes", "No"]
            )
            favc = 1 if favc == "Yes" else 0

            fcvc = st.sidebar.slider(
                "Vegetable consumption (FCVC)",
                min_value=1.0, max_value=3.0, value=2.0, step=0.1
            )

            caec_map = {
                "No": 0,
                "Sometimes": 1,
                "Frequently": 2,
                "Always": 3
            }
            caec = st.sidebar.selectbox(
                "Eating Between Meals (CAEC)",
                list(caec_map.keys())
            )
            caec = caec_map[caec]

            faf = st.sidebar.slider(
                "Physical Activity Frequency (FAF)",
                min_value=0.0, max_value=3.0, value=1.0, step=0.1
            )

            calc_map = {
                "No": 0,
                "Sometimes": 1,
                "Frequently": 2,
                "Always": 3
            }
            calc = st.sidebar.selectbox(
                "Alcohol Consumption (CALC)",
                list(calc_map.keys())
            )
            calc = calc_map[calc]

            scc = st.sidebar.radio(
                "Calories Consumption Monitoring (SCC)",
                ["Yes", "No"]
            )
            scc = 1 if scc == "Yes" else 0

            ch2o = st.sidebar.slider(
                "Daily Water Intake (CH2O)",
                min_value=1.0, max_value=3.0, value=2.0, step=0.1
            )

            data = {
                "Weight": weight,
                "family_history_with_overweight": family_history,
                "Age": age,
                "FAVC": favc,
                "FCVC": fcvc,
                "CAEC": caec,
                "FAF": faf,
                "CALC": calc,
                "SCC": scc,
                "CH2O": ch2o
            }

            return pd.DataFrame(data, index=[0])

        input_df = user_input_features()

    st.subheader("Input Data")
    st.write(input_df)

    if st.sidebar.button("Predict Obesity Level"):
        with open("obesity_rf_tuned_model.pkl", "rb") as file:
            model = pickle.load(file)

        prediction = model.predict(input_df)[0]

        label_map = {
            0: "Insufficient Weight",
            1: "Normal Weight",
            2: "Overweight Level I",
            3: "Overweight Level II",
            4: "Obesity Type I",
            5: "Obesity Type II",
            6: "Obesity Type III"
        }

        st.subheader("Prediction Result")
        with st.spinner("Predicting..."):
            time.sleep(2)
            st.success(f"Predicted Obesity Level: **{label_map[prediction]}**")
        
        # Add advice based on prediction
        if prediction == 0:  # Insufficient Weight
            st.info("Berat badan Anda diprediksi Insufficient Weight. Pertimbangkan untuk berkonsultasi dengan ahli gizi untuk memastikan Anda mendapatkan nutrisi yang cukup dan menjaga berat badan yang sehat.")
        elif prediction == 1:  # Normal Weight
            st.info("Berat badan Anda terprediksi Normal Weight. Tetap jaga kesehatan dengan diet sehat serta olahraga teratur.")
        elif prediction == 2:  # Overweight Level I
            st.info("Berat badan Anda diprediksi Overweight Level I. Tingkatkan aktivitas fisik harian dan perhatikan pola makan untuk mencegah peningkatan berat badan.")
        elif prediction == 3:  # Overweight Level II
            st.info("Berat badan Anda diprediksi Overweight Level II. Konsultasikan dengan dokter untuk rencana penurunan berat badan yang aman dan efektif.")
        elif prediction == 4:  # Obesity Type I
            st.info("Berat badan Anda menunjukkan Obesity Type I. Silakan konsultasikan dengan dokter untuk evaluasi kesehatan dan panduan pengelolaan berat badan.")
        elif prediction == 5:  # Obesity Type II
            st.info("Berat badan Anda menunjukkan Obesity Type II. Segera konsultasikan dengan spesialis kesehatan untuk intervensi medis yang diperlukan.")
        elif prediction == 6:  # Obesity Type III
            st.info("Berat badan Anda menunjukkan Obesity Type III. Segera cari bantuan medis profesional untuk penanganan yang komprehensif.")

elif select_var == "Fruit Classification": 
    st.title("🍎 Klasifikasi Buah Pepaya dan Alpukat")
    st.write("""
    Aplikasi ini memprediksi jenis buah (Pepaya atau Alpukat) dari gambar yang diunggah menggunakan model berbasis Pickle.
    """)

    st.sidebar.header("Unggah Gambar Buah")
    uploaded_file_fruit = st.sidebar.file_uploader("Pilih gambar buah...", type=["jpg", "jpeg", "png"])

    if uploaded_file_fruit is not None:
        # Load menggunakan pickle langsung dari root directory seperti model lainnya
        loaded_fruit_model = None
        try:
            with open("model_buah.pkl", 'rb') as file:
                loaded_fruit_model = pickle.load(file)
            st.success("Model Klasifikasi Buah berhasil dimuat!")
        except Exception as e:
            st.error(f"Gagal memuat model_buah.pkl. Pastikan file berada di root folder yang sama. Error: {e}")

        if loaded_fruit_model:
            fruit_class_names = ['alpukat', 'pepaya']
            fruit_img_height = 128
            fruit_img_width = 128

            # Fungsi pemrosesan citra untuk format model Machine Learning konvensional / Scikit-Learn
            def predict_fruit_image(image_file, model, class_names, img_height, img_width):
                # Membuka citra dan mengubah ukuran sesuai kebutuhan ekstraksi fitur model Anda
                image = Image.open(image_file).convert('RGB')
                image = image.resize((img_width, img_height))
                img_array = np.asarray(image)
                
                # Meratakan matriks piksel gambar menjadi 1 dimensi (Flatten) 
                # Sering digunakan jika model pkl berupa SVM, Random Forest, atau KNN.
                flat_img_array = img_array.flatten().reshape(1, -1)

                # Melakukan prediksi kelas buah
                prediction = model.predict(flat_img_array)[0]
                
                # Menangani output berupa index integer ataupun string teks langsung
                if isinstance(prediction, (int, np.integer)):
                    predicted_class = class_names[prediction]
                else:
                    predicted_class = str(prediction)
                
                # Mendapatkan nilai kepastian (jika model pkl mendukung predict_proba)
                try:
                    probabilities = model.predict_proba(flat_img_array)[0]
                    confidence = np.max(probabilities) * 100
                except AttributeError:
                    confidence = 100.0  # Default jika algoritma pkl tidak memiliki fitur probabilitas
                
                return predicted_class, confidence

            st.image(uploaded_file_fruit, caption='Gambar Buah Anda.', use_container_width=True)
            st.write("Memprediksi...")

            with st.spinner('Menganalisis gambar...'):
                time.sleep(1) 
                label, confidence = predict_fruit_image(uploaded_file_fruit, loaded_fruit_model, fruit_class_names, fruit_img_height, fruit_img_width)
                st.success(f"Prediksi: **{label.upper()}** dengan tingkat keyakinan **{confidence:.2f}%**")
    else:
        st.info("Silakan unggah gambar buah (alpukat atau pepaya) di sidebar.")
