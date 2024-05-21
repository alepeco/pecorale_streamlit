import streamlit as st
import os
import subprocess
import pandas as pd
import matplotlib.pyplot as plt

# Set up the Kaggle API key
def set_kaggle_api_key():
    kaggle_api_key = st.secrets["KAGGLE_API_KEY"]
    os.environ["KAGGLE_USERNAME"] = st.secrets["KAGGLE_USERNAME"]
    os.environ["KAGGLE_KEY"] = kaggle_api_key

# Download the dataset from Kaggle
def download_dataset():
    dataset = 'martj42/international-football-results-from-1872-to-2017'
    command = f'kaggle datasets download -d {dataset} --unzip -p ./data'
    subprocess.run(command, shell=True)
    st.success('Dataset downloaded successfully!')

# Load the dataset into a pandas DataFrame
def load_dataset():
    file_path = './data/results.csv'
    if os.path.exists(file_path):
        data = pd.read_csv(file_path)
        return data
    else:
        st.error('Dataset file not found. Please download the dataset first.')
        return None

# Main function to run the Streamlit app
def main():
    st.title('International football results from 1872 to 2017')

    # Set up Kaggle API key
    set_kaggle_api_key()

    # Button to download the dataset
    if st.button('Download Dataset'):
        with st.spinner('Downloading dataset...'):
            download_dataset()

    # Load and display the dataset
    data = load_dataset()
    if data is not None:
        st.subheader('Dataset Preview')
        st.write(data.head())

        # Display options
        display_option = st.radio(
            "Choose how to display the data:",
            ('Table', 'Plot')
        )

        if display_option == 'Table':
            st.dataframe(data)
        
        elif display_option == 'Plot':
            st.subheader('Number of Matches per Year')
            year_slider = st.slider('Select year range:', min_value=int(data['date'].min()[:4]), max_value=int(data['date'].max()[:4]), value=(1872, 2017))
            filtered_data = data[(data['date'].str[:4].astype(int) >= year_slider[0]) & (data['date'].str[:4].astype(int) <= year_slider[1])]
            matches_per_year = filtered_data['date'].str[:4].value_counts().sort_index()
            
            plt.figure(figsize=(10, 5))
            plt.plot(matches_per_year.index, matches_per_year.values, marker='o')
            plt.xlabel('Year')
            plt.ylabel('Number of Matches')
            plt.title('Number of Matches per Year')
            st.pyplot(plt)

if __name__ == "__main__":
    main()
