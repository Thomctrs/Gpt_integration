from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from starlette.responses import JSONResponse

from . import models, schemas, crud
from .database import engine, get_db
from .schemas import ImageBase

# Créer les tables
models.Base.metadata.create_all(bind=engine)

# Initialiser l'application FastAPI
app = FastAPI(title="Tempus Lux API", description="API pour la boutique de montres de luxe")

# Routes pour les montres
@app.get("/watches/", response_model=List[schemas.WatchResponse])
def read_watches(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Récupérer la liste des montres
    - skip: Nombre de montres à ignorer (pour pagination)
    - limit: Nombre max de montres à retourner
    """
    watches = crud.get_watches(db, skip=skip, limit=limit)
    print(watches)
    return [
        schemas.WatchResponse(
            watch_id=watch.watch_id,
            model=watch.model,
            price=watch.price,
            description=watch.description,
            technical_details=watch.technical_details,
            reference_number=watch.reference_number,
            movement_type=watch.movement_type,
            case_material=watch.case_material,
            water_resistance=watch.water_resistance,
            diameter=watch.diameter,
            stock_quantity=watch.stock_quantity,
            brand_name=watch.brand.name if watch.brand else None,  # Vérifie si la relation existe
            collection_name=watch.collection.name if watch.collection else None,  # Vérifie si la relation existe
            images=[
                schemas.ImageBase(image_url=image.image_url, is_primary=image.is_primary)
                for image in watch.images
            ]
        )
        for watch in watches
    ]

@app.get("/watches/{watch_id}", response_model=schemas.WatchResponse)
def read_watch(watch_id: int, db: Session = Depends(get_db)):
    """
    Récupérer les détails d'une montre spécifique
    """
    watch = crud.get_watch(db, watch_id=watch_id)
    if watch is None:
        raise HTTPException(status_code=404, detail="Montre non trouvée")
    return schemas.WatchResponse(
        watch_id=watch.watch_id,
        model=watch.model,
        price=watch.price,
        description=watch.description,
        technical_details=watch.technical_details,
        reference_number=watch.reference_number,
        movement_type=watch.movement_type,
        case_material=watch.case_material,
        water_resistance=watch.water_resistance,
        diameter=watch.diameter,
        stock_quantity=watch.stock_quantity,
        brand_name=watch.brand.name if watch.brand else None,
        collection_name=watch.collection.name if watch.collection else None,
        images=[
            schemas.ImageBase(image_url=image.image_url, is_primary=image.is_primary)
            for image in watch.images
        ]
    )

# Gestion des erreurs 404
@app.get("/health")
def health_check():
    """
    Point de terminaison pour vérifier la santé de l'API
    """
    return {"status": "healthy"}

# Gestion des erreurs 404 personnalisée
@app.exception_handler(404)
async def not_found_error(request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": "La ressource demandée n'existe pas"}
    )