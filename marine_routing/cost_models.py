import numpy as np

def calculate_asymmetric_costs(nodes: dict, current_vector: np.ndarray, base_speed: float = 2.0) -> np.ndarray:
    """
    Calculates the asymmetric energy cost matrix between target coordinates
    based on ocean current vector dynamics.
    
    Parameters:
    -----------
    nodes : dict
        Dictionary of node IDs mapped to 2D numpy arrays [x, y] or [lat, lon].
    current_vector : np.ndarray
        A 2D vector [u, v] representing ocean current velocity.
    base_speed : float
        The default speed capability of the AUV in stagnant water.
        
    Returns:
    --------
    np.ndarray
        An NxN matrix containing asymmetric energy cost weights.
    """
    num_nodes = len(nodes)
    cost_matrix = np.zeros((num_nodes, num_nodes))
    
    for i in range(num_nodes):
        for j in range(num_nodes):
            if i == j:
                cost_matrix[i, j] = 0
                continue
            
            # 1. Determine spatial trajectory vector
            displacement = nodes[j] - nodes[i]
            distance = np.linalg.norm(displacement)
            direction = displacement / distance
            
            # 2. Project current vectors onto the flight path (Dot Product)
            # Positive value means current tailwind assists; negative means headwind resists
            current_influence = np.dot(current_vector, direction)
            effective_speed = base_speed + current_influence
            
            # 3. Safety threshold: prevent infinite loops or division by zero if current is overpowering
            effective_speed = max(effective_speed, 0.5)
            
            # 4. Energy cost is directly proportional to traveling duration
            travel_time = distance / effective_speed
            
            # Scaled value optimization for QUBO matrices
            cost_matrix[i, j] = round(travel_time * 10, 2)
            
    return cost_matrix