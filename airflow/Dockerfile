# Use the Astronomer Certified Airflow Runtime image
FROM quay.io/astronomer/astro-runtime:12.7.1

# Copy requirements.txt and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your external project files into the Airflow container
COPY api/ /usr/local/airflow/api/
COPY database/ /usr/local/airflow/database/
COPY utils/ /usr/local/airflow/utils/
COPY app.py /usr/local/airflow/app.py
COPY config.py /usr/local/airflow/config.py


# Expose Airflow default webserver port
EXPOSE 8080