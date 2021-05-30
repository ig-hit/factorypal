**FactoryPal Parameters Service**


**Install and run:**
```bash
make install
. venv/bin/activate
make test
make server
```

**Fixtures:**<br>
Sample data loaded at install.<br>
To load more, adjust corresponding csv in [task folder](./resources/task) and execute:<br>
`make populate-machines`and `populate-parameters` or just re-run `make install`


**OpenAPI Documentation (Swagger):**<br>
Use `make swagger` to generate docs.<br>
Available in [resources/swagger](./resources/swagger)


**Postman endpoints:**<br>
Load [collection](./resources/postman)

**CURL:**<br>

**Add Machine:**
```bash
curl --location --request POST 'http://localhost:6600/machines/' \
--header 'Content-Type: application/json' \
--data-raw '{ 
    "key": "embosser", 
    "name": "Embosser" 
}'
```

**Add Parameters:**
```bash
curl --location --request POST 'http://localhost:6600/machines/embosser/parameters' \
--header 'Content-Type: application/json' \
--data-raw '{
    "machineKey": "embosser",
    "parameters": {
        "x": 2,
        "y": 3,
        "z": 4
    }
}'
```


**Get Latest Parameters:**
```bash
curl --location --request GET 'http://localhost:6600/machines/embosser/parameters/latest'
```

**Get Aggregated values for machine `embosser` and parameter `x` for the last 10 minutes:**
```bash
curl --location --request GET 'http://localhost:6600/machines/embosser/parameters/x/aggregates?lastMinutes=10'
```
