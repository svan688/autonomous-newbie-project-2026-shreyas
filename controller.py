VALID_STEERING = {"LEFT", "RIGHT", "STRAIGHT"}
VALID_SPEED = {"ACCELERATE", "SLOW", "STOP"}


def controller(
    obstacle_distance_m,
    lane_offset_m,
    heading_error_deg,
    speed_mps,
    e_stop,
    left_clear,
    right_clear,
    sensor_valid
):
    DANGER_OBSTACLE_M = 1.0
    CAUTION_OBSTACLE_M = 2.0

    MILD_HEADING_DEG = 3.0
    LARGE_HEADING_DEG = 15.0

    MILD_OFFSET_M = 0.15
    LARGE_OFFSET_M = 0.40

    HIGH_SPEED_MPS = 3.0

    centered = abs(lane_offset_m) <= MILD_OFFSET_M
    small_heading_error = abs(heading_error_deg) <= MILD_HEADING_DEG

    steering = "STRAIGHT"
    speed_action = "ACCELERATE"

    # sensor check — first thing checked, can't trust any data if sensors are broken
    if not sensor_valid:
        return "STRAIGHT", "STOP"

    # e_stop -> immediately stop no conditions
    if e_stop:
        return "STRAIGHT", "STOP"

    if centered and small_heading_error and obstacle_distance_m > CAUTION_OBSTACLE_M:
        steering = "STRAIGHT"
        speed_action = "ACCELERATE"

    # danger zone = obstacle within 1m
    elif obstacle_distance_m <= DANGER_OBSTACLE_M:
        if not left_clear and not right_clear:
            steering = "STRAIGHT"
            speed_action = "STOP"

        elif left_clear and not right_clear:
            steering = "LEFT"
            speed_action = "SLOW"

        elif right_clear and not left_clear:
            steering = "RIGHT"
            speed_action = "SLOW"

        elif heading_error_deg > MILD_HEADING_DEG or lane_offset_m > MILD_OFFSET_M:
            steering = "LEFT"
            speed_action = "SLOW"

        elif heading_error_deg < -MILD_HEADING_DEG or lane_offset_m < -MILD_OFFSET_M:
            steering = "RIGHT"
            speed_action = "SLOW"

        else:
            steering = "LEFT"
            speed_action = "SLOW"

    # caution zone = obstacle within 2m
    elif obstacle_distance_m <= CAUTION_OBSTACLE_M:
        if not left_clear and not right_clear:
            steering = "STRAIGHT"
            speed_action = "STOP"

        elif left_clear and not right_clear:
            steering = "LEFT"
            speed_action = "SLOW"

        elif right_clear and not left_clear:
            steering = "RIGHT"
            speed_action = "SLOW"

        elif heading_error_deg > MILD_HEADING_DEG or lane_offset_m > MILD_OFFSET_M:
            steering = "LEFT"
            speed_action = "SLOW"

        elif heading_error_deg < -MILD_HEADING_DEG or lane_offset_m < -MILD_OFFSET_M:
            steering = "RIGHT"
            speed_action = "SLOW"

        else:
            steering = "STRAIGHT"
            speed_action = "SLOW"

    elif speed_mps >= HIGH_SPEED_MPS:
        if heading_error_deg > LARGE_HEADING_DEG or lane_offset_m > LARGE_OFFSET_M:
            steering = "LEFT"
            speed_action = "SLOW"

        elif heading_error_deg < -LARGE_HEADING_DEG or lane_offset_m < -LARGE_OFFSET_M:
            steering = "RIGHT"
            speed_action = "SLOW"

        else:
            steering = "STRAIGHT"
            speed_action = "SLOW"

    # large error correction
    elif heading_error_deg > LARGE_HEADING_DEG or lane_offset_m > LARGE_OFFSET_M:
        steering = "LEFT" #left because positive heading error means car is pointing to the right of lane center, so we need to steer left to correct
        speed_action = "SLOW" 

    elif heading_error_deg < -LARGE_HEADING_DEG or lane_offset_m < -LARGE_OFFSET_M:
        steering = "RIGHT" #right because negative heading error means car is pointing to the left of lane center, so we need to steer right to correct
        speed_action = "SLOW"

    
    assert steering in VALID_STEERING, f"Invalid steering: {steering}"
    assert speed_action in VALID_SPEED, f"Invalid speed: {speed_action}"


    return steering, speed_action
