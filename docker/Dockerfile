FROM python:3.7

RUN  apt-get update -y \
  && apt-get -y install --no-install-recommends apt-utils dialog wget ca-certificates \
  #
  # Verify git, process tools, lsb-release (common in install instructions for CLIs) installed
  && apt-get -y install git iproute2 procps lsb-release openjdk-11-jdk zip unzip less vim\
  # Install pylint/awscli
  && pip --disable-pip-version-check --no-cache-dir install pylint awscli boto3 pytest pandas jupyterlab\
  #
  # Clean up
  && apt-get autoremove -y \
  && apt-get clean -y \
  && rm -rf /var/lib/apt/lists/*

# awscli
RUN curl -sSL "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
  && unzip awscliv2.zip \
  && ./aws/install

# maven (for glue)
ENV MAVEN_VERSION=3.6.0
RUN curl -sSOL https://aws-glue-etl-artifacts.s3.amazonaws.com/glue-common/apache-maven-${MAVEN_VERSION}-bin.tar.gz \
  && tar -xzvf apache-maven-${MAVEN_VERSION}-bin.tar.gz \
  && mv apache-maven-${MAVEN_VERSION} /opt/ \
  && ln -s /opt/apache-maven-${MAVEN_VERSION} /opt/apache-maven

# spark
ENV SPARK_FILE_NAME=spark-3.1.1-amzn-0-bin-3.2.1-amzn-3
RUN curl -sSOL https://aws-glue-etl-artifacts.s3.amazonaws.com/glue-3.0/${SPARK_FILE_NAME}.tgz
RUN ls && tar -xvf ${SPARK_FILE_NAME}.tgz \
  && mv ${SPARK_FILE_NAME} /opt/ \
  && ln -s /opt/${SPARK_FILE_NAME} /opt/spark

# glue 3.0
RUN git clone -b glue-3.0.0 --depth 1 https://github.com/mocyuto/aws-glue-libs \
  && mv aws-glue-libs /opt/ \
  && chmod -R ao+wr /opt/aws-glue-libs

ENV SPARK_HOME /opt/spark
ENV PATH $PATH:/opt/apache-maven/bin:/opt/aws-glue-libs/bin
ENV PYTHONPATH $PYTHONPATH:/opt/jupyter/workspace
ENV PYSPARK_DRIVER_PYTHON jupyter
ENV PYSPARK_DRIVER_PYTHON_OPTS ' lab --allow-root --NotebookApp.token="" --NotebookApp.password="" --no-browser --ip=0.0.0.0'

# jupyter setup
CMD /opt/aws-glue-libs/bin/gluepyspark
