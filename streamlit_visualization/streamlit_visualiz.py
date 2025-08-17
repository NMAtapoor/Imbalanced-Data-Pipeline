import pandas as pd
import streamlit as st
from train_svm_model import train_svm_model
from train_knn_model import train_knn_model
from train_randforest_model import train_randforest_model
from read_abalone_csv_files import read_abalone_csv_files
import matplotlib.pyplot as plt
import base64

def datasets_stats(data_dic: dict[str, pd.DataFrame]):
    col1, col2, col3, col4 = st.columns(4)
    for key, df in data_dic.items():
        with col1:
            st.success(f"{key}")
        with col2:
            minority_count = df["Class"].value_counts().get("P", 0)  # returns 0 if 'P' is missing
            
            st.success(f"Minority: {minority_count}")
        with col3:
            
            majority_count = df["Class"].value_counts().get("N", 0)
            st.success(f"Majority: {majority_count}")
            
        with col4:
            minority_count = df["Class"].value_counts().get("P", 0)
            majority_count = df["Class"].value_counts().get("N", 0)
            imb_rate = (round(minority_count/majority_count,2)*100)
            st.success(f"IR: {imb_rate}%")
    return " "

def visualize_perf_metrics(metrics, df: pd.DataFrame):
    #col1, col2= st.columns(2)
    #with col1:
    #st.success("Line Chart of Accuracy")
    fig, ax = plt.subplots()
    ax.plot(df["Dataset"], df[metrics], marker='o', 
            linestyle='--', color='blue', label= metrics, markersize=2, linewidth=0.5)
    #ax.set_title(f"{"Accuracy"} per Dataset")
    ax.set_xlabel("Dataset")
    ax.set_ylabel(metrics)
    ax.legend()
    ax.grid(True)
    ax.set_xlabel("20 Imbalance Abalone Dataset", fontsize=8)  # X-axis label
    ax.set_ylabel(metrics, fontsize=8) # Y-axis label

# Tick labels with smaller font
    ax.tick_params(axis='x', labelsize=5)  # X-axis ticks
    ax.tick_params(axis='y', labelsize=5)
    ax.grid(True, color='green', linestyle='--', linewidth=0.1)
    ax.spines['top'].set_color('yellow')
    ax.spines['top'].set_linewidth(0.5)

    ax.spines['bottom'].set_color('yellow')
    ax.spines['bottom'].set_linewidth(0.5)

    ax.spines['left'].set_color('yellow')
    ax.spines['left'].set_linewidth(0.5)

    ax.spines['right'].set_color('yellow')
    ax.spines['right'].set_linewidth(0.5)
    plt.xticks(rotation=90)
    st.pyplot(fig)
    #with col2:
       # st.success("Done")
    return " "
# Initialize session state
if "data_dict" not in st.session_state:
    st.session_state.data_dict = None
if "results_df" not in st.session_state:
    st.session_state.results_df = None
if "model_to_train" not in st.session_state:
    st.session_state.model_to_train = None
    
#st.sidebar.image("../data/image/aiimage.jpeg", width=150, heigth )


# Read local image and encode as base64
file_path = "../data/image/ai_image.jpg"
with open(file_path, "rb") as f:
    data = f.read()
encoded = base64.b64encode(data).decode()

# Inject with fixed size
st.sidebar.markdown(
    f"""
    <style>
    .custom-img {{
        width: 300px;
        height: 150px;
        object-fit: cover;
        border-radius: 8px;
    }}
    </style>
    <img class="custom-img" src="data:image/jpeg;base64,{encoded}" />
    """,
    unsafe_allow_html=True
)

file_path = "../data/image/ai_image2.jpeg"
with open(file_path, "rb") as f:
    data = f.read()
encoded = base64.b64encode(data).decode()

# Inject with fixed size
st.markdown(
    f"""
    <style>
    .custom-img {{
        width: 800px;
        height: 100px;
        object-fit: cover;
        border-radius: 8px;
    }}
    </style>
    <img class="custom-img" src="data:image/jpeg;base64,{encoded}" />
    """,
    unsafe_allow_html=True
)
# Sidebar: Load CSV files


st.sidebar.header("Load Datasets")
folder_path = "../data/data_versions/"  # replace with your folder path

if st.sidebar.button("Extract Datasets"):
    st.session_state.data_dict = read_abalone_csv_files(folder_path)
    st.session_state.results_df = None  # reset previous results
    st.success(f"All the {len(st.session_state.data_dict)} Imbalanced Datasets Was Extracted!")
    datasets_stats(st.session_state.data_dict)
    

# Sidebar: Train models (only shown if datasets are loaded)
if st.session_state.data_dict is not None:
    st.sidebar.subheader("Train Models")
    
    if st.sidebar.button("Train SVM Model"):
        st.session_state.results_df = train_svm_model(st.session_state.data_dict)
        st.session_state.model_to_train = "SVM"
    
    if st.sidebar.button("Train KNN Model"):
        st.session_state.results_df = train_knn_model(st.session_state.data_dict)
        st.session_state.model_to_train = "KNN"
    
    if st.sidebar.button("Train RF Model"):
        st.session_state.results_df = train_randforest_model(st.session_state.data_dict)
        st.session_state.model_to_train = "RF"


# Main page: Show results
##st.success("")
if st.session_state.results_df is not None and not st.session_state.results_df.empty:
    
# Add slider above dataframe
    num_rows = st.slider(
    f"Select number of rows to display the {st.session_state.model_to_train} Performance Metrics",
    min_value=1,
    max_value=len(st.session_state.results_df),
    value=5

)

# Limit dataframe rows by slider value
    df_display = st.session_state.results_df.head(num_rows)

# Display HTML table
    st.markdown(
    df_display.to_html(index=False),
    unsafe_allow_html=True
)

# Add CSS to make slider full-width, table full-width, and smaller font
    st.markdown(
    """
    <style>
    /* Style the slider track */
    div.stSlider > div[data-baseweb="slider"] > div {
        background: linear-gradient(to right, #ff7eb9, #ff65a3, #7afcff, #feff9c, #fff740);
        height: 5px;
        border-radius: 10px;
    }

    /* Style the slider handle (thumb) */
    div.stSlider > div[data-baseweb="slider"] > div > div {
        background-color: #ff4b4b;
        border: 2px solid white;
        height: 10px;
        width:100% !important;
    }
    table {
        font-size: 12px;
        width: 100% !important;
        border-collapse: collapse;
    }
    th, td {
        padding: 4px 8px;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

if st.session_state.results_df is not None:
   
    col1, col2 = st.columns([1,4])
    with col1:
        option = st.radio(
        "Choose Metrics:",
        ["Accuracy", "F1_Score","Precision","Recall","Kappa","AUC"],
        index=0,
        key="model_radio"
)
    with col2:    
        visualize_perf_metrics(option, st.session_state.results_df)

else:
    st.write("No results to show. Train a model first!")





