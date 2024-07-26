import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from io import BytesIO

# Function to create and display the graph
def draw_graph(interest_rate, consumer_confidence, gdp_growth):
    G = nx.DiGraph()
    G.add_node('Interest Rates', pos=(0, 1))
    G.add_node('Consumer Confidence', pos=(1, 1))
    G.add_node('GDP Growth', pos=(2, 1))
    G.add_node('Risk-On Environment', pos=(1, 0))
    G.add_node('Risk-Off Environment', pos=(1, -1))
    
    G.add_edges_from([
        ('Interest Rates', 'Risk-Off Environment'),
        ('Consumer Confidence', 'Risk-On Environment'),
        ('GDP Growth', 'Risk-On Environment'),
        ('Risk-On Environment', 'Crypto Assets'),
        ('Risk-Off Environment', 'Crypto Assets')
    ])
    
    pos = nx.get_node_attributes(G, 'pos')
    plt.figure(figsize=(10, 6))
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color="skyblue", node_shape="o",
            alpha=0.8, font_size=10, font_color="black", font_weight="bold", linewidths=2, width=2, edge_color="grey")
    
    edge_labels = {
        ('Interest Rates', 'Risk-Off Environment'): f'Impact: {interest_rate:.2f}',
        ('Consumer Confidence', 'Risk-On Environment'): f'Impact: {consumer_confidence:.2f}',
        ('GDP Growth', 'Risk-On Environment'): f'Impact: {gdp_growth:.2f}'
    }
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    return buffer

st.title('Risk-On/Risk-Off Environment Simulator')

interest_rate = st.slider('Interest Rate Impact', -1.0, 1.0, 0.0)
consumer_confidence = st.slider('Consumer Confidence Impact', -1.0, 1.0, 0.0)
gdp_growth = st.slider('GDP Growth Impact', -1.0, 1.0, 0.0)

st.write("### Risk Environment Graph")
graph_image = draw_graph(interest_rate, consumer_confidence, gdp_growth)
st.image(graph_image, use_column_width=True)

indicators = {
    'Interest Rates': interest_rate,
    'Consumer Confidence': consumer_confidence,
    'GDP Growth': gdp_growth
}
weights = {'Interest Rates': 0.5, 'Consumer Confidence': 0.3, 'GDP Growth': 0.2}
score = sum(indicators[i] * weights[i] for i in indicators)

if score > 0:
    st.write('### Risk-On Environment')
else:
    st.write('### Risk-Off Environment')
