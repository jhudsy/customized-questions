import sys
import random
import hashlib
import traceback
import numpy as np

class Question:
  questions={}

  def __init__(self,name,question_string,question_values,answer_values,info=None):
    """question string is a formatted string. question_values are a set of functions taking in a dictionary; they update the dictionary so as to set values to parameters in the question string. answer_values is a dict of string->functions which take the question parameter dict in and an answer dict. The function should return true if answer[string] is correct. info is a function which can be used to - for example - log expected answers. It should return whatever needs to be logged, and is passed a dict in. The entire answer dict is passed in so as to allow building on incorrect answers."""

    self.qs=question_string
    self.qv=question_values
    self.av=answer_values
    self.questions[name]=self
    self.oi=info

  def get_question(self,studentid):
    dict={}
    random.seed(int(hashlib.md5(studentid.encode('utf-8')).hexdigest(),16))
    np.random.seed(int(hashlib.md5(studentid.encode('utf-8')).hexdigest(),16)%(2**32-1)) #fixed from '123' here and below
    for v in self.qv:
	    v(dict)
    return self.qs.format(**dict)

  def check_answers(self,studentid,answers,app):
    marks={}
    dict={}
    random.seed(int(hashlib.md5(studentid.encode('utf-8')).hexdigest(),16))
    np.random.seed(int(hashlib.md5(studentid.encode('utf-8')).hexdigest(),16)%(2**32-1))
    for v in self.qv:
	    v(dict)

    for a in self.av:
            marks[a]=0
            try:
              if self.av[a](dict,answers):
                 marks[a]=1
            except:
              app.logger.debug(traceback.format_exc())
    return marks

  def other_information(self,studentid):
    dict={}
    random.seed(int(hashlib.md5(studentid.encode('utf-8')).hexdigest(),16))
    np.random.seed(int(hashlib.md5(studentid.encode('utf-8')).hexdigest(),16)%(2**32-1))
    for v in self.qv:
	    v(dict)
    if self.oi==None:
      return ""
    return self.oi(dict)


