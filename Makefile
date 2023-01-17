JS_LIB="./tagthunder/javascript/"
PPT_CRAWLER=${JS_LIB}/puppeteer-crawler/


build-crawler:
	$(MAKE) -C ${PPT_CRAWLER} build

install: 
	poetry install
	$(MAKE) build-crawler

run-crawler:
	$(MAKE) -C ${PPT_CRAWLER} run

run-api:
	poetry run tagthunder-api

run:
	screen -S tagthunder-crawler -d -m $(MAKE) run-crawler
	screen -S tagthunder-api -d -m $(MAKE) run-api


dev: install
	poetry install with dev
