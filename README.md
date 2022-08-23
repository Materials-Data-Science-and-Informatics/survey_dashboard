# Survey dashboard

A dashboard to display survey data in an interactive way.

## Overview

A dashboard using bokeh sever, developed to display data from HMC surveys in an interactive explorer way.

## Installation


## Usage
* In the top folder execute:
```
bokeh serve --show dashboard
```


* Navigate to `http://localhost:8000/` in your browser.


## Development

To embed the dashboard into any website, first you have to host a bokeh server with this application somewhere and then you can embed it with bokehs `sever_document` function [see](https://docs.bokeh.org/en/latest/docs/user_guide/embed.html#app-documents)

Do steps under `usage` above, but for a public exposed URL.

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
