FROM python:3.10

WORKDIR /src
EXPOSE 8080

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# necessary for profiler and install some more required os deps
RUN apt-get update \
    && apt-get install -y build-essential \
    && pip install virtualenv \
    && rm -rf /var/lib/apt/lists/*

RUN python -m virtualenv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install poetry==1.1.11
RUN poetry config virtualenvs.create false
COPY poetry.lock /src/
COPY pyproject.toml /src/
RUN poetry install
RUN apt-get remove -y build-essential && apt-get autoremove -y

COPY . /src
RUN cd /src && python setup.py develop

RUN chmod +x /src/bin/run.sh

CMD ["/src/bin/run.sh"]
