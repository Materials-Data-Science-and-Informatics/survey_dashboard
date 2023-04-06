# Survey dashboard

A dashboard to display survey data in an interactive way.

## Overview

This repository contains a dashboard using Panel and Bokeh, developed to display data from 
HMC surveys in an interactive exploratory way. It is designed such that the code for the interactive
visualizations might be reused for other projects.
Example of a deployed version can be found [here](https://dashboard.survey.helmholtz-metadaten.de/survey_dashboard)

Some impressions:
![dashboard_overview](https://user-images.githubusercontent.com/24694833/230306080-9ca68ff8-5b8b-4ac4-b2fa-51e2c5361c7d.png)
![dashboard_methods](https://user-images.githubusercontent.com/24694833/230306091-637188a9-359e-4ea0-8432-4d05a1ccc68f.png)
![Dashboard_survey_data_explorer](https://user-images.githubusercontent.com/24694833/230306099-4cf71bda-0990-4f9d-be14-9a65812e7ac4.png)

## Installation

After downloading the git repository you can install the software either with pip or poetry.
We recommend setting it up in a separate python virtual environment.

```shell
pip install survey_dashboard
```
or

```shell
poetry install .
```

## Usage


After installation you can start the app, i.e the panel server/bokeh server.
```shell
panel serve --port 50006 survey_dashboard/ 
```
If you have given the dashboard a specific layout like the layout specific to HMC, which is on the hmc_specific branch, you might have to link to to a specific template.
```shell
panel serve --port 50006 survey_dashboard/ --static-dirs en_files=./survey_dashboard/hmc_layout/static/en_files

```

* Navigate to `http://localhost:50006/` in your browser.

## Deployment

To embed the dashboard into any website, first you have to host a bokeh server with this application somewhere and then you can embed it with bokehs `sever_document` function [see](https://docs.bokeh.org/en/latest/docs/user_guide/embed.html#app-documents)

Do steps under `usage` above, but for a public exposed URL, or what ever is used for deployment.
The Language verison of the dashboard can be set with the environment variable: 'L


Add the code from 'script' to you website:

```python
from bokeh.embed import server_document
script = server_document("url_to_running_server")
script
```

## Copyright and Licence

See [LICENSE](./LICENSE).

### Main used libraries and dependencies

The following libraries are used directly (i.e. not only transitively) in this project:


## Acknowledgements

<div>
<img style="vertical-align: middle;" alt="HMC Logo" src="https://github.com/Materials-Data-Science-and-Informatics/Logos/raw/main/HMC/HMC_Logo_M.png" width=50% height=50% />
&nbsp;&nbsp;
<img style="vertical-align: middle;" alt="FZJ Logo" src="https://github.com/Materials-Data-Science-and-Informatics/Logos/raw/main/FZJ/FZJ.png" width=30% height=30% />
</div>
<br />

This project was developed at the Institute for Materials Data Science and Informatics
(IAS-9) of the Jülich Research Center and funded by the Helmholtz Metadata Collaboration
(HMC), an incubator-platform of the Helmholtz Association within the framework of the
Information and Data Science strategic initiative.
