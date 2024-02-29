import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from io import StringIO

# Your provided table
data = """
MAP	MRR	Top_1	Top_5	Top_10
F	F	F	F	F
S	M	M	M	M
S	S	M	S	S
L	L	L	P	L
S	M	M	S	M
L	F	F	F	L
P	L	L	F	L
L	L	L	S	L
L	L	B	R	R
L	S	L	F	L
P	S	S	S	S
S	S	S	L	S
S	S	S	S	S
L	L	L	S	L
S	S	S	P	S
M	M	M	S	L
S	S	S	S	S
S	S	S	S	S
S	S	M	S	S
L	L	L	S	L
P	P	P	P	L
S	S	S	S	S
S	S	S	M	S
S	L	L	L	P
S	S	L	S	L
F	L	L	P	P
S	S	S	L	P
B	B	B	B	B
M	A	A	A	S
C	C	C	L	C
L	L	L	L	L
L	A	L	A	L
L	L	L	L	L
M	M	S	M	L
M	M	M	C	A
L	L	L	L	L
L	L	L	L	L
S	S	L	L	M
S	L	L	L	L
"""

# Convert the string table to a pandas DataFrame
df = pd.read_csv(StringIO(data), delimiter='\t')

# Set project names as the index
projects = [
    'Derby', 'Drools', 'Hornetq', 'Izpack', 'Keycloak', 'Log4j2', 'Railo', 'Seam2', 'Teiid', 'Weld',
    'Wildfly', 'ARCHIVA', 'CASSANDRA', 'ERRAI', 'FLINK', 'GROOVY', 'HBASE', 'HIBERNATE', 'HIVE', 'JBOSS-T.-M.',
    'KAFKA', 'LUCENE', 'MAVEN', 'RESTEASY', 'SPARK', 'SWITCHYARD', 'ZOOKEEPER', 'CERTBOT', 'COMPOSE', 'DJANGO_R._F.',
    'FLASK', 'KERAS', 'MITMPROXY', 'PIPENV', 'REQUESTS', 'SCIKIT-LEARN', 'SCRAPY', 'SPACY', 'TORNADO'
]

df.index = projects

# Create a heatmap
plt.figure(figsize=(8, 20))
heatmap = sns.heatmap(df.apply(lambda x: x.map(x.value_counts())), cmap='Reds', cbar=False, annot=False, square=True)

# Add custom annotations to each cell
for i, row in enumerate(df.index):
    for j, col in enumerate(df.columns):
        value = df.at[row, col]
        count = df[col].value_counts()[value]
        text = f'{value}-{count}'
        heatmap.text(j + 0.5, i + 0.5, text, ha='center', va='center', fontsize=10, rotation=90)

# plt.title('Values and Counts Heatmap')
plt.savefig(r"heatmap2.jpg", dpi=600)
plt.show()
