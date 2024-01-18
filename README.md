# tree_propagation
194.076 Modeling and Simulation


Growth Function:
https://en.wikipedia.org/wiki/Gompertz_function

haversine distance formula:

d = 2R × sin⁻¹(√[sin²((θ₂ - θ₁)/2) + cosθ₁ × cosθ₂ × sin²((φ₂ - φ₁)/2)]).

where:

    (θ₁, φ₁) and (θ₂, φ₂) – Each point's coordinates;
    R – Earth's radius; and
    d – Great circle or 'as the crow flies' distance between the points.


In this example, wind_direction is a unit vector, meaning its components directly represent the x and y components of the wind direction. You can choose any valid unit vector for your simulation. For example:

    (1, 0) represents a wind blowing directly to the right.
    (0, 1) represents a wind blowing directly upwards.
    (-1, 0) represents a wind blowing directly to the left.
    (0, -1) represents a wind blowing directly downwards.
    (0.707, 0.707) represents a wind blowing diagonally up and to the right.


tree mortality rate funtion:
https://www.researchgate.net/figure/Probability-of-mortality-over-3-years-a-and-age-specific-mortality-rate-over-3years-b_fig4_355951613