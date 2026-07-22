# Chromocular: QAOA Asymmetric Energy Optimization for Marine Autonomous Underwater Vehicles (AUVs)

## Computational Oceanography & Quantum Logistics Framework

---

## Mission Engineering & Abstract

Autonomous Underwater Vehicles (AUVs) are critical components in modern oceanic monitoring frameworks, used for high-stakes missions such as underwater pipeline inspections, bathymetric ecosystem mapping, and green energy transitions (seafloor mapping for geothermal and hydrogen storage setups). However, AUVs operate under severe constraints: strictly limited battery capacities coupled with highly volatile underwater environments.

Unlike terrestrial drone routing, marine routing is inherently **asymmetric** due to fluid dynamic forces. Traveling *with* an ocean current vector acts as a kinetic accelerator, conserving battery life, whereas navigating *against* or perpendicular to a current vector introduces immense hydro-mechanical resistance, accelerating power depletion.

This framework models this environmental challenge as an **Asymmetric Traveling Salesperson Problem (ATSP)**. It ingests spatial target coordinates and active ocean current vector layers ($u, v$ components), maps the physics into a mathematical **Quadratic Unconstrained Binary Optimization (QUBO)** problem, and leverages variational quantum compilation frameworks via Qiskit primitives to calculate the most energy-efficient transit route.

---

## System Architecture

```text
                   FLUID LAYER MAP
        [ Ingest Ocean Current Vectors (u, v) ]
                        │
                        ▼
             COST MODEL MATRIX (ATSP)
 [ Calculate Asymmetric Node-to-Node Friction ]
                        │
                        ▼
             MATHEMATICAL QUBO MODEL
[ Formulate Binary Decision Variable Matrix System ]
                        │
                        ▼
          QUANTUM COMPUTATION ENGINE
[ Exact Diagonalization / Variational Ansatz Execution ]
                        │
                        ▼
          INTERACTIVE MAP DASHBOARD
     [ Render Optimal Dynamic Flow Routings ]
```

---

## Mathematical Formulation

### 1. The Asymmetric Fluid Cost Function

The directional travel cost between two nodes $i$ and $j$ under a uniform ocean current velocity field

$$
\vec{V}_{\text{current}} = u\hat{i} + v\hat{j}
$$

is formulated as

$$
C_{ij} = \frac{d_{ij}}{v_{\text{cruise}} + \vec{V}_{\text{current}} \cdot \hat{d}_{ij}}
$$

where:

- $d_{ij}$ is the Euclidean distance.
- $\hat{d}_{ij}$ is the unit directional vector pointing from node $i$ to node $j$.

Because the dot product changes sign depending on navigation direction,

$$
C_{ij} \neq C_{ji}
$$

making the routing problem inherently asymmetric.

### 2. The Decision Workspace (QUBO Matrix)

We define a binary decision matrix

$$
x_{i,t} =
\begin{cases}
1 & \text{if Node } i \text{ is visited at sequence slot } t \\
0 & \text{otherwise}
\end{cases}
$$

The objective function minimizing total energy expenditure across $N$ nodes is

$$
\min \sum_{i=1}^{N}\sum_{j=1}^{N}\sum_{t=1}^{N}
C_{ij}\,x_{i,t}\,x_{j,(t+1)\bmod N}
$$

subject to the following constraints.

### Spatial Constraint

The vehicle can occupy only one node at any sequence position:

$$
\sum_{i=1}^{N} x_{i,t}=1
\qquad \forall t
$$

### Temporal Constraint

Each target location must be visited exactly once:

$$
\sum_{t=1}^{N} x_{i,t}=1
\qquad \forall i
$$

---

## Repository Structure

```text
qtsp-qaoa-marine-auv-routing/
│
├── .github/
│   └── workflows/
│       └── deploy.yml
│
├── benchmarks/
│   └── AUV_Routing_Simulation.ipynb
│
├── marine_routing/
│   ├── __init__.py
│   ├── cost_models.py
│   └── quantum_engine.py
│
└── README.md
```

### Directory Overview

| File | Description |
|------|-------------|
| `.github/workflows/deploy.yml` | Automated CI/CD compilation and deployment workflow |
| `benchmarks/AUV_Routing_Simulation.ipynb` | Interactive routing simulation notebook |
| `marine_routing/cost_models.py` | Ocean current directional cost model |
| `marine_routing/quantum_engine.py` | Qiskit-based QUBO formulation and optimization engine |
| `README.md` | Project documentation |

---

## Technical Stack

### Quantum Computing

- Qiskit
- qiskit-algorithms
- qiskit-optimization

### Mathematical Optimization

- NumPy
- DOcplex (IBM CPLEX Modeling Engine)

### Visualization

- Plotly
- Matplotlib

### Automation

- GitHub Actions
- Python
- Jupyter Notebook
- nbconvert

---

## Interactive UI Features

To maintain a clean documentation interface suitable for research presentations and technical reports, the GitHub Pages deployment includes a built-in code visibility system.

### Default Behavior

- Python code cells are hidden by default.
- Documentation, mathematical equations, and interactive Plotly figures remain visible.

### On-Demand Code Inspection

Each notebook code cell is replaced with a **SHOW CODE** button.

Selecting **SHOW CODE**:

- Expands the corresponding source code.
- Preserves the current scroll position.
- Allows the code to be collapsed again without affecting page layout.

---

## Local Development

Clone the repository and install the required dependencies.

```bash
# Clone the repository
git clone https://github.com/xmita-ghx/qtsp-qaoa-marine-auv-routing.git

cd qtsp-qaoa-marine-auv-routing

# Install dependencies
pip install \
    jupyter \
    nbconvert \
    plotly \
    docplex \
    qiskit \
    qiskit-algorithms \
    qiskit-optimization \
    matplotlib

# Launch the notebook
jupyter notebook benchmarks/AUV_Routing_Simulation.ipynb
```

---

## Production Deployment

The repository uses a continuous deployment workflow.

Every verified push or pull request targeting the production branch automatically performs the following steps:

1. Launches an isolated Ubuntu GitHub Actions runner.
2. Installs all required dependencies.
3. Executes the notebook using:

   ```bash
   jupyter nbconvert --execute
   ```

4. Solves the optimization problem using the NumPy-based exact diagonalization engine.
5. Generates responsive interactive JavaScript visualizations.
6. Injects per-cell **SHOW CODE** controls into the generated HTML.
7. Deploys the final static site to GitHub Pages.

---

## Project Summary

Chromocular combines computational oceanography, asymmetric routing theory, and quantum optimization techniques to produce energy-efficient navigation strategies for Autonomous Underwater Vehicles operating in dynamic ocean current environments.

By integrating ocean current vector fields into an Asymmetric Traveling Salesperson Problem (ATSP), translating the optimization into a Quadratic Unconstrained Binary Optimization (QUBO) formulation, and solving it using Qiskit-based quantum optimization workflows, the framework provides an extensible research platform for next-generation marine mission planning.