import streamlit as st
import requests
import json
import pandas as pd
from typing import Optional

# Configure Streamlit page
st.set_page_config(
    page_title="Patient Data Management",
    page_icon="🏥",
    layout="wide"
)

# API Configuration
API_BASE_URL = "http://127.0.0.1:8000"  # Change this to your FastAPI server URL

# Helper functions
def make_api_request(method, endpoint, data=None, params=None):
    """Make API request and handle errors"""
    try:
        url = f"{API_BASE_URL}{endpoint}"
        
        if method == "GET":
            response = requests.get(url, params=params)
        elif method == "POST":
            response = requests.post(url, json=data)
        elif method == "PUT":
            response = requests.put(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url)
        else:
            # return None  # Invalid method
            raise ValueError("Invalid HTTP method specified.")
        
        return response
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to the API server. Make sure your FastAPI server is running.")
        return None
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        return None

def display_api_response(response):
    """Display API response in a formatted way"""
    if response and response.status_code == 200:
        return response.json()
    elif response:
        st.error(f"❌ Error {response.status_code}: {response.json().get('detail', 'Unknown error')}")
        return None
    return None

# Main App
def main():
    st.title("🏥 Patient Data Management System")
    st.markdown("---")
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page:",
        ["API Info", "View All Patients", "Get Patient by ID", "Sort Patients", 
         "Add Patient", "Update Patient", "Delete Patient"]
    )
    
    # API Info Page
    if page == "API Info":
        st.header("📋 API Information")
        
        if st.button("Get API Info"):
            response = make_api_request("GET", "/API INFO")
            data = display_api_response(response)
            
            if data:
                st.success("✅ API Info Retrieved Successfully!")
                st.json(data)
    
    # View All Patients Page
    elif page == "View All Patients":
        st.header("👥 All Patients Data")
        
        if st.button("Load All Patients"):
            response = make_api_request("GET", "/view_patients_data")
            data = display_api_response(response)
            
            if data and data.get("status") == "success":
                st.success("✅ Patient data loaded successfully!")
                
                if data["data"]:
                    # Convert to DataFrame for better display
                    patients_list = []
                    for patient_id, patient_info in data["data"].items():
                        patient_row = {"ID": patient_id}
                        patient_row.update(patient_info)
                        patients_list.append(patient_row)
                    
                    df = pd.DataFrame(patients_list)
                    st.dataframe(df, use_container_width=True)
                    
                    # Download option
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download as CSV",
                        data=csv,
                        file_name="patients_data.csv",
                        mime="text/csv"
                    )
                else:
                    st.info("ℹ️ No patients found in the database.")
    
    # Get Patient by ID Page
    elif page == "Get Patient by ID":
        st.header("🔍 Get Patient by ID")
        
        patient_id = st.text_input("Enter Patient ID:", placeholder="e.g., P001")
        
        if st.button("Get Patient") and patient_id:
            response = make_api_request("GET", f"/patients/{patient_id}")
            data = display_api_response(response)
            
            if data and data.get("status") == "success":
                st.success(f"✅ Patient {patient_id} found!")
                
                # Display patient info in a nice format
                col1, col2 = st.columns(2)
                
                patient_data = data["data"]
                with col1:
                    st.metric("Name", patient_data.get("name", "N/A"))
                    st.metric("City", patient_data.get("city", "N/A"))
                    st.metric("Age", patient_data.get("age", "N/A"))
                    st.metric("Gender", patient_data.get("gender", "N/A"))
                
                with col2:
                    st.metric("Height (m)", patient_data.get("height", "N/A"))
                    st.metric("Weight (kg)", patient_data.get("weight", "N/A"))
                    st.metric("BMI", patient_data.get("bmi", "N/A"))
                    st.metric("Verdict", patient_data.get("verdict", "N/A"))
    
    # Sort Patients Page
    elif page == "Sort Patients":
        st.header("📊 Sort Patients")
        
        col1, col2 = st.columns(2)
        
        with col1:
            sort_by = st.selectbox(
                "Sort by:",
                ["height", "weight", "bmi"]
            )
        
        with col2:
            order = st.selectbox(
                "Order:",
                ["asc", "desc"]
            )
        
        if st.button("Sort Patients"):
            params = {"sort_by": sort_by, "order": order}
            response = make_api_request("GET", "/sort_patients", params=params)
            data = display_api_response(response)
            
            if data and data.get("status") == "success":
                st.success(f"✅ Patients sorted by {sort_by} in {order}ending order!")
                
                if data["data"]:
                    df = pd.DataFrame(data["data"])
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("ℹ️ No patients found in the database.")
    
    # Add Patient Page
    elif page == "Add Patient":
        st.header("➕ Add New Patient")
        
        with st.form("add_patient_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                patient_id = st.text_input("Patient ID*", placeholder="e.g., P001")
                name = st.text_input("Name*", placeholder="John Doe")
                city = st.text_input("City*", placeholder="New York")
                age = st.number_input("Age*", min_value=1, max_value=119, value=1)
            
            with col2:
                gender = st.selectbox("Gender*", ["male", "female", "others"])
                height = st.number_input("Height (meters)*", min_value=0.0, value=0.0, step=0.01, format="%.2f")
                weight = st.number_input("Weight (kg)*", min_value=0.0, value=0.0, step=0.1)
            
            submitted = st.form_submit_button("Add Patient")
            
            if submitted:
                if all([patient_id, name, city, age > 0, gender, height > 0, weight > 0]):
                    patient_data = {
                        "id": patient_id,
                        "name": name,
                        "city": city,
                        "age": int(age),
                        "gender": gender,
                        "height": float(height),
                        "weight": float(weight)
                        # Note: BMI and verdict are computed fields, so we don't send them
                    }
                    
                    # Debug: Show the data being sent
                    with st.expander("Debug: Data being sent to API"):
                        st.json(patient_data)
                    
                    response = make_api_request("POST", "/add_patient", data=patient_data)
                    
                    if response and response.status_code == 201:
                        st.success("✅ Patient added successfully!")
                        st.balloons()
                    elif response:
                        st.error(f"❌ Error {response.status_code}: {response.text}")
                        # Show detailed error for debugging
                        try:
                            error_detail = response.json()
                            st.json(error_detail)
                        except:
                            st.text(response.text)
                    else:
                        st.error("❌ Failed to connect to API")
                else:
                    st.error("❌ Please fill in all required fields marked with *")
    
    # Update Patient Page
    elif page == "Update Patient":
        st.header("✏️ Update Patient")
        
        patient_id = st.text_input("Patient ID to Update:", placeholder="e.g., P001")
        
        if patient_id:
            with st.form("update_patient_form"):
                st.subheader("Update Fields (leave empty to keep current value)")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    name = st.text_input("Name", placeholder="John Doe")
                    city = st.text_input("City", placeholder="New York")
                    age = st.number_input("Age", min_value=0, max_value=119, value=0)
                
                with col2:
                    gender = st.selectbox("Gender", ["", "male", "female", "others"])
                    height = st.number_input("Height (meters)", min_value=0.0, value=0.0, step=0.01, format="%.2f")
                    weight = st.number_input("Weight (kg)", min_value=0.0, value=0.0, step=0.1)
                
                submitted = st.form_submit_button("Update Patient")
                
                if submitted:
                    update_data = {}
                    
                    if name:
                        update_data["name"] = name
                    if city:
                        update_data["city"] = city
                    if age > 0:
                        update_data["age"] = age
                    if gender:
                        update_data["gender"] = gender
                    if height > 0:
                        update_data["height"] = height
                    if weight > 0:
                        update_data["weight"] = weight
                    
                    if update_data:
                        # Ensure proper data types
                        if "age" in update_data:
                            update_data["age"] = int(update_data["age"])
                        if "height" in update_data:
                            update_data["height"] = float(update_data["height"])
                        if "weight" in update_data:
                            update_data["weight"] = float(update_data["weight"])
                        
                        response = make_api_request("PUT", f"/update_patient/{patient_id}", data=update_data)
                        
                        if response and response.status_code == 200:
                            st.success("✅ Patient updated successfully!")
                        else:
                            display_api_response(response)
                    else:
                        st.warning("⚠️ No fields to update. Please enter at least one field.")
    
    # Delete Patient Page
    elif page == "Delete Patient":
        st.header("🗑️ Delete Patient")
        
        patient_id = st.text_input("Patient ID to Delete:", placeholder="e.g., P001")
        
        if patient_id:
            st.warning(f"⚠️ You are about to delete patient: {patient_id}")
            st.write("This action cannot be undone!")
            
            if st.button("🗑️ Delete Patient", type="secondary"):
                response = make_api_request("DELETE", f"/delete_patient/{patient_id}")
                
                if response and response.status_code == 200:
                    st.success("✅ Patient deleted successfully!")
                else:
                    display_api_response(response)

if __name__ == "__main__":
    # Add some styling
    st.markdown("""
    <style>
    .stButton > button {
        width: 100%;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    main()