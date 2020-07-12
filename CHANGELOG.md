* Added scripts to convert the latest CA into pdf and csv and then serve it via a Flask endpoint (127.0.0.1:5000/public/filename.pdf)
* Added script to scrape the latest NSE Website
* Added script to merge latest data and old data for NSE
* Added script to get all the companies listed in NSE

**TODO**

Since the files needs to be refreshed every times the db is refreshed, add this script.

```python
from FileStorage import FileStorage

FileStorage.store_file_as_csv_pdf()
```