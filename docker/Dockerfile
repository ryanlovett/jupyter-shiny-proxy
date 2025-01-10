FROM rocker/binder

ENV NB_USER=rstudio
ENV HOME=/home/${NB_USER}

USER root

# Download and install shiny server
ENV SHINY_SERVER_URL https://download3.rstudio.org/ubuntu-18.04/x86_64/shiny-server-1.5.22.1017-amd64.deb
RUN curl --silent --location --fail ${SHINY_SERVER_URL} > /tmp/shiny-server.deb && \
    apt install --no-install-recommends --yes /tmp/shiny-server.deb && \
    rm /tmp/shiny-server.deb

COPY . /tmp/jupyter-shiny-proxy
RUN pip install --no-cache-dir \
		/tmp/jupyter-shiny-proxy

USER ${NB_USER}

WORKDIR ${HOME}

CMD jupyter lab --ip=*
