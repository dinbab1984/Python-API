from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session
from .. import models, schemas, auth
from ..database import get_db, engine
models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/customers"
    , tags=["Customers"]
    )


@router.get("/", status_code=status.HTTP_200_OK,response_model=List[schemas.CustomersReponse])
def all_customers(db: Session = Depends(get_db), user_id : int = Depends(auth.get_current_user)):
    # cur.execute("""SELECT * FROM customers""")
    # all_customers = cur.fetchall()
    # conn.commit()
    # qry = db.query(models.Customer)
    # print(qry)
    all_customers = db.query(models.Customer).all()
    return all_customers

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.CustomersReponse)
def create_customers(customer : schemas.Customers, db: Session = Depends(get_db), user_id : int = Depends(auth.get_current_user)):
    # cur.execute("""INSERT INTO customers(name, sex, birth_date) VALUES( %s, %s , %s ) RETURNING *"""
    #             , (customer.name, customer.sex.value,str(customer.birthdate),))
    # new_customer = cur.fetchone()
    # conn.commit()
    # new_customer = models.Customer(name=customer.name, sex=customer.sex.value, birth_date=customer.birth_date)
    new_customer = models.Customer(created_by=user_id,**customer.model_dump())
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    print(new_customer)
    return new_customer

@router.get("/{id}", status_code=status.HTTP_200_OK,response_model=schemas.CustomersReponse)
def get_customers(id: int, db: Session = Depends(get_db), user_id : int = Depends(auth.get_current_user)):
    # cur.execute("""SELECT * FROM customers WHERE id = %s""", (str(id),))
    # customer = cur.fetchone()
    # conn.commit()
    customer = db.query(models.Customer).filter(models.Customer.id == id).first()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return customer

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED,response_model=schemas.CustomersReponse)
def update_customers(id: int, customer : schemas.Customers, db: Session = Depends(get_db), user_id : int = Depends(auth.get_current_user)):
    # cur.execute("""UPDATE customers SET updated_at = now() , name = %s, sex = %s , birth_date = %s WHERE id = %s RETURNING *"""
    #            , (customer.name, customer.sex,str(customer.birthdate),str(id),))
    # updated_customer = cur.fetchone()
    # conn.commit()
    update_qry = db.query(models.Customer).filter(models.Customer.id == id)
    updated_customer = update_qry.first()
    if updated_customer == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if user_id != updated_customer.created_by:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    update_qry.update(customer.model_dump(),synchronize_session=False)
    db.commit()
    updated_customer = update_qry.first()
    return updated_customer

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customers(id: int , db: Session = Depends(get_db), user_id : int = Depends(auth.get_current_user)):
    # cur.execute("""DELETE FROM customers WHERE id = %s RETURNING *""", (str(id),))
    # deleted_customer = cur.fetchone()
    # conn.commit()
    del_qry = db.query(models.Customer).filter(models.Customer.id == id)
    deleted_customer = del_qry.first()
    if deleted_customer == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if user_id != deleted_customer.created_by:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    del_qry.delete(synchronize_session=False)
    db.commit()
    # db.refresh(deleted_customer)
    # return {"data": deleted_customer}
    return {"message" : f"customer with id : {id} deleted sucessfully"}

