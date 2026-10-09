# SOCIAL NETWORK COMMUNITY DETECTION
**Spectral Clustering and Eigenvalue Analysis**

## Overview
This mini-project demonstrates the application of Linear Algebra (specifically eigenvalues, eigenvectors, and the graph Laplacian) to identify communities within a social network. The primary dataset is Zachary's Karate Club.

## Objectives
- Represent a real-world social network as an Adjacency Matrix and Degree Matrix.
- Compute the Graph Laplacian ($L = D - A$).
- Perform eigenvalue and eigenvector analysis to evaluate graph connectivity (Algebraic Connectivity, Fiedler Vector).
- Apply Spectral Clustering to partition the network into communities.
- Evaluate the clustering using modularity and visual representations.

## Requirements
See `requirements.txt`. Built with Python 3.11+, Streamlit, NetworkX, NumPy, SciPy, and scikit-learn.

## Setup and Running (Windows)
1. Ensure Python 3.11+ is installed.
2. Open a command prompt or PowerShell in this directory.
3. (Optional but recommended) Create a virtual environment:
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```
4. Install dependencies:
   ```cmd
   pip install -r requirements.txt
   ```
5. Run the Streamlit application:
   ```cmd
   run_app.bat
   ```
   Or manually:
   ```cmd
   python -m streamlit run app.py
   ```

## Running Tests
To run the automated test suite, ensure pytest is installed, then run:
```cmd
python -m pytest tests/ -q
```

## Features
- **Interactive Dashboard**: View dataset statistics and matrices.
- **Spectral Clustering**: Adjust community counts (k=2, 3, 4).
- **Mathematical Validation**: Inspect adjacency, degree, and Laplacian matrices.
- **Export Data**: Download CSVs of matrices and community assignments.
