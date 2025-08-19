FROM python
RUN pip install flask
RUN pip install pymongo

COPY app.py .
COPY ./templates ./templates
COPY ./static ./static

EXPOSE 8080
CMD python3 app.py
