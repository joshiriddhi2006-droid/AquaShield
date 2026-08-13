from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


# ==========================================
# AQUASHIELD AI SERVICE
# ==========================================

app = FastAPI(
    title="AquaShield AI Service",
    description="AI service for citizen complaint analysis",
    version="1.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "https://aquashield-1.onrender.com"
],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# COMPLAINT CLASSIFICATION DATA
# ==========================================

complaints = [
    "Water is accumulated on my road",
    "My street is completely waterlogged",
    "There is severe waterlogging in my area",
    "Rain water is not draining from the road",
    "The road is flooded after heavy rain",

    "The road is damaged and needs repair",
    "There is a large damaged section of the road",
    "The road surface is broken and unsafe",
    "There are cracks on the road",

    "The flooded road is blocking traffic",
    "Vehicles cannot pass because of flooding",
    "This road is dangerous and traffic needs to be diverted",
    "An emergency vehicle cannot use this flooded road",
]

categories = [
    "Waterlogging",
    "Waterlogging",
    "Waterlogging",
    "Waterlogging",
    "Waterlogging",

    "Road Infrastructure",
    "Road Infrastructure",
    "Road Infrastructure",
    "Road Infrastructure",

    "Traffic Safety",
    "Traffic Safety",
    "Traffic Safety",
    "Traffic Safety",
]


# ==========================================
# TRAIN CATEGORY MODEL
# ==========================================

vectorizer = TfidfVectorizer()

X = vectorizer.fit_transform(complaints)

category_model = LogisticRegression()

category_model.fit(X, categories)


# ==========================================
# REQUEST FORMAT
# ==========================================

class ComplaintRequest(BaseModel):
    complaint: str


# ==========================================
# DEPARTMENT PREDICTION
# ==========================================

def get_department(category):

    department_map = {
        "Waterlogging": "Municipal / Water Management",
        "Road Infrastructure": "Road & Public Works",
        "Traffic Safety": "Traffic & Emergency Management"
    }

    return department_map.get(
        category,
        "Municipal Administration"
    )


# ==========================================
# PRIORITY DETECTION
# ==========================================

def get_priority(complaint):

    text = complaint.lower()

    if (
        "emergency" in text
        or "ambulance" in text
        or "cannot pass" in text
        or "inaccessible" in text
        or "dangerous" in text
    ):
        return "High"

    elif (
        "severe" in text
        or "heavy" in text
        or "flooded" in text
        or "traffic" in text
    ):
        return "Medium"

    else:
        return "Low"


# ==========================================
# SEVERITY DETECTION
# ==========================================

def get_severity(complaint):

    text = complaint.lower()

    if (
        "completely flooded" in text
        or "deep water" in text
        or "fully submerged" in text
        or "cannot pass" in text
    ):
        return "High"

    elif (
        "severe" in text
        or "heavy waterlogging" in text
        or "large amount of water" in text
        or "traffic affected" in text
    ):
        return "Medium"

    else:
        return "Low"


# ==========================================
# MAIN AI ENDPOINT
# ==========================================

@app.post("/predict")
def predict_complaint(request: ComplaintRequest):

    complaint = request.complaint

    # Category prediction
    complaint_vector = vectorizer.transform([complaint])

    category = category_model.predict(
        complaint_vector
    )[0]

    # Department
    department = get_department(category)

    # Priority
    priority = get_priority(complaint)

    # Severity
    severity = get_severity(complaint)

    # Final API response
    return {
        "success": True,
        "complaint": complaint,
        "category": category,
        "department": department,
        "priority": priority,
        "severity": severity
    }


# ==========================================
# HEALTH CHECK
# ==========================================

@app.get("/")
def home():

    return {
        "service": "AquaShield AI",
        "status": "running"
    }