from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import models, schemas, database
import json

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Custom Field Definitions ---

@app.post("/api/fields/", response_model=schemas.CustomFieldDefinition)
def create_field_definition(field: schemas.CustomFieldDefinitionCreate, db: Session = Depends(get_db)):
    db_field = models.CustomFieldDefinition(
        entity_type=field.entity_type,
        key_name=field.key_name,
        label=field.label,
        field_type=field.field_type,
        options=json.dumps(field.options),
        validation_rules=json.dumps(field.validation_rules),
        is_active=field.is_active
    )
    db.add(db_field)
    db.commit()
    db.refresh(db_field)
    return db_field

@app.get("/api/fields/{entity_type}", response_model=List[schemas.CustomFieldDefinition])
def get_field_definitions(entity_type: str, db: Session = Depends(get_db)):
    fields = db.query(models.CustomFieldDefinition).filter(
        models.CustomFieldDefinition.entity_type == entity_type,
        models.CustomFieldDefinition.is_active == True
    ).all()
    # Ensure JSON strings are parsed back to objects/lists for Pydantic response
    # Actually Pydantic `Json` type handles serialization automatically from string in DB to object in response
    return fields

# --- People ---

@app.post("/api/people/", response_model=schemas.Person)
def create_person(person: schemas.PersonCreate, db: Session = Depends(get_db)):
    db_person = models.Person(
        name=person.name,
        email=person.email,
        custom_data=json.dumps(person.custom_data)
    )
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person

@app.get("/api/people/", response_model=List[schemas.Person])
def get_people(db: Session = Depends(get_db)):
    people = db.query(models.Person).all()
    return people

# --- Forms Endpoints ---

@app.post("/api/forms/", response_model=schemas.Form)
def create_form(form: schemas.FormCreate, db: Session = Depends(get_db)):
    db_form = models.FormDefinition(name=form.name, description=form.description)
    db.add(db_form)
    db.commit()
    db.refresh(db_form)
    
    # Add fields associations
    for index, field_link in enumerate(form.fields):
        association = models.FormFields(
            form_id=db_form.id, 
            field_id=field_link.field_id, 
            order=index,
            is_required=field_link.is_required
        )
        db.add(association)
    
    db.commit()
    db.refresh(db_form)
    return db_form

@app.get("/api/forms/", response_model=List[schemas.Form])
def get_forms(db: Session = Depends(get_db)):
    return db.query(models.FormDefinition).all()

@app.get("/api/forms/{form_id}", response_model=schemas.Form)
def get_form(form_id: int, db: Session = Depends(get_db)):
    form = db.query(models.FormDefinition).filter(models.FormDefinition.id == form_id).first()
    if not form:
        raise HTTPException(status_code=404, detail="Form not found")
    # Sort fields by order
    form.fields.sort(key=lambda x: x.order)
    return form
