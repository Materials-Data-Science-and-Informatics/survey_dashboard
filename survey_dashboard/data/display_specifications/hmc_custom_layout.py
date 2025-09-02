hmc_custom_css_accordion ='''
.bk.card {
  border: 1px solid rgba(0,0,0,.125);
  border-radius: 0.25rem;
}
.bk.accordion {
  border: 1px solid rgba(0,0,0,.125);
}
.bk.card-header {
  align-items: center;
  background-color: rgba(0, 0, 0, 0.03);
  border-radius: 0.25rem;
  display: inline-flex;
  justify-content: start !important;
  width: 100%;
}
.bk.accordion-header {
  align-items: center;
  background-color: rgba(0, 0, 0, 0.03);
  border-radius: 0;
  display: flex;
  justify-content: flex-start;
  width: 100%;
}
.bk.card-button {
  background-color: transparent;
  margin-left: 0.5em;
  flex-basis: content;
  padding: 16px 24px !important;
  box-sizing: border-box;
  display: flex !important;
  align-items: center !important;
}
.bk.card-header-row {
  position: relative !important;
}
.bk.card-title {
  align-items: left;
  font-size: 1.4em;
  font-weight: bold;
  overflow-wrap: break-word;
}
.bk.card-header-row > .bk {
  overflow-wrap: break-word;
  text-align: left;
}

/* Fix scrolling issues without breaking Panel layout */
body {
  overflow-y: auto;
  overflow-x: auto;
}

#app {
  overflow: visible;
  width: 100%;
  max-width: 100%;
}

/* Ensure Panel accordion sections stack properly and span full width */
.bk-panel-models-accordion {
  overflow: visible;
  width: 100% !important;
  max-width: 100% !important;
}

.bk-panel-models-accordion .bk-panel-models-card {
  position: relative;
  margin-bottom: 8px;
  width: 100% !important;
}

/* Ensure all accordion headers have consistent width */
.bk-panel-models-accordion .bk-panel-models-card-header {
  width: 100% !important;
  min-width: 100% !important;
  box-sizing: border-box;
}

/* Add consistent padding to all accordion content */
.bk-panel-models-accordion .bk-panel-models-card-content {
  padding: 24px !important;
  box-sizing: border-box;
}

/* Ensure accordion button spans full header width */
.bk-panel-models-accordion .bk-panel-models-card-button {
  width: 100% !important;
  text-align: left;
  padding: 16px 24px !important;
  box-sizing: border-box;
  display: flex !important;
  justify-content: space-between !important;
  align-items: center !important;
}

/* Target the actual Panel accordion structure */
.bk-panel-models-accordion .bk-panel-models-card-header {
  display: flex !important;
  justify-content: flex-start !important;
  align-items: center !important;
  width: 100% !important;
  gap: 0 !important;
}

/* Fix the text and icon positioning in Panel accordion headers */
.bk-panel-models-accordion .bk-panel-models-card-header > *:first-child {
  flex: 1 !important;
  text-align: left !important;
  order: 1 !important;
}

.bk-panel-models-accordion .bk-panel-models-card-header > *:last-child {
  flex-shrink: 0 !important;
  margin-left: auto !important;
  order: 2 !important;
}

/* Alternative approach: target Panel's internal structure */
.bk-panel-models-accordion .bk-panel-models-card-header .bk-panel-models-markup-html {
  order: 1 !important;
  flex: 1 !important;
  text-align: left !important;
}

.bk-panel-models-accordion .bk-panel-models-card-header .bk-panel-models-icon {
  order: 2 !important;
  margin-left: 0 !important;
  flex-shrink: 0 !important;
}

/* Also target the legacy Panel classes */
.bk-panel-models-accordion .bk-panel-models-card-header .bk-panel-models-markup {
  order: 1 !important;
  flex: 1 !important;
  text-align: left !important;
}

.bk-panel-models-accordion .bk-panel-models-card-header .bk-panel-models-icon {
  order: 2 !important;
  margin-left: auto !important;
  flex-shrink: 0 !important;
}

/* Target Panel's actual accordion button structure */
.bk-panel-models-accordion .bk-panel-models-card-header button {
  display: flex !important;
  justify-content: flex-start !important;
  align-items: center !important;
  width: 100% !important;
  text-align: left !important;
  gap: 0 !important;
}

/* Ensure the text content is on the left */
.bk-panel-models-accordion .bk-panel-models-card-header button > *:first-child {
  order: 1 !important;
  flex: 1 !important;
  text-align: left !important;
}

/* Ensure the icon is on the right */
.bk-panel-models-accordion .bk-panel-models-card-header button > *:last-child {
  order: 2 !important;
  margin-left: 0 !important;
  flex-shrink: 0 !important;
}

/* Additional targeting for Panel's internal structure */
.bk-panel-models-accordion .bk-panel-models-card-header .bk-panel-models-markup-html,
.bk-panel-models-accordion .bk-panel-models-card-header .bk-panel-models-markup {
  order: 1 !important;
  flex: 1 !important;
  text-align: left !important;
}

.bk-panel-models-accordion .bk-panel-models-card-header .bk-panel-models-icon,
.bk-panel-models-accordion .bk-panel-models-card-header .bk-panel-models-markup-icon {
  order: 2 !important;
  margin-left: 0 !important;
  flex-shrink: 0 !important;
}

/* Ensure all Panel layout containers span full width */
.bk-panel-models-layout-Column,
.bk-panel-models-layout-row {
  width: 100% !important;
  max-width: 100% !important;
}

.bk-Row {
padding: 20px;
}

/* Fix carousel overflow issues */
.carousel__viewport {
  overflow: hidden;
}

/* Ensure proper spacing between accordion sections */
.bk-panel-models-accordion .bk-panel-models-card + .bk-panel-models-card {
  margin-top: 8px;
}

/* Consistent spacing for accordion content */
.bk-panel-models-accordion .bk-panel-models-card-content > * {
  margin-bottom: 16px;
}

.bk-panel-models-accordion .bk-panel-models-card-content > *:last-child {
  margin-bottom: 0;
}

/* Make sure the main container spans full viewport */
.bk-root {
  width: 100% !important;
  max-width: 100% !important;
}

/* Ensure consistent accordion appearance */
.bk-panel-models-accordion .bk-panel-models-card {
  border: 1px solid rgba(0, 0, 0, 0.125);
  border-radius: 0.25rem;
  overflow: hidden;
}

/* Smooth transitions for accordion interactions */
.bk-panel-models-accordion .bk-panel-models-card-content {
  transition: all 0.3s ease;
}

/* Remove spacing between text and icon in accordion headers */
.bk-panel-models-accordion .bk-panel-models-card-header * {
  margin: 0 !important;
  padding: 0 !important;
}

.bk-panel-models-accordion .bk-panel-models-card-header button {
  padding: 16px 24px !important;
}

.bk-panel-models-accordion .bk-panel-models-card-header button > *:first-child {
  margin-right: 8px !important;
}

.bk-panel-models-accordion .bk-panel-models-card-header button > *:last-child {
  margin-left: 8px !important;
}
'''
#rgba(0, 0, 0, 0.03);
#"#005AA0" :  rgba(0, 90, 160, 0.53);
#  background-color: rgba(0, 90, 160, 0.53);
