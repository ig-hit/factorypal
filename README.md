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
