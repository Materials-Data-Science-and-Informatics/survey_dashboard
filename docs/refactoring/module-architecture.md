# Module Architecture Documentation

## Overview

This document provides detailed technical specifications for each module created during the Survey Dashboard refactoring, including interfaces, dependencies, and design patterns.

---

## Architecture Diagram

```
┌─────────────────┐
│    main.py      │ ← Application Entry Point
│  (Orchestrator) │
└─────────────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  LayoutManager  │◄────│VisualizationMgr │◄────│ DataProcessor   │
│                 │     │                 │     │                 │
│ • Template      │     │ • Charts        │     │ • Data Loading  │
│ • Accordion     │     │ • Callbacks     │     │ • Filtering     │
│ • Responsive    │     │ • Updates       │     │ • Aggregation   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         ▲                       ▲                       ▲
         │                       │                       │
         │               ┌───────┴───────┐               │
         │               │               │               │
         │               ▼               ▼               │
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ WidgetFactory   │ │    config.py    │ │   text_display  │
│                 │ │                 │ │   (existing)    │
│ • UI Controls   │ │ • Constants     │ │                 │  
│ • Filters       │ │ • Colors        │ │ • Translations  │
│ • Selectors     │ │ • Paths         │ │ • UI Text       │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

---

## Module Specifications

### 1. config.py

**Purpose:** Centralized configuration and constants management

#### Key Classes/Objects:
```python
# Global Constants
LANGUAGE: str
ACCORDION_WIDTH: int  
SIZING_MODE: str
DATAFILE_PATH: str
RESEARCH_FIELDS: List[str]
RESEARCH_AREA_COLORS: Dict[str, str]
DEFAULT_QUESTIONS: Dict[str, Dict[str, str]]

# Functions
get_template_path() -> Path
get_assets_path() -> Path
```

#### Dependencies:
- `os` - Environment variable access
- `pathlib.Path` - Path manipulation
- `bokeh.palettes.Category20` - Color palette generation
- `survey_dashboard.plots.DEFAULT_FIGURE_*` - Figure dimensions
- `survey_dashboard.data.display_specifications.hcs_clean_dictionaries` - Data specs

#### Design Patterns:
- **Configuration Object Pattern** - Centralized settings
- **Factory Method Pattern** - Path generation functions
- **Constants Pattern** - Immutable configuration values

---

### 2. data_processor.py

**Purpose:** Data loading, transformation, and business logic

#### Key Classes:
```python
class DataProcessor:
    def __init__(self)
    def map_qkey_to_question(self, key: str, lang: str = LANGUAGE) -> str
    def map_question_to_qkey(self, question: str, lang: str = LANGUAGE) -> List[str]
    def select_data(self, question, data_filters, data_filters_method, filter_by) -> Tuple
    def select_data_corr(self, question, question2, data_filters, data_filters_method) -> Tuple  
    def select_data_wordcloud(self, data_filters, data_filters_method, content) -> List[str]
```

#### State Management:
- `self.survey_data: pd.DataFrame` - Main survey dataset
- `self.source: ColumnDataSource` - Bokeh data source  
- `self.source_corr: ColumnDataSource` - Correlation data source

#### Dependencies:
- `pandas` - Data manipulation
- `numpy` - Numerical operations
- `bokeh.models.ColumnDataSource` - Visualization data binding
- `survey_dashboard.analysis.*` - Statistical functions
- `survey_dashboard.config.*` - Configuration values

#### Design Patterns:
- **Data Access Object (DAO) Pattern** - Encapsulates data operations
- **Strategy Pattern** - Different filtering strategies
- **Factory Method Pattern** - Data source creation

---

### 3. widgets.py

**Purpose:** UI widget creation and management

#### Key Classes:
```python
class WidgetFactory:
    def __init__(self, data_processor: DataProcessor)
    def create_global_filters(self) -> List[pn.widgets]
    def create_question_selectors(self) -> Tuple[pn.widgets.Select, pn.widgets.Select]
    def create_chart_type_selectors(self) -> Tuple[pn.widgets.Select, pn.widgets.Select]  
    def create_hidden_filters(self) -> Tuple[pn.widgets.MultiChoice, pn.widgets.MultiChoice]
    def create_all_widgets(self) -> Dict[str, Dict[str, pn.widgets]]
    def get_control_groups(self, widgets: Dict) -> Dict[str, List]
```

#### Widget Organization:
```python
widgets = {
    "global_filters": {
        "research_area": MultiChoice,
        "method": MultiChoice  
    },
    "exploration": {
        "question1": Select,
        "question2": Select,
        "chart_type1": Select,  
        "chart_type2": Select,
        "filter1": MultiChoice,  # hidden
        "filter2": MultiChoice   # hidden
    }
}
```

#### Dependencies:
- `panel as pn` - UI widget framework
- `survey_dashboard.config.*` - Widget configuration
- `survey_dashboard.text_display.*` - UI text and translations
- `survey_dashboard.data.display_specifications.*` - Filter options

#### Design Patterns:
- **Factory Pattern** - Widget creation
- **Builder Pattern** - Complex widget composition
- **Facade Pattern** - Simplified widget interface

---

### 4. visualizations.py

**Purpose:** Chart creation and interactive updates

#### Key Classes:
```python
class VisualizationManager:
    def __init__(self, data_processor: DataProcessor)
    def create_overview_charts(self, data_filters, data_filters_method) -> Dict[str, pn.pane.Bokeh]
    def create_exploration_charts(self, question_select, question_select2, ...) -> Tuple[pn.pane.Bokeh, pn.pane.Bokeh]
    def create_correlation_chart(self, question_select, question_select2, ...) -> Tuple[pn.pane.Bokeh, pn.pane.Bokeh]
    def create_wordcloud_tabs(self, data_filters, data_filters_method) -> Tuple[pn.Column, Dict]
    def update_chart(self, target, event, question_sel, f_choice, m_choice, q_filter, charttype)
    def update_correlation_chart(self, target, event, question_sel, question_sel2, f_choice, m_choice)  
    def update_wordcloud(self, target, event, f_choice, m_choice, content)
    def create_update_callbacks(self, widgets) -> Dict[str, List[Callable]]
```

#### Chart Types Supported:
- **Overview Charts** - Bar charts for key metrics (4 charts)
- **Exploration Charts** - Configurable bar/pie charts (2 interactive charts)
- **Correlation Chart** - Scatter plot with sizing based on response frequency
- **Word Clouds** - Text frequency visualization (3 content types)

#### Dependencies:
- `panel as pn` - Visualization framework  
- `survey_dashboard.plots.*` - Chart generation functions
- `survey_dashboard.config.*` - Visualization configuration
- `survey_dashboard.text_display.*` - Chart labels and text

#### Design Patterns:
- **Command Pattern** - Update callbacks
- **Observer Pattern** - Widget event handling  
- **Factory Method Pattern** - Chart creation
- **Template Method Pattern** - Chart update workflow

---

### 5. layout_manager.py

**Purpose:** Dashboard layout and template integration

#### Key Classes:
```python
class LayoutManager:
    def __init__(self)
    def setup_panel_config(self)
    def setup_template(self)  
    def setup_overview_icons(self)
    def create_global_filters_section(self, control_groups) -> pn.Column
    def create_overview_section(self, overview_charts) -> pn.Column
    def create_question_explorer_section(self, control_groups, exploration_charts, correlation_chart) -> pn.Column
    def create_accordion_layout(self, sections) -> pn.Accordion
    def create_complete_layout(self, ...) -> pn.Column
    def setup_template_variables(self, layout) -> pn.Template
    def make_servable(self) -> pn.Template
```

#### Layout Hierarchy:
```
pn.Column (Main Container)
└── pn.Accordion
    ├── Global Filters Section
    │   ├── Filter Description Text  
    │   ├── Research Area MultiChoice
    │   └── Method MultiChoice
    ├── Overview Section  
    │   ├── Overview Description Text
    │   ├── pn.Row (Charts Row 1)
    │   │   ├── Research Area Chart
    │   │   └── Years in Research Chart
    │   └── pn.Row (Charts Row 2)  
    │       ├── FAIR Familiarity Chart
    │       └── Publication Amount Chart
    ├── Methods/Tools Section
    │   ├── Tools Description Text
    │   └── pn.Tabs  
    │       ├── Methods Word Cloud
    │       ├── Software Word Cloud  
    │       └── Repositories Word Cloud
    └── Question Explorer Section
        ├── Explorer Description Text
        ├── pn.Row (Controls)
        │   ├── Chart 1 Controls Column
        │   └── Chart 2 Controls Column  
        ├── pn.Row (Charts)
        │   ├── Exploration Chart 1
        │   └── Exploration Chart 2
        └── Correlation Section
            ├── Correlation Description Text
            └── pn.Row (Correlation)
                ├── Spacer
                ├── Correlation Chart  
                ├── Correlation Legend
                └── Spacer
```

#### Dependencies:
- `panel as pn` - Layout framework
- `pathlib.Path` - Template path handling  
- `jinja2.Environment, FileSystemLoader` - Template processing
- `survey_dashboard.config.*` - Layout configuration
- `survey_dashboard.text_display.*` - Section text and labels

#### Design Patterns:
- **Composite Pattern** - Hierarchical layout structure
- **Builder Pattern** - Step-by-step layout construction
- **Template Method Pattern** - Layout creation workflow
- **Facade Pattern** - Simplified layout interface

---

### 6. main.py

**Purpose:** Application orchestration and initialization

#### Key Functions:
```python
# Application Flow
print("Initializing HMC Survey Dashboard...")
# → Component initialization
# → Widget creation  
# → Visualization creation
# → Callback setup
# → Layout creation
# → Template configuration
print("Dashboard ready! 🎉")
```

#### Orchestration Workflow:
1. **Dependency Injection** - Initialize all managers with required dependencies
2. **Widget Creation** - Create all UI components and organize into control groups  
3. **Visualization Creation** - Generate all charts with initial data
4. **Event Binding** - Wire up callbacks between widgets and charts
5. **Layout Assembly** - Compose final dashboard layout
6. **Template Configuration** - Setup Jinja2 template with variables
7. **Servable Configuration** - Make application ready for Panel server

#### Dependencies:
- `survey_dashboard.data_processor.DataProcessor` - Data operations
- `survey_dashboard.widgets.WidgetFactory` - UI components  
- `survey_dashboard.visualizations.VisualizationManager` - Charts
- `survey_dashboard.layout_manager.LayoutManager` - Layout

#### Design Patterns:
- **Facade Pattern** - Simplified application interface
- **Dependency Injection Pattern** - Loose coupling between components
- **Orchestrator Pattern** - Coordinates component interactions

---

## Inter-Module Communication

### Data Flow:
1. **config.py** → Provides constants to all modules
2. **data_processor.py** → Transforms data for visualizations  
3. **widgets.py** → Creates controls that trigger updates
4. **visualizations.py** → Uses data_processor for chart updates
5. **layout_manager.py** → Composes widgets and visualizations
6. **main.py** → Orchestrates initialization and event binding

### Event Flow:
1. **User Interaction** → Widget value change
2. **Panel Framework** → Triggers registered callback  
3. **VisualizationManager** → Calls data_processor methods
4. **DataProcessor** → Filters and transforms data
5. **VisualizationManager** → Updates chart with new data
6. **Panel Framework** → Re-renders updated visualization

---

## Extension Points

### Adding New Chart Types:
1. Add chart function to `survey_dashboard.plots`
2. Extend `VisualizationManager.update_chart()` method
3. Add chart type option to `config.CHART_TYPES`
4. Update widget factory to include new option

### Adding New Data Sources:
1. Extend `DataProcessor.__init__()` to load additional data
2. Add new selection methods (e.g., `select_data_timeseries()`)  
3. Create corresponding visualization methods
4. Update configuration for new data paths

### Adding New Filters:
1. Add filter options to `config.py`
2. Extend `WidgetFactory` to create filter widgets
3. Update `DataProcessor` filtering methods  
4. Wire up callbacks in `main.py`

---

## Testing Strategy

### Unit Testing Approach:
- **config.py** - Test configuration loading and path generation
- **data_processor.py** - Test with mock CSV data and known expected outputs  
- **widgets.py** - Test widget creation and configuration
- **visualizations.py** - Test chart creation with mock data
- **layout_manager.py** - Test layout composition and template setup

### Integration Testing:
- **Component Integration** - Test module interactions
- **End-to-End Testing** - Full application workflow testing  
- **Callback Testing** - Widget interaction and chart updates

---

*This modular architecture provides a solid foundation for maintainable, testable, and extensible dashboard development.*