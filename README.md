# Egyptian National ID Sieve.
Egyptian national ID validator, decoder and metadata extractor, it provides single RESTful API for validating a national ID and extracting as much information as it can from that ID, this [Wikipedia](https://ar.wikipedia.org/wiki/%D8%A8%D8%B7%D8%A7%D9%82%D8%A9_%D9%87%D9%88%D9%8A%D8%A9) Page and this [blog](https://mqaall.com/knowing-a-persons-data-by-the-national-number/) was used a reference for the implementation.

### Technologies

[FastAPI](https://fastapi.tiangolo.com/) for its high performance,  automatic interactive documentation support, concise and simple design, [Pydantic](https://pydantic-docs.helpmanual.io/) for representation and validation of the national ID and the metadata it encodes, [pytest](https://docs.pytest.org/en/7.0.x/) for running the unit tests.

i tried to follow the **"12 factor app"** methodology as much as i can by using the following tools/technologies.
* [GIT](https://git-scm.com/) for applying the following factor/s
    - One codebase tracked in revision control, many deploys
* [Docker](https://docs.docker.com/) for applying the following factor/s
    - Explicitly declare and isolate dependencies
    - Enviroment based configuration
    - Robust and easy build, release and run process.
    - Publish the service as a one or more stateless containers/processes.
    - Container/process/service export via port binding
    - Fast and easy container/service startup and graceful shutdown
    - Keeping development, staging, and production as similar as possible
* [Loguru](https://github.com/Delgan/loguru) for applying the following factor/s
    - logging, specially for logging unexpected errors or exceptions (no unexpected exceptions or failures should went unnoticed specially on production env).


### Project Structure

* `requirements.txt` the project requirements with version pinning
* `manage.sh` provides an interface for running, deploying, restarting, and killing the service's container.
* `service/utils/utils.py` shared utilites that can reused throughout the code to avoid code repetition.
* `service/models.py` the Pydantic Models definitions.
* `service/main.py` defines the `FastAPI()` instance and hooks service's `APIRouter()` instances with it.
* `service/routers/enid.py` defines the endpoints that are specific to the egyptian national ID operations (decoding, validation, etc...).
    - currently the module defines a single RESTful endpoint on its `APIRouter()` instance for handling the validation and decoding of the egyptian national ID.
* `service/exceptions/exceptions.py` defines the custom exceptions which are specific to the app domain.
* `serivce/tests/` defines the unit tests.

### Why did i use HTTP POST dialect/method for the single RESTful endpoint and not other HTTP methods like GET ?

Hmm, although the request here (validate and decode the egyptaion national ID) is idempotent, it might be the case that we don't want the national ID to appear in the web servers logs as part of the URL's query parameters.

PS:
I did not use HTTPS to keep the service review simple and it's assumed that this service might be used as a micro-service on the internal AWS network so actually going w/o HTTPS would improve the request's response time as there will be no TLS handshake, certificate validation etc...

### Run the service's unit tests

```
./manage.sh unittests
```

### Build the service's container image (build operation includes the purge of dangling/residue intermediate container images

```
./manage.sh build
```

### Run the service's container from the service's container image created

```
./manage.sh run
```

### kill the service's running container

```
./manager kill
```

### Deploy the service's container (Build container image and run the container from it in one step)

```
./manage deploy
```