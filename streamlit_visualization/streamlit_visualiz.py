import pandas as pd
import streamlit as st
from train_svm_model import train_svm_model
from train_knn_model import train_knn_model
from train_randforest_model import train_randforest_model
from read_abalone_csv_files import read_abalone_csv_files
import matplotlib.pyplot as plt
import base64
import os
#-------------------------------------------------------------------

st.set_page_config(layout="wide")

st.markdown("""
<style>

    /* Main page background */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(to right, #8ABCDE, #EBF4F9);
        min-height: 100vh;
        padding: 0;
        margin: 0;
    }
.banner {
        position: fixed;       /* stick at top */
        top: 0;                /* top of the page */
        left: 0;
        width: 100%;           /* full width */
        background: linear-gradient(#131335, #36369B, #CACAEC);
        padding: 20px;
        text-align: center;
        color: white;
        font-size: 30px;
        font-weight: bold;
        z-index: 9999;         /* stay above other elements */
    }

    /* Add spacing at the top of the page so content is not hidden behind banner */
        .app-content {
        margin-top: 80px;
    }
    
     /* Style the slider track */
    div.stSlider > div[data-baseweb="slider"] > div {
        background: linear-gradient(to right, #282A33, #304ABA, #5969A8, #A8B6F0);
        height: 2px;
        border-radius: 6px;
        border: 1px solid black;
        
    }
    
    table {
        font-size: 14px;
        width: 100% !important;
        border-collapse: collapse;
        border: 2px solid #CFD4B5;
    }
    th, td {
        padding: 4px 8px;
        text-align: center;
    }
    th {
    background-color: #697BC3;  /* Header background color */
    color: black; /* Header text color */
    text-align: center;
    }

    /* Optional: make the top header transparent */
    [data-testid="stHeader"]{
      background: rgba(0,0,0,0);
        }
div[role='radiogroup'] > label {
        background-color: #CCE5EA; /* default background */
        padding: 6px 12px;
        border-radius: 8px;
        margin-right: 8px;
        cursor: pointer;
        }
div[role='radiogroup'] > label:hover {
    background-color: #C2DFFF; /* background color on hover */
    transform: scale(1.05);     /* subtle zoom effect */
}
/* Container for radio buttons on main page */
.stRadio > div {
    display: flex;
    flex-direction: row;
    gap: 40px;  /* spacing between options */
}


/* Sidebar background */
    [data-testid="stSidebar"] > div:first-child {
        background: linear-gradient(to bottom, #131335, #5CA2D1, #CACAEC);
        color: #242B2D;
        padding: 10px;
    }

    /* Sidebar header style */
    [data-testid="stSidebar"] h2 {
        color: #224ABF;
        font-size: 24px;
        font-weight: bold;
        text-align: left;
        margin-bottom: 20px;
    }

   
    .custom-img {
        width: 500px;
        height: auto;
        border-radius: 15px;
        
        margin: 20px auto;
        display: block;
    }
   
    section[data-testid="stSidebar"] button {
    background-color: #429ABD;   /* green background */
    color: white;
    width: 100% !important;/* white text */
    font-size: 16px;             /* larger font */
    font-weight: bold;           /* bold text */
    border-radius: 8px;          /* rounded corners */
    border: 1px solid #3e8e41;   /* darker border */
    padding: 8px 16px;
    transition: 0.3s;
}

/* Hover effect */
section[data-testid="stSidebar"] button:hover {
    background-color: #193A47;   /* darker green on hover */
    border: 1px solid #2d7032;
    transform: scale(1.05);      /* slight zoom */
}

/* Optional: make text uppercase */
section[data-testid="stSidebar"] button p {
    text-transform: uppercase;
}

</style>
<div class="banner">
        Examine Impact of Imbalance Data on ML Models
    </div>

""", unsafe_allow_html=True)



#--------------------------------------------------------------------

def datasets_stats(data_dic: dict[str, pd.DataFrame]):
    #col1, col2, col3, col4 = st.columns(4)
    data = []
    for key, df in data_dic.items():
        #with col1:
        col1 = key
        #st.success(f"{key}")
        #with col2:
            #minority_count = df["Class"].value_counts().get("P", 0)  # returns 0 if 'P' is missing
        col2 = df["Class"].value_counts().get("P", 0)
            #st.success(f"Minority: {minority_count}")
        #with col3:
        col3 = df["Class"].value_counts().get("N", 0)

            
        #with col4:
        col4 = f"{(round(col2/col3,2)*100)}%"
        data.append([col1,col2,col3,col4])
    data_stat_df = pd.DataFrame(data, columns=["Name", "Minority", "Majority", "IR (min/maj)"])
    return data_stat_df

def visualize_perf_metrics_linechart(metrics, df: pd.DataFrame):

    fig, ax = plt.subplots()
    ax.plot(df["Dataset"], df[metrics], marker='o', 
            linestyle='--', color='blue', label= metrics, markersize=3, linewidth=0.5)
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
def visualize_perf_metrics_barchart(metrics, df: pd.DataFrame):
    #col1, col2= st.columns(2)
    #with col1:
    #st.success("Line Chart of Accuracy")
    fig, ax = plt.subplots()
    ax.bar(df["Dataset"], df[metrics], color='#8C9DCF')
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
    ax.set_ylim(df[metrics].min(), df[metrics].max())
    st.pyplot(fig)
    return " "

# Initialize session state
if "data_dict" not in st.session_state:
    st.session_state.data_dict = None
if "results_df" not in st.session_state:
    st.session_state.results_df = None
if "model_to_train" not in st.session_state:
    st.session_state.model_to_train = None
if "data_stat" not in st.session_state:
    st.session_state.data_stat = None
    
#st.sidebar.image("../data/image/ai_image2.jpeg", width=150 )


st.sidebar.write("Please, Load Data First!")
folder_path = "../data/data_versions/"  # replace with your folder path

if st.sidebar.button("Extract Datasets"):
    st.session_state.data_dict = read_abalone_csv_files(folder_path)
    st.session_state.results_df = None  # reset previous results
    
    st.session_state.data_stat = datasets_stats(st.session_state.data_dict)
    

# Sidebar: Train models (only shown if datasets are loaded)
if st.session_state.data_dict is not None:
    #st.sidebar.subheader("Train Models")
    st.sidebar.write("To Train Model, Click Bellow!")
    
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
    st.subheader(f"{st.session_state.model_to_train} model was trained, and below is its performance metrics list")
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
    df_display.to_html(index=False ,classes= "mytable"),
    unsafe_allow_html=True
    )

if st.session_state.results_df is not None:
    option = st.radio(
    "Choose Metrics:",
    ["Accuracy", "F1_Score","Precision","Recall","Kappa","AUC"],
    index=0,
    key="model_radio",
    horizontal=True)
    col1, col2 = st.columns(2)
    with col1:
        visualize_perf_metrics_barchart(option, st.session_state.results_df)
    with col2:    
        visualize_perf_metrics_linechart(option, st.session_state.results_df)
        

else:
    def get_base64_of_image(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()

    img_base64 = get_base64_of_image("../data/image/ai_image.jpg")
    col1, col2 = st.columns(2)
    
    with col1:
    
        st.subheader("Imbalanced-Data-Pipeline (IPD)")
        st.write("""is a capstone project developed for the Data Engineering training program at Digital Future Academy.
                The project focuses on extracting, cleaning, transforming, and synthetically generating multiple versions of an imbalanced dataset with varying imbalance rates using oversampling techniques, and then loading the results into a database.
                In addition, the project trains several machine learning models on these imbalanced datasets to examine the impact of imbalance rates on model performance.
                The evaluation includes algorithms such as K-Nearest Neighbors (KNN), Support Vector Machine (SVM), and Random Forest.
                """)
    with col2:
        st.markdown(
        f"""
        <img class="custom-img" src="data:image/png;base64,{img_base64}" alt="Local Image">
        """,
        unsafe_allow_html=True)
         
    # display the stats table for extracted datasets
    if st.session_state.data_stat is not None:
        st.success(f" {len(st.session_state.data_dict)} Imbalanced Datasets Were Extracted Successfully!")
        num_rows = st.slider(
        f"Scroll To Change The Extracted Datasets:",
        min_value=1,
        max_value= 20,
        value=5
        )
        stat_df = st.session_state.data_stat.head(num_rows)
        st.markdown(
        stat_df.to_html(index=False),
        unsafe_allow_html=True
    )            
      
     
    
    

    

