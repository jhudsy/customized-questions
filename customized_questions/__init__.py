import nacl
from nacl.public import PrivateKey,SealedBox,PublicKey

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import base64
import configparser
import threading
import os
import csv
import glob
import time
import io
import logging
from flask import Flask,url_for,Response,request,session,redirect,render_template,escape
from customized_questions.question import Question

PUBLIC_KEY=None

def setup_encryption(key_file):
  global PUBLIC_KEY
  if key_file=="":
     return
  with open(key_file,"rb") as kf:
    PUBLIC_KEY=PublicKey(kf.read(),encoder=nacl.encoding.Base64Encoder)


"""o is a dictionary of results"""
def write_result(o):

     with lock:

        with open(MARKFILE,'ab') as f:
           si=io.StringIO()
           dw=csv.DictWriter(si,fieldnames=list(o.keys()))
           dw.writerow(o)
           si=si.getvalue()
           
           #si now contains the unencrypted string.
           if PUBLIC_KEY==None:
              f.write(str.encode(si)+b'\n')
           else:
              sb=SealedBox(PUBLIC_KEY)
              enc=sb.encrypt(str.encode(si),encoder=nacl.encoding.Base64Encoder)
              f.write(enc+b'\n')

config=configparser.ConfigParser({'secret_key':'lkrj345asf/','mark_file':'marks/marks.csv','question_path':'questions/','public_key_file':"",'log_level':"INFO"})
config.read('config/config.ini')
SECRET_KEY=str.encode(config.get('main','secret_key'))
MARKFILE=config.get('main','mark_file')
QUESTIONPATH=config.get('main','question_path')
PUBLIC_KEY=None
LOGLEVEL=config.get('main','log_level')
LOGLEVEL=getattr(logging,LOGLEVEL.upper(),None)
logging.basicConfig(level=LOGLEVEL)


lock=threading.Lock()

setup_encryption(config.get('main','public_key_file'))

app = Flask(__name__)
app.secret_key=SECRET_KEY



fl=glob.glob(f"{QUESTIONPATH}/*py")
for filename in fl:
  exec(compile(open(filename,"rb").read(),filename,'exec'))

class QuestionsChanged(FileSystemEventHandler):
  def on_any_event(self,event):
    Question.questions={}
    fl=glob.glob(f"{QUESTIONPATH}/*py")
    for filename in fl:
      exec(compile(open(filename,"rb").read(),filename,'exec'))

observer=Observer()
observer.schedule(QuestionsChanged(),path=QUESTIONPATH,recursive=False)
observer.start()


@app.route('/',methods=["POST","GET"])
def index():
  if request.method=='GET' and "studentid" not in session:
    return render_template('student_id_form.html')
  elif request.method == 'POST' and "studentid" in request.form:
      session['studentid']=escape(request.form['studentid'].strip())
      return redirect(url_for('index'))
  elif request.method == 'POST' and request.form['changeid']=="change ID":
      session.pop('studentid')
      return redirect(url_for('index'))
  else:
    return render_template('index.html',q=Question,studentid=session['studentid'])


@app.route('/<assignment>',methods=["POST","GET"])
def show_assignment(assignment):
  if request.method=='GET' and "studentid" not in session:
    return render_template('student_id_form.html')
  elif request.method == 'POST' and "studentid" in request.form:
      session['studentid']=escape(request.form['studentid'].strip())
      return redirect(url_for('show_assignment',assignment=assignment))
  elif request.method == 'POST' and request.form['changeid']=="change ID":
      session.pop('studentid')
      return redirect(url_for('show_assignment',assignment=assignment))
  else:
    return render_template('question.html',a=assignment,q=Question.questions[assignment],studentid=session['studentid'])

@app.route('/favicon.ico')
def favicon():
  return ''

@app.route('/submission/<assignment>',methods=["POST"])
def submission(assignment):
     ans=Question.questions[assignment].check_answers(session['studentid'],request.form.to_dict(),app)
     if Question.questions[assignment].other_information!=None:
        other_information=Question.questions[assignment].other_information(session['studentid'])
     t=0
     for a in ans:
       t+=ans[a]
     o={"question":assignment,"student_id":session['studentid'],"total_mark":t,"marks_breakdown":ans,"answers":request.form.to_dict(),"other_information":other_information,"time":time.time(),"ip":request.remote_addr}

     write_result(o)

     return 'Submission received'
