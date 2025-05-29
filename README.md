# Patient Data Management System

A comprehensive patient data management system built with FastAPI backend and Streamlit frontend, designed to efficiently manage patient records with CRUD operations and advanced sorting capabilities.

## 🏥 Overview

This project provides a complete solution for managing patient data through both REST API endpoints and a user-friendly web interface. The system allows healthcare professionals to store, retrieve, update, and analyze patient information including basic demographics and health metrics.

## ✨ Features

### Backend (FastAPI)
- **RESTful API** with comprehensive CRUD operations
- **Data Validation** using Pydantic models
- **Automatic BMI Calculation** when adding/updating patients
- **Flexible Sorting** by height, weight, or BMI
- **Error Handling** with appropriate HTTP status codes
- **JSON Data Persistence** for easy data management

### Frontend (Streamlit)
- **Intuitive Web Interface** for non-technical users
- **Real-time Data Visualization** with tables and metrics
- **Form Validation** with user-friendly error messages
- **CSV Export** functionality for data analysis
- **Responsive Design** that works on various screen sizes
- **Navigation Sidebar** for easy page switching

## 📁 Project Structure

```
PatientVault/
│
├── main.py                 # FastAPI application with API endpoints
├── streamlit_app.py        # Streamlit web interface
├── utils.py               # Utility functions and Pydantic models
├── data/patients_data.json     # JSON file for data storage (auto-generated)
├── requirements.txt       # Python dependencies
└── README.md             # Project documentation
```

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd PatientVault
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# ------- With Conda -------
conda create -n env_name 
conda activate env_name

# ------- With Python venv -------
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

If `requirements.txt` doesn't exist, install packages manually:
```bash
pip install fastapi uvicorn streamlit requests pandas pydantic
```

## 🚀 Usage

### Running the FastAPI Backend

1. **Start the FastAPI server:**
```bash
uvicorn patient_data_api:app --reload
```

2. **Access the API:**
   - **API Base URL:** `http://localhost:8000`
   - **Interactive API Docs:** `http://localhost:8000/docs`
   - **Alternative Docs:** `http://localhost:8000/redoc`

### Running the Streamlit Frontend

1. **In a new terminal (keep FastAPI running):**
```bash
streamlit run streamlit_app.py
```

2. **Access the Web Interface:**
   - **Streamlit App:** `http://localhost:8501`

## 📊 Data Model

### Patient Model
```python
{
    "id": "P001",           # Unique patient identifier
    "name": "John Doe",     # Patient's full name
    "age": 30,              # Age in years
    "gender": "Male",       # Gender (Male/Female/Other)
    "height": 1.75,        # Height in meters
    "weight": 70.2,         # Weight in kilograms
    "bmi": 22.8            # Body Mass Index (auto-calculated)
}
```

## 🌐 API Endpoints

### GET Endpoints

| Endpoint | Description | Parameters |
|----------|-------------|------------|
| `/API INFO` | Get API information | None |
| `/view_patients_data` | Get all patients | None |
| `/patients/{patient_id}` | Get specific patient | `patient_id` (path) |
| `/sort_patients` | Get sorted patients | `sort_by`, `order` (query) |

### POST Endpoints

| Endpoint | Description | Body |
|----------|-------------|------|
| `/add_patient` | Add new patient | Patient object |

### PUT Endpoints

| Endpoint | Description | Body |
|----------|-------------|------|
| `/update_patient/{patient_id}` | Update patient | UpdatePatient object |

### DELETE Endpoints

| Endpoint | Description | Parameters |
|----------|-------------|------------|
| `/delete_patient/{patient_id}` | Delete patient | `patient_id` (path) |

## 📱 Streamlit Interface Guide

### Navigation Pages

1. **API Info** - View API version and description
2. **View All Patients** - Browse all patient records with export option
3. **Get Patient by ID** - Search for specific patients
4. **Sort Patients** - Sort patients by various metrics
5. **Add Patient** - Add new patient records
6. **Update Patient** - Modify existing patient information
7. **Delete Patient** - Remove patient records

### Key Features

- **Real-time Validation:** Forms validate input before submission
- **Error Handling:** Clear error messages for API connection issues
- **Data Export:** Download patient data as CSV files
- **Responsive Tables:** Interactive data tables with sorting
- **Metric Display:** Visual representation of patient statistics

## 🔧 Configuration

### API Configuration
To change the API server URL, modify the `API_BASE_URL` variable in `streamlit_app.py`:

```python
API_BASE_URL = "http://localhost:8000"  # Change to your server URL
```

### Data Storage
Patient data is stored in `data/patients_data.json`. The file is automatically created when the first patient is added.

## 📝 Example Usage

### Adding a Patient via API
```bash
curl -X POST "http://localhost:8000/add_patient" \
     -H "Content-Type: application/json" \
     -d '{
       "id": "P001",
       "name": "John Doe",
       "age": 30,
       "gender": "Male",
       "height": 1.75,
       "weight": 70.2
     }'
```

### Sorting Patients
```bash
curl "http://localhost:8000/sort_patients?sort_by=bmi&order=desc"
```

## 🛡️ Error Handling

The system includes comprehensive error handling:

- **404 Errors:** When patients are not found
- **400 Errors:** For invalid input data or duplicate IDs
- **Connection Errors:** When the API server is unavailable
- **Validation Errors:** For invalid data formats

## 🧪 Testing

### Manual Testing with Streamlit
1. Start both servers (FastAPI and Streamlit)
2. Use the web interface to test all functionality
3. Verify data persistence by refreshing the page

### API Testing with curl
```bash
# Test API info
curl http://localhost:8000/API\ INFO

# Test viewing all patients
curl http://localhost:8000/view_patients_data

# Test adding a patient
curl -X POST http://localhost:8000/add_patient \
     -H "Content-Type: application/json" \
     -d '{"id":"TEST001","name":"Test User","age":25,"gender":"Male","height":180,"weight":75}'
```

## 🔄 Data Backup and Recovery

### Backup
```bash
# Create backup of patient data
cp patients_data.json patients_data_backup_$(date +%Y%m%d).json
```

### Recovery
```bash
# Restore from backup
cp patients_data_backup_YYYYMMDD.json patients_data.json
```

## 🚨 Troubleshooting

### Common Issues

1. **"Cannot connect to API server"**
   - Ensure FastAPI server is running on correct port
   - Check if `API_BASE_URL` matches your server configuration

2. **"Patient not found" errors**
   - Verify patient ID exists using "View All Patients"
   - Check for typos in patient ID

3. **Validation errors**
   - Ensure all required fields are filled
   - Check data types (numbers for age, height, weight)

4. **Port conflicts**
   - Change FastAPI port: `uvicorn main:app --port 8001`
   - Change Streamlit port: `streamlit run streamlit_app.py --server.port 8502`

## 🔮 Future Enhancements

- **Database Integration** (PostgreSQL, MySQL, MongoDB)
- **User Authentication** and role-based access
- **Patient Photo Upload** capability
- **Medical History** tracking
- **Appointment Scheduling** system
- **Data Analytics** and reporting dashboard
- **Email Notifications** for appointments
- **Mobile App** development
- **Docker Containerization**
- **Unit Testing** suite

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

For support and questions:
- Create an issue in the repository

## 🙏 Acknowledgments

- **FastAPI** - Modern, fast web framework for building APIs
- **Streamlit** - Framework for creating data applications
- **Pydantic** - Data validation using Python type annotations
- **Uvicorn** - Lightning-fast ASGI server

---

**Made with ❤️ for healthcare professionals**