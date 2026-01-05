# Duel Quiz Feature Implementation
## Date: 2026-01-05

### Overview
Implementation of a new "Duel Quiz" feature that allows players to challenge each other in real-time quiz competitions.

### Features Implemented

#### 1. Core Entities
- **DuelMatch Entity** (`DuelMatch.java`)
  - Tracks duel matches between two players
  - Manages duel status lifecycle (SEARCHING → MATCHED → COUNTDOWN → IN_PROGRESS → FINISHED)
  - Supports up to 2 rematches per duel
  - Stores scores and ready states for both players

#### 2. Services
- **DuelService** (`DuelService.java`)
  - `startSearching()`: Initiates search for opponent or matches with waiting player
  - `acceptMatch()`: Players accept the duel match
  - `startQuiz()`: Starts the quiz after countdown
  - `submitScore()`: Submits player score at completion
  - `requestRematch()`: Handles rematch requests
  - `cancelDuel()`: Cancels an active duel

- **DuelMatchRepository** (`DuelMatchRepository.java`)
  - Custom queries for finding searching matches
  - Finding active duels for a user

#### 3. User Interface
- **DuelQuizView** (`DuelQuizView.java`)
  - Initial view with "Search for Opponent" button
  - Searching view with animated spinner
  - Matched view showing opponent and randomly selected quiz
  - Countdown view (5 seconds) before quiz starts
  - Scoreboard view showing results
  - Rematch view (up to 2 rematches allowed)
  - Auto-polling every 2 seconds to detect status changes
  - Real-time updates using UI.access() and push

#### 4. Quiz Integration
- **QuizQuestionView** modified to:
  - Detect `duel` parameter in URL
  - Submit score to DuelService upon completion
  - Redirect back to duel view after quiz completion

#### 5. Translations
Added translations in 3 languages (English, French, Italian) for:
- Menu entry
- Welcome screen
- Search screen
- Match acceptance
- Countdown
- Results display
- Rematch options
- Error messages

### User Flow

1. **Start Duel**
   - Player clicks "Duel Quiz" menu
   - Player clicks "Search for Opponent"

2. **Matchmaking**
   - System searches for another player in SEARCHING state
   - If found: Both players are notified and a random quiz is selected
   - If not found: Player waits in queue until another player joins

3. **Match Acceptance**
   - Both players see opponent name and quiz name
   - Both players must click "Accept Duel"
   - Either player can decline to cancel

4. **Countdown**
   - Once both accept, 5-second countdown starts
   - Countdown displayed in large font
   - Auto-starts quiz when countdown reaches 0

5. **Quiz Execution**
   - Both players answer the same quiz independently
   - Standard quiz interface with timer
   - Score tracked for each player

6. **Results**
   - Scoreboard shows both players' scores
   - Winner is declared (or draw if tied)
   - Option for rematch (max 2 rematches)

7. **Rematch**
   - Both players must accept rematch
   - New random quiz is selected
   - Countdown starts again
   - After 3 total matches (1 + 2 rematches), duel ends

8. **Cancel Anytime**
   - Players can cancel during search or after completion
   - Returns to main menu

### Technical Details

#### Database Schema
New table: `duel_match`
- `duel_id` (Primary Key)
- `player1_id` (Foreign Key to User)
- `player2_id` (Foreign Key to User)
- `quiz_id` (Foreign Key to Quiz)
- `status` (Enum: SEARCHING, MATCHED, COUNTDOWN, IN_PROGRESS, FINISHED, REMATCH_PENDING, CANCELLED)
- `player1_score`, `player2_score`
- `player1_ready`, `player2_ready`
- `player1_rematch`, `player2_rematch`
- `rematch_count`
- `created_at`, `started_at`, `finished_at`, `countdown_started_at`

#### Real-time Updates
- Uses `ScheduledExecutorService` for polling
- Polls every 2 seconds for status changes
- Uses Vaadin Push for instant UI updates
- Separate countdown scheduler for 5-second timer

#### Random Quiz Selection
- DuelService randomly selects a quiz from all available quizzes
- Uses Java's `Random` class
- Different quiz for each rematch

### Menu Integration
- Added menu entry "menu.duelquiz" with trophy icon
- Menu order: 2 (after "Start a quizz", before "Join Session")
- Route: `/duel-quiz`

### Translation Keys Added
```
menu.duelquiz
duelquiz.title
duelquiz.welcome
duelquiz.description
duelquiz.search
duelquiz.back
duelquiz.cancel
duelquiz.searching
duelquiz.searching.text
duelquiz.matched
duelquiz.opponent
duelquiz.quiz
duelquiz.accept
duelquiz.decline
duelquiz.countdown.title
duelquiz.countdown.ready
duelquiz.countdown.go
duelquiz.finished
duelquiz.winner
duelquiz.draw
duelquiz.rematch
duelquiz.rematch.available
duelquiz.rematch.accepted
duelquiz.rematch.waiting
duelquiz.exit
duelquiz.cancelled
duelquiz.cancelled.message
```

### Files Created
1. `src/main/java/com/quizz/core/entity/DuelMatch.java`
2. `src/main/java/com/quizz/core/repository/DuelMatchRepository.java`
3. `src/main/java/com/quizz/core/service/DuelService.java`
4. `src/main/java/com/quizz/core/ui/DuelQuizView.java`

### Files Modified
1. `src/main/java/com/quizz/core/ui/QuizQuestionView.java`
   - Added DuelService injection
   - Added duelId tracking
   - Added score submission for duels

2. `src/main/resources/messages.properties`
3. `src/main/resources/messages_en.properties`
4. `src/main/resources/messages_fr.properties`
5. `src/main/resources/messages_it.properties`

### Next Steps (Future Enhancements)
1. Add ELO rating system for competitive ranking
2. Add duel history and statistics
3. Add friend challenges (direct invites)
4. Add tournament mode (bracket system)
5. Add chat during duel
6. Add spectator mode
7. Add duel leaderboards
8. Add difficulty-based matchmaking
9. Add time-limited special events

### Testing Checklist
- [ ] Two players can successfully match
- [ ] Countdown works correctly
- [ ] Quiz starts automatically after countdown
- [ ] Scores are submitted correctly
- [ ] Scoreboard displays correctly
- [ ] Rematch works (up to 2 times)
- [ ] Cancel works at any stage
- [ ] Multiple concurrent duels work
- [ ] Translations work in all languages
- [ ] UI updates in real-time
- [ ] No memory leaks (executors properly shut down)

