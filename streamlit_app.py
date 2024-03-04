import streamlit as st
import altair as alt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder

def app():
    if "reset_app" not in st.session_state:
        st.session_state.reset_app = False

    if "user_inputs" not in st.session_state:
        st.session_state['user_inputs'] = []

    if "clf" not in st.session_state:
        st.session_state["clf"] = []

    #initialize the slider variables
    if "initial_payment" not in st.session_state:        
        st.session_state['initial_payment'] = 200
    if "last_payment" not in st.session_state:
        st.session_state['last_payment'] = 12000
    if "credit_score" not in st.session_state:
        st.session_state['credit_score'] = 500
    if "house_number" not in st.session_state:
        st.session_state['house_number'] = 4000

    # Use session state to track the current form
    if "current_form" not in st.session_state:
        st.session_state["current_form"] = 1    

    # Display the appropriate form based on the current form state
    if st.session_state["current_form"] == 1:
        display_form1()
    elif st.session_state["current_form"] == 2:
        display_form2()
    elif st.session_state["current_form"] == 3:
        display_form3()

def display_form1():
    st.session_state["current_form"] = 1
    form1 = st.form("intro")

    # Display the DataFrame with formatting
    form1.title("Students' Adaptivity Level Prediction in Online Education")
    text = """(c) 2024 Louie F. Cervantes, M.Eng. [Information Engineering] 
    CCS 229 - Intelligent Systems
    Computer Science Department
    College of Information and Communications Technology
    West Visayas State University"""
    form1.text(text)
                
    form1.subheader('Decision Tree')
    text = """A very fast classfier but vulnerable to overfitting. May struggle with 
    overlapping clusters due to rigid decision boundaries. Misclassification is 
    likely at the cluster overlap regions.  Simple to interpret, efficient training."""
    form1.write(text)

    form1.subheader('Random Forest')
    text = """Generally handles overlapping clusters better than decision trees due 
    to averaging predictions from multiple trees. Can still have issues with 
    highly overlapped clusters. Ensemble method, improves robustness and reduces 
    overfitting compared to single decision trees."""
    form1.write(text)

    form1.subheader('Extreme Random Forest')
    form1.write("""Often shows better performance on overlapping clusters than both 
    decision trees and random forests. This is due to additional randomization in 
    feature selection and splitting criteria. Builds on random forests by 
    introducing additional randomness in feature selection and splitting criteria, 
    potentially improving performance on complex data.""")

    form1.subheader('Adativity Level Dataset')
    text = """The adaptivity dataset contains information about 
    the adaptivity of students in an online learning environment. 
    It has 1205 data points, representing individual students. 
    There are 14 features, including:
    Demographic information:
    Gender, Age, Education Level, Institution Type, Location
    \nLearning environment: IT Student, Load-shedding, 
    Financial Condition, Internet Type, Network Type, 
    Class Duration
    \nStudent behaviour: Self Lms, Device
    \nTarget variable: Adaptivity Level"""
    form1.write(text)

    # Create the selecton of classifier
    clf = DecisionTreeClassifier()
    options = ['Decision Tree', 'Random Forest Classifier', 'Extreme Random Forest Classifier']
    selected_option = form1.selectbox('Select the classifier', options)
    if selected_option =='Random Forest Classifier':
        clf = RandomForestClassifier(n_jobs=2, random_state=0)
    elif selected_option=='Extreme Random Forest Classifier':        
        clf = ExtraTreesClassifier(n_estimators=100, max_depth=4, random_state=0)        
    else:
        clf = DecisionTreeClassifier()

    #save the clf to session state
    st.session_state['clf'] = clf

    submit1 = form1.form_submit_button("Start")
    if submit1:
        # Go to the next form        
        display_form2()

def display_form2():
    st.session_state["current_form"] = 2
    form2 = st.form("training")
    form2.subheader('Classifier Training')        

    #load the data and the labels
    dbfile = 'adaptability.csv'
    df = pd.read_csv(dbfile, header=0)

    #display the data set
    form2.write('Browse the dataset')
    form2.write(df)

    form2.write('The dataset descriptive stats')
    form2.write(df.describe().T)

    fig, ax = plt.subplots(figsize=(6, 2))

    # Create the horizontal barplot
    sns.countplot(y='Adaptivity Level', data=df, hue='Adaptivity Level', palette='bright', ax=ax)

    # Add the title
    ax.set_title('Distribution of Adaptivity Level')
    # Display the plot using Streamlit
    form2.pyplot(fig)
    form2.write("""Figure 1. The data shows the distribution of respondents as to their Adaptivity Level""")
    
    # Plot the Gender and Adaptivity
    fig, ax = plt.subplots(figsize=(6, 3))
    # Create the countplot with clear title and legend
    p = sns.countplot(x='Gender', data = df, hue='Adaptivity Level',  palette='bright')
    ax.set_title("Adaptivity Grouped by Sex", fontsize=14)
    legend = ax.legend(loc='upper right', bbox_to_anchor=(1.2, 1))
    # Display the plot
    plt.tight_layout()  # Prevent overlapping elements
    form2.pyplot(fig)

    # Plot the Device and Adaptivity
    fig, ax = plt.subplots(figsize=(6, 3))
    # Create the countplot with clear title and legend
    p = sns.countplot(x='Device', data = df, hue='Adaptivity Level',  palette='bright')
    ax.set_title("Adaptivity Grouped by Device", fontsize=14)
    legend = ax.legend(loc='upper right', bbox_to_anchor=(1.2, 1))
    # Display the plot
    plt.tight_layout()  
    form2.pyplot(fig)

    # Plot the Class Duration and Adaptivity
    fig, ax = plt.subplots(figsize=(6, 3))
    # Create the countplot with clear title and legend
    p = sns.countplot(x='Class Duration', data = df, hue='Adaptivity Level',  palette='bright')
    ax.set_title("Adaptivity Grouped by Class Duration", fontsize=14)
    legend = ax.legend(loc='upper right', bbox_to_anchor=(1.2, 1))
    # Display the plot
    plt.tight_layout()  
    form2.pyplot(fig)

    le = LabelEncoder()
    #Get the list of column names
    column_names = df.columns.tolist()
    # Loop through each column name
    for cn in column_names:
        df[cn] = le.fit_transform(df[cn])

    # Separate features and target variable
    X = df.drop('Adaptivity Level', axis=1)  # Target variable column name
    y = df['Adaptivity Level']
    
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create and train the classifer
    clf = st.session_state['clf']
    clf.fit(X_train, y_train)
    st.session_state["clf"] = clf

    # Make predictions on the test set
    y_test_pred = clf.predict(X_test)

    form2.subheader('Confusion Matrix')
    cm = confusion_matrix(y_test, y_test_pred)
    form2.text(cm)

    form2.subheader('Performance Metrics')
    form2.text(classification_report(y_test, y_test_pred))
        
    submit2 = form2.form_submit_button("Predict")
    if submit2:        
        display_form3()

def display_form3():
    st.session_state["current_form"] = 3
    form3 = st.form("prediction")
    form3.subheader('Prediction')
    form3.write('The trained model will predict if a debtor will repay the loan or not')

    update_values()

    predictbn = form3.form_submit_button("Predict")
    if predictbn:
        user_inputs = np.array(st.session_state['user_inputs'])

        form3.write(user_inputs)

        predicted =  st.session_state["clf"].predict(test_data_scaled)
        result = 'Will the debtor pay? The model predicts: ' + predicted[0]
        form3.subheader(result)

    submit3 = form3.form_submit_button("Reset")
    if submit3:
        st.session_state.reset_app = True
        st.session_state.clear()
        form3.write('Click reset again to reset this app.')

def update_values():
    """Get the updated values from the sliders."""
    initial_payment = st.session_state['initial_payment']
    last_payment = st.session_state['last_payment']
    credit_score = st.session_state['credit_score']
    house_number = st.session_state['house_number']

    st.session_state['user_inputs'] = [[initial_payment, 
        last_payment, credit_score, house_number]]

if __name__ == "__main__":
    app()
