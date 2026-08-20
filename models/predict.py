import pickle
import os


# ---------------------------------------
# Model Path
# ---------------------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(__file__)
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "complaint_classifier.pkl"
)


# ---------------------------------------
# Load Trained Model
# ---------------------------------------

if os.path.exists(MODEL_PATH):

    with open(
        MODEL_PATH,
        "rb"
    ) as file:

        model = pickle.load(file)

else:

    model = None


# ---------------------------------------
# AI Department Prediction
# ---------------------------------------

def predict_complaint(text):

    if model is None:

        return "Unknown", 0.0


    prediction = model.predict(
        [text]
    )[0]


    # -----------------------------------
    # Confidence Calculation
    # -----------------------------------

    if hasattr(
        model,
        "decision_function"
    ):

        scores = model.decision_function(
            [text]
        )[0]


        exp_scores = [

            pow(
                2.71828,
                float(score)
            )

            for score in scores

        ]


        total = sum(
            exp_scores
        )


        confidence = (

            max(exp_scores)
            / total

        ) * 100


    else:

        confidence = 0.0


    return prediction, round(
        confidence,
        2
    )


# ---------------------------------------
# AI Priority Prediction
# ---------------------------------------

def predict_priority(text):

    text = text.lower().strip()


    # -----------------------------------
    # HIGH PRIORITY
    # -----------------------------------

    high_priority_words = [

        "emergency",
        "urgent",
        "immediately",
        "danger",
        "dangerous",
        "accident",
        "fire",
        "hospital",
        "life threatening",
        "life-threatening",
        "major accident",
        "severe",
        "critical",
        "flood",
        "gas leak",
        "electric shock",
        "no water",
        "drinking water unavailable",
        "power outage",
        "power cut"

    ]


    # -----------------------------------
    # MEDIUM PRIORITY
    # -----------------------------------

    medium_priority_words = [

        "problem",
        "issue",
        "complaint",
        "repair",
        "damaged",
        "damage",
        "broken",
        "not working",
        "garbage",
        "waste",
        "pothole",
        "potholes",
        "leakage",
        "leaking",
        "dirty",
        "blocked",
        "delay",
        "overflow",
        "drainage",
        "sewage",
        "road damage"

    ]


    # -----------------------------------
    # HIGH PRIORITY CHECK
    # -----------------------------------

    for word in high_priority_words:

        if word in text:

            return "High"


    # -----------------------------------
    # MEDIUM PRIORITY CHECK
    # -----------------------------------

    for word in medium_priority_words:

        if word in text:

            return "Medium"


    # -----------------------------------
    # DEFAULT
    # -----------------------------------

    return "Low"


# ---------------------------------------
# AI Complaint Summary
# ---------------------------------------

def generate_summary(text):

    text = text.strip()


    if text == "":

        return (
            "No complaint description provided."
        )


    words = text.split()


    if len(words) <= 20:

        return text


    summary = " ".join(
        words[:20]
    )


    return summary + "..."