import random

class Question:
  questions={}

  def __init__(self,name,question_string,question_values,answer_values):
    """question string is a formatted string. question_values are a set of functions taking in a dictionary; they update the dictionary so as to set values to parameters in the question string. answer_values is a dict of string->functions which take the question parameter dict in and an answer dict. The function should return true if answer[string] is correct. The entire answer dict is passed in so as to allow building on incorrect answers."""

    self.qs=question_string
    self.qv=question_values
    self.av=answer_values
    self.questions[name]=self

  def get_question(self,studentid):
    dict={}
    random.seed(hash(studentid))
    for v in self.qv:
	    v(dict)
    return self.qs.format(**dict)

  def check_answers(self,studentid,answers):
    marks={}
    dict={}
    random.seed(hash(studentid))
    for v in self.qv:
	    v(dict)

    for a in self.av:
            marks[a]=0
            try:
              if self.av[a](dict,answers):
                 marks[a]=1
            except:
              pass
    return marks

