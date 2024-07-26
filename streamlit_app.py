import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from io import BytesIO

# Function to create and display the graph
def draw_graph(node_weights):
    G = nx.DiGraph()
    
    # Define nodes and positions
    nodes = {
        'Central Bank Policies\n(Interest Rates)': (0, 3),
        'Bond Yields\n(Yield Curve)': (1, 3),
        'Economic Growth\n(GDP)': (2, 3),
        'Inflation Rates': (0, 2),
        'Employment Data\n(Unemployment Rate, NFP)': (1, 2),
        'Consumer Confidence': (2, 2),
        'US Dollar Index\n(DXY)': (0, 1),
        'Oil Prices\n(WTI, Brent)': (1, 1),
        'Equities\n(Stocks)': (2, 1),
        'High-Yield Bonds': (0, 0),
        'Commodities': (1, 0),
        'Cryptocurrencies': (2, 0),
        'Bitcoin (BTC)': (2, -1),
        'Ethereum (ETH)': (1, -1),
        'Large-Cap Altcoins': (0, -1),
        'Small-Cap Altcoins': (2, -2)
    }
    
    G.add_nodes_from(nodes.keys())
    
    # Define edges
    edges = [
        ('Central Bank Policies\n(Interest Rates)', 'Inflation Rates'),
        ('Central Bank Policies\n(Interest Rates)', 'Bond Yields\n(Yield Curve)'),
        ('Bond Yields\n(Yield Curve)', 'High-Yield Bonds'),
        ('Economic Growth\n(GDP)', 'Consumer Confidence'),
        ('Economic Growth\n(GDP)', 'Equities\n(Stocks)'),
        ('Inflation Rates', 'High-Yield Bonds'),
        ('Employment Data\n(Unemployment Rate, NFP)', 'Equities\n(Stocks)'),
        ('US Dollar Index\n(DXY)', 'Oil Prices\n(WTI, Brent)'),
        ('Oil Prices\n(WTI, Brent)', 'Commodities'),
        ('Commodities', 'High-Yield Bonds'),
        ('Commodities', 'Cryptocurrencies'),
        ('Cryptocurrencies', 'Bitcoin (BTC)'),
        ('Cryptocurrencies', 'Ethereum (ETH)'),
        ('Cryptocurrencies', 'Large-Cap Altcoins'),
        ('Cryptocurrencies', 'Small-Cap Altcoins')
    ]
    
    G.add_edges_from(edges)
    
    # Retrieve node positions
    pos = nodes
    
    # Determine node colors
    node_colors = {node: 'red' if node_weights[node] < 0 else 'green' for node in G.nodes()}
    
    # Draw the graph
    plt.figure(figsize=(12, 8))
    node_size = [500 + 1000 * weight for weight in node_weights.values()]  # Adjust node size based on weight
    edge_width = [0.5 + 1.5 * weight for weight in node_weights.values() if weight > 0]  # Adjust edge width based on weight
    nx.draw(G, pos, with_labels=True, node_size=node_size, node_color=[node_colors[node] for node in G.nodes()],
            alpha=0.8, font_size=10, font_color="black", font_weight="bold", linewidths=2, width=edge_width, edge_color="grey")
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    return buffer

st.title('Risk-On/Risk-Off Environment Simulator - Manual Mode')

# Initialize node weights
node_weights = {
    'Central Bank Policies\n(Interest Rates)': 0,
    'Bond Yields\n(Yield Curve)': 0,
    'Economic Growth\n(GDP)': 0,
    'Inflation Rates': 0,
    'Employment Data\n(Unemployment Rate, NFP)': 0,
    'Consumer Confidence': 0,
    'US Dollar Index\n(DXY)': 0,
    'Oil Prices\n(WTI, Brent)': 0,
    'Equities\n(Stocks)': 0,
    'High-Yield Bonds': 0,
    'Commodities': 0,
    'Cryptocurrencies': 0,
    'Bitcoin (BTC)': 0,
    'Ethereum (ETH)': 0,
    'Large-Cap Altcoins': 0,
    'Small-Cap Altcoins': 0
}

# Input sliders for manual mode
for node in node_weights.keys():
    node_weights[node] = st.slider(f'{node} Impact', -1.0, 1.0, 0.0)

st.write("### Risk Environment Graph")
try:
    graph_image = draw_graph(node_weights)
    st.image(graph_image, use_column_width=True)
except Exception as e:
    st.error(f"An error occurred while generating the graph: {e}")
