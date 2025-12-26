import json
import uuid
from datetime import datetime

# Load existing quiz data
with open('src/main/resources/quiz-questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Create World Cities Latitude & Longitude Quiz
world_cities_quiz = {
    "name": "World Cities - Latitude & Longitude",
    "imageFileName": "world-map.svg",
    "questions": [
        {
            "id": 1,
            "uuid": str(uuid.uuid4()),
            "question": "What is the approximate latitude of Paris, France?",
            "options": ["41.9°N", "48.9°N", "55.8°N", "37.6°N"],
            "answer": "48.9°N"
        },
        {
            "id": 2,
            "uuid": str(uuid.uuid4()),
            "question": "What is the approximate longitude of Tokyo, Japan?",
            "options": ["121.5°E", "139.7°E", "114.1°E", "103.8°E"],
            "answer": "139.7°E"
        },
        {
            "id": 3,
            "uuid": str(uuid.uuid4()),
            "question": "Which city is located at approximately 51.5°N latitude?",
            "options": ["Berlin", "London", "Amsterdam", "Copenhagen"],
            "answer": "London"
        },
        {
            "id": 4,
            "uuid": str(uuid.uuid4()),
            "question": "What is the approximate latitude of Sydney, Australia?",
            "options": ["33.9°S", "37.8°S", "41.3°S", "27.5°S"],
            "answer": "33.9°S"
        },
        {
            "id": 5,
            "uuid": str(uuid.uuid4()),
            "question": "Which city is located at approximately 74.0°W longitude?",
            "options": ["Boston", "Philadelphia", "New York City", "Washington D.C."],
            "answer": "New York City"
        },
        {
            "id": 6,
            "uuid": str(uuid.uuid4()),
            "question": "What is the approximate latitude of Cairo, Egypt?",
            "options": ["30.0°N", "33.9°N", "25.3°N", "36.8°N"],
            "answer": "30.0°N"
        },
        {
            "id": 7,
            "uuid": str(uuid.uuid4()),
            "question": "Which city is located at approximately 2.2°S latitude?",
            "options": ["Singapore", "Nairobi", "Kuala Lumpur", "Jakarta"],
            "answer": "Nairobi"
        },
        {
            "id": 8,
            "uuid": str(uuid.uuid4()),
            "question": "What is the approximate longitude of Moscow, Russia?",
            "options": ["30.3°E", "37.6°E", "44.8°E", "27.6°E"],
            "answer": "37.6°E"
        },
        {
            "id": 9,
            "uuid": str(uuid.uuid4()),
            "question": "Which city is located at approximately 55.8°N latitude?",
            "options": ["Edinburgh", "Moscow", "Copenhagen", "Hamburg"],
            "answer": "Moscow"
        },
        {
            "id": 10,
            "uuid": str(uuid.uuid4()),
            "question": "What is the approximate latitude of Rio de Janeiro, Brazil?",
            "options": ["22.9°S", "34.6°S", "12.0°S", "4.7°S"],
            "answer": "22.9°S"
        },
        {
            "id": 11,
            "uuid": str(uuid.uuid4()),
            "question": "Which city is located at approximately 121.5°E longitude?",
            "options": ["Manila", "Hong Kong", "Shanghai", "Taipei"],
            "answer": "Manila"
        },
        {
            "id": 12,
            "uuid": str(uuid.uuid4()),
            "question": "What is the approximate longitude of Los Angeles, USA?",
            "options": ["118.2°W", "122.4°W", "104.9°W", "112.1°W"],
            "answer": "118.2°W"
        },
        {
            "id": 13,
            "uuid": str(uuid.uuid4()),
            "question": "Which city is located at approximately 13.4°E longitude?",
            "options": ["Berlin", "Vienna", "Prague", "Munich"],
            "answer": "Berlin"
        },
        {
            "id": 14,
            "uuid": str(uuid.uuid4()),
            "question": "What is the approximate latitude of Mumbai, India?",
            "options": ["19.1°N", "28.6°N", "13.1°N", "22.6°N"],
            "answer": "19.1°N"
        },
        {
            "id": 15,
            "uuid": str(uuid.uuid4()),
            "question": "Which city is located at approximately 151.2°E longitude?",
            "options": ["Brisbane", "Sydney", "Melbourne", "Auckland"],
            "answer": "Sydney"
        },
        {
            "id": 16,
            "uuid": str(uuid.uuid4()),
            "question": "What is the approximate latitude of Stockholm, Sweden?",
            "options": ["59.3°N", "64.1°N", "55.7°N", "60.4°N"],
            "answer": "59.3°N"
        },
        {
            "id": 17,
            "uuid": str(uuid.uuid4()),
            "question": "Which city is located at approximately 77.2°E longitude?",
            "options": ["Kolkata", "New Delhi", "Mumbai", "Bangalore"],
            "answer": "New Delhi"
        },
        {
            "id": 18,
            "uuid": str(uuid.uuid4()),
            "question": "What is the approximate longitude of Buenos Aires, Argentina?",
            "options": ["58.4°W", "70.7°W", "47.9°W", "43.2°W"],
            "answer": "58.4°W"
        },
        {
            "id": 19,
            "uuid": str(uuid.uuid4()),
            "question": "Which city is located at approximately 0°W/E longitude (Prime Meridian)?",
            "options": ["Paris", "London", "Madrid", "Lisbon"],
            "answer": "London"
        },
        {
            "id": 20,
            "uuid": str(uuid.uuid4()),
            "question": "What is the approximate latitude of Singapore?",
            "options": ["1.3°N", "6.9°N", "3.1°S", "10.8°N"],
            "answer": "1.3°N"
        },
        {
            "id": 21,
            "uuid": str(uuid.uuid4()),
            "question": "Which city is located at approximately 116.4°E longitude?",
            "options": ["Beijing", "Seoul", "Pyongyang", "Ulaanbaatar"],
            "answer": "Beijing"
        },
        {
            "id": 22,
            "uuid": str(uuid.uuid4()),
            "question": "What is the approximate latitude of Cape Town, South Africa?",
            "options": ["33.9°S", "26.2°S", "29.9°S", "25.7°S"],
            "answer": "33.9°S"
        },
        {
            "id": 23,
            "uuid": str(uuid.uuid4()),
            "question": "Which city is located at approximately 4.9°E longitude?",
            "options": ["Brussels", "Amsterdam", "Paris", "Frankfurt"],
            "answer": "Paris"
        },
        {
            "id": 24,
            "uuid": str(uuid.uuid4()),
            "question": "What is the approximate longitude of Dubai, UAE?",
            "options": ["55.3°E", "51.5°E", "46.7°E", "48.5°E"],
            "answer": "55.3°E"
        },
        {
            "id": 25,
            "uuid": str(uuid.uuid4()),
            "question": "Which city is located at approximately 41.9°N latitude?",
            "options": ["Rome", "Madrid", "Barcelona", "Athens"],
            "answer": "Rome"
        },
        {
            "id": 26,
            "uuid": str(uuid.uuid4()),
            "question": "What is the approximate latitude of Bangkok, Thailand?",
            "options": ["13.8°N", "21.0°N", "16.8°N", "10.8°N"],
            "answer": "13.8°N"
        },
        {
            "id": 27,
            "uuid": str(uuid.uuid4()),
            "question": "Which city is located at approximately 87.6°W longitude?",
            "options": ["Milwaukee", "Chicago", "Indianapolis", "Detroit"],
            "answer": "Chicago"
        },
        {
            "id": 28,
            "uuid": str(uuid.uuid4()),
            "question": "What is the approximate longitude of Istanbul, Turkey?",
            "options": ["28.9°E", "35.2°E", "32.9°E", "26.1°E"],
            "answer": "28.9°E"
        },
        {
            "id": 29,
            "uuid": str(uuid.uuid4()),
            "question": "Which city is located at approximately 45.5°N latitude?",
            "options": ["Milan", "Montreal", "Venice", "Belgrade"],
            "answer": "Montreal"
        },
        {
            "id": 30,
            "uuid": str(uuid.uuid4()),
            "question": "What is the approximate latitude of Mexico City, Mexico?",
            "options": ["19.4°N", "25.7°N", "15.8°N", "32.6°N"],
            "answer": "19.4°N"
        },
        {
            "id": 31,
            "uuid": str(uuid.uuid4()),
            "question": "Which city is located at approximately 114.1°E longitude?",
            "options": ["Hong Kong", "Guangzhou", "Shenzhen", "Macau"],
            "answer": "Hong Kong"
        },
        {
            "id": 32,
            "uuid": str(uuid.uuid4()),
            "question": "What is the approximate longitude of Vancouver, Canada?",
            "options": ["123.1°W", "114.1°W", "79.4°W", "106.6°W"],
            "answer": "123.1°W"
        },
        {
            "id": 33,
            "uuid": str(uuid.uuid4()),
            "question": "Which city is located at approximately 37.9°N latitude?",
            "options": ["Lisbon", "Athens", "San Francisco", "Seoul"],
            "answer": "San Francisco"
        },
        {
            "id": 34,
            "uuid": str(uuid.uuid4()),
            "question": "What is the approximate latitude of Lima, Peru?",
            "options": ["12.0°S", "4.7°S", "0.2°S", "8.5°S"],
            "answer": "12.0°S"
        },
        {
            "id": 35,
            "uuid": str(uuid.uuid4()),
            "question": "Which city is located at approximately 12.5°E longitude?",
            "options": ["Copenhagen", "Hamburg", "Rome", "Stockholm"],
            "answer": "Rome"
        },
        {
            "id": 36,
            "uuid": str(uuid.uuid4()),
            "question": "What is the approximate longitude of Johannesburg, South Africa?",
            "options": ["28.0°E", "18.4°E", "31.0°E", "23.8°E"],
            "answer": "28.0°E"
        },
        {
            "id": 37,
            "uuid": str(uuid.uuid4()),
            "question": "Which city is located at approximately 39.9°N latitude?",
            "options": ["Beijing", "Madrid", "Ankara", "Philadelphia"],
            "answer": "Beijing"
        },
        {
            "id": 38,
            "uuid": str(uuid.uuid4()),
            "question": "What is the approximate latitude of Wellington, New Zealand?",
            "options": ["41.3°S", "36.8°S", "43.5°S", "37.8°S"],
            "answer": "41.3°S"
        },
        {
            "id": 39,
            "uuid": str(uuid.uuid4()),
            "question": "Which city is located at approximately 100.5°E longitude?",
            "options": ["Chiang Mai", "Bangkok", "Yangon", "Hanoi"],
            "answer": "Bangkok"
        },
        {
            "id": 40,
            "uuid": str(uuid.uuid4()),
            "question": "What is the approximate longitude of Santiago, Chile?",
            "options": ["70.7°W", "58.4°W", "78.5°W", "56.2°W"],
            "answer": "70.7°W"
        },
        {
            "id": 41,
            "uuid": str(uuid.uuid4()),
            "question": "Which city is located at approximately 52.5°N latitude?",
            "options": ["Amsterdam", "Berlin", "Warsaw", "Dublin"],
            "answer": "Berlin"
        },
        {
            "id": 42,
            "uuid": str(uuid.uuid4()),
            "question": "What is the approximate latitude of Havana, Cuba?",
            "options": ["23.1°N", "18.5°N", "14.6°N", "25.8°N"],
            "answer": "23.1°N"
        },
        {
            "id": 43,
            "uuid": str(uuid.uuid4()),
            "question": "Which city is located at approximately 174.8°E longitude?",
            "options": ["Wellington", "Auckland", "Christchurch", "Suva"],
            "answer": "Auckland"
        },
        {
            "id": 44,
            "uuid": str(uuid.uuid4()),
            "question": "What is the approximate longitude of Nairobi, Kenya?",
            "options": ["36.8°E", "32.6°E", "30.1°E", "39.3°E"],
            "answer": "36.8°E"
        },
        {
            "id": 45,
            "uuid": str(uuid.uuid4()),
            "question": "Which city is located at approximately 35.7°N latitude?",
            "options": ["Tehran", "Tokyo", "Seoul", "Beirut"],
            "answer": "Tokyo"
        },
        {
            "id": 46,
            "uuid": str(uuid.uuid4()),
            "question": "What is the approximate latitude of Oslo, Norway?",
            "options": ["59.9°N", "64.1°N", "55.7°N", "60.4°N"],
            "answer": "59.9°N"
        },
        {
            "id": 47,
            "uuid": str(uuid.uuid4()),
            "question": "Which city is located at approximately 103.8°E longitude?",
            "options": ["Bangkok", "Singapore", "Hanoi", "Kuala Lumpur"],
            "answer": "Singapore"
        },
        {
            "id": 48,
            "uuid": str(uuid.uuid4()),
            "question": "What is the approximate longitude of Bogota, Colombia?",
            "options": ["74.1°W", "77.0°W", "66.9°W", "79.5°W"],
            "answer": "74.1°W"
        },
        {
            "id": 49,
            "uuid": str(uuid.uuid4()),
            "question": "Which city is located at approximately 50.1°N latitude?",
            "options": ["Prague", "Brussels", "Frankfurt", "Krakow"],
            "answer": "Prague"
        },
        {
            "id": 50,
            "uuid": str(uuid.uuid4()),
            "question": "What is the approximate latitude of Quito, Ecuador?",
            "options": ["0.2°S", "4.7°S", "8.1°S", "12.0°S"],
            "answer": "0.2°S"
        }
    ]
}

# Add the quiz to the existing data
data['quizzes'].append(world_cities_quiz)

# Save the updated data
with open('src/main/resources/quiz-questions.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"✅ Quiz 'World Cities - Latitude & Longitude' added successfully!")
print(f"📊 Total number of quizzes: {len(data['quizzes'])}")
print(f"❓ Number of questions in new quiz: {len(world_cities_quiz['questions'])}")

