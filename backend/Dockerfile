
FROM python:3.10-alpine
 
WORKDIR /backend
 
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt
 
COPY . .

EXPOSE 5000
 
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]

 