class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, func, args, connection=None):
        """Add an item to the end of the queue."""
        if connection:
            self.items.append((func, args, connection))
        else:
            self.items.append((func, args))

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
