build:
	docker build -t flask/customized-questions .

run:
	docker run -d -p 8000:8000 --restart unless-stopped \
	--mount type=bind,source="$(CURDIR)/questions",target=/app/questions,readonly \
	--mount type=bind,source="$(CURDIR)/config",target=/app/config,readonly \
	--mount type=bind,source="$(CURDIR)/marks",target=/app/marks \
	flask/customized-questions

