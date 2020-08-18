from customized_questions.question import Question
import random

name="Q2"

qs="What is (a) {a}x{b}; (b) {c}%{a}?"

def a(dict):
  dict["a"]=random.randint(1,5)

def b(dict):
  dict["b"]=random.randint(6,10)
  dict["c"]=random.randint(11,15)

def add(dict,answers):
  return int(answers["a"])==(int(dict["a"])*int(dict["b"]))

def diff(dict,answers):
  return int(answers["b"])==(int(dict["c"])%int(dict["a"]))

qv=(a,b)
av={"a":add,"b":diff}

Question(name,qs,qv,av)


