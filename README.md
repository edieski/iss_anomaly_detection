# iss_anomaly_detection
this project involves using Airflow to collect real-time location and altitude data from the International Space Station API, storing it in a time-series database, and creating a Grafana dashboard with anomaly detection alerts.

Sprint 1:

I love space so this is my first project of the space series :) Go space !

Goal: Set up the project infrastructure and data collection pipeline.

Set up a Python environment with the necessary packages and dependencies.

Define the schema for the ISS data and create a table in the relational database to store the data.

Develop an Airflow DAG to collect the ISS data periodically using the Open Notify API and store it in the database.

Verify that the data collection pipeline is working correctly and data is being stored in the database.

Sprint 2:

Goal: Develop the anomaly detection algorithm and integrate it with the data pipeline.

Research and select an appropriate anomaly detection algorithm for time-series data.

Develop Python code to process the data from the database and detect anomalies using the selected algorithm.

Integrate the anomaly detection code with the Airflow DAG to automate the detection process.

Test the anomaly detection process using sample data and verify that it is detecting anomalies correctly.

Sprint 3:

Goal: Develop the Grafana dashboard and set up alerts for detected anomalies.

Design a Grafana dashboard that displays the ISS data and highlights detected anomalies.

Develop Python code to push the data from the database to Grafana using the Grafana API.

Set up alerts in Grafana to notify users when anomalies are detected.

Test the dashboard and alerting system using sample data and verify that it is working correctly.
