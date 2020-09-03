FROM python:3.8


WORKDIR /app
COPY customized_questions /app/customized_questions
RUN mkdir /app/questions/
RUN mkdir /app/config/
RUN mkdir /app/marks/
COPY requirements.txt /app
RUN pip install -r requirements.txt

ENV FLASK_APP customized_questions

CMD [ "gunicorn", "-w", "4", "customized_questions:app", "-b", "0.0.0.0:8000" ]
