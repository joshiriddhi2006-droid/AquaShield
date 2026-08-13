from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


# AquaShield training examples
complaints = [
    "Water is accumulated on my road",
    "My street is completely waterlogged",
    "There is severe waterlogging in my area",
    "Rain water is not draining from the road",
    "The road is flooded after heavy rain",

    "The road is damaged and needs repair",
    "There is a large damaged section of the road",
    "The road surface is broken and unsafe",
    "There are cracks on the road after flooding",

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


# Convert complaint text into numerical features
vectorizer = TfidfVectorizer()

X = vectorizer.fit_transform(complaints)


# Train the classifier
model = LogisticRegression()

model.fit(X, categories)


# Get complaint from user
user_complaint = input("Enter AquaShield complaint: ")

# Convert new complaint into the same numerical format
new_complaint = vectorizer.transform([user_complaint])

# Predict category
prediction = model.predict(new_complaint)

print("\nAquaShield AI Result")
print("--------------------")
print("Category:", prediction[0])
# Department mapping
department_map = {
    "Waterlogging": "Municipal / Water Management",
    "Road Infrastructure": "Road & Public Works",
    "Traffic Safety": "Traffic & Emergency Management"
}

department = department_map[prediction[0]]

print("Department:", department)
# Priority detection
complaint_lower = user_complaint.lower()

if (
    "emergency" in complaint_lower
    or "ambulance" in complaint_lower
    or "cannot pass" in complaint_lower
    or "inaccessible" in complaint_lower
    or "dangerous" in complaint_lower
):
    priority = "High"

elif (
    "severe" in complaint_lower
    or "heavy" in complaint_lower
    or "flooded" in complaint_lower
    or "traffic" in complaint_lower
):
    priority = "Medium"

else:
    priority = "Low"

print("Priority:", priority)
# Severity detection
if (
    "completely flooded" in complaint_lower
    or "deep water" in complaint_lower
    or "fully submerged" in complaint_lower
    or "cannot pass" in complaint_lower
):
    severity = "High"

elif (
    "severe" in complaint_lower
    or "heavy waterlogging" in complaint_lower
    or "large amount of water" in complaint_lower
    or "traffic affected" in complaint_lower
):
    severity = "Medium"

else:
    severity = "Low"

print("Severity:", severity)