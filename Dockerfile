FROM python
USER root
COPY classifier_models app/classifier_models
COPY dashboard app/dashboard
COPY historical_data app/historical_data
COPY constants.py app/
COPY requirements.txt app/
RUN pip install -r requirements.txt
EXPOSE 8080
WORKDIR app/dashboard
CMD ['python dashboard.py']