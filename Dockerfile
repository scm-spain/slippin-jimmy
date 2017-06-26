FROM ubuntu:xenial
MAINTAINER Carlos Gálvez <carlos.galvez@scmspain.com>

RUN set -ex \
    && deps=' \
        bzip2 \
        ca-certificates \
        curl \
        libgomp1 \
        libaio1 \
        gcc \
        libssl-dev \
        libsodium-dev \
        python-dev \
        libffi-dev \
        libtiff5-dev \
        zlib1g-dev \
        libfreetype6-dev \
        liblcms2-dev \
        libwebp-dev \
        tcl8.6-dev \
        tk8.6-dev \
        python-tk \
        dbus \
        ghostscript \
        groff-base \
        gsfonts \
        libavahi-client3 \
        libavahi-common-data \
        libavahi-common3 \
        libcap-ng0 \
        libcups2 \
        libcupsfilters1 \
        libcupsimage2 \
        libdbus-1-3 \
        libgs9 \
        libgs9-common \
        libijs-0.35 \
        libjbig2dec0 \
        libnetpbm10 \
        libpaper-utils \
        libpaper1 \
        libxaw7 \
        libxmu6 \
        netpbm \
        poppler-data \
        psutils \
        build-essential \
        vim \
    ' \
    && apt-get update \
    && apt-get install -y $deps \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/*

ENV PKG_URL https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh
ENV INSTALLER miniconda.sh

RUN set -ex \
    && curl -kfSL $PKG_URL -o $INSTALLER \
    && chmod 755 $INSTALLER \
    && ./$INSTALLER -b -p /opt/conda \
    && rm $INSTALLER

ENV PATH /opt/conda/bin:$PATH

RUN conda install -y oracle-instantclient setuptools freetds \
    && pip install tuf[tools] \
    && pip install tuf \
    && pip install slippinj \
    && pip install --upgrade --user awscli 

ENV PATH ~/.local/bin:$PATH

RUN mkdir ~/.ssh ~/.aws

VOLUME /shared-data