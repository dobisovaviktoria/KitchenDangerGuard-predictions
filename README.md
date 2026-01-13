# KDG - Predictions

## Authors
- Khaled Asfour
- Viktória Dobišová
- Nang Cherry Naw
- Deren Ozen
- Alec Tuffin

---
## **Prediction System Overview**
This system predicts continuous temperature values using a **Random Forest Regressor**. Ths repository is dependent on other repositories named Kitchen Danger Guard - backend and arduino. They should be treated as one project and ran together. Below are the steps to set up, run, and understand the system in **PyCharm**.

---
## **Prerequisites**
To run this system, ensure the following Python libraries are installed:
- `os`
- `joblib`
- `sklearn`
- `pandas`
- `numpy`
- `sqlalchemy`
- `flask`
This system is designed to run in a **development environment** like **PyCharm**. Follow the steps below to set it up properly.
---

## **Running the Application in PyCharm**

### **1. Install Required Libraries**
1. Open **PyCharm** and create a new project or open an existing one.
2. Set up a **virtual environment** for the project.
3. Install the necessary libraries:
   - Go to **File > Settings  > Python Interpreter**.
   - Click the **+** icon to search for and install the libraries listed above.

### **2. Configure the Application**
1. Make sure **Python 3.x** is selected as the interpreter.
2. Set up the run configuration to select the main script (e.g., `app.py`).

### **3. Run the Application**
1. Once the environment is set up, click **Run > Run 'Your Script'**.
2. The server should start locally, typically at `http://127.0.0.1:5000`.
---

## **Accessing the Prediction Endpoint**
- Open the prediction page through your browser.
- If the system isn’t running properly, you will encounter an error page.
---

## **Prediction Model**
The system predicts **5 temperature values** using a **Random Forest Regressor**. The number of predictions can be adjusted as needed.

### **Data Interpolation**
- The dataset lacks regular time intervals between data points.
- The system uses the time difference between the last two data points for interpolation to simulate regular intervals.

### **Prediction Validation**

Predictions are validated based on the following:
- **Time Restriction**: Only predictions within the **next 2 hours** are valid.
- **Threshold**: Predictions exceeding a predefined threshold are discarded.
---

## **Handling Invalid Predictions**
- Predictions falling outside the time frame or threshold are ignored.
- Among valid predictions, the closest one to the most recent timestamp is selected and displayed.
---

## **Integration with the Web Application**
- Predictions are returned as **JSON responses** and displayed dynamically using **JavaScript** on the frontend.
---

## **Troubleshooting**
If you see an error page, check the following:
1. Ensure **PyCharm’s virtual environment** is active and the required libraries are installed.
2. Make sure the **Flask server** is running. If not, the web interface will not load.
---

## **Summary**
By following the steps above, you will be able to:
1. Run the application in **PyCharm**.
2. Generate predictions.
3. Display predictions on the web interface.
Ensure the **Python environment** is properly configured, and the application is running before accessing the prediction page.

--- 

