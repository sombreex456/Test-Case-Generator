# Test Case Generator

A tool that uses the Claude API to generate structured test cases from software requirements.

## Features

* Generates positive, negative, boundary and edge-case test cases
* Generates security test cases where relevant
* Includes test type, priority, preconditions, steps and expected results
* Export test cases to Excel
* Send test cases by email

## Technologies

* Python
* Claude API
* Streamlit
* Pydantic
* Pandas
* OpenPyXL

## How It Works

The user enters a software requirement, and the Claude API generates structured test cases based on it. The generated test cases can then be viewed in the application, exported to Excel or sent by email.

## Example

**Requirement:**

> Users should be able to reset their password using their registered email address.

The tool generates relevant test cases covering positive, negative, boundary, edge-case and security scenarios.
