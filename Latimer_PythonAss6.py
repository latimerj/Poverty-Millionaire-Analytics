import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

st.title("Poverty & Millionaire Analytics Dashboard")

st.write(
    "Upload the Poverty/Millionaire Excel dataset to explore poverty counts, "
    "millionaire counts, millionaire density, and poverty rates across U.S. states."
)

# File uploader
uploaded_file = st.file_uploader(
    "Upload the Poverty/Millionaire Excel file",
    type=["xlsx"]
)

if uploaded_file is not None:
    # Read the Excel file
    df = pd.read_excel(uploaded_file)

    # ---- CHANGE THESE COLUMN NAMES TO MATCH YOUR EXCEL FILE ----
    STATE_COL = "State"                  # should be state abbreviations for the map (e.g., MD, VA, CA)
    POP_COL = "State Popiulation"        #spelled incorrectly in excel
    POVERTY_COL = "Number in Poverty"
    MILLION_COL = "Number of Millionaires"
    # ------------------------------------------------------------

    # Calculated fields
    df["Millionaire_Density"] = df[MILLION_COL] / df[POP_COL]
    df["Poverty_Rate"] = df[POVERTY_COL] / df[POP_COL]

    # Tabs for questions
    tab1, tab2, tab3 = st.tabs([
        "Q1: Poverty vs Millionaires",
        "Q2: Millionaire Density Map",
        "Q3: Poverty Rate"
    ])

    # Q1: Side-by-side bar chart (poverty vs millionaires)
    with tab1:
        st.subheader("Question 1: Compare Poverty vs Millionaire Population Across States")

        states = sorted(df[STATE_COL].unique()) #creates a clean list of states.unique no duplicates and sorted alphabetically
        default_states = states[:5] if len(states) >= 5 else states #default selection to ensure chart appears on page open

        #dropdown with all possible states and a default of 5 already selected
        selected_states = st.multiselect(
            "Select at least 5 states:",
            options=states,
            default=default_states
        )

        if len(selected_states) > 0: #ensures atleast one state was selected
            subset = df[df[STATE_COL].isin(selected_states)] #filter to only keep slected row data

            fig, ax = plt.subplots(figsize=(10, 5)) #sets figure size

            x = range(len(subset)) #generates axis posirion
            width = 0.4 #set bar width 
            #draw bars
            ax.bar(
                [i - width / 2 for i in x], #move bars to the left
                subset[POVERTY_COL], #height of each bar based on dataset
                width=width,        
                label="Number in Poverty"  #name for legend
            )

            ax.bar(
                [i + width / 2 for i in x], #move bar to right
                subset[MILLION_COL],
                width=width,
                label="Number of Millionaires"
            )

            ax.set_xticks(list(x)) #where to place labels
            ax.set_xticklabels(subset[STATE_COL], rotation=45, ha="right") #set bar label using state name stop names from overlapping
            ax.set_ylabel("Number of People") #add y axis
            ax.set_title("Poverty vs Millionaire Population by State") #chart title
            ax.legend() #display legend

            st.pyplot(fig) #display chart in streamlit

    # Q2: Millionaire Density Map (choropleth)
    with tab2:
        st.subheader("Question 2: Millionaire Density by U.S. State")

        fig_map = px.choropleth(
            df,
            locations=STATE_COL,
            locationmode="USA-states",
            color="Millionaire_Density",
            scope="usa",
            hover_data={
                STATE_COL: True,
                POP_COL: True,
                MILLION_COL: True,
                "Millionaire_Density": ":.6f"
            },
            title="Millionaire Density by U.S. State"
        )

        fig_map.update_layout(
            coloraxis_colorbar=dict(
                title="Millionaires / Population"
            )
        )

        st.plotly_chart(fig_map)

    # Q3: Poverty Rate (horizontal bar chart)
    with tab3:
        st.subheader("Question 3: Poverty Rate Across States")

        df_sorted = df.sort_values("Poverty_Rate", ascending=False).copy()
        df_sorted["Poverty_Rate_Percent"] = df_sorted["Poverty_Rate"] * 100

        fig2, ax2 = plt.subplots(figsize=(10, 10))

        ax2.barh(
            df_sorted[STATE_COL],
            df_sorted["Poverty_Rate_Percent"]
        )

        ax2.set_xlabel("Poverty Rate (%)")
        ax2.set_ylabel("State")
        ax2.set_title("Poverty Rate by State (Highest to Lowest)")
        ax2.invert_yaxis()

        st.pyplot(fig2)

else:

    st.info("Please upload the Poverty/Millionaire Excel file to begin.")

