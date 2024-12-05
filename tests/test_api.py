from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from api.main import app, get_db
from api.database import Base
from api.models import Watch, Brand, Collection

# Configuration de la base de données de test
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    """Générer une session de base de données de test"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Créer les tables de test
Base.metadata.create_all(bind=engine)

# Client de test
client = TestClient(app)

def test_read_watches():
    """Tester la récupération de la liste des montres"""
    response = client.get("/watches/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_watch_not_found():
    """Tester la gestion d'une montre inexistante"""
    response = client.get("/watches/9999")
    assert response.status_code == 404