import sqlite3
import re

# connect to the db
conn = sqlite3.connect(R'D:\your\path\here\xxx_xxx.gpkg')
cursor = conn.cursor()

# fetch patterns to exclude from the existing (exclusion_patterns) table
cursor.execute("SELECT pattern FROM exclusion_patterns;")
patterns_to_exclude = [row[0] for row in cursor.fetchall()]

# define the specific tables you want to include in the query
selected_tables = ['table_01', 'table_02', 'table_03'] 

# define ANSI color codes for green and red (not sure if these will show up well in every console)
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

for table_name in selected_tables:
    query = f"PRAGMA table_info('{table_name}')"
    cursor.execute(query)
    columns = cursor.fetchall()

    accepted_columns = []
    excluded_columns = []
    
    for column in columns:
        column_name = column[1]
        # check if any column name matches any of the patterns to exclude
        if any(re.search(rf'\b{pattern}\b', column_name) for pattern in patterns_to_exclude):
            excluded_columns.append(column_name)
        else:
            accepted_columns.append(column_name)
    
    # print accepted and excluded columns with color highlighting (green is ok, red is flagged)
    print(f"\nTable: {table_name}")
    
    if accepted_columns:
        print(f"{GREEN}Accepted Columns: {', '.join(accepted_columns)}{RESET}")
    if excluded_columns:
        print(f"{RED}Excluded Columns: {', '.join(excluded_columns)}{RESET}")

# close the connection (probably always)
conn.close()