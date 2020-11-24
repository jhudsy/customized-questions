from customized_questions.question import Question
from io import BytesIO
import random,matplotlib
import matplotlib.pyplot as plt
import networkx as nx

matplotlib.use('Agg')

name = "NX Example"
qs="""
How many nodes are in the following graph?

{svg}
"""

def set_values(dict):
 dict["nodes"]=random.randint(5,10)
 f=BytesIO()
 g=nx.complete_graph(dict["nodes"])
 nx.draw(g)
 #plt.gca().set_position([0,0,1,1])
 plt.savefig(f,format="svg")
 dict["svg"]=f.getvalue().decode('UTF-8')

def q1(dict,answers):
  return int(answers["Q1"])==dict["nodes"]

Question(name,qs,[set_values],{"Q1":q1},marks_dict={"Q1":5})
