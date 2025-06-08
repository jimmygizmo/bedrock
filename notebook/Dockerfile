FROM quay.io/jupyter/minimal-notebook:python-3.11
# This image is fairly large at 2.2GB+ compressed, but if you try to get a similarly
# full-featured Jupyter server by doing a custom build, you might only save a few
# hundred megabytes and add additional complexity and stability risks.
# Use the "minimal" quay image over the "base", ironic, because the "minimal" is
# loaded up. Over time I may decide to customize and optimize a Jupyter image.

# On other topics, it is best to stick to Python 3.10 or 3.11 and still avoid
# Python 3.12 in 2025 for things like Data Science, Geospatial or Machine Learning.
# Those domains have many libraries and drivers that are not yet compatible with
# Python 3.12.

# Custom settings like dark them as default
COPY overrides.json /opt/conda/share/jupyter/lab/settings/

COPY requirements.txt /tmp/

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

RUN pip install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /home/bedrock/workspace

COPY book.ipynb /home/bedrock/workspace/

EXPOSE 8888

# NOTE: Compose file has notebook start options required for our large response payloads. Use the compose CMD.
#CMD ["start-notebook.sh", "--NotebookApp.token=''", "--NotebookApp.password=''"]

# For reference, here is the Compose start command showing those important options:
#    command: [
#      "start-notebook.sh",
#      "--NotebookApp.token=''",
#      "--NotebookApp.password=''",
#      "--ServerApp.iopub_data_rate_limit=10000000",
#      "--ServerApp.rate_limit_window=10.0",
#      "--LabApp.default_url='/lab/tree/book.ipynb'",
#    ]

