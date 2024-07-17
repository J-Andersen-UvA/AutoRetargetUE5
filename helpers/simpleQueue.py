class QueueItem:
    def __init__(self, func, args, connection=None, connection_type=None, url=None):
        self.func = func
        self.args = args
        self.connection = connection
        self.connection_type = connection_type
        self.url = url

class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, func, args, connection=None, connection_type=None, url=None):
        """Add an item to the end of the queue."""
        item = QueueItem(func, args, connection, connection_type, url)
        self.items.append(item)

    def dequeue(self):
        """Remove and return the front item of the queue."""
        if not self.is_empty():
            return self.items.pop(0)
        else:
            print("Queue is empty.")
            return None

    def is_empty(self):
        """Check if the queue is empty."""
        return len(self.items) == 0

    def size(self):
        """Return the number of items in the queue."""
        return len(self.items)

    def __str__(self):
        """Return a string representation of the queue."""
        return str(self.items)
