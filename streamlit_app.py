import streamlit as st
import networkx as nx
from pyvis.network import Network
from io import StringIO

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
    ('Central Bank Policies\n(Interest Rates)', 'Inflation Rates'): 'Rising interest rates reduce inflation by lowering spending and investment.',
    ('Central Bank Policies\n(Interest Rates)', 'Bond Yields\n(Yield Curve)'): 'Higher interest rates lead to higher bond yields.',
    ('Bond Yields\n(Yield Curve)', 'High-Yield Bonds'): 'Rising government bond yields increase the returns required from high-yield bonds.',
    ('Economic Growth\n(GDP)', 'Consumer Confidence'): 'Higher GDP growth boosts consumer confidence.',
    ('Economic Growth\n(GDP)', 'Equities\n(Stocks)'): 'Economic growth leads to higher corporate earnings, boosting stock prices.',
    ('Inflation Rates', 'High-Yield Bonds'): 'Higher inflation leads to higher yields on high-yield bonds to compensate for inflation risk.',
    ('Employment Data\n(Unemployment Rate, NFP)', 'Equities\n(Stocks)'): 'Lower unemployment leads to higher consumer spending, boosting stock prices.',
    ('US Dollar Index\n(DXY)', 'Oil Prices\n(WTI, Brent)'): 'A stronger dollar makes oil more expensive in other currencies, lowering demand.',
    ('Oil Prices\n(WTI, Brent)', 'Commodities'): 'Higher oil prices increase production costs, raising commodity prices.',
    ('Commodities', 'High-Yield Bonds'): 'Higher commodity prices can increase revenues for commodity-producing companies, affecting their bond yields.',
    ('Commodities', 'Cryptocurrencies'): 'Rising commodity prices can drive investors to cryptocurrencies as an inflation hedge.',
    ('Cryptocurrencies', 'Bitcoin (BTC)'): 'Bitcoin is a major component of the cryptocurrency market.',
    ('Cryptocurrencies', 'Ethereum (ETH)'): 'Ethereum is a significant part of the cryptocurrency market.',
    ('Cryptocurrencies', 'Large-Cap Altcoins'): 'Large-cap altcoins are part of the broader cryptocurrency market.',
    ('Cryptocurrencies', 'Small-Cap Altcoins'): 'Small-cap altcoins are part of the broader cryptocurrency market.'
}

# Define node positions
node_positions = {
    'Central Bank Policies\n(Interest Rates)': (0, 0),
    'Bond Yields\n(Yield Curve)': (-200, 100),
    'Economic Growth\n(GDP)': (0, 100),
    'Inflation Rates': (200, 100),
    'Employment Data\n(Unemployment Rate, NFP)': (-200, 200),
    'Consumer Confidence': (0, 200),
    'US Dollar Index\n(DXY)': (200, 200),
    'Oil Prices\n(WTI, Brent)': (-200, 300),
    'Equities\n(Stocks)': (0, 300),
    'High-Yield Bonds': (200, 300),
    'Commodities': (0, 400),
    'Cryptocurrencies': (200, 400),
    'Bitcoin (BTC)': (400, 400),
    'Ethereum (ETH)': (600, 400),
    'Large-Cap Altcoins': (800, 500),
    'Small-Cap Altcoins': (1000, 600)
}

def draw_graph(node_weights):
    G = nx.DiGraph()

    # Add nodes with attributes
    for node, description in node_descriptions.items():
        size = max(20 + 50 * abs(node_weights.get(node, 0)), 20)  # Minimum size of 20
        color = 'green' if node_weights.get(node, 0) >= 0 else 'red'
        G.add_node(node, size=size, color=color, title=description,
                   x=node_positions[node][0], y=node_positions[node][1], fixed=True)
    
    # Add edges with attributes
    for u, v in edge_descriptions.keys():
        width = max(5 + 10 * abs(node_weights.get(u, 0)), 2)  # Minimum width of 2
        G.add_edge(u, v, width=width, title=edge_descriptions[(u, v)])

    # Create a Pyvis Network
    net = Network(notebook=True, height='800px', width='100%', bgcolor='#ffffff', font_color='black')
    net.from_nx(G)

    # Set the physics layout to False for fixed positions
    net.repulsion(node_distance=420, central_gravity=0.33, spring_length=110, spring_strength=0.10, damping=0.95)
    net.toggle_physics(False)

    # Generate the graph as HTML
    return net.generate_html()

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
    graph_html = draw_graph(node_weights)
    st.components.v1.html(graph_html, height=800)
except Exception as e:
    st.error(f"An error occurred while generating the graph: {e}")
