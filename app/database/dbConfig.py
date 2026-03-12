class DatabaseConnection:
    _instance = None
    
    def __new__(self):
        if self._instance is None:
            print("Creating DB connection")
            self._instance = super().__new__(self)
        return self._instance