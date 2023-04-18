FROM python:3.11.3-slim

WORKDIR /app

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY  requirements.txt requirements.txt
RUN  pip3 install  --no-cache-dir -r requirements.txt

EXPOSE 8000

# copy project
COPY . .

# run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
