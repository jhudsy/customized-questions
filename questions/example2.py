from customized_questions.question import Question
import random

name="Q2"

qs="What is (2a) {a}x{b}; (2b) {c}%{a}?"

def set_values(dict):
  dict["a"]=random.randint(1,5)
  dict["b"]=random.randint(6,10)
  dict["c"]=random.randint(11,15)


def add(dict,answers):
  return int(answers["2a"])==(int(dict["a"])*int(dict["b"]))

def diff(dict,answers):
  return int(answers["2b"])==(int(dict["c"])%int(dict["a"]))

qv=[set_values]
av={"2a":add,"2b":diff}

Question(name,qs,qv,av)


