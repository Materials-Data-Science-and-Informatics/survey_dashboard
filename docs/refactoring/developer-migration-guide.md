# Developer Migration Guide

## Overview

This guide helps developers transition from the old monolithic `main.py` structure to the new modular architecture. It provides practical examples and migration patterns for common development tasks.

---

## Before vs After Comparison

### Old Structure (Before Refactoring)
```python
# main.py (1,198 lines)
# Everything was in one file:
# - Global constants
# - Data processing functions  
# - Widget creation
# - Chart generation
# - Layout assembly
# - Event callbacks
# - Template setup

def select_data(question, data_filters, ...):
    # 160 lines of data processing logic
    
def update_chart(target, event, ...):
    # 63 lines of chart update logic
    
# 47 total functions in main.py
# 23 import statements
```

### New Structure (After Refactoring)
```python
# main.py (113 lines) - Orchestration only
from survey_dashboard.data_processor import DataProcessor
from survey_dashboard.widgets import WidgetFactory
from survey_dashboard.visualizations import VisualizationManager
from survey_dashboard.layout_manager import LayoutManager

# Clear initialization flow
data_processor = DataProcessor()
widget_factory = WidgetFactory(data_processor)
# ... etc

# config.py - All constants
# data_processor.py - All data logic
# widgets.py - All widget creation
# visualizations.py - All chart logic
# layout_manager.py - All layout logic
```

---

## Common Migration Scenarios

### 1. Finding Configuration Values

#### ❌ Before (searching through main.py):
```python
# Had to search through 1,198 lines to find:
LANGUAGE = os.environ.get("LANGUAGE_DASHBOARD", "EN")
ACCORDION_WIDTH = int(DEFAULT_FIGURE_WIDTH * 2) 
SIZING_MODE = "stretch_width"
# ... scattered throughout the file
```

#### ✅ After (config.py):
```python
from survey_dashboard.config import (
    LANGUAGE,
    ACCORDION_WIDTH,
    SIZING_MODE,
    RESEARCH_AREA_COLORS,
    DEFAULT_QUESTIONS
)
```

### 2. Modifying Data Processing Logic

#### ❌ Before (mixed with other concerns):
```python
# main.py lines 238-398 (160 lines)
def select_data(question, data_filters, data_filters_method, filter_by=FILTER_BY):
    """Select the data to display"""
    # Complex logic mixed with widget and layout code
    # Hard to test in isolation
    # Risk of breaking other functionality
```

#### ✅ After (isolated in data_processor.py):
```python
from survey_dashboard.data_processor import DataProcessor

# Easy to test with mock data
data_processor = DataProcessor()
result = data_processor.select_data(question, filters, method_filters)

# Clear responsibilities
# Can be unit tested
# Changes don't affect UI or layout
```

### 3. Adding New Widget Types

#### ❌ Before (searching and modifying main.py):
```python
# Had to find widget creation code scattered throughout main.py
# Lines 584-651 contained widget creation
# Mixed with other logic
# Risk of breaking existing widgets
```

#### ✅ After (focused in widgets.py):
```python
from survey_dashboard.widgets import WidgetFactory

class WidgetFactory:
    def create_new_widget_type(self):
        """Add new widget here"""
        return pn.widgets.NewWidgetType(
            name="New Widget",
            options=self.get_options()
        )
    
    def create_all_widgets(self):
        # Easy to extend
        widgets["new_category"] = {
            "new_widget": self.create_new_widget_type()
        }
```

### 4. Creating New Chart Types

#### ❌ Before (complex modification in main.py):
```python
# Had to modify update() function (lines 861-923)
# Add new elif condition  
# Risk of breaking existing chart types
def update(target, event, question_sel, f_choice, m_choice, q_filter, charttype):
    # ... existing code ...
    elif charttype == "New Chart Type":  # Added here
        # New chart logic mixed with existing logic
```

#### ✅ After (clean extension in visualizations.py):
```python
from survey_dashboard.visualizations import VisualizationManager

class VisualizationManager:
    def update_chart(self, target, event, question_sel, f_choice, m_choice, q_filter, charttype):
        # ... existing code ...
        elif charttype == "New Chart Type":
            fig = self.create_new_chart_type(source, **display_options)
        
        target.object = fig
    
    def create_new_chart_type(self, source, **options):
        """New chart creation logic isolated here"""
        return new_chart_function(source, **options)
```

### 5. Modifying Layout

#### ❌ Before (layout mixed with everything else):
```python
# main.py lines 1117-1197 (80 lines of layout)
# Mixed with data processing and widget creation
# Hard to visualize layout structure
# Changes affected multiple concerns
```

#### ✅ After (clean separation in layout_manager.py):
```python
from survey_dashboard.layout_manager import LayoutManager

layout_manager = LayoutManager()

# Easy to modify specific sections
def create_new_section(self, components):
    return pn.Column(
        self.section_title,
        pn.Row(*components, sizing_mode="stretch_width"),
        sizing_mode="stretch_width"
    )

# Add to accordion
sections["new_section"] = self.create_new_section(components)
```

---

## Development Workflow Changes

### Adding a New Feature

#### Old Workflow:
1. ❌ Open massive main.py file (1,198 lines)
2. ❌ Search for relevant section (time-consuming)
3. ❌ Make changes carefully to avoid breaking other parts
4. ❌ Test entire application (no isolation possible)
5. ❌ Risk merge conflicts with other developers

#### New Workflow:
1. ✅ Identify which module(s) need changes
2. ✅ Open specific module file (150-400 lines)
3. ✅ Make focused changes with clear boundaries
4. ✅ Unit test specific module if needed
5. ✅ Integration test with other modules
6. ✅ Reduced merge conflicts due to modularity

### Debugging Issues

#### Old Approach:
1. ❌ Problem could be anywhere in 1,198 lines
2. ❌ Data, UI, and layout issues mixed together
3. ❌ Hard to isolate root cause
4. ❌ Debugging required understanding entire codebase

#### New Approach:
1. ✅ Identify issue category (data, UI, visualization, layout)
2. ✅ Focus debugging on specific module
3. ✅ Clear module boundaries help isolate problems
4. ✅ Can test individual components in isolation

---

## Code Location Reference

### Where to Find Things Now:

| What you need | Old location | New location |
|---------------|-------------|--------------|
| **Configuration values** | Throughout main.py | `config.py` |
| **Color schemes** | Lines 210-224 in main.py | `config.py` → `RESEARCH_AREA_COLORS` |
| **Data file paths** | Lines 162-163 in main.py | `config.py` → `DATAFILE_PATH` |
| **Data processing** | Lines 238-571 in main.py | `data_processor.py` → `DataProcessor` class |
| **Widget creation** | Lines 584-651 in main.py | `widgets.py` → `WidgetFactory` class |
| **Chart updates** | Lines 861-963 in main.py | `visualizations.py` → `VisualizationManager` class |
| **Layout assembly** | Lines 1117-1197 in main.py | `layout_manager.py` → `LayoutManager` class |
| **Application startup** | Mixed throughout main.py | `main.py` (now clean orchestration) |

---

## Import Strategy Changes

### Old Import Pattern:
```python
# main.py had everything imported at the top
import os
from os.path import dirname, join
from pathlib import Path
import pandas as pd
import panel as pn
import numpy as np
from bokeh.palettes import Category20
from bokeh.models import ColumnDataSource, Div
from jinja2 import Environment, FileSystemLoader
from survey_dashboard.plots import *
# ... 23 total imports
```

### New Import Pattern:
```python
# Each module imports only what it needs
# main.py (minimal imports):
from survey_dashboard.data_processor import DataProcessor
from survey_dashboard.widgets import WidgetFactory  
from survey_dashboard.visualizations import VisualizationManager
from survey_dashboard.layout_manager import LayoutManager

# Module-specific imports in their respective files
# config.py imports configuration-related modules
# data_processor.py imports data-related modules
# etc.
```

---

## Testing Changes

### Old Testing Approach:
```python
# Could only test entire application
# No way to test individual components
# Mock data required loading entire CSV
# Integration tests only
```

### New Testing Approach:
```python
# Unit testing now possible
def test_data_processor():
    mock_data = pd.DataFrame({"test": [1, 2, 3]})
    processor = DataProcessor()
    processor.survey_data = mock_data
    result = processor.select_data(...)
    assert result is not None

def test_widget_factory():
    processor = Mock()
    factory = WidgetFactory(processor) 
    widgets = factory.create_global_filters()
    assert len(widgets) == 2

# Integration testing between modules
def test_visualization_manager():
    data_processor = Mock()
    viz_manager = VisualizationManager(data_processor)
    charts = viz_manager.create_overview_charts([], [])
    assert len(charts) == 4
```

---

## Performance Considerations

### Before Refactoring:
- ❌ IDE slowdown with 1,198-line file
- ❌ Entire application loaded for any change
- ❌ No selective loading possible
- ❌ Memory usage for entire application

### After Refactoring:  
- ✅ Faster IDE performance with smaller files
- ✅ Selective module loading possible
- ✅ Better memory management
- ✅ Faster development iteration

---

## Common Gotchas and Solutions

### 1. Import Path Changes
**Problem:** Old code references don't work
```python
# ❌ This won't work anymore:
from main import select_data

# ✅ Use this instead:
from survey_dashboard.data_processor import DataProcessor
data_processor = DataProcessor()
data_processor.select_data(...)
```

### 2. Global Variable Access
**Problem:** Global variables moved to config
```python  
# ❌ This won't work:
LANGUAGE = "EN"  # was global in main.py

# ✅ Use this instead:
from survey_dashboard.config import LANGUAGE
```

### 3. Function Signatures Changed  
**Problem:** Some methods are now class methods
```python
# ❌ Old function call:
result = select_data(question, filters, methods)

# ✅ New method call:
data_processor = DataProcessor()
result = data_processor.select_data(question, filters, methods)
```

### 4. Callback Registration
**Problem:** Callbacks now handled differently
```python
# ❌ Old callback pattern:
control.link(fig, callbacks={"value": gen_update_exp1})

# ✅ New callback pattern:
callbacks = visualization_manager.create_update_callbacks(widgets)
control.link(fig, callbacks={"value": callbacks["exploration"][0]})
```

---

## Migration Checklist

### For Each Feature Change:

- [ ] **Identify module:** Which module contains the functionality?
- [ ] **Check dependencies:** Does your change affect other modules?
- [ ] **Update tests:** Add/modify tests for the specific module
- [ ] **Verify interfaces:** Ensure module interfaces remain compatible
- [ ] **Test integration:** Check that modules work together
- [ ] **Update documentation:** Document any interface changes

### For New Developers:

- [ ] **Read architecture documentation:** Understand module responsibilities
- [ ] **Set up development environment:** Install dependencies  
- [ ] **Run existing tests:** Ensure setup is correct
- [ ] **Make small change:** Practice with the new structure
- [ ] **Review code patterns:** Understand how modules interact

---

## Getting Help

### Resources:
- **Architecture Documentation:** `docs/refactoring/module-architecture.md`
- **Main Overview:** `docs/refactoring/main-refactoring-overview.md`
- **Testing Guide:** `docs/refactoring/testing-validation.md`

### Common Questions:
- **"Where is function X now?"** → Check the code location reference table above
- **"How do I add a new chart?"** → Extend `VisualizationManager` in `visualizations.py`
- **"How do I change configuration?"** → Modify values in `config.py`
- **"Tests are failing after my change"** → Check if you broke module interfaces

---

*This migration guide should help you transition smoothly to the new modular architecture. The improved structure will make your development work more efficient and less error-prone.*