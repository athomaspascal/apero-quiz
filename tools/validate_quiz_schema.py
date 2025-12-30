import json
from jsonschema import validate, ValidationError

# Charger le schéma
schema_file = r'C:\Users\athom\IdeaProjects\quizz1\src\main\resources\quiz-questions-schema.json'
quiz_file = r'C:\Users\athom\IdeaProjects\quizz1\src\main\resources\quiz-questions.json'

print("Chargement du schéma JSON...")
with open(schema_file, 'r', encoding='utf-8') as f:
    schema = json.load(f)

print("Chargement du fichier quiz...")
with open(quiz_file, 'r', encoding='utf-8') as f:
    quiz_data = json.load(f)

print("\nValidation du fichier quiz avec le schéma...")
try:
    validate(instance=quiz_data, schema=schema)
    print("\n✓ Le fichier quiz est VALIDE selon le schéma JSON!")
    print(f"✓ Nombre total de quiz: {len(quiz_data['quizzes'])}")

    # Compter le nombre total de questions
    total_questions = sum(len(quiz['questions']) for quiz in quiz_data['quizzes'])
    print(f"✓ Nombre total de questions: {total_questions}")

except ValidationError as e:
    print(f"\n❌ Erreur de validation:")
    print(f"  Message: {e.message}")
    print(f"  Chemin: {' > '.join(str(p) for p in e.path)}")
    print(f"  Instance: {str(e.instance)[:200]}...")

