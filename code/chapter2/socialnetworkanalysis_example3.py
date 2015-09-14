from glob import glob
import pandas as pd
import d3py
import networkx as nx
import matplotlib.pyplot as plt

dfs = []
for CSV in glob("sna_example*.csv"):
    dfs.append(pd.DataFrame().from_csv(CSV,index_col=False))

#we assume column names are consistent across all csv's, please ensure this is true!
graphs = []
for df in dfs:
    graphs.append(nx.from_pandas_dataframe(df,"source","target"))

G = nx.compose_all(graphs)
nx.draw(G, with_labels=True)
plt.savefig("sna_example3.png")

