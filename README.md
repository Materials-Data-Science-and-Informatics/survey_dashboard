# Survey Dashboard

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

### Prerequisites
- Python 3.12 or higher
- Poetry (recommended) or pip

### Using Poetry (Recommended)

After downloading the git repository, install the dependencies using Poetry:

```shell
poetry install
```

### Using pip

Alternatively, you can install directly from the repository:

```shell
pip install .
```

## Usage

### Development Mode

For development, you can run the app directly using Panel serve:

```shell
# Using Poetry
poetry run survey-dashboard

# Using Python directly
panel serve app.py --port 5006 --show --autoreload
```

The `--autoreload` flag enables automatic reloading when you make changes to the code, which is useful during development.

### Manual Panel Serve

If you need more control over the server configuration:

```shell
panel serve app.py --port 5006 --static-dirs en_files=./survey_dashboard/hmc_layout/static/en_files --show
```

### Access the Dashboard

* Navigate to `http://localhost:5006/` in your browser after starting the server.

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
