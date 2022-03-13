FROM python:3.7-buster

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt 

COPY trainer /trainer

ENTRYPOINT ["python", "-m", "trainer.train"]