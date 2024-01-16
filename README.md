# Basic ETL 1
# Description
This is a basic ETL Project where the two .csv files in this repository were first downloaded from a source and saved to a local machine, and then imported to a locally hosted database using PostgreSQL as two separate tables. 

The objective of this basic project is to use Python to:
    Extract     - By creating a link to the local PostgreSQL database and get the two tables.
    Transform   - By writing a function that will INNER JOIN the two tables and become a single table. This single table would become a pseudo data warehouse.
    Load        - By saving the newly created pseudo data warehouse to the local PostgreSQL database

The Python libraries used in this simple project are SQLAlchemy and Pandas. SQLAlchemy was used during the Extract Phase, while Pandas was used to do some data wrangling during the Transform Phase.