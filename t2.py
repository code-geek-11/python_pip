import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Load the CSV file
csv_path = r"C:\Users\ponma\OneDrive\Desktop\datamodel\data_model.csv"
df = pd.read_csv(csv_path)

# Create a directed graph
G = nx.DiGraph()

# Add nodes (Tables)
tables = set(df["Left_Table"]).union(set(df["Right_Table"]))
for table in tables:
    G.add_node(table, shape="rectangle", color="lightblue")

# Add edges (Joins)
for _, row in df.iterrows():
    left_table = row["Left_Table"]
    right_table = row["Right_Table"]
    join_condition = row["Join_condition"]
    G.add_edge(left_table, right_table, label=join_condition)

# === IMPROVED LAYOUT ===
try:
    pos = nx.nx_agraph.graphviz_layout(G, prog="dot")  # Hierarchical Layout
except:
    pos = nx.kamada_kawai_layout(G)  # Fallback Layout

# Create figure
fig, ax = plt.subplots(figsize=(25, 20))  # Increase size for clarity

# Draw graph
nx.draw(G, pos, with_labels=True, node_size=1500, node_color="lightblue",
        edge_color="gray", font_size=7, font_weight="bold", ax=ax)

# Draw edge labels (join conditions)
edge_labels = {(u, v): d['label'] for u, v, d in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=5, ax=ax)

# Save High-Resolution Image
plt.title("Optimized ER Model Diagram", fontsize=16, fontweight="bold")
plt.savefig("ER_Diagram_HighRes.png", dpi=300, bbox_inches="tight")
plt.show()
