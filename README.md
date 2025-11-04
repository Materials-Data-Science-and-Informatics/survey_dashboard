# Survey Dashboard

A dashboard to display survey data in an interactive way using Panel and Bokeh.

## Overview

This repository contains an interactive dashboard developed to display data from HMC surveys in an exploratory way. The dashboard is designed to be reusable for other survey visualization projects.

**Live Demo:** [https://dashboard.survey.helmholtz-metadaten.de/2021community](https://dashboard.survey.helmholtz-metadaten.de/2021community)

### Screenshots

![dashboard_overview](https://user-images.githubusercontent.com/24694833/230306080-9ca68ff8-5b8b-4ac4-b2fa-51e2c5361c7d.png)
![dashboard_methods](https://user-images.githubusercontent.com/24694833/230306091-637188a9-359e-4ea0-8432-4d05a1ccc68f.png)
![Dashboard_survey_data_explorer](https://user-images.githubusercontent.com/24694833/230306099-4cf71bda-0990-4f9d-be14-9a65812e7ac4.png)

## Features

- **Interactive Visualizations**: Explore survey data through dynamic charts and plots
- **Multiple Languages**: Support for English and German (configurable via environment variables)
- **Dockerized Deployment**: Production-ready Docker setup with HTTPS support
- **Responsive Design**: Works across different screen sizes
- **Self-hosted Fonts**: Uses HIFIS DIN fonts for consistent branding

## Installation

### Prerequisites

- Python 3.12 or higher
- Poetry (recommended for development)
- Docker & Docker Compose (for production deployment)

### Local Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Materials-Data-Science-and-Informatics/survey_dashboard.git
   cd survey_dashboard
   ```

2. **Install dependencies using Poetry:**
   ```bash
   poetry install
   ```

3. **Run the development server:**
   ```bash
   poetry run survey-dashboard
   ```

   The dashboard will be available at `http://localhost:5006/2021community/`

### Alternative: Using pip

```bash
pip install .
python -m survey_dashboard.scripts
```

## Usage

### Development Mode

The easiest way to run the dashboard in development mode:

```bash
poetry run survey-dashboard
```

This starts the server with:
- Auto-reload on code changes
- Browser opens automatically
- Development-friendly error messages

### Manual Panel Serve

For more control over server configuration:

```bash
panel serve survey_dashboard/app.py \
  --port 5006 \
  --static-dirs en_files=./survey_dashboard/hmc_layout/static/en_files \
  --prefix /2021community \
  --show
```

### Environment Variables

- `VIRTUAL_PATH` - URL path prefix (default: `/2021community`)
- `LANGUAGE` - Dashboard language: `EN` or `DE` (default: `EN`)

## Production Deployment

This project includes Docker support for production deployment with automatic HTTPS using Let's Encrypt.

### Docker Deployment

1. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your domain and settings
   ```

2. **Build and start containers:**
   ```bash
   docker compose up -d --build
   ```

3. **Access your dashboard:**
   ```
   https://your-domain.com/2021community/
   ```

### Deployment Architecture

The deployment uses:
- **nginx-proxy**: Automatic reverse proxy with virtual host routing
- **acme-companion**: Automatic Let's Encrypt SSL certificate management
- **Dashboard container**: Panel/Bokeh application server

See `docker-compose.yml` and `Dockerfile` for detailed configuration.

## Project Structure

```
survey_dashboard/
├── survey_dashboard/          # Main application code
│   ├── app.py                # Main Panel application
│   ├── scripts.py            # CLI entry point
│   ├── data/                 # Data processing modules
│   ├── ui/                   # UI components and layout
│   ├── i18n/                 # Internationalization
│   └── hmc_layout/           # Templates and static assets
│       ├── en_template.html  # English template
│       ├── de_template.html  # German template
│       └── static/           # CSS, JS, images
├── docs/                     # Documentation
│   └── refactoring/          # Architectural documentation
├── docker-compose.yml        # Docker orchestration
├── Dockerfile               # Container build instructions
├── .env.example             # Environment template
└── pyproject.toml           # Python dependencies
```

## Development

### Running Tests

```bash
poetry run pytest
```

### Code Style

This project uses:
- Black for code formatting
- Flake8 for linting
- MyPy for type checking

### Making Changes

1. Create a feature branch
2. Make your changes
3. Test locally with `poetry run survey-dashboard`
4. Test with Docker if deployment-related
5. Submit a pull request

## Documentation

Detailed documentation can be found in the `docs/refactoring/` directory:
- Architectural overview
- Module structure
- Development guide
- Migration guide

## Troubleshooting

### Port Already in Use

If port 5006 is already in use:
```bash
lsof -ti:5006 | xargs kill -9
```

### Docker Issues

Check container logs:
```bash
docker compose logs -f dashboard
```

Rebuild without cache:
```bash
docker compose build --no-cache
```

### Font Loading Issues

Clear browser cache (Ctrl+Shift+Del) or test in incognito mode.

## Technology Stack

### Core Framework
- **Panel** (1.7.5) - High-level app and dashboarding solution
- **Bokeh** (3.7.3) - Interactive visualization library
- **Python** (3.12+) - Programming language

### Data Processing
- **Pandas** (2.3.2) - Data manipulation
- **NumPy** (2.3.2) - Numerical computing

### Visualization
- **Matplotlib** (3.10.6) - Plotting library
- **WordCloud** (1.9.4) - Word cloud generation

### Web Server
- **Tornado** (6.5.2) - Async web framework (used by Bokeh)

### Deployment
- **Docker** - Containerization
- **nginx-proxy** - Automatic reverse proxy
- **acme-companion** - Let's Encrypt automation

## License

See [LICENSE](./LICENSE) for details.

## Acknowledgements

<div>
<img style="vertical-align: middle;" alt="HMC Logo" src="https://github.com/Materials-Data-Science-and-Informatics/Logos/raw/main/HMC/HMC_Logo_M.png" width=50% height=50% />
&nbsp;&nbsp;
<img style="vertical-align: middle;" alt="FZJ Logo" src="https://github.com/Materials-Data-Science-and-Informatics/Logos/raw/main/FZJ/FZJ.png" width=30% height=30% />
</div>
<br />

This project was developed at the **Institute for Materials Data Science and Informatics (IAS-9)** of the Forschungszentrum Jülich and funded by the **Helmholtz Metadata Collaboration (HMC)**, an incubator-platform of the Helmholtz Association within the framework of the Information and Data Science strategic initiative.

## Citation

If you use this dashboard in your research, please cite:

```bibtex
@software{survey_dashboard,
  title = {Survey Dashboard},
  author = {Bröder, Jens and Gerlich, Silke Christine and Hofmann, Volker},
  year = {2024},
  url = {https://github.com/Materials-Data-Science-and-Informatics/survey_dashboard},
  organization = {Forschungszentrum Jülich GmbH}
}
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Ensure all tests pass
6. Submit a pull request

For major changes, please open an issue first to discuss what you would like to change.

## Support

For questions or issues:
- **GitHub Issues**: [Report a bug or request a feature](https://github.com/Materials-Data-Science-and-Informatics/survey_dashboard/issues)
- **Email**: Contact the maintainers (see repository contributors)

---

**Last Updated:** November 2024
