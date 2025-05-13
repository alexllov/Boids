# Boids
Boids is a seminal work in the **Artificial Life** (AL) space, demonstrating how simple rules can cause complex group dynamics to emerge.

**Base Boids** contains an implementation of Craig Reynolds' original boids in python using tkinter. This implementation is expanded upon, adding different more complex conditions and rules in the separate projects.

- https://en.m.wikipedia.org/wiki/Boids

- Reynolds, C. W. (1987) 'Flocks, herds and schools: a distributed behaviour model', _Computer Graphics_, 21(4), 25-34

**The movement of Boids is governed by three relations:**

- **Separation** - moving away from any other boids that are too close.

- **Cohesion** - adjusting velocity to match the speed and heading of neighbouring boids.

- **Alignment** - moving towards the centre of all local boids.

<ins>**Variations**</ins>

**Roosting Boids**: a target 'roost' location is added, which boids are encouraged to fly towards. Two sub-variations are presented. In 'Solo', a boid is influenced solely by its own prior experience (local knowledge), while in 'Global', information is shared across the flock, influencing the behaviour of all individuals (global knowledge) 
This variant was inspired by early work in **Particle Swarm Optimisaion** (PSO), which originally drew on the boids project and similar AL simulations.

- Kennedy, J. and Eberhart, R. (1995) Particle swarm optimization. _Proceedings of ICNN'95 - International Conference on Neural Networks_, vol.4, 1942-1948. doi:10.1109/ICNN.1995.488968

**Predators**: boids are divided into 'Predators' and 'Prey' subclasses. Predators attempt to flock with prey, who in turn are set to avoid them. This creates a 'chasing' behaviour as flocks of prey move away from a trailing predator.
