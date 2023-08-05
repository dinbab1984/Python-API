from fastapi import FastAPI, status, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from enum import Enum
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from datetime import date
from sqlalchemy.orm import Session
from . import models, schemas
from .database import get_db, engine

models.Base.metadata.create_all(bind=engine)


# while True:
#     try:
#         conn = psycopg2.connect(host="localhost", database="Customers",user="postgres"
#             ,password="Nithya28", cursor_factory=RealDictCursor)
#         cur = conn.cursor()
#         print("Database connection success!")
#         break
#     except Exception as error:
#         print("Database connection failed!")
#         print(error)
#         time.sleep(3)

app = FastAPI()


@app.get("/")
def root():
    return {"message" : "Hello World!"}


@app.get("/customers", status_code=status.HTTP_200_OK)
def all_customers(db: Session = Depends(get_db)):
    # cur.execute("""SELECT * FROM customers""")
    # all_customers = cur.fetchall()
    # conn.commit()
    # qry = db.query(models.Customer)
    # print(qry)
    all_customers = db.query(models.Customer).all()
    return {"data" : all_customers}

@app.post("/customers",status_code=status.HTTP_201_CREATED)
def create_customers(customer : schemas.Customers, db: Session = Depends(get_db)):
    # cur.execute("""INSERT INTO customers(name, sex, birth_date) VALUES( %s, %s , %s ) RETURNING *"""
    #             , (customer.name, customer.sex.value,str(customer.birthdate),))
    # new_customer = cur.fetchone()
    # conn.commit()
    # new_customer = models.Customer(name=customer.name, sex=customer.sex.value, birth_date=customer.birth_date)
    new_customer = models.Customer(**customer.dict())
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return { "data" : new_customer}

@app.get("/customers/{id}", status_code=status.HTTP_200_OK)
def get_customers(id: int, db: Session = Depends(get_db)):
    # cur.execute("""SELECT * FROM customers WHERE id = %s""", (str(id),))
    # customer = cur.fetchone()
    # conn.commit()
    customer = db.query(models.Customer).filter(models.Customer.id == id).first()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {"data" : customer}

@app.put("/customers/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_customers(id: int, customer : schemas.Customers, db: Session = Depends(get_db)):
    # cur.execute("""UPDATE customers SET updated_at = now() , name = %s, sex = %s , birth_date = %s WHERE id = %s RETURNING *"""
    #            , (customer.name, customer.sex,str(customer.birthdate),str(id),))
    # updated_customer = cur.fetchone()
    # conn.commit()
    update_qry = db.query(models.Customer).filter(models.Customer.id == id)
    updated_customer = update_qry.first()
    if updated_customer == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    update_qry.update(customer.dict(),synchronize_session=False)
    db.commit()
    updated_customer = update_qry.first()
    return {"data": updated_customer}

@app.delete("/customers/{id}", status_code=status.HTTP_202_ACCEPTED)
def delete_customers(id: int , db: Session = Depends(get_db)):
    # cur.execute("""DELETE FROM customers WHERE id = %s RETURNING *""", (str(id),))
    # deleted_customer = cur.fetchone()
    # conn.commit()
    del_qry = db.query(models.Customer).filter(models.Customer.id == id)
    deleted_customer = del_qry.first()
    if deleted_customer == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    del_qry.delete(synchronize_session=False)
    db.commit()
    # db.refresh(deleted_customer)
    # return {"data": deleted_customer}
    return {"message" : f"customer with id : {id} deleted sucessfully"}

