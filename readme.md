# Learning Robust Control Barrier Functions for Guaranteed Safety of Car-Like Robots

This is the code base for the CORL2022 submission "Learning Robust Control Barrier Functions for Guaranteed Safety of Car-Like Robots". It contains simulation code in Python and a ROS package for implementation, both incl. the vectorized computation of the Input Constrained Control Barrier Functions (ICCBFs).

## Simulation

Samples from the Euclidean Distance Function (EDF) of a road are loaded and used to train a SVM regression model. This model is used to compose a robust safety filter. The learned filter is then used in closed-loop simulation. For the dynamics of the car-like robot we use the modified kinematic bicycle model with constant velocity. The nominal steering angle is supervised by the learned safety filter.
- 'main' runs the main simulation and plots the results.
- 'control' contains the dynamics for the solver of the initial value problem, the filter and the nominal control.
- 'car' contains the Car class with various parameters such as car length and velocity (of the front wheels). 

## ROS package 

This is the packge we used for experimental validation on the 1:10 RC car (see 'https://www.youtube.com/watch?v=U8eZPTDpHEo'). All required parameters to start node 'cbf_safety_filter' are set via config/cbf_params.yaml. The velocity command (linear speed in x and angular speed in z) is published as a Twist message, with constant velocity in x and angular velocity being computed by the filter. The trained model using scikit-learn ('https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVR.html') incl. scaler are loaded via the launch file (adjust path to your scaler/model). Importantly, the scaler needs to be the standard scaler as it affects the computations of the steering safety filter and hence steering command.

The node subscribes to 
```
POSE_TOPIC_NAME = '/amcl_pose'
```
for position estimation and publishes the velocity command (via Twist) and filter data (see msg/CbfFilterData for message details) on
```
CMD_VEL_PUB_TOPIC = '/cmd_vel'
FILTER_TOPIC_NAME = '/cbf/filterData'
```
These values can be adjusted in scripts/cbf_node.py. Note that the throttle command as part of the Twist message is from [-1,1], where values less than zero mean driving backwards and 1 demands maximum RPM (also a parameter). THus, conversion from desired velocity to throttle value is necessary.

Particularly, we use the linear function 
```math
throttle_cmd = a.v + b
```
The parameter "a" refers to 'vel2throttle_grad' and "b" to 'vel2throttle_off', both set in config/cbf_params.yaml. They need to be adjusted to the particular car.

## Vectorized computation 
The efficient implementation using vectorized calculations is part of both the simulation and the ROS package. For the simulation, it is part of the function 
```
def getBarrier(xy, svm_params, alpha, vectorized=True, loop=False, time_it=False, xdot=[]):
    ...
```
with which we also compare computing time to a loop implementation. In the ROS package, the vectorized computation happens in 
```
def getBarrierAndPartials(self):
    ...
```
