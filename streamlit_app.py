import streamlit as st
from pyvis.network import Network
import pandas as pd
from io import BytesIO

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

# Define node positions explicitly for a clear hierarchy
node_positions = {
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

def draw_interactive_graph(node_weights):
    net = Network(notebook=True, height="800px", width="100%", bgcolor="#fafafa", font_color="black")

    # Add nodes with tooltips
    for node, description in node_descriptions.items():
        size = max(20 + 50 * abs(node_weights.get(node, 0)), 20)  # Minimum size of 20
        color = 'green' if node_weights.get(node, 0) >= 0 else 'red'
        pos = node_positions.get(node, (0, 0))  # Default to (0,0) if not specified
        net.add_node(node, label=node, title=description, size=size, color=color, x=pos[0], y=pos[1])
    
    # Add edges with tooltips
    for u, v in edge_descriptions.keys():
        width = max(2 + 4 * abs(node_weights.get(u, 0)), 2)  # Minimum width of 2
        net.add_edge(u, v, title=edge_descriptions[(u, v)], width=width)
    
    # Return the network as an HTML file
    path = '/tmp/network.html'
    net.save_graph(path)
    return path

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
    path = draw_interactive_graph(node_weights)
    st.components.v1.html(open(path, 'r').read(), height=800)
except Exception as e:
    st.error(f"An error occurred while generating the graph: {e}")
