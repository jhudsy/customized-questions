import cryptography
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


import base64
import configparser
import threading
import os
import csv
import glob
import time
import io
from flask import Flask,url_for,Response,request,session,redirect,render_template
from customized_questions.question import Question

def setup_encryption(key_file):
  global PUBLIC_KEY
  if key_file=="":
     return
  with open(key_file,"rb") as kf:
    PUBLIC_KEY=serialization.load_pem_public_key(kf.read(),backend=default_backend())


"""o is a dictionary of results"""
def write_result(o):

     with lock:
        #we don't really need to write the headers, TODO: remove?
        #if not os.path.exists(MARKFILE):
        #  with open(MARKFILE,'a') as f:
        #    dw=csv.DictWriter(f,fieldnames=list(o.keys()))
        #    dw.writeheader()

        with open(MARKFILE,'a') as f:
           si=io.StringIO()
           dw=csv.DictWriter(si,fieldnames=list(o.keys()))
           dw.writerow(o)
           si=si.getvalue()
           
           #si now contains the unencrypted string.
           if PUBLIC_KEY==None:
              print(si,file=f)
              #f.writelines([si])
           else:
              encrypted=PUBLIC_KEY.encrypt(
                   str.encode(si),
                   padding.OAEP(
                     mgf=padding.MGF1(algorithm=hashes.SHA256()),
                     algorithm=hashes.SHA256(),
                     label=None
                   )
              )
              print("".join(chr(x) for x in base64.b64encode(encrypted)),file=f) #turn into string
              #f.writelines(["".join(chr(x) for x in base64.b64encode(encrypted))]) #turn into string



config=configparser.ConfigParser({'secret_key':'lkrj345asf/','mark_file':'marks/marks.csv','question_path':'questions/','public_key_file':""})
config.read('config/config.ini')
SECRET_KEY=str.encode(config.get('main','secret_key'))
MARKFILE=config.get('main','mark_file')
QUESTIONPATH=config.get('main','question_path')
PUBLIC_KEY=None

lock=threading.Lock()

setup_encryption(config.get('main','public_key_file'))

app = Flask(__name__)
app.secret_key=SECRET_KEY


fl=glob.glob(f"{QUESTIONPATH}/*py")
for filename in fl:
  exec(compile(open(filename,"rb").read(),filename,'exec'))


@app.route('/',methods=["POST","GET"])
def index():
  if request.method=='GET' and "studentid" not in session:
    return render_template('student_id_form.html')
  elif request.method == 'POST' and "studentid" in request.form:
      session['studentid']=int(request.form['studentid'])
      return redirect(url_for('index'))
  elif request.method == 'POST' and request.form['changeid']=="change ID":
      session.pop('studentid')
      return redirect(url_for('index'))
  else:
    return render_template('index.html',q=Question,studentid=int(session['studentid']))


@app.route('/<assignment>',methods=["POST","GET"])
def show_assignment(assignment):
  if request.method=='GET' and "studentid" not in session:
    return render_template('student_id_form.html')
  elif request.method == 'POST' and "studentid" in request.form:
      session['studentid']=int(request.form['studentid'])
      return redirect(url_for('show_assignment',assignment=assignment))
  elif request.method == 'POST' and request.form['changeid']=="change ID":
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

     write_result(o)

     return 'Submission received'
