# Introduction

This is a Dockerized project designed to analyze customer data efficiently. The project provides tools to:

- **Generate Data**: Create sample datasets for analysis.
- **Analyze Shoppers' Behavior**: Derive insights from customer shopping patterns and behaviors.

## Setting Up the Environment

### Create a `.env` File

The project requires a `.env` file for configuration. You can create a sample `.env` file with the following command:

```bash
cp .env.example .env
```

### Start the Project

To start the project, build the Docker image using the following command:

```bash
sudo docker-compose up --build -d
```