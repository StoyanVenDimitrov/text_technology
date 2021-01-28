# Text techology project - WS 20/21
## Installation
Initially, create a python virtual environment, with the name venv:
```bash
python3 -m venv venv
```
Activate the virtual environment:
```bash
source venv/bin/activate
```
Install the needed packages:
```bash
pip install -r requirements.pip
```

Additionally, make sure you have running MySQL v.14.*

## Usage
Extract an .xml file from wikipedia pages, where the search term occures. Optionally, change the number of results, default is 5. E.g. search for 'matrix' and return the first 10 results:
```python
python wikipedia_to_xml.py --term="matrix" --search_limit=10
```
The resulting .xml file is saved as matrix.xml at the xml_single_files folder. 
Validate the .xml file with a DTD grammar

Translate the content of the XML file in MySQL database:
```python
python xml_to_sql.py --file="xml_single_files/matrix.xml"
```
It creates SQL table with the same name as the XML file, e.g. matrix

Perform full text search on the SQL table for a specific term:
```python
python sql_text_search.py --term="array" --table="matrix"
```
This prints the titles of the found wikipedia pages where matrix and array co-occure in the snippet from the search result. 