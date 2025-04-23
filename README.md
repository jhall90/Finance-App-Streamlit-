# 💸 Simple Finance App

This is a lightweight, interactive finance app built with Python and Streamlit to help you make sense of your spending. Just upload a CSV bank statement and start categorizing!

---

## 🚀 Features

-   📁 **Upload Your Bank Statement (CSV)**  
    A sample CSV is included in the repository to help you get started.

-   🏷️ **Custom Categories**  
    Add your own categories to keep things organized. In the **Debit** tab, double-click the “Category” column to:

    -   View all existing categories
    -   Assign a category to a transaction
    -   Automatically update all records with matching descriptions

-   📊 **Visual Spending Breakdown**  
    A Plotly pie chart at the bottom of the Debit tab shows how your spending is distributed across categories.

-   💰 **Incoming Payments Overview**  
    In the **Payments** tab, you’ll see a live metric showing the total amount paid **to you** — perfect for tracking income.

---

## 🛠️ Tech Stack

-   [Python](https://www.python.org/)
-   [Streamlit](https://streamlit.io/)
-   [Pandas](https://pandas.pydata.org/)
-   [Plotly Express](https://plotly.com/python/plotly-express/)

---

## 📦 How to Run It

1. **Clone the repo**

    ```bash
    git clone https://github.com/yourusername/simple-finance-app.git
    cd simple-finance-app
    ```

2. **Create a virtual environment**

    - **macOS/Linux:**

        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

    - **Windows (Command Prompt):**

        ```cmd
        python -m venv venv
        venv\Scripts\activate
        ```

    - **Windows (PowerShell):**
        ```powershell
        python -m venv venv
        .\venv\Scripts\Activate.ps1
        ```

3. **Create a virtual environment**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run Streamlit **

    - Opens a port in your browser for you
    - after saving you just click reload

    ```bash
    streamlit run main.py
    ```
