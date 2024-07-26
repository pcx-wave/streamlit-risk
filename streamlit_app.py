import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
from io import BytesIO  # Import BytesIO for handling in-memory files

# Define node descriptions and edge details
node_descriptions = {
    'Central Bank Policies\n(Interest Rates)': 'Interest rates set by the central bank.',
    'Bond Yields\n(Yield Curve)': 'Interest rates on government bonds.',
    'Economic Growth\n(GDP)': 'Rate of growth of a country\'s GDP.',
    'Inflation Rates': 'Rate of increase in prices over time.',
    'Employment Data\n(Unemployment Rate, NFP)': 'Unemployment rate and non-farm payroll data.',
    'Consumer Confidence': 'Measures consumer sentiment and spending.',
    'US Dollar Index\n(DXY)': 'Index of the US dollar against a basket of other currencies.',
    'Oil Prices\n(WTI, Brent)': 'Prices of crude oil in the global market.',
    'Equities\n(Stocks)': 'Stock prices and equity markets.',
    'High-Yield Bonds': 'Bonds with higher returns but higher risk.',
    'Commodities': 'Prices of raw materials and primary agricultural products.',
    'Cryptocurrencies': 'Digital currencies using cryptographic techniques.',
    'Bitcoin (BTC)': 'Leading cryptocurrency by market cap.',
    'Ethereum (ETH)': 'Second largest cryptocurrency, known for its smart contract functionality.',
    'Large-Cap Altcoins': 'Cryptocurrencies other than Bitcoin and Ethereum with large market caps.',
    'Small-Cap Altcoins': 'Cryptocurrencies with smaller market caps.'
}

edge_descriptions = {
    ('Central Bank Policies\n(Interest Rates)', 'Inflation Rates'): 'Interest rates impact inflation rates.',
    ('Central Bank Policies\n(Interest Rates)', 'Bond Yields\n(Yield Curve)'): 'Central bank policies influence bond yields.',
    ('Bond Yields\n(Yield Curve)', 'High-Yield Bonds'): 'Bond yields affect high-yield bonds returns.',
    ('Economic Growth\n(GDP)', 'Consumer Confidence'): 'Economic growth influences consumer confidence.',
    ('Economic Growth\n(GDP)', 'Equities\n(Stocks)'): 'Economic growth affects stock prices.',
    ('Inflation Rates', 'High-Yield Bonds'): 'Inflation rates impact high-yield bonds.',
    ('Employment Data\n(Unemployment Rate, NFP)', 'Equities\n(Stocks)'): 'Employment data influences stock market performance.',
    ('US Dollar Index\n(DXY)', 'Oil Prices\n(WTI, Brent)'): 'Dollar index impacts oil prices.',
    ('Oil Prices\n(WTI, Brent)', 'Commodities'): 'Oil prices affect commodity prices.',
    ('Commodities', 'High-Yield Bonds'): 'Commodities influence high-yield bonds.',
    ('Commodities', 'Cryptocurrencies'): 'Commodities prices affect cryptocurrencies.',
    ('Cryptocurrencies', 'Bitcoin (BTC)'): 'Cryptocurrencies include Bitcoin.',
    ('Cryptocurrencies', 'Ethereum (ETH)'): 'Cryptocurrencies include Ethereum.',
    ('Cryptocurrencies', 'Large-Cap Altcoins'): 'Cryptocurrencies include large-cap altcoins.',
    ('Cryptocurrencies', 'Small-Cap Altcoins'): 'Cryptocurrencies include small-cap altcoins.'
}

def draw_graph(node_weights):
    G = nx.DiGraph()

    # Add nodes with attributes
    for node, description in node_descriptions.items():
        size = max(20 + 50 * abs(node_weights.get(node, 0)), 20)  # Minimum size of 20
        color = 'green' if node_weights.get(node, 0) >= 0 else 'red'
        G.add_node(node, size=size, color=color, description=description)
    
    # Add edges with attributes
    for u, v in edge_descriptions.keys():
        width = max(2 + 4 * abs(node_weights.get(u, 0)), 2)  # Minimum width of 2
        G.add_edge(u, v, width=width, description=edge_descriptions[(u, v)])

    # Define node positions explicitly
    pos = {
        'Central Bank Policies\n(Interest Rates)': (0, 10),
        'Bond Yields\n(Yield Curve)': (0, 8),
        'Economic Growth\n(GDP)': (0, 6),
        'Inflation Rates': (0, 4),
        'Employment Data\n(Unemployment Rate, NFP)': (0, 2),
        'Consumer Confidence': (0, 0),
        'US Dollar Index\n(DXY)': (0, -2),
        'Oil Prices\n(WTI, Brent)': (0, -4),
        'Equities\n(Stocks)': (0, -6),
        'High-Yield Bonds': (0, -8),
        'Commodities': (0, -10),
        'Cryptocurrencies': (0, -12),
        'Bitcoin (BTC)': (0, -14),
        'Ethereum (ETH)': (0, -16),
        'Large-Cap Altcoins': (0, -18),
        'Small-Cap Altcoins': (0, -20)
    }

    # Draw the graph
    plt.figure(figsize=(12, 10))
    nx.draw(G, pos, with_labels=True, node_size=[G.nodes[node]['size'] for node in G.nodes],
            node_color=[G.nodes[node]['color'] for node in G.nodes],
            edge_color='grey', font_size=8, width=[G.edges[edge]['width'] for edge in G.edges])
    
    # Draw node labels with descriptions
    labels = {node: G.nodes[node]['description'] for node in G.nodes}
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=8)
    
    # Draw edge labels with descriptions
    edge_labels = {(u, v): G.edges[(u, v)]['description'] for u, v in G.edges}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    # Save the plot to a BytesIO object
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    return buf

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
    buf = draw_graph(node_weights)
    st.image(buf)
except Exception as e:
    st.error(f"An error occurred while generating the graph: {e}")
