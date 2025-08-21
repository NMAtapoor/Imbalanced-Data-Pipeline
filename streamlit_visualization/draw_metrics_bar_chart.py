import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd

def visualize_perf_metrics_barchart(metrics, model, df: pd.DataFrame):
    #col1, col2= st.columns(2)
    #with col1:
    #st.success("Line Chart of Accuracy")
    fig, ax = plt.subplots()
    ax.bar(df["Dataset"], df[metrics], color='#8C9DCF')
    ax.set_xlabel("Dataset")
    ax.set_title(f"{model} Model {metrics} performance metrics visualization", color = "grey")
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