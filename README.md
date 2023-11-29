
# 📈 Expenses


## 📖 Table of Contents
- [📖 Table of Contents](#-table-of-contents)
- [📍 Overview](#-overview)
- [📦 Features](#-features)
- [📂 repository Structure](#-repository-structure)
- [⚙️ Modules](#modules)
- [🚀 Getting Started](#-getting-started)
    - [🔧 Installation](#-installation)
    - [🤖 Running ](#-running-)
    - [🧪 Tests](#-tests)
- [🛣 Roadmap](#-roadmap)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [👏 Acknowledgments](#-acknowledgments)

---


## 📍 Overview

This repository hosts an expenses tracking application named 'expenses'. The application reads bank statements, visualizes data, and tracks metrics. Powered by python with Docker for containerization, it uses technologies like Streamlit for an interactive frontend, pandas and numpy for data handling, and plotly for creating insightful visualizations. The application supports a variety of banks, demonstrating versatility. Power features include interactive filtering, sorting, and advanced data visualizations. The application offers detailed metrics, efficient data manipulation, and modularized code for easy maintenance and scalability.

---

## 📦 Features

|    | Feature            | Description                                                                                                        |
|----|--------------------|--------------------------------------------------------------------------------------------------------------------|
| ⚙️ | **Architecture**   | The codebase follows a microservices architecture, containerized with Docker. Python and Poetry versions are specified, with services defined in the Docker Compose file.
| 📄 | **Documentation**  | The codebase, although lacking explicit external documentation, has well-commented code snippets that provide insights into the functionality of each module.|
| 🔗 | **Dependencies**   | Dependencies include Python packages like Streamlit, pandas, and Plotly, as well as development-specific tools like MyPy and Black, managed with Poetry.|
| 🧩 | **Modularity**     | The code is modular, split into components like 'app.py', 'models.py', 'metrics.py' etc., inside the 'expenses' directory, allowing easy adjustment and maintenance.|
| 🧪 | **Testing**        | There is no evidence of formal testing strategies or tools in the repository. This is one area for potential improvement.|
| ⚡️  | **Performance**    | Use of data caching in Streamlit and efficient data manipulation with pandas suggest good performance. However, no explicit performance metrics are available.|
| 🔐 | **Security**       | The Dockerfile runs the app as a non-root user, which is a good practice for security. No other explicit security measures are evident.|
| 🔀 | **Version Control**| Version updates are managed via Poetry, with different severity levels. No mention of any specific version control system like Git is found.|
| 🔌 | **Integrations**   | The system integrates with banks (Revolut, BancaSella) through statements processing. Further analysis is required to fully understand other integrations.|
| 📶 | **Scalability**    | Use of modular architecture and containers indicates a certain level of scalability. Detailed performance profiling is required for a comprehensive assessment.|


---


## 📂 Repository Structure

```sh
└── /
    ├── Dockerfile
    ├── Makefile
    ├── docker-compose.yml
    ├── expenses/
    │   ├── app.py
    │   ├── metrics.py
    │   ├── models.py
    │   ├── ops.py
    │   ├── plots.py
    │   ├── sidebar.py
    │   └── statements.py
    ├── poetry.lock
    └── pyproject.toml

```

---


## ⚙️ Modules

<details closed><summary>Root</summary>

| File                         | Summary                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| ---                          | ---                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| [Dockerfile]({file})         | The code represents a Dockerfile for managing a Python-based application structure. It builds three Docker images-a base image called builder-base with specified Python and Poetry versions, a production image which copies requirements and sets up virtual environment from builder-base, and runs the app as a non-root user. Lastly, there's a development image for testing, which copies Poetry and the set up virtual environment from builder-base and installs dependencies.                                                                                                                         |
| [Makefile]({file})           | The provided Makefile controls Docker compose commands for managing a Docker containerized application,'app'. Key functions include setting up (`up`), shutting down (`down`), and building (`build`) the application. Other tasks include accessing the application's shell (`shell`), enforcing code formatting with Black and isort (`format`), type checking with mypy (`typecheck`), installing mypy stubs (`mypy-stubs`), and managing version updates of'app' using Poetry with different severity levels: patch, minor, or major.                                                                       |
| [pyproject.toml]({file})     | The code represents the project configuration for a Python-based'expenses' application. It dictates app dependencies such as streamlit for web frontend, pandas and numpy for data manipulation, and plotly for data visualization.'myPy','black', and'isort' are specified for development dependencies. The dependencies and configurations are managed using Poetry, exhibiting in'pyproject.toml' and'poetry.lock'.'Dockerfile' and'docker-compose.yml' suggest containerization of the app. The app logic is divided into modules like'app.py','models.py','ops.py', etc., within the'expenses' directory. |
| [docker-compose.yml]({file}) | The depicted codebase is for a Dockerized application with streamlit, primarily handling expenses. It follows a microservices architecture with services defined in a docker-compose file. Key functionalities include metrics tracking, operations management, generation of statements, creation of plots, and a sidebar for navigation. The Dockerfile, Makefile, poetry.lock, and pyproject.toml files manage dependencies and build processes.                                                                                                                                                             |
| [poetry.lock]({file})        | The code is a'poetry.lock' file automatically generated by Poetry for python package management. It contains details about the Altair package, a declarative statistical visualization library for Python, such as name, version, description, python version compatibility, and related files with their hashes. It lists package dependencies (including Jinja2, Numpy, and Pandas) and extra dependencies for development purposes. Maintains consistency and repeatable builds in Python projects.                                                                                                          |

</details>

<details closed><summary>Expenses</summary>

| File                    | Summary                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| ---                     | ---                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| [sidebar.py]({file})    | The given code is part of an application dealing with bank statements. It provides a sidebar in the interface for users to upload their bank statement as a CSV file. It supports statements from'Revolut' and'BancaSella' banks. It also provides settings for adjusting the plot height. Upon successful uploading of a file, it returns a structured view of it (Pandas DataFrame `df`) and a value indicating plot height.                                                                                                               |
| [metrics.py]({file})    | The provided Python code in "metrics.py" is part of a larger project structure. It defines a function'total' that uses Streamlit's caching mechanism to save computation time. The function receives a pandas DataFrame and a category string as input, filters the DataFrame based on the category, and then computes and returns the total sum of the'euro' column for the filtered entries.                                                                                                                                               |
| [models.py]({file})     | The code defines an enumeration,'Granularity', which represents the granularity of time. It has two possible values:'Month' and'Week'. This enumeration could be used in the wider application to specify the time granularity for processing or displaying expenses.                                                                                                                                                                                                                                                                        |
| [ops.py]({file})        | The code in'expenses/ops.py' consists of several functions that manipulate and present data from a pandas Dataframe, with the help of the streamlit library for caching data for faster performance. These functions allow the loading of CSV files into dataframes, filtering data based on date ranges and user-specified options, retrieving unique options from a column, and obtaining the earliest and latest dates in a specified column in the dataframe.                                                                            |
| [plots.py]({file})      | The code describes a set of data visualization functions in a finance context. It generates a variety of interactive plots (bar, line, pie, heatmap) from a DataFrame. The plots represent different analyses of earnings/expenses data such as earnings vs expenses groups, profit/loss over time, or top transactors/vendors by transactions or amount. It uses'plotly' for generating plots and'streamlit' for caching data, optimizing web app performance. Data is grouped, aggregated, and manipulated as required for specific plots. |
| [app.py]({file})        | The code represents a Transaction Dashboard web application developed using Streamlit. The dashboard provides filters to sort data based on date, categories, sub-categories, and operations. Total Earnings, Expenses, and Savings/Losses metrics are displayed, followed by several interactive Plotly charts illustrating profit/loss, category and subcategory expenses, earnings, transactors, and transaction heatmap for better data visulization. Transactions are listed at the end of the page.                                    |
| [statements.py]({file}) | The given code includes classes to process bank statements from arbitrary banks. Specifically, it includes a base class `BankStatement` to define a common schema for statements, and child classes `BancaSella` and `Revolut` to process their respective formats into the common schema. Bank statements are imported as DataFrames. Elements include date and amount of operation, type of operation, transaction kind, and transaction categories and subcategories.                                                                     |

</details>

---

## 🚀 Getting Started

***Dependencies***

Please ensure you have the following dependencies installed on your system:

`- ℹ️ Docker`

### 🔧 Installation

1. Clone the  repository:
```sh
git clone https://github.com/ab3llini/expenses.git
```

2. Change to the project directory:
```sh
cd expenses
```

### 🤖 Running 

```sh
# Start Docker Engine, then:
make run
```
---

## 🛣 Project Roadmap

> - [ ] `ℹ️  Better documentation`
> - [ ] `ℹ️  Improved Analysis`
> - [ ] `ℹ️  Add ML / NLP features`



---

## 🤝 Contributing

Contributions are welcome! Here are several ways you can contribute:

- **[Submit Pull Requests](https://github.com/local//blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.
- **[Join the Discussions](https://github.com/local//discussions)**: Share your insights, provide feedback, or ask questions.
- **[Report Issues](https://github.com/local//issues)**: Submit bugs found or log feature requests for LOCAL.

#### *Contributing Guidelines*

<details closed>
<summary>Click to expand</summary>

1. **Fork the Repository**: Start by forking the project repository to your GitHub account.
2. **Clone Locally**: Clone the forked repository to your local machine using a Git client.
   ```sh
   git clone <your-forked-repo-url>
   ```
3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
   ```sh
   git checkout -b new-feature-x
   ```
4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear and concise message describing your updates.
   ```sh
   git commit -m 'Implemented new feature x.'
   ```
6. **Push to GitHub**: Push the changes to your forked repository.
   ```sh
   git push origin new-feature-x
   ```
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.

Once your PR is reviewed and approved, it will be merged into the main branch.

</details>

---


