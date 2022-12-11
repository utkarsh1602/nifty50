FROM python
USER root
COPY dashboard app/dashboard
COPY requirements.txt app/
EXPOSE 8050
WORKDIR app/
RUN pip install -r requirements.txt
CMD python dashboard/dashboard.py