from customized_questions.question import Question
import random

name = "Q3 - multiple choice"

qs='''Which of the following is true?

<p>1. {o[0]}
<p>2. {o[1]}
<p>3. {o[2]}
'''

def make_options(dict):
  '''Note in the following we first set the correct answer as a static string, create random strings, and shuffle them around.'''
  o=['1+2=3',f"{random.randint(0,5)}+{random.randint(0,5)}={random.randint(11,15)}","The rain in spain stays mainly in the plain"]
  random.shuffle(o)
  dict["o"]=o

def correct_answer(dict,answers):
  '''Just find the correct answer'''
  return dict["o"].index('1+2=3')==int(answers["a"])-1

qv=[make_options]
av={"Answer":correct_answer}

Question(name,qs,qv,av)

