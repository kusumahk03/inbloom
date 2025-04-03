import pandas as pd
import random

# Define dataset parameters
num_participants = 250
first_names = ["Aarav", "Vivaan", "Diya", "Rohan", "Ananya", "Meera", "Karthik", "Sneha", "Rahul", "Pooja"]
last_names = ["Sharma", "Iyer", "Verma", "Nair", "Pillai", "Gupta", "Reddy", "Das", "Mehta", "Kapoor"]
events = [
    "Dance", "Singing", "Drama", "Photography", "Painting", 
    "Poetry", "Debate", "Quiz", "Stand-up Comedy", "Instrumental Music"
]
colleges = ["ABC University", "XYZ College", "PQR Institute", "LMN Academy", "EFG University"]
states = ["Karnataka", "Tamil Nadu", "Maharashtra", "Kerala", "Andhra Pradesh"]
days = ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5"]
ratings = [1, 2, 3, 4, 5]
feedback_samples = [
    "Amazing event!", "Loved the experience!", "Could be better.", 
    "Well organized!", "Had a great time!", "Needs more clarity.", 
    "Super fun and engaging!", "Moderate experience.", "Fantastic performance!", "Could improve logistics."
]

# Generate dataset
data = []
for i in range(num_participants):
    participant = {
        "Participant_ID": i + 1,
        "Name": f"{random.choice(first_names)} {random.choice(last_names)}",
        "Age": random.randint(18, 30),
        "Gender": random.choice(["Male", "Female", "Other"]),
        "College": random.choice(colleges),
        "State": random.choice(states),
        "Event": random.choice(events),
        "Day": random.choice(days),
        "Rating": random.choice(ratings),
        "Feedback": random.choice(feedback_samples),
    }
    data.append(participant)

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv("inbloom_participants.csv", index=False)

print("✅ Dataset generated successfully and saved as 'inbloom_participants.csv'")
