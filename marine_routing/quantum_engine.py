import numpy as np
from docplex.mp.model import Model
from qiskit_optimization.translators import from_docplex_mp
from qiskit_algorithms import QAOA
from qiskit_algorithms.optimizers import COBYLA
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit.primitives import Sampler

def build_tsp_qubo(energy_matrix: np.ndarray) -> QuantumCircuit:
    """
    Constructs a mathematical QUBO optimization problem from an asymmetric matrix
    and translates it natively into a Qiskit compatible formulation.
    """
    num_nodes = len(energy_matrix)
    mdl = Model(name='Ocean_Routing_Optimization')
    
    # x[i, t] = 1 if node i is visited at step t
    x = mdl.binary_var_matrix(num_nodes, num_nodes, name='x')
    
    # Objective: Minimize total energy expenditure along dynamic flow vectors
    total_energy = mdl.sum(
        energy_matrix[i, j] * x[i, t] * x[j, (t + 1) % num_nodes]
        for i in range(num_nodes) 
        for j in range(num_nodes) 
        for t in range(num_nodes) if i != j
    )
    mdl.minimize(total_energy)
    
    # Spatial Constraint: One coordinate assignment per time allocation
    for t in range(num_nodes):
        mdl.add_constraint(mdl.sum(x[i, t] for i in range(num_nodes)) == 1)
        
    # Temporal Constraint: Each target visited exactly once across circuit
    for i in range(num_nodes):
        mdl.add_constraint(mdl.sum(x[i, t] for t in range(num_nodes)) == 1)
        
    # Map raw Docplex model arrays out to Qiskit Optimization primitives
    qubo = from_docplex_mp(mdl)
    return qubo

def solve_with_qaoa(qubo, max_iterations: int = 150) -> list:
    """
    Executes the Quantum Approximate Optimization Algorithm optimization loop
    to resolve structural path ordering.
    """
    sampler = Sampler()
    optimizer = COBYLA(maxiter=max_iterations)
    
    # Initialize QAOA framework with 3 variational layers (reps=3)
    qaoa = QAOA(sampler=sampler, optimizer=optimizer, reps=3)
    
    # Solve the Hamiltonian via Minimum Eigenvalue Optimization wrappers
    optimizer_algorithm = MinimumEigenOptimizer(qaoa)
    result = optimizer_algorithm.solve(qubo)
    
    # Reshape flattened output vector back to structural matrices
    num_nodes = int(np.sqrt(len(result.x)))
    route_matrix = result.x.reshape((num_nodes, num_nodes))
    
    # Trace high activation indices to construct sequence path array
    route_order = [np.argmax(route_matrix[:, t]) for t in range(num_nodes)]
    route_order.append(route_order[0]) # Loop circuit route back to launch base
    
    return route_order

if __name__ == "__main__":
    # Internal module debugging block execution
    from cost_models import calculate_asymmetric_costs
    
    test_nodes = {0: np.array([0,0]), 1: np.array([2,3]), 2: np.array([5,1]), 3: np.array([6,5])}
    test_current = np.array([0.8, 0.5])
    
    print("Calculating environmental cost layers...")
    costs = calculate_asymmetric_costs(test_nodes, test_current)
    
    print("Compiling Ising Hamiltonian QUBO matrices...")
    qubo_problem = build_tsp_qubo(costs)
    
    print("Launching QAOA Quantum Simulation loop...")
    optimal_path = solve_with_qaoa(qubo_problem)
    
    print(f"Calculated Success Route Configuration Sequence: {optimal_path}")