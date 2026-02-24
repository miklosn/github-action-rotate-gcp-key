FROM python:3.12-slim
WORKDIR /app
RUN pip install pipenv
COPY Pipfile* /app/
RUN pipenv install --system --deploy
COPY . /app/
CMD ["python", "/app/main.py"]
