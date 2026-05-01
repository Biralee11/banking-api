class EmailNotification():
    def update(self, message):
        print(f"EmailNotification — \"Email sent: {message}\"")

class SMSNotification():
    def update(self, message):
        print(f"SMSNotification — \"SMS sent: {message}\"")

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update()
