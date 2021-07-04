FROM nvidia.1-cudnn7-devel-ubuntu18.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get upgrade -y && apt-get autoremove && apt-get autoclean
#RUN apt-get install -y python3-dev python3-pip ffmpeg

ARG PROJECT=sova-asr
ARG PROJECT_DIR=/$PROJECT
RUN mkdir -p $PROJECT_DIR
WORKDIR $PROJECT_DIR

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
#RUN pip install --no-cache-dir -r requirments.txt
RUN ln -s /usr/local/cuda/targets/x86_64-linux/lib/ /usr/local/cuda/lib64/
RUN rm -rf $PROJECT_DIR/*

RUN apt-get install -y locales && locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8