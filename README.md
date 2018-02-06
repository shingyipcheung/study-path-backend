# Study path analyzer

### Install packages
**you should have python3 installed**

`pip install -r requirements.txt`

### Preprocess data
you should have the graded sql under the folder **data** 

**HKUSTx-COMP102x-2T2014-courseware_studentmodule-prod-analytics.sql**

`python migrations/preprocess_data.py`

some .pkl files will be generated, these are the serialized result for responding the requests

### Files
* edxDB/constants.py: constants include problem weights, edges, ...
* edxDB/preprocess_data.py: preprocess the raw data 
* edxDB/urls.py: the url parser
* edxDB/views.py: render functions

### Run the Django server by

#### localhost
`python manage.py runserver`

#### public
`python manage.py runserver 0.0.0.0:8000`

### Usage

#### Force-Directed Graph (Example)
index.html

#### return the concepts grades of a student with parameter student_id (e.g. 342)
http://127.0.0.1:8000/study_plan/concept_score/342/

#### return the concepts grades of all students
http://127.0.0.1:8000/study_plan/concept_score/all/

#### return the edges with risk ratio values
http://127.0.0.1:8000/study_plan/graph/

#### Work with built application by Vue
Put dist inside current directory

```
dist
    static
        css
        js
    index.html
edxDB
edxback
.gitignore
django-admin.py
manage.py
requirements.txt
```
