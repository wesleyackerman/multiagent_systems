def rotate(x_angles, t_angles, turning_rate, tau=.1):
    # Turning rate: turning rate * tau (timestep) - can we scale this to be from 0 to 1?
    tau_turning_rate = tau * turning_rate
    
    for i in range(x_angles.shape[0]):
        
        # angle from direction to target direction
        angle = np.arccos(np.dot(x_angles[i], t_angles[i]) / 
                          (np.linalg.norm(x_angles[i]) * np.linalg.norm(t_angles[i])))
        if angle < tau_turning_rate:
            x_angles[i] = t_angles[i]
        elif angle >= tau_turning_rate:
            # Turn in direction of target_angle
            convex_rate = tau_turning_rate/abs(angle) # always between 0 and 1
            # Take a weighted average
            x_angles[i] = x_angles[i] * (1-convex_rate) + target_angles[i] * (convex_rate)
    return x_angles

    