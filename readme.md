# Learning Robust Control Barrier Functions for Guaranteed Safety of Car-Like Robots

This is the code base for the CORL2022 submission "Learning Robust Control Barrier Functions for Guaranteed Safety of Car-Like Robots". It contains simulation code Python and a ros package for implementation.

## Simulation

Samples from the Euclidean Distance Function (EDF) of a road are loaded and used to train a SVM regression model. The learned robust safety filter is then used in simulation. For the dynamics of the car-like robot we use the modified kinematic bicycle model with constant velocity. The nominal steering angle is supervised by the learned safety filter.
- 'main' runs the main simulation and plots the results.
- 'control' contains the dynamics for the solver of the initial value problem, the filter and the nominal control.
- 'car' contains the Car class and contains various parameters such as length and velocity (of the front wheels). 

## ROS package 

This is the packge we used for experimental validation on the 1:10 RC car. All required parameters to start node 'cbf_safety_filter' are set via config/cbf_params.yaml. The velocity command is published as a Twist message, with constant linear velocity in x and angular velocity being computed by the filter. The trained model incl. scaler are loaded via the launch file. Importantly, the scaler needs to be the standard scaler as it affects the computations of the steering command.

The node subscribes to 
```
POSE_TOPIC_NAME = '/amcl_pose'
```
for position estimation and publishes the velocity command (throttle command linear.x is from [-1,1]! Conversion from velocity is necessary in this case, see below.) and filter data (see msg/CbfFilterData for message details) on
```
CMD_VEL_PUB_TOPIC = '/cmd_vel'
FILTER_TOPIC_NAME = '/cbf/FilterData'
```
These values can be adjusted in scripts/cbf_node.py.

For the mapping from velocity to throttle command [-1,1], we use the linear function 
```math
u_{\rm throttle} = av+b
```
which we estimated in experiments.
The parameter a refers to 'vel2throttle_grad' and b to 'vel2throttle_off', both set in config/cbf_params.yaml.
