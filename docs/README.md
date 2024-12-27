# Script Sharing Platform via Zowe CLI

## Overview
The **Script Sharing Platform** is a project designed to allow mainframe users to easily share and upload scripts using **Zowe CLI**. It includes an automatic validation process to check file types and script indentation before uploading to the mainframe. This ensures that only valid scripts are uploaded, preventing issues like uploading incorrect file types (e.g., images or Word documents).

## Features
- **Automatic Script Validation**: Validates file types and ensures correct indentation for uploaded scripts.
- **Zowe CLI Integration**: Directly integrates with Zowe CLI for seamless interaction with the mainframe environment.
- **Local Script Testing**: Tests scripts locally before uploading them to the mainframe.
- **File Upload**: Uploads scripts to the mainframe using Zowe CLI commands.

## Getting Started

### Prerequisites
1. **Install Zowe CLI**:
    ```bash
    npm install -g @zowe/cli
    ```
2. **Configure Zowe CLI**:
    ```bash
    zowe profiles create zosmf-profile --host <hostname> --user <username> --password <password>
    ```

### Using the Platform
1. **Upload a Script**:
    ```bash
    zowe zos-files upload file "path/to/your/script.sh" "MDSDS"
    ```
2. **Validate Script Locally**:
    ```bash
    python src/validation.py "path/to/your/script.sh"
    ```
3. **Example Command to View Logs**:
    ```bash
    zowe zosmf view logs
    ```

### Troubleshooting
- **Invalid File Type**: The platform rejects image or document types (Word, PowerPoint).
- **Indentation Errors**: Ensure the script meets required indentation standards.
- **Zowe CLI Issues**: Double-check the configuration:
    ```bash
    zowe profiles update zosmf-profile --host <hostname> --user <username> --password <password>
    ```

## Contact
For questions or support, reach out at rafaella.jardim@student.kdg.be

