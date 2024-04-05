## This is how you install and run the fastapi pipeline server

* The website is hosted at https://dull-scrubs-bee.cyclic.app/
* You can view all the endpoints at https://dull-scrubs-bee.cyclic.app/docs

* Clone the repo
* Install the dependencies
    * `pip install fastapi uvicorn pydantic`
* Run the server
    * `cd python/pipeline/`
    * `uvicorn app:app --reload`
* See the API
    * go to the url displayed in the terminal
        * should get "API is working"
    * add `/docs` to the end of the url
        * should get the swagger UI
    * The url is likely `http://127.0.0.1:8000/docs`