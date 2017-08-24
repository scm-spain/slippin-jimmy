FROM centos:centos7
MAINTAINER Carlos Gálvez <carlos.galvez@scmspain.com>

RUN set -ex \
    && deps=' \
    	bzip2 \
        gcc \
        java-1.8.0-openjdk \
    ' \
    && yum update -y \
    && yum install -y $deps \
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

ENV TZ 'UTC'

RUN rm -f /etc/localtime; ln -s /usr/share/zoneinfo/$TZ /etc/localtime 
RUN echo 'ZONE="$TZ"' > /etc/sysconfig/clock

VOLUME /shared-data