from customized_questions.question import Question
from io import BytesIO
import random,matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.use('Agg')

name="Q1"

qs="""
What is (1a) {a}+{b}; (1b) {a}-{c}?

{svg}
"""

def set_values_1(dict):
  dict["a"]=random.randint(0,5)

def set_values_2(dict): #illustrating that multiple methods can be called to set values
  dict["b"]=random.randint(6,10)
  dict["c"]=random.randint(11,15)
  plt.figure(figsize=[6, 6])
  x = np.arange(0, 100, 0.00001)
  y = x*np.sin(2* np.pi * x)
  plt.plot(y)
  plt.axis('off')
  plt.gca().set_position([0, 0, 1, 1])
  f=BytesIO()
  plt.savefig(f,format="svg")
  dict["svg"]=f.getvalue().decode('UTF-8')

def add(dict,answers):
  return int(answers["1a"])==(int(dict["a"])+int(dict["b"]))

def diff(dict,answers):
  return int(answers["1b"])==(int(dict["a"])-int(dict["c"]))

qv=[set_values_1,set_values_2]
av={"1a":add,"1b":diff}

Question(name,qs,qv,av)


