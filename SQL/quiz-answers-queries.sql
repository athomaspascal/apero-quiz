-- ================================================
-- QUIZ ANSWERS - SQL QUERIES FOR DATA ANALYSIS
-- ================================================

-- 1. VIEW ALL ANSWERS FOR A PARTICIPANT
SELECT
    qa.answer_id,
    u.name as participant_name,
    qq.question,
    qa.user_answer,
    qq.answer as correct_answer,
    qa.is_correct,
    qa.time_taken_seconds,
    qa.answered_at
FROM quiz_answer qa
JOIN quiz_participant qp ON qa.participant_id = qp.participant_id
JOIN users u ON qp.user_id = u.user_id
JOIN quiz_question qq ON qa.question_id = qq.question_id
WHERE qp.participant_id = ?
ORDER BY qa.answered_at;

-- 2. GET PARTICIPANT STATISTICS
SELECT
    u.name as participant_name,
    COUNT(*) as total_answers,
    SUM(CASE WHEN qa.is_correct = true THEN 1 ELSE 0 END) as correct_answers,
    ROUND(AVG(CASE WHEN qa.is_correct = true THEN 100.0 ELSE 0.0 END), 2) as score_percentage,
    ROUND(AVG(qa.time_taken_seconds), 2) as avg_time_seconds
FROM quiz_answer qa
JOIN quiz_participant qp ON qa.participant_id = qp.participant_id
JOIN users u ON qp.user_id = u.user_id
WHERE qp.participant_id = ?
GROUP BY u.name;

-- 3. FIND MOST DIFFICULT QUESTIONS (lowest success rate)
SELECT
    qq.question_id,
    qq.question,
    COUNT(*) as total_attempts,
    SUM(CASE WHEN qa.is_correct = true THEN 1 ELSE 0 END) as correct_attempts,
    ROUND(100.0 * SUM(CASE WHEN qa.is_correct = true THEN 1 ELSE 0 END) / COUNT(*), 2) as success_rate
FROM quiz_question qq
JOIN quiz_answer qa ON qq.question_id = qa.question_id
GROUP BY qq.question_id, qq.question
HAVING COUNT(*) > 0
ORDER BY success_rate ASC
LIMIT 10;

-- 4. FIND EASIEST QUESTIONS (highest success rate)
SELECT
    qq.question_id,
    qq.question,
    COUNT(*) as total_attempts,
    SUM(CASE WHEN qa.is_correct = true THEN 1 ELSE 0 END) as correct_attempts,
    ROUND(100.0 * SUM(CASE WHEN qa.is_correct = true THEN 1 ELSE 0 END) / COUNT(*), 2) as success_rate
FROM quiz_question qq
JOIN quiz_answer qa ON qq.question_id = qa.question_id
GROUP BY qq.question_id, qq.question
HAVING COUNT(*) > 0
ORDER BY success_rate DESC
LIMIT 10;

-- 5. COMPARE PARTICIPANTS IN A SESSION
SELECT
    u.name as participant_name,
    COUNT(*) as answers_given,
    SUM(CASE WHEN qa.is_correct = true THEN 1 ELSE 0 END) as correct_answers,
    ROUND(100.0 * SUM(CASE WHEN qa.is_correct = true THEN 1 ELSE 0 END) / COUNT(*), 2) as score_percentage,
    ROUND(AVG(qa.time_taken_seconds), 2) as avg_time_seconds,
    MIN(qa.answered_at) as started_at,
    MAX(qa.answered_at) as finished_at
FROM quiz_answer qa
JOIN quiz_participant qp ON qa.participant_id = qp.participant_id
JOIN users u ON qp.user_id = u.user_id
JOIN quiz_session qs ON qp.session_id = qs.session_id
WHERE qs.session_code = ?
GROUP BY u.name, qp.participant_id
ORDER BY score_percentage DESC, avg_time_seconds ASC;

-- 6. GET FASTEST CORRECT ANSWERS
SELECT
    u.name as participant_name,
    qq.question,
    qa.user_answer,
    qa.time_taken_seconds
FROM quiz_answer qa
JOIN quiz_participant qp ON qa.participant_id = qp.participant_id
JOIN users u ON qp.user_id = u.user_id
JOIN quiz_question qq ON qa.question_id = qq.question_id
WHERE qa.is_correct = true
  AND qa.time_taken_seconds IS NOT NULL
ORDER BY qa.time_taken_seconds ASC
LIMIT 20;

-- 7. GET WRONG ANSWERS WITH COMMON MISTAKES
SELECT
    qq.question,
    qq.answer as correct_answer,
    qa.user_answer as common_wrong_answer,
    COUNT(*) as times_selected
FROM quiz_answer qa
JOIN quiz_question qq ON qa.question_id = qq.question_id
WHERE qa.is_correct = false
GROUP BY qq.question_id, qq.question, qq.answer, qa.user_answer
HAVING COUNT(*) > 1
ORDER BY times_selected DESC;

-- 8. PARTICIPANT PERFORMANCE OVER TIME
SELECT
    DATE(qa.answered_at) as quiz_date,
    u.name as participant_name,
    COUNT(*) as questions_answered,
    SUM(CASE WHEN qa.is_correct = true THEN 1 ELSE 0 END) as correct_answers,
    ROUND(100.0 * SUM(CASE WHEN qa.is_correct = true THEN 1 ELSE 0 END) / COUNT(*), 2) as daily_score
FROM quiz_answer qa
JOIN quiz_participant qp ON qa.participant_id = qp.participant_id
JOIN users u ON qp.user_id = u.user_id
WHERE u.user_id = ?
GROUP BY DATE(qa.answered_at), u.name
ORDER BY quiz_date DESC;

-- 9. QUIZ COMPLETION RATE
SELECT
    q.name as quiz_name,
    COUNT(DISTINCT qp.participant_id) as total_participants,
    COUNT(DISTINCT CASE WHEN qp.completed = true THEN qp.participant_id END) as completed_participants,
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN qp.completed = true THEN qp.participant_id END) /
          COUNT(DISTINCT qp.participant_id), 2) as completion_rate
FROM quiz q
JOIN quiz_session qs ON q.quiz_id = qs.quiz_id
JOIN quiz_participant qp ON qs.session_id = qp.session_id
GROUP BY q.quiz_id, q.name;

-- 10. DETAILED ANSWER ANALYSIS FOR A SPECIFIC QUESTION
SELECT
    qq.question,
    qq.answer as correct_answer,
    qa.user_answer,
    COUNT(*) as times_selected,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) as percentage,
    CASE WHEN qa.user_answer = qq.answer THEN 'CORRECT' ELSE 'WRONG' END as status
FROM quiz_answer qa
JOIN quiz_question qq ON qa.question_id = qa.question_id
WHERE qq.question_id = ?
GROUP BY qq.question, qq.answer, qa.user_answer
ORDER BY times_selected DESC;

-- 11. LEADERBOARD - TOP PERFORMERS
SELECT
    ROW_NUMBER() OVER (ORDER BY
        100.0 * SUM(CASE WHEN qa.is_correct = true THEN 1 ELSE 0 END) / COUNT(*) DESC,
        AVG(qa.time_taken_seconds) ASC
    ) as rank,
    u.name as participant_name,
    COUNT(*) as total_questions,
    SUM(CASE WHEN qa.is_correct = true THEN 1 ELSE 0 END) as correct_answers,
    ROUND(100.0 * SUM(CASE WHEN qa.is_correct = true THEN 1 ELSE 0 END) / COUNT(*), 2) as score_percentage,
    ROUND(AVG(qa.time_taken_seconds), 2) as avg_time_seconds
FROM quiz_answer qa
JOIN quiz_participant qp ON qa.participant_id = qp.participant_id
JOIN users u ON qp.user_id = u.user_id
GROUP BY u.user_id, u.name
HAVING COUNT(*) >= 5  -- At least 5 questions answered
ORDER BY score_percentage DESC, avg_time_seconds ASC
LIMIT 20;

-- 12. SESSION SUMMARY
SELECT
    qs.session_code,
    q.name as quiz_name,
    qs.created_at,
    qs.status,
    COUNT(DISTINCT qp.participant_id) as total_participants,
    COUNT(qa.answer_id) as total_answers,
    ROUND(AVG(CASE WHEN qa.is_correct = true THEN 100.0 ELSE 0.0 END), 2) as avg_score,
    ROUND(AVG(qa.time_taken_seconds), 2) as avg_time_per_question
FROM quiz_session qs
JOIN quiz q ON qs.quiz_id = q.quiz_id
LEFT JOIN quiz_participant qp ON qs.session_id = qp.session_id
LEFT JOIN quiz_answer qa ON qp.participant_id = qa.participant_id
WHERE qs.session_code = ?
GROUP BY qs.session_id, qs.session_code, q.name, qs.created_at, qs.status;

