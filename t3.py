from pyvis.network import Network

# Create interactive network
net = Network(height="900px", width="100%", directed=True, notebook=True, cdn_resources="remote")

# Add nodes
for table in tables:
    net.add_node(table, label=table, color="lightblue")

# Add edges with tooltips
for _, row in df.iterrows():
    net.add_edge(row["Left_Table"], row["Right_Table"], title=row["Join_condition"])

# Save and display
net.show("ER_Diagram.html")  # Opens in the browser
