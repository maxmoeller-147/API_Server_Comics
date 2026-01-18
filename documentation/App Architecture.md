# DEV1004 - AS01: Containerization of an Existing Application

## Table of Contents

1. [Project Summary](#project-summary)
2. [Application Architecture](#section-1-application-architecture)
3. [Container Internal Design](#section-2-container-internal-design)
4. [Security & Secrets Management](#section-3-security--secrets-management)
5. [CI/CD Pipeline](#section-4-cicd-pipeline)

## Project Summary
The Comics API Server is a containerised web application that provides a RESTful API that allows users to manage the operations of a comic store, such as comics, customers, orders, artists, writers, and publishers. The project was developed using Python and Flask, with PostgreSQL as the database engine, and is containerised and executed using Docker. In addition to the core application, a continuous integration pipeline was implemented using GitHub Actions to automate building, testing, and validation.

This documentation explains the architecture of the application through diagrams and descriptions that illustrate how each component of the system interacts.

More Info on:  

- [Technical Readme](./README.md)
- [Leave your Feedback!](./documentation/Feedback.md)

## Application Architecture 