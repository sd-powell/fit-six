# Fit Six – Testing

> [!NOTE]  
> Return to the main [README.md](README.md) file.

This document outlines the testing strategy, process, and results for the **Fit Six Store** e-commerce application. It verifies that the site’s core functionality operates correctly across all user roles, provides a responsive and accessible experience, and meets the acceptance criteria defined by the project’s user stories and feature plan.

Both **manual and automated testing** were conducted throughout development, covering functionality, responsiveness, browser compatibility, accessibility, and data validation. Django’s built-in test framework was used for backend testing, while real-device and browser tools were used to assess front-end behaviour.

This file includes:
- ✅ User story-based test cases  
- ✅ Manual testing across devices and browsers  
- ✅ Automated unit tests (Django views, forms, models)  
- ✅ HTML, CSS, Python, and accessibility validation  
- ✅ Bug tracking and fixes  
- ✅ Known issues (if any)

---

<a id=contents></a>

- [VALIDATION TESTING](#validation-testing)
  - [W3C Validator](#w3c-validation)
  - [W3C CSS Validator](#css-validation)
  - [JavaScript Validator](#js-validation)
  - [Python Validator](#python-validation)
  - [Lighthouse](#lighthouse)
- [AUTOMATED TESTING](#automated-testing)
- [MANUAL TESTING](#manual-testing)
  - [Full Testing](#full-testing)
  - [Browser Compatibility](#browser)
  - [Responsiveness](#responsiveness)
  - [Accessibility](#accessibility)
  - [Testing User Stories](#user-story-testing)
  - [Features Testing](#features-testing)
  - [Manual Features Testing](#manual-features-testing)
  - [Solved Issues & Bugs](#solved-issues)
  - [Known Issues & Bugs](#known-issues)
  - [Conclusion](#conclusion)

<br>
<hr>

Testing was an **essential part of the Fit Six development workflow**, ensuring that the application remained **robust, responsive, and user-friendly** at every stage. Continuous testing allowed issues to be identified and resolved early, improving both development efficiency and overall site reliability.

A range of tools and methods were employed to validate the site’s functionality and presentation. **Chrome Developer Tools** were used extensively to test responsiveness, inspect layout behaviour, debug JavaScript interactions, and assess performance under different viewport sizes. These tools proved invaluable for tuning the user experience across devices.

**ChatGPT** was used throughout the project to support testing strategies, clarify Django logic, refine user journeys, and improve the accessibility and clarity of interface elements. This assisted in building maintainable, production-ready code and supported critical thinking during test planning and debugging.

To confirm that the site was **responsive and accessible across all modern devices**, every page and interactive element was manually tested using Chrome’s responsive design mode, as well as physical testing on **desktop monitors, laptops, tablets, and smartphones**. Navigation, forms, and key e-commerce flows were verified at various screen sizes to ensure a **seamless and consistent experience** for all users.

---

<a id="validation-testing"></a>

## Validation Testing

<a id="w3c-validation"></a>

### W3C Validator

The [W3C Markup Validation Service](https://validator.w3.org/) was used to check the **HTML and CSS** output across all key pages of the Fit Six site. Because Django templates include dynamic content and logic tags (e.g. `{% %}`, `{{ }}`), the validator was run against the **fully rendered HTML output** by viewing the page source in the browser and pasting that into the validator.

This ensured the final output — as seen by users and browsers — conformed to HTML5 and CSS3 standards.

---

<a id="css-validation"></a>

### CSS Validator

[CSS W3C Validator](https://jigsaw.w3.org/css-validator/) was used to validate my CSS file.

---

<a id="js-validation"></a>

### JavaScript

All JavaScript was validated using [JSHint](https://jshint.com/) to ensure proper syntax, code quality, and adherence to best practices.

---

<a id="python-validation"></a>

### Python Validator

All Python code was validated using the [Code Institute Python Linter](https://pep8ci.herokuapp.com/), which checks for compliance with PEP8 — the official Python style guide. This ensured consistent, readable, and well-structured code throughout the project.

---

<a id=lighthouse></a>

### Lighthouse

I've tested my deployed project using the Lighthouse Audit tool to test the performance, accessibility, best practices and SEO of the website.

