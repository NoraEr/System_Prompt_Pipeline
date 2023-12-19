From python:3.10.13-slim-bookworm

ENV HOME /HOME
WORKDIR ${HOME}

COPY llm/. llm/.
COPY requirements.txt .
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "-m", "llm"]
