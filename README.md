# python-police-reports-berlin-crawler

## Install

The project uses pipenv to manage dependencies.
You can install all requirements with the following command:

```bash
pipenv install
```

If you want to crawl locally create a .env file in the root-directory with the following content:

```bash
SCRAPY_POLICE_REPORTS_CRAWLER_MONGO_ENABLED=0
SCRAPY_POLICE_REPORTS_CRAWLER_MONGO_URI=
SCRAPY_POLICE_REPORTS_CRAWLER_MONGO_DATABASE=
SCRAPY_POLICE_REPORTS_CRAWLER_MONGO_COLLECTION=
```

## Run 

To run the crawler enter following command in the pipenv shell:

```bash
scrapy crawl reports
```

## Deployment

To deploy project to [Scrapinghub](https://scrapinghub.com/):

```bash
shub deploy
```