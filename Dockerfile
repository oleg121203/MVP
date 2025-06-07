FROM python:3.9-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install django-cors-headers djangorestframework-simplejwt

COPY wait-for-postgres.sh .
RUN chmod +x wait-for-postgres.sh

COPY backend .

CMD ["./wait-for-postgres.sh", "python", "manage.py", "runserver", "0.0.0.0:8000"]
