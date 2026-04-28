# TSIS 4 Snake Game — Database Integration & Advanced Gameplay

## Structure

```text
TSIS4/
├── main.py
├── game.py
├── db.py
├── config.py
├── settings.json
└── assets/
```

## Features

- PostgreSQL leaderboard
- Username entry in Pygame
- Auto-save result after game over
- Leaderboard Top 10 screen
- Personal best during gameplay
- Weighted food with timer
- Poison food
- Speed boost, slow motion, shield power-ups
- Obstacles from Level 3
- Settings saved to JSON
- Main menu, game over, leaderboard, settings screens

## 1. Create database

```bash
createdb -U postgres snake_db
```

If that does not work:

```bash
psql -U postgres -d postgres
```

Then:

```sql
CREATE DATABASE snake_db;
\q
```

## 2. Edit config.py

Change:

```python
DB_PASSWORD = "your_password"
```

to your real PostgreSQL password.

## 3. Install requirements

```bash
pip3 install pygame psycopg2-binary
```

## 4. Run

```bash
cd /Users/zanajym/Desktop/PP2/TSIS4
python3 main.py
```

The game creates these tables automatically:

```sql
players
game_sessions
```

## Controls

```text
Arrow keys - move snake
Mouse      - menu buttons
```

## GitHub

```bash
git add TSIS4/
git commit -m "Add TSIS4 Snake with database leaderboard"
git push origin main
```
