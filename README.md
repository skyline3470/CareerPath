# Career Path Explorer

A simple Flask web app for students to explore career paths.

## Setup & Run

```bash
# 1. Install Flask
pip install flask

# 2. Enter the project folder
cd career_explorer

# 3. Run the app
python app.py

# 4. Open your browser
# http://localhost:5000
```

## Pages

| URL | Description |
|-----|-------------|
| `/` | Home page |
| `/careers` | Browse all career cards |
| `/career/<name>` | Detail page for one career |
| `/quiz` | 2-question career quiz |
| `/form` | Save your career interest |
| `/admin` | View all saved student data |

## File Structure

```
career_explorer/
├── app.py              ← Flask backend + all routes
├── database.db         ← SQLite DB (auto-created)
├── static/
│   ├── style.css       ← All styling
│   └── script.js       ← Small JS helpers
└── templates/
    ├── base.html        ← Shared nav/footer layout
    ├── index.html       ← Home
    ├── careers.html     ← Career grid
    ├── career_detail.html ← Individual career
    ├── quiz.html        ← Interactive quiz
    ├── form.html        ← Student form (saves to DB)
    └── admin.html       ← Admin table view
```
