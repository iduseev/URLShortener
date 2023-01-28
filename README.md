
# URL Shortener

Repo for storing URL Shortener project based on `FastAPI`  utilizing `uvicorn` web-server and running in `Docker` container. It also uses `SQLite` DB implemented to store URL and related data.

The project itself is created based on the following RealPython tutorial:

https://realpython.com/build-a-python-url-shortener-with-fastapi/
_________________________________________________________________________________________________________________________________________________________________


## Launch:


```shell
docker compose up
```

## For further development:
1. Cleanup requirements.txt
2. Complete SQL DB implementation
3. Refactor code
4. Write proper unit tests using pytest
5. Deploy on Docker container instead of uvicorn


## Documentation used:


FastAPI
---------------
https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/
https://fastapi.tiangolo.com/tutorial/security/get-current-user/
https://stackoverflow.com/questions/63580229/how-to-save-uploadfile-in-fastapi

Docker
---------------
https://docs.docker.com/engine/reference/builder/
https://docs.docker.com/compose/compose-file/compose-file-v3/

pydantic
---------------
https://pydantic-docs.helpmanual.io/usage/models/

SQLAlchemy
---------------
https://www.sqlalchemy.org/docs/
