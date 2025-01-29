import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Load synthetic data CSV
csv_path = r"C:\Users\ponma\OneDrive\Desktop\datamodel\synthetic_data.csv"
df = pd.read_csv(csv_path)

# Create directed graph
G = nx.DiGraph()

# Add tables as nodes
tables = set(df["Left_Table"]).union(set(df["Right_Table"]))
for table in tables:
    G.add_node(table, shape="rectangle", color="lightblue")

# Add joins as edges
for _, row in df.iterrows():
    G.add_edge(row["Left_Table"], row["Right_Table"], label=row["Join_condition"])

# Function to get the hierarchy up to a specified number of levels
def get_table_hierarchy(table, G, visited=None, level=0, max_levels=None):
    if visited is None:
        visited = set()

    # If max_levels is None or '*', we allow unlimited recursion
    if max_levels is not None and max_levels != "*" and level >= max_levels:
        return {}

    # Add the current table to the visited set to avoid cycles
    visited.add(table)

    # Dictionary to hold the current table and its related tables (subtree)
    hierarchy = {}

    # Find neighbors (tables connected to the current table)
    neighbors = set()
    
    # Check connections where the table is the "Left Table"
    for _, row in df[df["Left_Table"] == table].iterrows():
        neighbors.add(row["Right_Table"])
    
    # Check connections where the table is the "Right Table"
    for _, row in df[df["Right_Table"] == table].iterrows():
        neighbors.add(row["Left_Table"])

    # Recursively find the sub-trees for each neighbor
    for neighbor in neighbors:
        if neighbor not in visited:
            # Recursively call to get deeper levels
            sub_hierarchy = get_table_hierarchy(neighbor, G, visited, level + 1, max_levels)
            join_condition = ""
            
            # Get the join condition for this neighbor
            if table in G.neighbors(neighbor):
                join_condition = G[neighbor][table]["label"]
            if neighbor in G.neighbors(table):
                join_condition = G[table][neighbor]["label"]

            hierarchy[neighbor] = f"{join_condition}"

            # If the sub-hierarchy exists, include it in the current level's hierarchy
            if sub_hierarchy:
                hierarchy[neighbor] = {"join_condition": join_condition, "sub_tables": sub_hierarchy}
    
    return hierarchy

# Function to print the hierarchy in a readable format
def print_hierarchy(hierarchy, level=0):
    for table, details in hierarchy.items():
        join_condition = details["join_condition"] if isinstance(details, dict) else details
        print('  ' * level + f"- {table} ({join_condition})")
        if isinstance(details, dict) and "sub_tables" in details:
            print_hierarchy(details["sub_tables"], level + 1)

# Prompt the user for the starting table name and the number of levels
starting_table = input("Please enter the table name to start the hierarchy from: ")
max_levels_input = input("Please enter the number of levels of hierarchy to display (or '*' for full hierarchy): ")

# Determine max_levels value
max_levels = None
if max_levels_input != "*":
    try:
        max_levels = int(max_levels_input)
    except ValueError:
        print("Invalid input for levels. Enter an integer or '*' for full hierarchy.")

# Check if the table exists in the graph
if starting_table not in G.nodes:
    print(f"Table '{starting_table}' does not exist in the data.")
else:
    # Get the hierarchy for the starting table
    hierarchy = get_table_hierarchy(starting_table, G, max_levels=max_levels)

    # Print the hierarchy for the starting table
    print(f"\nHierarchy for table '{starting_table}' (up to {max_levels_input} levels):")
    print_hierarchy(hierarchy)
