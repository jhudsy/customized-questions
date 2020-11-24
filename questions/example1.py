from customized_questions.question import Question
from io import BytesIO
import numpy as np


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

def add(dict,answers):
  return int(answers["1a"])==(int(dict["a"])+int(dict["b"]))

def diff(dict,answers):
  return int(answers["1b"])==(int(dict["a"])-int(dict["c"]))

qv=[set_values_1,set_values_2]
av={"1a":add,"1b":diff}

Question(name,qs,qv,av)


