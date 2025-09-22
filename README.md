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

1. **Clone the repository**

   ```cmd
   git clone <repository-url>
   cd EventManager-PY
   ```

2. **Install dependencies**
   ```cmd
   script.bat install-dev
   ```
   This installs both production and development dependencies.

### Alternative Installation

```bash
# Linux/macOS
make install          # production only
make install-dev      # production + dev

# Windows
script.bat install    # production only
script.bat install-dev # production + dev
```

## Overview

Desktop application for event and ticket management, built in **Python** with **PyPySimpleGUI** for the GUI and **SQLite** for the database.
