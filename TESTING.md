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

---

<a id="automated-testing"></a>

## Automated Testing

Automated testing was a key part of the development workflow for **Fit Six**, helping to ensure that critical components of the e-commerce site functioned reliably under various user scenarios. The test suite covers **models, forms, views, and admin logic** using Django’s built-in [TestCase](https://docs.djangoproject.com/en/4.2/topics/testing/overview/) framework.

[coverage.py](https://pypi.org/project/coverage/) was used to monitor test coverage and identify any untested areas. The goal was to validate backend functionality, prevent regressions, and support a maintainable codebase as the project scaled in complexity.

### Scope of Automated Testing

The automated test suite was planned and executed to cover the following key areas:

#### Newsletter App

- **Form logic** tested to validate unique email submissions and reject duplicates
- **Model logic** tested for email uniqueness, optional user linking, and string output
- **View logic** tested for success, warning, and error message feedback with redirects

#### Profiles App

- **Model logic** tested to confirm automatic `UserProfile` creation via Django signals, correct string representation, field defaults, and update persistence  
- **Form logic** tested to verify field validation, placeholder and CSS class rendering, autofocus behavior, and label suppression in `UserProfileForm`  
- **App configuration** verified to ensure proper `AppConfig` registration and name resolution

--
<a id="manual-testing"></a>

## Manual Testing

<a id="full-testing"></a>

### Full Testing

This section outlines the **manual testing** conducted to ensure the Fit Six e-commerce application functions correctly across all major user interactions, devices, and screen sizes. Testing focused on key areas such as form validation, navigation flows, user authentication, responsive layout behaviour, and secure checkout processes.

Each feature was tested systematically to identify and resolve potential issues relating to layout, business logic, error handling, or access control. Special attention was paid to high-impact views such as the **product catalogue**, **shopping bag**, **checkout**, and **user account dashboard**.

In addition to structured manual testing, **informal feedback** was gathered from friends and family using a variety of devices and browsers. This helped validate the real-world usability, responsiveness, and accessibility of the site across different screen sizes and operating systems.

<a id="browser"></a>

### Browser Compatibility

To ensure broad accessibility and a consistent user experience, the **Fit Six** application was manually tested on all major modern browsers, including:

- [Google Chrome](https://www.google.com/chrome)
- [Mozilla Firefox](https://www.mozilla.org/firefox)
- [Apple Safari](https://www.apple.com/uk/safari/)
- [Microsoft Edge](https://www.microsoft.com/en-gb/edge)

Each page and core user flow (e.g. registration, product filtering, cart interaction, and checkout) was tested for rendering consistency, interactive behaviour, and layout responsiveness.

---

<a id="responsiveness"></a>

### Responsiveness

To ensure a consistent user experience across all devices, the Fit Six site was thoroughly tested for responsiveness using **Chrome Developer Tools** and physical testing on smartphones, tablets, laptops, and desktops.

Based on research from [Stack Exchange](https://ux.stackexchange.com/questions/74798/are-there-devices-narrower-than-320px-and-data-on-their-usage-for-web-browsing), testing was anchored at a minimum width of **320px**, which reflects the narrowest modern screen size still in common use.

In addition to using Chrome’s responsive design mode, the [Mobile First](https://www.webmobilefirst.com/en/) Chrome extension was used to simulate how the site renders across various devices and breakpoints.



---

<a id="accessibility"></a>

### Accessibility

Accessibility was a key consideration throughout the development of **Fit Six**, to ensure the site is usable by people of all abilities and assistive needs. The goal was to meet **WCAG 2.1 AA** standards where possible, particularly for navigation, colour contrast, and form usage.

#### Colour Contrast Compliance

To support users with visual impairments, all key colour combinations (text, buttons, backgrounds) were tested using the [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/). This ensured that foreground and background combinations meet or exceed recommended contrast ratios for legibility.

In addition, form labels, alt attributes, and ARIA roles were reviewed to improve screen reader compatibility and keyboard accessibility.




---
<a id="conclusion"></a>

## Conclusion

Through a combination of **validation tools**, **automated test coverage**, **manual device/browser testing**, and **accessibility checks**, the **Fit Six** application has been rigorously tested to ensure a robust, user-friendly, and inclusive experience across platforms.

Areas for future improvement — such as extended screen reader testing or broader JavaScript test coverage — have been identified and documented for future iterations. Overall, the site meets the project’s functional and technical requirements, offering a stable and scalable foundation for real-world e-commerce use.

<br><hr>
[🔼 Back to top](#contents)