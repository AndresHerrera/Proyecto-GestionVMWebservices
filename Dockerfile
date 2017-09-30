FROM blacklabelops/virtualbox
MAINTAINER Andres Herrera - Mario Castillo "fabio.herrera@correounivalle.edu.co - mario.castillo@correounivalle.edu.co"
USER root
RUN yum -y update
RUN yum groupinstall -y development
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python get-pip.py
RUN pip install Flask
COPY . /app
WORKDIR /app
ENTRYPOINT ["python"]
CMD ["prj-vmwebservice.py"]
