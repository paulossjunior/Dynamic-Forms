from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import models, schemas, database
from src.infrastructure.repositories.section_repository import SectionRepository
from src.application.use_cases.create_section import CreateSection
from src.application.use_cases.list_sections import ListSections
from src.application.use_cases.update_section import UpdateSection
from src.application.use_cases.delete_section import DeleteSection
import json

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], 
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
    try:
        db_person = models.Person(
            name=person.name,
            email=person.email,
            custom_data=json.dumps(person.custom_data)
        )
        db.add(db_person)
        db.commit()
        db.refresh(db_person)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="A person with this email already exists.")
    return db_person

@app.get("/api/people/", response_model=List[schemas.Person])
def get_people(db: Session = Depends(get_db)):
    people = db.query(models.Person).all()
    return people

# --- Forms Endpoints ---

from sqlalchemy.exc import IntegrityError

@app.post("/api/forms/", response_model=schemas.Form)
def create_form(form: schemas.FormCreate, db: Session = Depends(get_db)):
    # 1. Create Form
    try:
        db_form = models.FormDefinition(name=form.name, description=form.description)
        db.add(db_form)
        db.commit()
        db.refresh(db_form)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="A form with this name already exists.")
    
    # Map temp_id to real_id for sections created inline
    temp_id_map = {}

    # 2. Create Sections if provided
    repo = SectionRepository(db)
    for section_create in form.sections:
        # Assign form_id to the new section
        section_create.form_id = db_form.id
        
        # Use existing CreateSection use case logic (or repository directly for simplicity here)
        # We need to convert pydantic model to dict for entity creation if using use case, 
        # or manually create model. Let's use the Repository directly to keep it simple in the controller
        # but adhering to the architecture would be better. 
        # Given the imports, we can use the entity/model mapping from repository.
        
        db_section = models.Section(
            name=section_create.name,
            description=section_create.description,
            order_index=section_create.order_index,
            form_id=db_form.id
        )
        db.add(db_section)
        db.commit()
        db.refresh(db_section)
        
        if section_create.temp_id:
            temp_id_map[section_create.temp_id] = db_section.id

    # 3. Add fields associations
    for index, field_link in enumerate(form.fields):
        # Resolve section_id
        final_section_id = field_link.section_id
        
        # If no direct section_id, check for temp_id linkage
        if final_section_id is None and field_link.section_temp_id:
            final_section_id = temp_id_map.get(field_link.section_temp_id)

        association = models.FormFields(
            form_id=db_form.id, 
            field_id=field_link.field_id, 
            section_id=final_section_id,
            order=index,
            is_required=field_link.is_required
        )
        db.add(association)

    db.commit()
    db.refresh(db_form)
    
    # Reload form with relationships to return full object
    # Pydantic "from_attributes" will handle the conversion
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
    # Sections are already ordered by Section.order_index in the relationship
    return form

# --- Sections Endpoints ---

@app.post("/api/sections/", response_model=schemas.Section)
def create_section(section: schemas.SectionCreate, db: Session = Depends(get_db)):
    repo = SectionRepository(db)
    use_case = CreateSection(repo)
    return use_case.execute(section)

@app.get("/api/forms/{form_id}/sections/", response_model=List[schemas.Section])
def list_sections(form_id: int, db: Session = Depends(get_db)):
    repo = SectionRepository(db)
    use_case = ListSections(repo)
    return use_case.execute(form_id)

@app.put("/api/sections/{section_id}", response_model=schemas.Section)
def update_section(section_id: int, section: schemas.SectionBase, db: Session = Depends(get_db)):
    repo = SectionRepository(db)
    use_case = UpdateSection(repo)
    try:
        dto = schemas.SectionCreate(**section.dict()) # Using SectionCreate schema for update values
        return use_case.execute(section_id, dto)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.delete("/api/sections/{section_id}")
def delete_section(section_id: int, db: Session = Depends(get_db)):
    repo = SectionRepository(db)
    use_case = DeleteSection(repo)
    use_case.execute(section_id)
    return {"status": "success"}

@app.post("/api/forms/{form_id}/fields/{field_id}/section/{section_id}")
def associate_field_to_section(form_id: int, field_id: int, section_id: int, db: Session = Depends(get_db)):
    association = db.query(models.FormFields).filter(
        models.FormFields.form_id == form_id,
        models.FormFields.field_id == field_id
    ).first()
    
    if not association:
        raise HTTPException(status_code=404, detail="Association not found")
        
    association.section_id = section_id
    db.commit()
    return {"status": "success"}

# --- Analytics Endpoints ---

@app.get("/api/analytics/field-stats")
def get_field_stats(db: Session = Depends(get_db)):
    """
    Aggregate statistics for dynamic fields across all people.
    Returns value counts for select/multiselect fields and stats for numeric fields.
    """
    # Get all active fields
    fields = db.query(models.CustomFieldDefinition).filter(
        models.CustomFieldDefinition.is_active == True
    ).all()
    
    # Get all people with their custom data
    people = db.query(models.Person).all()
    
    stats = []
    
    for field in fields:
        field_stats = {
            "field_key": field.key_name,
            "field_label": field.label,
            "field_type": field.field_type,
            "total_responses": 0,
            "value_counts": {},
            "numeric_stats": None
        }
        
        values = []
        for person in people:
            try:
                custom_data = json.loads(person.custom_data)
                if field.key_name in custom_data:
                    value = custom_data[field.key_name]
                    if value is not None and value != "":
                        values.append(value)
            except:
                continue
        
        field_stats["total_responses"] = len(values)
        
        # Aggregate based on field type
        if field.field_type in ['select', 'radio', 'checkbox']:
            # Count occurrences of each value
            for value in values:
                value_str = str(value)
                field_stats["value_counts"][value_str] = field_stats["value_counts"].get(value_str, 0) + 1
        
        elif field.field_type == 'multiselect':
            # Flatten and count array values
            for value in values:
                if isinstance(value, list):
                    for item in value:
                        item_str = str(item)
                        field_stats["value_counts"][item_str] = field_stats["value_counts"].get(item_str, 0) + 1
        
        elif field.field_type == 'number':
            # Calculate numeric statistics
            numeric_values = []
            for value in values:
                try:
                    numeric_values.append(float(value))
                except:
                    continue
            
            if numeric_values:
                field_stats["numeric_stats"] = {
                    "min": min(numeric_values),
                    "max": max(numeric_values),
                    "avg": sum(numeric_values) / len(numeric_values),
                    "count": len(numeric_values)
                }
        
        stats.append(field_stats)
    
    return {
        "total_people": len(people),
        "field_stats": stats
    }
