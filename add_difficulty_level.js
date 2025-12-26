// Script to add difficulty_level attribute to all questions in quiz-questions.json
const fs = require('fs');
const path = require('path');

function addDifficultyLevel() {
    console.log("Starting script...");
    console.log("Current directory:", process.cwd());

    const inputFile = path.join('src', 'main', 'resources', 'quiz-questions.json');

    // Check if file exists
    if (!fs.existsSync(inputFile)) {
        console.error(`ERROR: File not found: ${inputFile}`);
        return false;
    }

    console.log(`File found: ${inputFile}`);

    // Create backup with timestamp
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').replace('T', '_').split('Z')[0];
    const backupFile = path.join('src', 'main', 'resources', `quiz-questions_backup_${timestamp}.json`);

    console.log(`Creating backup: ${backupFile}`);
    try {
        fs.copyFileSync(inputFile, backupFile);
        console.log("Backup created successfully");
    } catch (e) {
        console.error("ERROR creating backup:", e.message);
        return false;
    }

    // Read the JSON file
    console.log(`Reading ${inputFile}...`);
    let quizzes;
    try {
        const data = fs.readFileSync(inputFile, 'utf-8');
        quizzes = JSON.parse(data);
        console.log(`JSON loaded successfully. Number of quizzes: ${quizzes.length}`);
    } catch (e) {
        console.error("ERROR reading JSON:", e.message);
        return false;
    }

    // Add difficulty_level to each question
    let totalQuestions = 0;
    let modifiedQuestions = 0;

    for (const quiz of quizzes) {
        const quizName = quiz.name || 'Unknown';
        console.log(`\nProcessing quiz: ${quizName}`);

        if (quiz.questions && Array.isArray(quiz.questions)) {
            for (const question of quiz.questions) {
                totalQuestions++;

                // Add difficulty_level if not present
                if (!question.hasOwnProperty('difficulty_level')) {
                    question.difficulty_level = 1;
                    modifiedQuestions++;
                }
            }
        }
    }

    console.log(`\nTotal questions: ${totalQuestions}, Modified: ${modifiedQuestions}`);

    // Write back to the file
    console.log(`\nWriting modified JSON to ${inputFile}...`);
    try {
        fs.writeFileSync(inputFile, JSON.stringify(quizzes, null, 2), 'utf-8');
        console.log("File written successfully");
    } catch (e) {
        console.error("ERROR writing JSON:", e.message);
        return false;
    }

    console.log("\n" + "=".repeat(60));
    console.log("✅ COMPLETED SUCCESSFULLY!");
    console.log("=".repeat(60));
    console.log(`Total questions processed: ${totalQuestions}`);
    console.log(`Questions modified: ${modifiedQuestions}`);
    console.log(`Backup created: ${backupFile}`);
    console.log(`Output file: ${inputFile}`);
    console.log("=".repeat(60));
    return true;
}

// Execute
try {
    const success = addDifficultyLevel();
    process.exit(success ? 0 : 1);
} catch (e) {
    console.error("❌ ERROR:", e.message);
    console.error(e.stack);
    process.exit(1);
}

