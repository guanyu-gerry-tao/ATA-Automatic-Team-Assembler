# Configuration for team matching algorithm
# Defines available choices and weights for each attribute category
# Weights are normalized by sqrt(number of choices) in the vector construction
CONFIG = {
    "skill_level":
        {"choices": ["noob", "ok", "pro"],
         "weight": 3},
    "ambition":
        {"choices": ["just_pass", "ambitious"],
         "weight": 2},
    "role":
        {"choices": ["leader", "follower"],
         "weight": 2},
    "teamwork_style":
        {"choices": ["online_meeting", "offline_meeting", "divide_and_conquer"],
         "weight": 2},
    "pace":
        {"choices": ["finish_early", "finish_late", "little_by_little"],
         "weight": 2},
    "backgrounds":
        {"choices": [
            "Technology/Math",
            "Finance",
            "Consulting",
            "Healthcare & Biotech",
            "Education & Research",
            "Arts, Media & Design",
            "Architecture & Engineering",
            "Business & Operations",
            "Others"
        ],
            "weight": 1},
    "hobbies":
        {"choices": [
            "Gaming",
            "Outdoor Sports & Fitness",
            "Travel & Adventure",
            "Tech & DIY",
            "Arts & Media",
            "Food & Cooking",
            "Music & Performing"
        ],
            "weight": 1}
}
