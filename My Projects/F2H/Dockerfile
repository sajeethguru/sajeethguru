FROM python:3.9
WORKDIR /app
ADD . /app
COPY templates /app/templates
COPY requirements.txt /app
RUN python3 -m pip install -r requirements.txt
EXPOSE 5000
CMD ["python","f2h.py"]