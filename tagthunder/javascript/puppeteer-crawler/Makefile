HTML_AUG_DIR="../html-augmentation/"
IMAGE_NAME="tagthunder-crawler"

run:
	docker run -ti -p 8080:8080 tagthunder-crawler

build:
	@npm install .
	@npm pack $(HTML_AUG_DIR) --pack-destination ./node_modules
	@npm install .
	docker build . -t $(IMAGE_NAME)

clean:
	rm ./node_modules -rf
	rm $(HTML_AUG_DIR)/*.tar.gz
