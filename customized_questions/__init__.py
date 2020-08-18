import threading
import os
import csv
import glob
import time
from flask import Flask,url_for,Response,request,session,redirect,render_template
from customized_questions.question import Question

MARKFILE='marks.csv'

app = Flask(__name__)
app.secret_key=b'lkej345asf/'

lock=threading.Lock()

fl=glob.glob("customized_questions/questions/*py")
for filename in fl:
  exec(compile(open(filename,"rb").read(),filename,'exec'))

@app.route('/',methods=["POST","GET"])
def index():
  if request.method=='GET' and "studentid" not in session:
    return '''
      <form method="post">
      <p><input type=text name=studentid>
      <input type=submit></p>
      </form>
    '''
  elif request.method == 'POST' and "studentid" not in session:
      session['studentid']=int(request.form['studentid'])
      return redirect(url_for('index'))
  elif request.method == 'POST' and request.form['changeid']=="changeId":
      session.pop('studentid')
      return redirect(url_for('index'))
  else:
    return render_template('index.html',q=Question,studentid=int(session['studentid']))


@app.route('/<assignment>',methods=["POST","GET"])
def show_assignment(assignment):
  if request.method=='GET' and "studentid" not in session:
    return '''
      <form method="post">
      <p><input type=text name=studentid>
      <input type=submit></p>
      </form>
    '''
  elif request.method == 'POST' and "studentid" not in session:
      session['studentid']=int(request.form['studentid'])
      return redirect(url_for('show_assignment',assignment=assignment))
  elif request.method == 'POST' and request.form['changeid']=="changeId":
      session.pop('studentid')
      return redirect(url_for('show_assignment',assignment=assignment))
  else:
    return render_template('question.html',a=assignment,q=Question.questions[assignment],studentid=int(session['studentid']))

@app.route('/favicon.ico')
def favicon():
  return ''

@app.route('/submission/<assignment>',methods=["POST"])
def submission(assignment):
     ans=Question.questions[assignment].check_answers(int(session['studentid']),request.form.to_dict())
     t=0
     for a in ans:
       t+=ans[a]
     o={"question":assignment,"student_id":int(session['studentid']),"total_mark":t,"marks_breakdown":ans,"answers":request.form.to_dict(),"time":time.time()}

     with lock:
        if not os.path.exists(MARKFILE):
          with open(MARKFILE,'a') as f:
            dw=csv.DictWriter(f,fieldnames=list(o.keys()))
            dw.writeheader()

        with open(MARKFILE,'a') as f:
           dw=csv.DictWriter(f,fieldnames=list(o.keys()))
           dw.writerow(o)

     #print(o)
     return 'Submission received'
