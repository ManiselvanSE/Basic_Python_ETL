import sqlalchemy
import pandas as pd

# Extract
db_engine = sqlalchemy.create_engine(
    "postgresql+psycopg2://postgres:password123@localhost:5432/PopCRT"
)


def extract_table_from_db(tablename, db_engine):
    return pd.read_sql(f"SELECT * FROM {tablename}", db_engine)


# Transform
def join_tables_into_one(first_table, second_table, db_engine):
    return pd.read_sql(
        f"SELECT * FROM {first_table} AS a FULL OUTER JOIN {second_table} AS b ON a.user_id = b.user_id WHERE is_campaign = True",
        db_engine,
    )


# Join two tables "marketing_impressions" and "sales" into one with specific columns
def join_two_tables_into_one(first_table, second_table, db_engine):
    return pd.read_sql(
        f"SELECT a.user_id, a.session_id AS marketing_session_id, b.session_id AS sales_session_id, a.campaign_id, a.campaign_name, a.product_category AS marketing_prod_cat, b.product_category AS sales_prod_cat, a.gender, a.age_level, a.region AS marketing_region, b.region AS sales_region, a.is_click, b.is_campaign, b.total_php FROM {first_table} AS a LEFT JOIN {second_table} AS b ON a.user_id = b.user_id WHERE b.total_php IS NOT NULL",
        db_engine,
    )


# Calculate Click-Through-Rate (CTR) Per Campaign
def calculate_CTR_per_campaign(tablename, db_engine):
    return pd.read_sql(
        f"SELECT campaign_id, campaign_name, COUNT(is_click::boolean)::numeric AS impressions_per_campaign, COUNT(is_click::boolean) FILTER(WHERE is_click = TRUE)::numeric AS clicked_campaign, ROUND(((COUNT(is_click::boolean) FILTER(WHERE is_click = TRUE)::numeric) /  (COUNT(is_click::boolean))::numeric)*100, 2) AS CTR_per_campaign FROM {tablename} GROUP BY campaign_id, campaign_name ORDER BY CTR_per_campaign DESC",
        db_engine,
    )


def etl(db_engine):
    # Extract
    marketing_impressions_df = extract_table_from_db("marketing_impressions", db_engine)
    sales_df = extract_table_from_db("sales", db_engine)
    print(marketing_impressions_df)
    print(sales_df)

    # Transform
    transformed_df = join_tables_into_one("marketing_impressions", "sales", db_engine)
    print(transformed_df)

    analysis_marketing_sales = join_two_tables_into_one(
        "marketing_impressions", "sales", db_engine
    )
    print(analysis_marketing_sales)

    CTR_per_campaign = calculate_CTR_per_campaign("marketing_impressions", db_engine)
    print(CTR_per_campaign)

    # Load
    analysis_marketing_sales.to_sql(
        "analysis_marketing_sales",
        db_engine,
        index=False,
        if_exists="replace",
    )

    AMS_df = pd.read_sql("SELECT * FROM analysis_marketing_sales", db_engine)
    print(AMS_df)


etl(db_engine)
