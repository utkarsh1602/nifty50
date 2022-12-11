FROM python
USER root
COPY classifier_models app/classifier_models
COPY dashboard app/dashboard
COPY historical_data app/historical_data
COPY utils app/utils
COPY requirements.txt app/
EXPOSE 8080
WORKDIR app/
RUN pip install -r requirements.txt
CMD python dashboard/dashboard.py