from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Global DB instance
db = SQLAlchemy()
migrate = Migrate()
