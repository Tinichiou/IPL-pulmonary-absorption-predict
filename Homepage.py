import streamlit as st
import pandas as pd
import numpy as np
import subprocess
# import rpy2.robjects as robjects

st.set_page_config(
    page_title="IPL App"
)

st.title("Main Page")
st.sidebar.success("Select a page above.")



# def load_data():
#     return pd.DataFrame(
#         {
#             "logka": np.array([1, 2, 3, 4]),
#             "ka": np.array([1, 2, 3, 4]),
#             "absorption half-time": [5,5,5,5]
#         }
#     )


# df = load_data()
# st.dataframe(df, use_container_width=True)
