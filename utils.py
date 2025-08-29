def log_action(filename, message):
        import os
    from datetime import datetime
    
    # Ensure the directory exists
    log_dir = os.path.dirname(filename)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"{timestamp} - {message}\n"
    
    with open(filename, 'a') as log_file:
        log_file.write(log_message)