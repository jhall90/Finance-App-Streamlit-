import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os

st.set_page_config(page_title="Finance App", page_icon="💵", layout="wide")
category_file = "categories.json"

# default set categories to Uncategorized
if "categories" not in st.session_state:
    st.session_state.categories = {
      "Uncategorized": []
    }

# if the file category file exists open and set default categories to existing saved categories.json
if os.path.exists(category_file):
  with open(category_file, "r") as f:
    st.session_state.categories = json.load(f)


def save_categories():
  with open(category_file, "w") as f:
    json.dump(st.session_state.categories, f)

def categorize_transactions(df):
  df["Category"] = "Uncategorized"        # set to Uncategorized by default

  for category, keywords in st.session_state.categories.items():
    if category == "Uncategorized" or not keywords:
      continue

    
    lowered_keywords = [keyword.lower().strip() for keyword in keywords]        # converting all keywords to lower and stripping whitespace

    # there are more efficient ways to do this, but I wanted to get this demo out for my portfolio at the moment
    for idx, row in df.iterrows():                    # iterate over each row like a list so we have access to the values
      details = row["Details"].lower().strip()
      
      if details in lowered_keywords:                 # if the detail is in lowered_keywords it fits that category
        df.at[idx, "Category"] = category

  return df

# Load the csv file or give an error
def load_transactions(file):
  try:
    df = pd.read_csv(file) 
    
    df.columns = [col.strip() for col in df.columns]                  # remove whitespace from the columns incase the csv has random whitespace
    # formatting the amount column 
    df["Amount"] = df["Amount"].str.replace(",", "").astype(float)    # removing whitespace and converting to float so we get them as a number instead of string for math purposes
    df["Date"] = pd.to_datetime(df["Date"], format="%d %b %Y")        # format="date name-of-month year"

    return categorize_transactions(df)
  except Exception as e:
    st.error(f"Error processing file: {str(e)}")
    return None

def add_keyword_to_category(category, keyword):
  keyword = keyword.strip()
  # check if the keyword is already in the category and adds if not
  if keyword and keyword not in st.session_state.categories[category]:
    st.session_state.categories[category].append(keyword)
    save_categories()
    return True
  
  return False

###################################
# Main function 
def main():
  st.title("Finance Dashboard")
  uploaded_file = st.file_uploader("Upload your transaction CSV file", type=["csv"])

  if uploaded_file is not None:
    df = load_transactions(uploaded_file)

    if df is not None:
      # Get a copy of the debit and credit columns to separate
      debits_df = df[df["Debit/Credit"] == "Debit"].copy() 
      credits_df = df[df["Debit/Credit"] == "Credit"].copy()

      # store the dfs in session storage so edited df doesnt overwrite this right away
      st.session_state.debits_df = debits_df.copy()

      #############################
      # Create Tabs

      tab1,tab2 = st.tabs(["Expenses (Debits)", "Payments (Credits)"])
      with tab1:
        new_category = st.text_input("New Category Name")
        add_button = st.button("Add Category")

        # if new_category has some text value in it and add_button is pressed
        if add_button and new_category:
          if new_category not in st.session_state.categories:
            st.session_state.categories[new_category] = []
            save_categories()
            st.rerun()

        st.subheader("Your Expenses")
        edited_df = st.data_editor(
          st.session_state.debits_df[["Date", "Details", "Amount", "Category"]],
          column_config={
            "Date": st.column_config.DateColumn("Date", format="DD/MM/YYYY"),
            "Amount": st.column_config.NumberColumn("Amount", format="%.2f USD"),
            "Category": st.column_config.SelectboxColumn(
              "Category",
              options=list(st.session_state.categories.keys())
            )
          },
          hide_index=True,
          use_container_width=True,
          key="category_editor"
        )

        save_button = st.button("Apply Changes", type="primary")
        
        if save_button:
          for idx, row in edited_df.iterrows():
            new_category = row["Category"]
            if new_category == st.session_state.debits_df.at[idx, "Category"]: #No change made in this row
              continue
            
            # if a change is made 
            details = row["Details"]                                            # Get the location 
            st.session_state.debits_df.at[idx, "Category"] = new_category       # Update the state
            add_keyword_to_category(new_category, details)                      # Save to json file
            

        #############################
        #  Expense Summary

        st.subheader("Expense Summary")
        category_totals = st.session_state.debits_df.groupby("Category")["Amount"].sum().reset_index()      # grabs the Amount from Category of the debits. Sums the amount of all in that category and resets index
        category_totals = category_totals.sort_values("Amount", ascending=False)                            # grab the totals and show in descending order

        # Create the dataframe
        st.dataframe(
          category_totals, 
          column_config= {
            "Amount": st.column_config.NumberColumn("Amount", format="%.2f USD")
          },
          use_container_width=True,
          hide_index=True
        )

      #############################################
      # PLOTLY Express
      # Show charts

      fig = px.pie(
        category_totals,
        values="Amount",
        names="Category",
        title="Expenses by Category"
      )

      st.plotly_chart(
        fig, 
        use_container_width=True
      )

      with tab2:
        st.subheader("Payment Summary")
        total_payments = credits_df["Amount"].sum()
        st.metric("Total Payments", f"{total_payments:,.2f} USD")    # Display the total payments in bigger font
        st.write(credits_df)

# call main function
main()