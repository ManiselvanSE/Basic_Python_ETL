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

### 1. PostgreSQL Setup on Mac

#### Option A: Using Homebrew (Recommended)
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install PostgreSQL
brew install postgresql@15

# Start PostgreSQL service
brew services start postgresql@15

# Verify installation
postgres --version
```

#### Option B: Using PostgreSQL Official Installer
- Download from [postgresql.org](https://www.postgresql.org/download/macosx/)
- Follow the installer wizard
- Remember the password you set for the `postgres` user

### 2. Database Creation

```bash
# Connect to PostgreSQL as the default postgres user
psql -U postgres

# Inside psql, create a new database
CREATE DATABASE etl_lab;

# Verify database creation
\l

# Exit psql
\q
```

### 3. Table Creation

Connect to the database and create tables:

```bash
# Connect to the etl_lab database
psql -U postgres -d etl_lab

# Create sales_data table
CREATE TABLE sales_data (
    id SERIAL PRIMARY KEY,
    product VARCHAR(255),
    quantity INTEGER,
    price DECIMAL(10, 2),
    sale_date DATE,
    region VARCHAR(100)
);

# Create marketing_impressions table
CREATE TABLE marketing_impressions (
    id SERIAL PRIMARY KEY,
    campaign_id INTEGER,
    impressions INTEGER,
    clicks INTEGER,
    date DATE,
    channel VARCHAR(100)
);

# Verify table creation
\dt

# Exit psql
\q
```

### 4. Load Data from CSV Files

```bash
# Connect to the etl_lab database
psql -U postgres -d etl_lab

# Import sales_data.csv
\COPY sales_data(product, quantity, price, sale_date, region) FROM '/path/to/sales_data.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');

# Import marketing_impressions_.csv
\COPY marketing_impressions(campaign_id, impressions, clicks, date, channel) FROM '/path/to/marketing_impressions_.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');

# Verify data was loaded
SELECT COUNT(*) FROM sales_data;
SELECT COUNT(*) FROM marketing_impressions;

# Exit psql
\q
```

**Note:** Replace `/path/to/` with the actual path to your CSV files in the repository.

### 5. Python Environment Setup

```bash
# Navigate to the project directory
cd /path/to/basic-etl-1

# Create a virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install required dependencies
pip install -r requirements.txt
# or manually install:
pip install sqlalchemy pandas psycopg2-binary
```

### 6. Configure Database Connection

Update the database connection string in your Python script:

```python
# In basic-etl-1.py, update the connection string:
DATABASE_URL = "postgresql://postgres:your_password@localhost:5432/etl_lab"

# Create engine
engine = create_engine(DATABASE_URL)
```

**Note:** Replace `your_password` with the password you set for the PostgreSQL `postgres` user.

### 7. Run the Python Script

```bash
# Make sure you're in the project directory with the virtual environment activated
cd /path/to/basic-etl-1
source .venv/bin/activate

# Execute the ETL script
python basic-etl-1.py

# Expected output:
# - Data extracted from sales_data and marketing_impressions tables
# - Data transformed (INNER JOIN applied)
# - Transformed data loaded to a new table in PostgreSQL
```

### 8. Verify the Results

```bash
# Connect to the database
psql -U postgres -d etl_lab

# Check the newly created table (usually named 'pseudo_data_warehouse' or similar)
SELECT * FROM pseudo_data_warehouse LIMIT 5;

# Check row count
SELECT COUNT(*) FROM pseudo_data_warehouse;

# Exit psql
\q
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `psql: command not found` | Add PostgreSQL to PATH: `export PATH="/usr/local/opt/postgresql@15/bin:$PATH"` |
| `FATAL: role "postgres" does not exist` | Recreate the postgres user or use your system username |
| `Connection refused` | Ensure PostgreSQL service is running: `brew services start postgresql@15` |
| `CSV import fails` | Check file path is absolute, file exists, and permissions are correct |
| `ModuleNotFoundError: sqlalchemy` | Activate virtual environment: `source .venv/bin/activate` |

---