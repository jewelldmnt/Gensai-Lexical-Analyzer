# Gensai Lexical Analyzer

Welcome to the Gensai Lexical Analyzer project! This repository is open to contributions, and we encourage developers to actively participate in making this project better. Below is a guide on how you can contribute to this project.

## Contribution Guide

### Cloning the Repository

1. Create a new folder where you can store the project files and refer to it as the Project Folder.

2. Open the Terminal (or Command Prompt) and change the current directory to the Project Folder.
    ```bash
    cd <PATH TO PROJECT FOLDER>
    ```

3. Clone the repository using the following command:
    ```bash
    git clone https://github.com/jewelldmnt/Gensai-Lexical-Analyzer.git
    ```

4. Open the folder in your preferred Integrated Development Environment (IDE).

### Pull the Changes First

1. Switch to the main branch:
    ```bash
    git checkout -b main
    ```

2. Pull the latest changes from the main branch:
    ```bash
    git pull origin main
    ```

### Create a Branch for Contributing

1. Create a new branch for your contribution:
    ```bash
    git checkout -b <new-branch-name>
    ```

#### Branch Name Guide
- `<new-branch-name>` format is `[dev-name]-[branch-type]-[task-desc]`
- `[dev-name]`: Your nickname
- `[branch-type]`: Type of task (feat, fix, refactor)
  - `feat`: New feature
  - `fix`: Bug fix
  - `refactor`: Code change that doesn't fix a bug or add a feature
- `[task-desc]`: Brief description of your task (2-3 words, connected by underscores '_')

Example of a branch name: `jewell-feat-variable_identification`

2. Check if you are on your working branch:
    ```bash
    git branch
    ```

### Pushing Changes to the Repository

1. Add changes to the staging area:
    - To add all changes:
      ```bash
      git add -A
      ```
    - To add specific files:
      ```bash
      git add <filename>
      ```

2. Commit your changes with a descriptive message:
    ```bash
    git commit -m "{Describe your proposed changes}"
    ```

3. Push your changes to your branch:
    ```bash
    git push origin <your-branch-name>
    ```

### Open Pull Request

1. Open a new Pull Request on the [GitHub repository](https://github.com/jewelldmnt/Gensai-Lexical-Analyzer) under the Pull Request tab.

2. Ensure the Pull Request flow is as follows: base: main <- compare: yourname-branchtype-taskdesc.

3. Write a detailed description of your Pull Request, including:
   - Changes includes
     - Add: What files are added and the reason.
     - Modify: What files are modified and the reason.
     - Remove: What files are deleted and the reason.
   - Packages installed (if any): Name of the library/package and why it's added.
   - Questions/Issues: Free format and any order.
   - Tasks to do (In case it is still a work in progress upon PR): Free format and any order.

4. Notify the team about your new Pull Request.

Happy contributing! 🚀
