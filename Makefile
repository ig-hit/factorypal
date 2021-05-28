.PHONY: install server swagger

install:
	@./resources/install.sh

server:
	@./resources/server.sh

swagger:
	./manage.py generate_swagger -f yaml -o ./resources/swagger/api.yaml

test:
	./manage.py test -v=3
