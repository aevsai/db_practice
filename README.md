# πΈ Practice work for Database classes at HSE

# How to:
1. Install postgresql
2. Create database `movies`
3. Run following code in terminal
```zsh
git clone git@github.com:aevsai/db_practice.git
cd db_practice
pip install -r requirements.txt
python -m streamlit run ./app/main.py
```

# Models πΊοΈ
Folder `/app/data/models` contains database models:
- `persons` - short info about persons π¨βπ
- `movies` - short info about movies π¬
- `creators` - relation of person and movies with job title and role for actors π§βπ¨
- `countries` β iso alpha-3 πΊπ¦
- `genres`

# Data Access Layer πͺ
Folder `/app/data/access` contains data access objects for each model that provide all CRUD functions.
SqlAlchemy 2.0 used for access to database. Config data stored at `app/database.py`

# UI and Business Logic Layer π§βπ»
UI created with Streamlit integrated with business logic

![UI Screenshot](./screen.png)
