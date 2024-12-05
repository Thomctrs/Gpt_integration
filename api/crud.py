from sqlalchemy.orm import Session, joinedload
from . import models, schemas


def get_watches(db: Session, skip: int = 0, limit: int = 10):
    """
    Récupérer une liste de montres avec leurs images et informations de marque
    """
    return (
        db.query(models.Watch)
        .options(
            joinedload(models.Watch.brand),
            joinedload(models.Watch.collection)
        )
        .offset(skip)
        .limit(limit)
        .all()

    )


def get_watch(db: Session, watch_id: int):
    """
    Récupérer les détails d'une montre spécifique
    """
    return (
        db.query(models.Watch)
        .options(
            joinedload(models.Watch.brand),
            joinedload(models.Watch.collection),
            joinedload(models.Watch.images)
        )
        .filter(models.Watch.watch_id == watch_id)
        .first()
    )


def create_watch(db: Session, watch: schemas.WatchCreate):
    """
    Créer une nouvelle montre
    """
    db_watch = models.Watch(**watch.dict())
    db.add(db_watch)
    db.commit()
    db.refresh(db_watch)
    return db_watch


def update_watch(db: Session, watch_id: int, watch: schemas.WatchCreate):
    """
    Mettre à jour les informations d'une montre
    """
    db_watch = get_watch(db, watch_id)
    if not db_watch:
        return None

    for key, value in watch.dict().items():
        setattr(db_watch, key, value)

    db.commit()
    db.refresh(db_watch)
    return db_watch