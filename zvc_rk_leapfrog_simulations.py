# -*- coding: utf-8 -*-
"""ZVC_RK_leapfrog_simulations.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nLpfMXOghKZ8Bai7umTJ4DIjLBKcQt3o

In the context of the circular restricted three-body problem (CR3BP), the kinetic energy of the test particle (the third body) is determined based on the principle of conservation of mechanical energy. The mechanical energy in a conservative system is the sum of the kinetic and potential energies, and it remains constant if there are no external forces acting on the system. This constant sum is referred to as the Jacobi constant, \( E \), in the CR3BP.

The kinetic energy $ K $ of the test particle is computed using the difference between the Jacobi constant $ E $ and the potential energy $ U $ at the particle's position:

$$ K = E - U $$

The potential energy $ U $ is given by the effective potential function $ V(x, y, \mu) $, which includes both the gravitational potential energy due to the two primary bodies and the centrifugal potential energy due to the rotation of the reference frame:

$$U(x, y) = V(x, y, \mu) =  -(\frac{1}{2}(x^2 + y^2) + \frac{1 - \mu}{r_1} + \frac{\mu}{r_2})$$

where $ r_1 $ and $ r_2 $ are the distances from the test particle to the two primary bodies, and $ \mu $ is the mass ratio of the two primaries.

Given a position \( (x, y) \), the potential energy \( U \) at that position is calculated using the effective potential function \( V \). Then, the kinetic energy \( K \) is obtained by subtracting this potential energy from the Jacobi constant:

$$ K = E - V(x, y, \mu) $$

If the resulting kinetic energy \( K \) is positive, it means that the test particle has enough energy to move at that position. The magnitude of the velocity \( v \) that the particle can have while maintaining the energy level \( E \) is derived from the kinetic energy:

$$ v = \sqrt{2K} $$

This is because the kinetic energy in terms of velocity is given by $$K = \frac{1}{2}mv^2 $$ for a particle of mass \( m \). Since the mass of the test particle does not appear in the equations of motion for the CR3BP (it is assumed to be infinitesimally small), we can consider \( m = 1 \) to the assumption in the paper, and the velocity magnitude can be directly calculated from \( 2K \).

In conclusion, the kinetic energy is computed as the difference between the constant total energy \( E \) and the potential energy \( U \) at a specific position in the rotating frame of reference. This calculation allows determining the speed at which the test particle can move while staying on an energy contour defined by the Jacobi constant.

The direction of the velocities for the test particle in the CR3BP is determined by the condition that the motion must be tangent to the zero-velocity curve (ZVC) at a given energy level. The ZVC is a contour line of the effective potential \( V(x, y, \mu) \) that corresponds to the constant energy value \( E \). The velocity vector at any point on this curve must be perpendicular to the gradient of \( V \) at that point because the gradient points in the direction of the steepest increase in potential, and hence, the kinetic energy would not be conserved if the particle were to move in that direction.

To calculate the direction of the velocity, we first compute the gradient of the effective potential function:

$$ \nabla V(x, y) = \left( \frac{\partial V}{\partial x}, \frac{\partial V}{\partial y} \right) $$

This gradient vector at the position $ (x, y)$ is given by the partial derivatives of $ V $ with respect to $ x $ and $ y $. The velocity vector $ \vec{v} $ must satisfy the condition $\vec{v} \cdot \nabla V = 0 $ to ensure that the particle stays on the same energy contour.

In the code, the gradient is calculated and then rotated by 90 degrees to obtain a vector that is tangent to the ZVC. This is achieved by swapping the gradient components and changing the sign of one of them:

$$\text{gradient} = \left( \frac{\partial V}{\partial x}, \frac{\partial V}{\partial y} \right) $$
$$ \text{velocity\_vector} = \left( -\text{gradient}[1], \text{gradient}[0] \right) $$

By normalizing this velocity vector, we obtain a unit vector that points in the direction of the allowed velocity:
"""

import numpy as np
import matplotlib.pyplot as plt

# Redefine the constants after state reset
mu = 1/11  # Example value for mu, the mass ratio
E = [-1.82,-1.73,-1.70,-1.50]  # Example value for the energy level (C in the text)

# Redefine the effective potential function V
def V(x, y, mu):
    r1 = np.sqrt((x + mu)**2 + y**2)
    r2 = np.sqrt((x - 1 + mu)**2 + y**2)
    return -(0.5*(x**2 + y**2) + (1 - mu)/r1 + mu/r2)

# Redefine the zero velocity curve (ZVC) and shade the forbidden region
def plot_ZVC(E, mu):
    # Create a grid of points
    x = np.linspace(-2, 2, 400)
    y = np.linspace(-2, 2, 400)
    X, Y = np.meshgrid(x, y)
    # Calculate the effective potential on the grid
    Z = V(X, Y, mu)
    levels = np.linspace(Z.min(), Z.max(), 10000)
    forbidden_levels = levels[levels >= E]
    # Plot the effective potential and shade the forbidden regions
    plt.contourf(X, Y, Z, levels=forbidden_levels, colors='grey', alpha=0.5)
    # Return the contour lines at the energy level E
    plt.contour(X, Y, Z, levels=[E], colors='black')

# Plot the ZVC and shade the forbidden regions
for energy_level in E:
  plot_ZVC(energy_level, mu)
  plt.xlabel('x')
  plt.ylabel('y')
  plt.title(f'Zero Velocity Curve (ZVC) for E = {energy_level}')
  plt.grid(True)
  plt.show()

"""# For now, let's take the energy level of -1.82 and determine what are the allowed initial conditions.

First we determine the allowed positions and then we determine the allowed velocities by taking perpendicular velocities to the gradient of the potential function at these positions


"""

E = -1.82

"""With negative values of V and E, we should be taking V greater than E to be the allowed region, but if i do so the forbidden regions will not be the same as the paper (we would get the white region to be the forbidden region)"""

print(V(0.5,0,mu))
print(E)
print('Note that V is less than E but the magnitude of V is not less than E, so this looks a bit suspicious')

"""# Let's automatically find the allowed initial conditions using the above method, if we enumerate all positions in the grid [0,0.5] x [0,0.5] and taking grid size 100"""

def grad_V(x, y, mu):
    r1 = np.sqrt((x + mu)**2 + y**2)
    r2 = np.sqrt((x - 1 + mu)**2 + y**2)
    dVdx = (x - ((1 - mu) * (x + mu) / r1**3) - (mu * (x - 1 + mu) / r2**3))
    dVdy = (y - (1 - mu) * y / r1**3 - mu * y / r2**3)
    return np.array([dVdx, dVdy])

def initial_velocities(x, y, E, mu):
    Vxy = V(x, y, mu)
    kinetic_energy = E - Vxy
    if kinetic_energy <= 0:
        return np.array([0, 0]), False  # No real velocities possible, point is in forbidden region
    v_mag = np.sqrt(2 * kinetic_energy)
    gradV = grad_V(x, y, mu)
    # Velocity is perpendicular to gradient of V
    vel_dir = np.array([-gradV[1], gradV[0]])
    vel_dir /= np.linalg.norm(vel_dir)
    return v_mag * vel_dir, True

grid_size = 100  # Size of the grid for initial positions
x_vals = np.linspace(0, 0.5, grid_size)
y_vals = np.linspace(0, 0.5, grid_size)

# Storage for initial conditions that are not in forbidden regions
initial_conditions = []

for x in x_vals:
    for y in y_vals:
        velocity, is_allowed = initial_velocities(x, y, E, mu)
        if is_allowed:
            initial_conditions.append((x, y, velocity[0], velocity[1]))

print(initial_velocities(0.5,0,E,mu))

"""# Let's print the first 50 initial conditions found"""

for i in range(50):
  print(initial_conditions[i])

"""# We use 3 integration methods: RK45, leapfrog and velocity verlet inetegration

## Velocity Verlet Integration Method

The Velocity Verlet integration method is an algorithm used for numerically solving differential equations of motion, especially in systems where energy conservation is critical. It is a second-order method that provides a good balance between accuracy and computational efficiency.

### Algorithm Steps

1. **Initialization**: Start with initial conditions for positions (`x`, `y`) and velocities (`vx`, `vy`). Calculate the initial accelerations (`ax`, `ay`) using the equations of motion.

2. **Loop Over Time Steps**:
   - **Position Update**: Calculate the new positions (`x`, `y`) using the current velocities and accelerations.
     ```
     x += vx * dt + 0.5 * ax * dt^2
     y += vy * dt + 0.5 * ay * dt^2
     ```
   - **Intermediate Velocity Update**: Calculate the new accelerations (`new_ax`, `new_ay`) at the updated positions.
   - **Velocity Update**: Update the velocities (`vx`, `vy`) using the average of the current and new accelerations.
     ```
     vx += 0.5 * (ax + new_ax) * dt
     vy += 0.5 * (ay + new_ay) * dt
     ```
   - **Acceleration Update**: Set the current accelerations to the new accelerations for the next iteration.
   
3. **Repeat**: Continue the loop over the specified time span, storing the state (positions and velocities) at each time step.

### Characteristics

- The Velocity Verlet method is **symplectic**, making it particularly suited for long-term simulations of conservative systems.
- It offers a **second-order accuracy** in time, ensuring precise results with reasonable computational effort.
- This method calculates positions and velocities that are **synchronously updated**, providing coherent snapshots of the system's state.
"""

# Velocity Verlet integration method
def velocity_verlet_integrator(eom, state0, t_span, dt, mu):
    times = np.arange(t_span[0], t_span[1], dt)
    states = np.zeros((len(times), 4))
    states[0] = state0

    x, y, vx, vy = state0
    ax, ay = eom(0, state0, mu)[2:]

    for i in range(1, len(times)):
        x += vx * dt + 0.5 * ax * dt**2
        y += vy * dt + 0.5 * ay * dt**2

        new_ax, new_ay = eom(times[i], [x, y, vx, vy], mu)[2:]
        vx += 0.5 * (ax + new_ax) * dt
        vy += 0.5 * (ay + new_ay) * dt

        states[i] = [x, y, vx, vy]
        ax, ay = new_ax, new_ay

    return times, states

"""## Leapfrog Integration Method

The Leapfrog integration method is a numerical technique used for integrating differential equations, especially in the context of Hamiltonian mechanics. This method is symplectic, making it ideal for simulations of conservative systems where energy conservation is essential.

### Algorithm Steps

1. **Initialization**: Begin with the initial conditions for the system's positions (`x`, `y`) and velocities (`vx`, `vy`). Compute the initial accelerations (`ax`, `ay`) from the equations of motion.

2. **Loop Over Time Steps**:
   - **Half-step Velocity Update**: First, update the velocities by half a time step using the initial accelerations.
     ```
     vx -= 0.5 * ax * dt
     vy -= 0.5 * ay * dt
     ```
   - **Position Update**: Move the system's positions (`x`, `y`) forward by a full time step using the updated velocities.
     ```
     x += vx * dt
     y += vy * dt
     ```
   - **Full-step Velocity Update**: Calculate the new accelerations at the updated positions and then complete the velocity update by moving it the remaining half time step.
     ```
     vx += ax * dt
     vy += ay * dt
     ```
   - **Save State**: Record the system's state, including the updated positions and velocities, for each time step.

3. **Repeat**: Continue iterating over the specified time span, storing the state at each step.

### Characteristics

- **Symplectic Nature**: The Leapfrog method preserves the symplectic structure of Hamiltonian systems, making it particularly useful for long-term integrations where energy conservation is crucial.
- **Second-order Accuracy**: Despite its simplicity, the Leapfrog method offers second-order accuracy, providing a good compromise between computational efficiency and precision.
- **Staggered Updates**: The method updates velocities and positions in a staggered fashion, which contributes to its stability and accuracy for certain types of problems.


"""

def leapfrog_integrator(eom, state0, t_span, dt, mu):
    """Leapfrog integration for the equations of motion of the CR3BP."""
    # Initialize time and state arrays
    times = np.arange(t_span[0], t_span[1] + dt, dt)
    states = np.zeros((len(times), len(state0)))

    # Initial conditions
    states[0] = state0
    x, y, vx, vy = state0

    # Half-step velocity initialization
    ax, ay = eom(0, [x, y, vx, vy], mu)[2:]
    vx -= 0.5 * ax * dt
    vy -= 0.5 * ay * dt

    # Leapfrog integration loop
    for i, t in enumerate(times[:-1]):
        # Update positions
        x += vx * dt
        y += vy * dt

        # Full-step velocity update
        ax, ay = eom(t, [x, y, vx, vy], mu)[2:]
        vx += ax * dt
        vy += ay * dt

        # Save the state
        states[i + 1] = [x, y, vx, vy]

    return times, states

from scipy.integrate import solve_ivp

# Define the function that performs the numerical integration using Runge-Kutta and Leapfrog methods
# and plots the results.
def equations_of_motion(t, state, mu):
    x, y, vx, vy = state
    ax = 2*vy - grad_V(x, y, mu)[0]
    ay = -2*vx - grad_V(x, y, mu)[1]
    return [vx, vy, ax, ay]




def numerical_integration_plot(initial_state, mu, t_span, dt):
    # Runge-Kutta method using solve_ivp (RK45)
    sol_rk = solve_ivp(equations_of_motion, t_span, initial_state, args=(mu,), t_eval=np.linspace(t_span[0], t_span[1], int((t_span[1] - t_span[0]) / dt)))

    # Leapfrog Integration
    times_leapfrog, states_leapfrog = leapfrog_integrator(equations_of_motion, initial_state, t_span, dt, mu)

    #velocity verlet inetgration (also a symplectic integrator that compares with leapfrog)
    times_vv, states_vv= velocity_verlet_integrator(equations_of_motion, initial_state, t_span, dt, mu)

    # Plotting
    fig, axes = plt.subplots(1, 3, figsize=(14, 6))

    # Runge-Kutta plot
    axes[0].plot(sol_rk.y[0], sol_rk.y[1], label='Runge-Kutta')
    axes[0].scatter([-mu], [0], color='blue', zorder=5, label='Primary 1')  # Primary 1
    axes[0].scatter([1-mu], [0], color='orange', zorder=5, label='Primary 2')  # Primary 2
    axes[0].scatter([initial_state[0]], [initial_state[1]], color='red', zorder=5, label='Body')  # Initial position
    axes[0].set_title('Runge-Kutta Integration')
    axes[0].set_xlabel('x')
    axes[0].set_ylabel('y')
    axes[0].grid(True)
    axes[0].legend()

    # Leapfrog plot
    axes[1].plot(states_leapfrog[:, 0], states_leapfrog[:, 1], label='Leapfrog')
    axes[1].scatter([-mu], [0], color='blue', zorder=5, label='Primary 1')  # Primary 1
    axes[1].scatter([1-mu], [0], color='orange', zorder=5, label='Primary 2')  # Primary 2
    axes[1].scatter([initial_state[0]], [initial_state[1]], color='red', zorder=5, label ='Body')  # Initial position
    axes[1].set_title('Leapfrog Integration')
    axes[1].set_xlabel('x')
    axes[1].set_ylabel('y')
    axes[1].grid(True)
    axes[1].legend()

    #velocity verlet plot
    axes[2].plot(states_vv[:, 0], states_vv[:, 1], label='Velocity Verlet')
    axes[2].scatter([-mu], [0], color='blue', zorder=5, label='Primary 1')  # Primary 1
    axes[2].scatter([1-mu], [0], color='orange', zorder=5, label='Primary 2')  # Primary 2
    axes[2].scatter([initial_state[0]], [initial_state[1]], color='red', zorder=5, label ='Body')  # Initial position
    axes[2].set_title('Velocity Verlet Integration')
    axes[2].set_xlabel('x')
    axes[2].set_ylabel('y')
    axes[2].grid(True)
    axes[2].legend()

    plt.tight_layout()
    plt.show()

# Use the first initial condition for demonstration
numerical_integration_plot((0.5,0,-0.0, -0.36244658), mu, (0, 10), 0.01)

"""# For all the initial conditions in the grid, we now find the orbits of the third body using all three numerical methods"""

#let's calculate the trajectory for 10 initial conditions
for initial_condition in initial_conditions:
  # Use the first initial condition for demonstration
  numerical_integration_plot(initial_condition, mu, (0, 10), 0.01)