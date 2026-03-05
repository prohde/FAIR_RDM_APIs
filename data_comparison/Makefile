.PHONY: start stop

start:
	docker build -t datacomparison .
	docker run -p 5009:5000 --name datacomparison -d datacomparison

stop:
	docker stop datacomparison
	docker rm datacomparison
	docker rmi datacomparison