import time

def wait_start_cook(id, order):
    time.sleep(1)

def wait_end_cook(id, order):
    time.sleep(1)

def wait_end_order(id, wait_time, order):
    # passed_time = 0
    # while order.in_queue() and passed_time < time:
    #     time.sleep(1)
    #     passed_time += 1
    # return order.in_queue
    time.sleep(1)
    return True