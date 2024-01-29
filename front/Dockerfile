FROM python:3.11

LABEL authors="Jalon"

WORKDIR .

COPY ../requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

RUN pip install "uvicorn[standard]"

COPY . .

CMD [ "python3", "-m" , "flask", "--app", "app", "run", "--host=0.0.0.0"]