from customized_questions.question import Question
import random

name="Q1"

qs="What is (a) {a}+{b}; (b) {a}-{c}?"

def a(dict):
  dict["a"]=random.randint(0,5)

def b(dict):
  dict["b"]=random.randint(6,10)
  dict["c"]=random.randint(11,15)

def add(dict,answers):
  return int(answers["a"])==(int(dict["a"])+int(dict["b"]))

def diff(dict,answers):
  return int(answers["b"])==(int(dict["a"])-int(dict["c"]))

qv=(a,b)
av={"a":add,"b":diff}

Question(name,qs,qv,av)


