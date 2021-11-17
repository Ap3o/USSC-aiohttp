FROM python:3
WORKDIR /web
COPY . .
RUN pip3 install -r requirements.txt
EXPOSE 8000

CMD ["python", "code/application.py"]