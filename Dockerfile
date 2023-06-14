ARG python_version=3.11.2
ARG poetry_version=1.4.1

FROM "casavo/python-poetry:${poetry_version}_${python_version}" as builder-base

COPY poetry.lock pyproject.toml ./

RUN poetry install --no-dev

################################################################################


# `production` image used for runtime
FROM "casavo/python:${python_version}" as production

# this is where our requirements + virtual environment will live
ENV PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$VENV_PATH/bin:$PATH"

COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
COPY . /app/

USER nobody

WORKDIR /app

CMD ["/app/run.sh", "prod"]

################################################################################


# `development` image is used during development / testing
FROM builder-base as development

WORKDIR $PYSETUP_PATH

# copy in our built poetry + venv
COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

# quicker install as runtime deps are already installed
RUN poetry install

# will become mountpoint of our code
WORKDIR /app
