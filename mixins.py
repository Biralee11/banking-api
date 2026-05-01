class LogMixin():
    def log(self,message):
        print(f"{self.account_holder}: {message}")