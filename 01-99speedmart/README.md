# Optimizing Logistic Route: 99 Speedmart

This project aims to optimize delivery routes for a fleet of vehicles, minimizing costs while meeting all stores demands and constraints.

## Table of Contents
- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Overview

This repository contains the code and documentation for optimizing the logistics routes of 99 Speedmart, a popular chain of convenience stores. The project aims to improve delivery efficiency, reduce costs, and enhance overall supply chain performance.

## Problem Statement

As a logistics manager for a local conveniece stores chain company, you need to optimize the routing of a fleet of vehicles to efficiently deliver goods to various customer locations. The goal is to minimize delivery costs while ensuring all delivery locations are visited and all demands are met.

### Constraints

#### Hard Constraints:
- Each delivery location must be visited exactly once.
- The total demand for each vehicle route must not exceed its maximum capacity.

#### Soft Constraints:
- Minimize the cost required to meet all demands.

### Assumptions:
- Vehicles start and end their routes at the same depot location.
- Each vehicle only travels one round trip (depart from depot and back to the depot).
- There is no limit on the number of vehicles.
- Travel times between any two locations are the same in both directions.
- Deliveries can be made at any time; there are no time windows for deliveries.