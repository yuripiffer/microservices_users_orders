FROM python

COPY ./app.py ./app.py
COPY ./db_orders.py ./db_orders.py
COPY ./model_orders.py ./model_orders.py

RUN pip3 install flask
RUN pip3 install requests
RUN pip3 install pandas
RUN pip3 install mysql
RUN pip3 install cpf_tools

CMD python -m flask run --host=0.0.0.0 --port=5000