# zwe-scrape-dam-level

Scrape data on dam levels in Zimbabwe from [ZINWA](https://www.zinwa.co.zw/dam-levels/).

Built to support  Zimbabwe Red Cross Society (ZRCS).

## Setup
Generic requirements:
-   OPTIONAL (upload to Azure datalake): active [Azure account](https://azure.microsoft.com/en-us/get-started/) and [Azure Data Lake Storage Gen2](https://docs.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-introduction)

### with Docker
1. Install [Docker](https://www.docker.com/get-started)
5. Copy your Azure credentials in
```
credentials/
```
3. Build the docker image from the root directory
```
docker build -t rodekruis/zwe-scrape-dam-level .
```
4. Run and access the docker container
```
docker run -it --entrypoint /bin/bash rodekruis/zwe-scrape-dam-level
```
5. Check that everything is working by running the pipeline (see [Usage](https://github.com/rodekruis/zwe-scrape-dam-level#usage) below)


### Manual Setup
TBI

## Usage
```
Usage: run-pipeline [OPTIONS]

Options:
  --nodatalake                   do not upload to Azure datalake
  --help                         show this message and exit
  ```
