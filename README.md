# Event Manager System

Repository for the project of the course INE5608 - Systems Analysis and Design.

## Installation

### Linux/macOS

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd EventManager-PY
   ```

2. **Install dependencies**
   ```bash
   make install-dev
   ```
   This installs both production and development dependencies (including Ruff).

### Windows

⚠️ **Important:** Please install the version of Python from the official Python website and not from the Microsoft Store, to avoid compatibility issues.

1. **Clone the repository**

   ```cmd
   git clone <repository-url>
   cd EventManager-PY
   ```

2. **Install dependencies**
   ```cmd
   .\build.bat install-dev
   ```
   This installs both production and development dependencies.

### Alternative Installation

```bash
# Linux/macOS
make install          # production only
make install-dev      # production + dev

# Windows
.\build.bat install          # production only
.\build.bat install-dev      # production + dev
```

## Overview

Desktop application for event and ticket management, built in **Python** with **FreeSimpleGUI** for the GUI and **SQLite** for the database.
