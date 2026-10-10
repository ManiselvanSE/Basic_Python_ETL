# Basic ETL 1
# Description
This is a basic ETL Project where the two .csv files in this repository were first downloaded from a source and saved to a local machine, and then imported to a locally hosted database using PostgreSQL as two separate tables. 

The objective of this basic project is to use Python to:
    Extract     - By creating a link to the local PostgreSQL database and get the two tables.
    Transform   - By writing a function that will INNER JOIN the two tables and become a single table. This single table would become a pseudo data warehouse.
    Load        - By saving the newly created pseudo data warehouse to the local PostgreSQL database

The Python libraries used in this simple project are SQLAlchemy and Pandas. SQLAlchemy was used during the Extract Phase, while Pandas was used to do some data wrangling during the Transform Phase.

---

## Step-by-Step Execution Guide

### Step 1: Set Up Python Virtual Environment

```bash
# Navigate to project directory
cd basic-etl-1

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install required dependencies
pip install sqlalchemy pandas psycopg2-binary
```

### Step 2: Install PostgreSQL on Mac

```bash
# Install PostgreSQL using Homebrew
brew install postgresql@16

# Start the PostgreSQL service
brew services start postgresql@16

# Verify installation
psql --version
# Expected output: psql (PostgreSQL) 16.15 (Homebrew)
```

### Step 3: Create Database and Connect

```bash
# Connect to PostgreSQL default database
psql -d postgres

# Create the basic_etl database
CREATE DATABASE basic_etl;

# Connect to the new database
\c basic_etl

# List all databases to verify
\l

# Exit psql
\q
```

### Step 4: Create Tables in PostgreSQL

```bash
# Connect to basic_etl database
psql -d basic_etl

# Create marketing_impressions table
CREATE TABLE marketing_impressions (
    session_id INTEGER,
    user_id INTEGER,
    campaign_id INTEGER,
    campaign_name VARCHAR(255),
    webpage_id INTEGER,
    product_category VARCHAR(255),
    gender VARCHAR(50),
    age_level VARCHAR(50),
    region VARCHAR(100),
    is_click INTEGER
);

# Create sales_data table
CREATE TABLE sales_data (
    session_id INTEGER,
    user_id INTEGER,
    product_category VARCHAR(255),
    region VARCHAR(100),
    is_campaign INTEGER,
    total_php INTEGER
);

# Verify tables created
\dt

# Exit psql
\q
```

### Step 5: Load CSV Data into PostgreSQL

```bash
# Connect to basic_etl database
psql -d basic_etl

# Load marketing_impressions data from CSV
\copy marketing_impressions FROM 'marketing_impressions_.csv' CSV HEADER;
# Expected: COPY 128858

# Load sales_data from CSV
\copy sales_data FROM 'sales_data.csv' CSV HEADER;
# Expected: COPY 99999

# Verify data loaded correctly
SELECT COUNT(*) FROM marketing_impressions;
SELECT COUNT(*) FROM sales_data;

# Exit psql
\q
```

### Step 6: Configure Database Connection (Update basic-etl-1.py)

Edit `basic-etl-1.py` and update the database connection string:

```python
db_engine = sqlalchemy.create_engine(
    "postgresql+psycopg2://maniselvank@localhost:5432/basic_etl"
)

```

**Note:** Use your macOS username (e.g., maniselvank) instead of 'postgres'

### Step 7: Fix Table Names and SQL Queries (if needed)

If the script references a table name that doesn't exist, rename it:

```bash
psql -d basic_etl

# Example: Rename sales_data to sales if script expects 'sales' table
ALTER TABLE sales_data RENAME TO sales;

# Exit
\q
```

**Common SQL Issues:**
- Change `WHERE is_click = TRUE` to `WHERE is_click = 1` (comparing integer, not boolean)
- Ensure table names match between CSV import and Python script expectations

### Step 8: Run the ETL Python Script

```bash
# Make sure virtual environment is activated
source .venv/bin/activate

# Execute the ETL script
python3 basic-etl-1.py

# Expected Output:
# - Extracts 128,858 marketing records
# - Extracts 99,999 sales records
# - Transforms via INNER JOIN → 131,051 matched records
# - Loads analysis_marketing_sales table to PostgreSQL
# - Calculates CTR (Click-Through Rate) per campaign
```

### Step 9: Verify Results in PostgreSQL

```bash
# Connect to database
psql -d basic_etl

# Check tables created
\dt

# Count rows in analysis table
SELECT COUNT(*) FROM analysis_marketing_sales;
# Expected: 131051

# View sample data
SELECT * FROM analysis_marketing_sales LIMIT 5;

# Exit
\q
```

---

## Troubleshooting & Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| `connection to server at "localhost" (::1), port 5432 failed: FATAL: role "postgres" does not exist` | Homebrew doesn't create postgres role on macOS | Use your macOS username in connection string: `postgresql+psycopg2://maniselvank@localhost:5432/basic_etl` |
| `relation "sales" does not exist` | Table name mismatch between script and database | Rename table: `ALTER TABLE sales_data RENAME TO sales;` |
| `operator does not exist: integer = boolean` | Script compares integer with TRUE instead of 1 | Replace `WHERE is_click = TRUE` with `WHERE is_click = 1` |
| `psql: command not found` | PostgreSQL bin not in PATH | Run: `export PATH="/opt/homebrew/opt/postgresql@16/bin:$PATH"` |
| `CONNECT tunnel failed, response 403` | Network connectivity issue with GitHub | Check internet connection; retry git push |
| `ModuleNotFoundError: sqlalchemy` | Dependencies not installed | Install: `pip install sqlalchemy pandas psycopg2-binary` |
| `psql: error: connection to server on socket "/tmp/.s.PGSQL.5432" failed` | PostgreSQL service not running | Start service: `brew services start postgresql@16` |

---