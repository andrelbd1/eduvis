Quick Setup
-----------

1. Clone this repository.
2. Create a virtualenv:
````bash
    virtualenv venv
````
3. Activate the virtualenv:
````bash
    source venv/bin/activate
````
4. Install the requirements:
````bash
    pip install -r requirements.txt
````
5. Start the Flask application on your original terminal window:
````bash
    venv/bin/python run.py
````
6. Go to `http://localhost:8558/eduvis/` and enjoy this application!

About
-----------

This project was part of my Ph.D. research performed between 2016 and 2020, which we shed light on how to support instructors in analyzing student logs from Virtual Learning Environments. Our main goal in this project is enable Virtual Learning Environments to assist instructors in gaining insights about both students’ behavior and performance.

Firstly, we conducted interviews with instructors who work in Brazil and a systematic mapping of the state-of-art about Education Data Mining and Learning Analytics. This study aimed to identify which kinds of information about students the instructors regard as meaningful (e.g., performance, behavior, engagement); how these kinds of information are gathered; and how they drive requirements for improving their analyses.

- [A. L. B. Damasceno, D. S. Ribeiro and S. D. J. Barbosa, "What the Literature and Instructors Say about the Analysis of Student Interaction Logs on Virtual Learning Environments", *2019 IEEE Frontiers in Education Conference (FIE)*, Covington, KY, USA, 2019, pp. 1-9, doi: 10.1109/FIE43999.2019.9028398](https://ieeexplore.ieee.org/document/9028398)

Then, we analyzed logs from online courses offered in Brazil and compared our findings with results presented in the literature. We explored and analyzed these logs using statistical methods and machine learning techniques.

- [A. L. B. Damasceno, C. Almeida, W. Fernandes, H. Lopes and S. D. J. Barbosa, "What Can Be Found from Student
Interaction Logs of Online Courses Offered in Brazil", *XXX Simpósio Brasileiro de Informática na Educação (SBIE 2019)*, Brasilia, Brazil, 2019, pp 1641–1650, doi: 10.5753/cbie.sbie.2019.1641](https://www.researchgate.net/publication/335840428_What_Can_Be_Found_from_Student_Interaction_Logs_of_Online_Courses_Offered_in_Brazil)

Furthermore, we have not found in the literature works about instructors’ visualization preferences of student logs. Therefore, we conducted a study to identify how much the instructors take into account topics related to both students’ behavior and performance, as well as their visualization preferences.

- [A. L. B. Damasceno, D. S. Ribeiro and S. D. J. Barbosa, "Visualizing Student Interactions to Support Instructors in Virtual Learning Environments", *Antona, M., Stephanidis, C. (eds) Universal Access in Human-Computer Interaction. Theory, Methods and Tools. HCII 2019. Lecture Notes in Computer Science(), vol 11572. Springer, Cham*, doi: 10.1007/978-3-030-23560-4_33](https://link.springer.com/chapter/10.1007/978-3-030-23560-4_33)

We also noted a lack of work showing models to support the development of learning analytics tools. In order to bridge this gap, we presented a model connecting both Visual Analytics theories and models as well as instructors’ requirements, their visualization preferences, literature guidelines and methods for analyzing student logs.

![MODEL](https://andrelbd1.github.io/assets/img/projects/eduvis/model.png)

We developed EDUVIS as an open source online tool to assemble dashboards based on our proposed model. This tool was built using Python and Javascript. In particular, all the visualizations (total of 141) were designed using [Plotly](https://github.com/plotly), which provides interactivity, such as zoom in, zoom out, pan, select, toggle spike lines, and mouse hover.

We captured evidence of their acceptance of our proposal and obtained instructors’ feedback about the tool such as their both analysis and visualization preferences. The combination of the answers to the research questions yields a framework to enable Virtual Learning Environments to assist instructors in gaining insights about both students’ behavior and performance. We hope that our proposed model might be a guide to the development of new dashboards and ground future research.

- [Thesis](https://doi.org/10.17771/PUCRio.acad.50335)

Preview
-----------
![EDUVIS](https://andrelbd1.github.io/assets/img/projects/eduvis/interface.png)