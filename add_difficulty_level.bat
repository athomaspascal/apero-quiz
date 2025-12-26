@echo off
echo Starting PowerShell script to add difficulty_level...
powershell -ExecutionPolicy Bypass -Command ^
"$inputFile = 'src/main/resources/quiz-questions.json'; ^
Write-Host 'Reading file...' -ForegroundColor Green; ^
$json = Get-Content $inputFile -Raw -Encoding UTF8 | ConvertFrom-Json; ^
Write-Host \"Total quizzes: $($json.Count)\" -ForegroundColor Green; ^
$totalQuestions = 0; ^
$modified = 0; ^
foreach ($quiz in $json) { ^
    if ($quiz.questions) { ^
        foreach ($question in $quiz.questions) { ^
            $totalQuestions++; ^
            if (-not ($question.PSObject.Properties.Name -contains 'difficulty_level')) { ^
                $question | Add-Member -MemberType NoteProperty -Name 'difficulty_level' -Value 1 -Force; ^
                $modified++; ^
            } ^
        } ^
    } ^
} ^
Write-Host \"Total questions: $totalQuestions\" -ForegroundColor Green; ^
Write-Host \"Modified: $modified\" -ForegroundColor Green; ^
$timestamp = Get-Date -Format 'yyyyMMdd_HHmmss'; ^
$backupFile = \"src/main/resources/quiz-questions_backup_$timestamp.json\"; ^
Write-Host \"Creating backup: $backupFile\" -ForegroundColor Yellow; ^
Copy-Item $inputFile $backupFile; ^
Write-Host 'Writing JSON...' -ForegroundColor Green; ^
$json | ConvertTo-Json -Depth 100 | Set-Content $inputFile -Encoding UTF8; ^
Write-Host 'COMPLETED SUCCESSFULLY!' -ForegroundColor Green"
echo Done!
pause

