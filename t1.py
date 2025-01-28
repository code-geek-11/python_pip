import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Define the path to your CSV file
csv_path = r"C:\Users\ponma\OneDrive\Desktop\datamodel\data_model.csv"

# Read the CSV file
df = pd.read_csv(csv_path)

# Create a directed graph
G = nx.DiGraph()

# Add nodes (Tables)
tables = set(df["Left_Table"]).union(set(df["Right_Table"]))
for table in tables:
    G.add_node(table, shape="rectangle", color="lightblue")

# Add edges (Relationships)
for _, row in df.iterrows():
    left_table = row["Left_Table"]
    right_table = row["Right_Table"]
    join_condition = row["Join_condition"]
    
    G.add_edge(left_table, right_table, label=join_condition)

# Draw the graph
plt.figure(figsize=(10, 6))
pos = nx.spring_layout(G)  # Layout for positioning nodes
edge_labels = {(u, v): d['label'] for u, v, d in G.edges(data=True)}

# Draw nodes
nx.draw(G, pos, with_labels=True, node_size=3000, node_color="lightblue", edge_color="black", font_size=10, font_weight="bold")

# Draw edge labels (Join Conditions)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, label_pos=0.5)

# Display the ER diagram
plt.title("ER Model Diagram", fontsize=14, fontweight="bold")
plt.show()
