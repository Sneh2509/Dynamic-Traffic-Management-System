def predict_signal_time(vehicle_counts):
    """Predicts the optimal traffic signal time based on vehicle density."""
    total_vehicles = sum(vehicle_counts.values())
    
    if total_vehicles > 50:
        return 90  # 90 seconds for high traffic
    elif total_vehicles > 20:
        return 60  # 60 seconds for medium traffic
    else:
        return 30  # 30 seconds for low traffic
