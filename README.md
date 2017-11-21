# Study path analyzer

### Install packages
pip install -r requirements.txt

### Preprocess data
you should have the graded sql under the folder **data** 

**HKUSTx-COMP102x-2T2014-courseware_studentmodule-prod-analytics.sql**

python migrations/preprocess_data.py

### Files
* constants.py : constants include problem weights, edges,...
* preprocess_data.py : preprocess the raw data 
* urls.py : the url parser
* views.py : render functions

### Run the Django server by
python manage.py runserver

### Usage

#### Force-Directed Graph
index.html

#### return the concepts grades of a student with parameter student_id (e.g. 342)
http://127.0.0.1:8000/study_plan/concept_score/342/

#### return the concepts grades of all students
http://127.0.0.1:8000/study_plan/concept_score/all/

#### return the edges with risk ratio values
http://127.0.0.1:8000/study_plan/graph/
