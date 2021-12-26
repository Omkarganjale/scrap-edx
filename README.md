# scrap-edx

Python Selenium web scrapping bot for parsing meta data of edx courses.

---

## Data fields

Description of the data fields

| subject | Subject of course                     |
| ------- | ------------------------------------- |
| title   | Course Title                          |
| desc    | Course Description                    |
| weeks   | Estimated Weeks required to complete  |
| hours   | Average hours per week for completion |
| outcome | What you'll learn                     |
| instit  | Hosting Institure                     |
| level   | Difficulty level of course            |
| prereq  | Prerequisite of course                |
| lang    | Language                              |
| url     | URL of course                         |

<br/>

---

<br />

## Configure

<br />

-   ```python
    MAX_COURSES_PER_SUBJECT
    ```

    Is the number of courses user wish to parse per subject

-   ```python
    subjects
    ```

    List of all the subjects which will be processed. <br />
    By default All.<br />
    Following are the subjects which will be processed by default.

    ```python
    Architecture
    Art & Culture
    Biology & Life Sciences
    Business & Management
    Chemistry
    Communication
    Computer Science
    Data Analysis & Statistics
    Design
    Economics & Finance
    Education & Teacher Training
    Electronics
    Energy & Earth Sciences
    Engineering
    Environmental Studies
    Ethics
    Food & Nutrition
    Health & Safety
    History
    Humanities
    Language
    Law
    Literature
    Math
    Medicine
    Music
    Philanthropy
    Philosophy & Ethics
    Physics
    Science
    Social Sciences
    ```

-   ```python
      driver
    ```

    Install a compatible driver

    Edge users can download webdriver from here:
    https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/

    ```python
    driver = webdriver.Edge('Path/to/driver')
    ```

    Chrome user's can download webdriver from here:
    https://sites.google.com/chromium.org/driver/

    ```python
    driver = webdriver.Chrome('Path/to/driver')
    ```
