<p align="center">
  <img src="https://img.icons8.com/pulsar-color/96/markdown.png" width="100" />
</p>
<p align="center">
    <h1 align="center">SILAEDER_PROJECTS</h1>
</p>
<p align="center">
    <em><code>Site with projects of the Silaeder students</code></em>
</p>

<hr>

## 🔗 Quick Links

> - [📍 Overview](#-overview)
> - [📦 Features](#-features)
> - [📂 Repository Structure](#-repository-structure)
> - [🧩 Modules](#-modules)
> - [🚀 Getting Started](#-getting-started)
>     - [⚙️ Installation](#-installation)
>     - [🤖 Running Silaeder_projects](#-running-Silaeder_projects)
> - [👏 Acknowledgments](#-acknowledgments)

---


## 📂 Repository Structure

```sh
└── Silaeder_projects/
    ├── db.py
    ├── main.py
    ├── parse.py
    └── templates
        ├── about.html
        ├── create.html
        ├── edit.html
        ├── home.html
        ├── login.html
        ├── projects.html
        ├── register.html
        ├── settings.html
        └── view.html
```

---

## 🧩 Modules

<details>

| File                                                                               | Summary                                       |
| ---                                                                                | ---                                           |
| [db.py](https://github.com/ilyastar9999/Silaeder_projects/blob/master/db.py)       | <code>code of database communication</code> |
| [parse.py](https://github.com/ilyastar9999/Silaeder_projects/blob/master/parse.py) | <code>code of parsing google tables</code>  |
| [main.py](https://github.com/ilyastar9999/Silaeder_projects/blob/master/main.py)   | <code>main code file</code>                 |

</details>

---

## 🚀 Getting Started

***Requirements***

Ensure you have the following dependencies installed on your system:

* **Python**: `version 3.10`
* **Docker**

### ⚙️ Installation

1. Clone the Silaeder_projects repository:

```sh
git clone https://github.com/ilyastar9999/Silaeder_projects
```

2. Change to the project directory:

```sh
cd Silaeder_projects
```

3. Install the dependencies:

```sh
pip install requirements.txt
```

### 🤖 Running Silaeder_projects

Use the following command to run Silaeder_projects:

```sh
docker-compose up 
```

or without docker

```sh
python3 main.py
```


## 👏 Acknowledgments

- Thanks to @Minuta18 for docker config

[**Return**](#-quick-links)

---
