class DatabaseRouter:
    """Route specific models to specific databases"""
    
    mongo_models = ['MongoAuthor', 'MongoBook']  # Your MongoDB models
    
    def db_for_read(self, model, **hints):
        if model.__name__ in self.mongo_models:
            return 'mongodb'
        return 'default'
    
    def db_for_write(self, model, **hints):
        if model.__name__ in self.mongo_models:
            return 'mongodb'
        return 'default'
    
    def allow_relation(self, obj1, obj2, **hints):
        return True
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == 'mongodb':
            return model_name in [m.lower() for m in self.mongo_models]
        return True