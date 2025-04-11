message_handlers = {}


def message_handler(message_type):
    def wrapper(func):
        message_handlers[message_type] = func
        print(f"Handler for {message_type} registered.")
        return func

    return wrapper
