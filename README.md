# Survey Dashboard

An interactive dashboard for exploring survey data, built with Panel and Bokeh.

**Live Demo:** [https://2021.dashboard.survey.helmholtz-metadaten.de/](https://2021.dashboard.survey.helmholtz-metadaten.de/)

## Features

- Interactive filtering and data exploration
- Real-time chart updates with multiple visualization types
- Correlation analysis between survey questions
- Word cloud visualizations for methods and tools
- Bilingual support (English/German)
- Production-ready Docker deployment with HTTPS

## Quick Start

**Requirements:** Python 3.12+ and Poetry

```bash
# Clone and install
git clone https://github.com/Materials-Data-Science-and-Informatics/survey_dashboard.git
cd survey_dashboard
poetry install

# Run development server
poetry run survey-dashboard
```

The dashboard opens automatically at `http://localhost:5006/`

## Configuration

Set environment variables to customize:

- `LANGUAGE_DASHBOARD` - Interface language: `EN` or `DE` (default: `EN`)
- `VIRTUAL_PATH` - URL path prefix (default: `/2021community`)

## Project Structure

```
survey_dashboard/
├── survey_dashboard/
│   ├── app.py              # Main application entry
│   ├── core/               # Data processing and chart generation
│   ├── ui/                 # Widgets, layout, and callbacks
│   ├── data/               # Survey data and mappings
│   ├── i18n/               # Language translations
│   └── hmc_layout/         # Templates and styling
├── docker-compose.yml      # Docker orchestration
└── pyproject.toml          # Dependencies and configuration
```

## Development

Code style tools: Black, Flake8, MyPy

## Deployment

Merge changes to main and create a version tag. The app is deployed on Kubernetes - contact the project manager for deployment steps.

## Troubleshooting

**Port in use:**
```bash
lsof -ti:5006 | xargs kill -9
```

**Docker logs:**
```bash
docker compose logs -f dashboard
```

## Technology Stack

- **Python 3.12+** with Panel 1.7.5 and Bokeh 3.7.3
- **Data processing:** Pandas, NumPy
- **Visualization:** Matplotlib, WordCloud
- **Deployment:** Docker and Kubernetes

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
