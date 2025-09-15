# HMC Community Survey 2021 - Column Mapping Guide

This document provides a comprehensive mapping of the columns in the `responses_cleaned_mapped_to_publish.csv` dataset to their corresponding survey questions from the HMC Community Survey 2021.

## Survey Overview

The HMC Community Survey 2021 was conducted to understand research data management practices among researchers in the Helmholtz Association. The survey used a **dynamic questioning approach** where follow-up questions were shown based on previous answers, explaining the varying column counts per section.

## Dataset Summary

- **Actual columns in published CSV**: 263 columns
- **Potential survey columns**: 305 columns (from survey design)
- **Completed responses**: 631 responses
- **Data file**: `responses_cleaned_mapped_to_publish.csv`

## Survey Question Groups and Column Mappings

### 1. **Personal Background (PERBG)** - 26 columns

Characterizes survey respondents by their institutional affiliation, research field, scientific discipline, career level, and research experience.

- `PERBG1/_` - Helmholtz center affiliation
- `PERBG1/other` - Other center specification  
- `PERBG2/_` - Helmholtz research field
- `PERBG3/_` - Primary research area
- `PERBG3/other` - Other research area
- `PERBG3AGRI/_`, `PERBG3AGRI/other` - Agricultural sciences
- `PERBG3BIO/_`, `PERBG3BIO/other` - Biological sciences
- `PERBG3CHEM/_`, `PERBG3CHEM/other` - Chemistry
- `PERBG3GEO/_`, `PERBG3GEO/other` - Earth sciences
- `PERBG3ING/_`, `PERBG3ING/other` - Engineering sciences
- `PERBG3LIFE/_`, `PERBG3LIFE/other` - Life sciences
- `PERBG3MATH/_`, `PERBG3MATH/other` - Mathematics
- `PERBG3MED/_`, `PERBG3MED/other` - Medical sciences
- `PERBG3PHYS/_`, `PERBG3PHYS/other` - Physics
- `PERBG3PSYCH/_`, `PERBG3PSYCH/other` - Psychology
- `PERBG4/_` - Years working in research
- `PERBG6/_`, `PERBG6/other` - Career level
- `PERBG7/_` - ORCID ID availability
- `PERBG8/_` - Familiarity with FAIR data guidelines

### 2. **Research Data Properties (RSDP)** - 71 columns

Characterizes the research data generated or used by respondents, including data sources, methods, tools, and formats.

- `RSDP1/1A2`, `RSDP1/3A4` - Data origin (reused vs self-generated)
- `RSDP1b/1` - Data origin (simulated vs experimental)
- `RSDP1c/1` through `RSDP1c/11`, `RSDP1c/other` - Data generation methods (12 columns)
- `RSDP2/1` through `RSDP2/6`, `RSDP2/other` - Data collection methods (7 columns)
- `RSDP2b/1-1` through `RSDP2b/7-3` - Detailed data collection workflows (21 columns)
- `RSDP3/1` through `RSDP3/15`, `RSDP3/other` - Data formats used (16 columns)
- `RSDP4/_` - Data collection duration
- `RSDP7/_` - Publication data volume estimation
- `RSDP8/_` - Data processing time
- `RSDP10/_` - Important software applications
- `RSDP11/_` - Software application importance

### 3. **Research Data Management Practices (RDMPR)** - 86 columns

Focuses on research data storage routines, data annotation, documentation practices, and metadata handling.

- `RDMPR1/1` through `RDMPR1/3`, `RDMPR1/0`, `RDMPR1/other` - Data storage locations (5 columns)
- `RDMPR3/1` through `RDMPR3/3`, `RDMPR3/other`, `RDMPR3/0` - Documentation methods (5 columns)
- `RDMPR4/_` - Structured documentation (yes/no)
- `RDMPR5/_` - International standards usage
- `RDMPR6/1` through `RDMPR6/26`, `RDMPR6/other` - Metadata categories collected (27 columns)
- `RDMPR7/2` through `RDMPR7/9`, `RDMPR7/other` - Digital metadata documentation (9 columns)
- `RDMPR8/2` through `RDMPR8/10` - Automated metadata collection (9 columns)
- `RDMPR9/2` through `RDMPR9/10` - Manual metadata collection (9 columns)
- `RDMPR10/1` through `RDMPR10/3` - Structured documentation motivations (3 columns)
- `RDMPR11/0` through `RDMPR11/9`, `RDMPR11/other` - Metadata collection obstacles (11 columns)
- `RDMPR12/1` through `RDMPR12/6`, `RDMPR12/0`, `RDMPR12/other` - International standards used (8 columns)

### 4. **Data Publishing Practices (DTPUB)** - 62 columns

Addresses respondents' experience in making research data publicly available, including motivations and challenges.

- `DTPUB1b/1` through `DTPUB1b/3`, `DTPUB1b/other` - Data publishing methods (4 columns)
- `DTPUB3/1` through `DTPUB3/7`, `DTPUB3/other` - Data publishing motivations (8 columns)
- `DTPUB4a/0` through `DTPUB4a/7`, `DTPUB4a/other` - Data publishing obstacles (9 columns)
- `DTPUB4b/0` through `DTPUB4b/7`, `DTPUB4b/other` - Barriers for non-publishers (9 columns)
- `DTPUB5/1` through `DTPUB5/5` - Publishing percentage estimation (5 columns)
- `DTPUB6/1` - Repository usage (1 column)
- `DTPUB7/1`, `DTPUB7/21` through `DTPUB7/93`, `DTPUB7/other`, `DTPUB7/0` - Published metadata types (26 columns)

### 5. **Services and Support Needs (SERVC)** - 12 columns

Addresses respondents' perceived need for support in various topics of research data management and preferred service formats.

- `SERVC1/1` through `SERVC1/9`, `SERVC1/other`, `SERVC1/0` - Support needs areas (11 columns)
- `SERVC2/1` through `SERVC2/6` - Service format preferences (6 columns)

### 6. **Technical/Administrative Columns** - 8 columns

System-generated fields for survey administration and analysis.

- `id` - Response identifier
- `interviewtime/_` - Interview duration
- `lastpage/_` - Last page reached in survey
- `submitdate/_` - Submission timestamp

## Survey Logic and Adaptive Questioning

The survey implemented **conditional logic** where:
- Questions were dynamically adapted to respondents' expertise levels
- Follow-up questions appeared based on previous answers
- Different paths were available for different experience levels
- Not all respondents saw all questions

This explains why there were 305 possible columns in the survey design, but the published dataset contains only 263 columns after data cleaning and anonymization.

## Key Survey Focus Areas

The survey particularly focused on understanding:

1. **Current practices** in research data management
2. **Metadata handling** and documentation approaches  
3. **Data publishing behaviors** and motivations
4. **Support needs** for FAIR data implementation
5. **Barriers and obstacles** researchers face
6. **Community-specific requirements** across six Helmholtz research fields

## Research Fields Covered

The survey covered all six Helmholtz research fields:
- Aeronautics, Space, and Transport (AST)
- Earth and Environment (E&E)
- Energy
- Health
- Information
- Matter

## Data Collection Details

- **Survey Period**: September to November 2021
- **Total Responses**: 631 completed responses
- **Implementation**: LimeSurvey platform
- **Data Collection**: Fully anonymized
- **Target Group**: Scientific staff across all Helmholtz research centers

## Data Processing and Column Reduction

The published dataset contains **263 columns** rather than the full 305 possible columns from the survey design. This reduction occurred during data processing for the following reasons:

1. **Anonymization**: Institutional affiliation data and other identifying information was removed
2. **Privacy protection**: Software names used by fewer than 4 respondents were anonymized
3. **Data cleaning**: Empty or unused columns may have been filtered out
4. **Conditional questions**: Some survey paths may not have generated responses, resulting in unused columns

The report specifically mentions: "Before the data publication the following information was removed or anonymized from the survey data in order to prevent the identification of individuals: Any information – including that might reveal a respondent's institutional affiliation, Names of software that is used by less than 4 respondents, Any information about institutional repositories."

## Usage Notes

- Column headers use a hierarchical naming convention (GROUP/SUBQUESTION/OPTION)
- Multiple choice questions have separate columns for each option
- Rating scales and slider questions have numeric values
- Free text responses were cleaned and categorized where applicable
- The `/_` suffix typically indicates single-choice or numeric responses
- Numbered suffixes (e.g., `/1`, `/2`) indicate multiple choice options

This mapping enables researchers and analysts to understand the structure and content of the survey data for further analysis and visualization.