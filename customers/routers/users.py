from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db, engine
from ..utils import hash

models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/Users"
    , tags=["users"]
    )


@router.get("/", status_code=status.HTTP_200_OK,response_model=List[schemas.UsersResponse])
def all_users(db: Session = Depends(get_db)):
    # cur.execute("""SELECT * FROM customers""")
    # all_customers = cur.fetchall()
    # conn.commit()
    # qry = db.query(models.Customer)
    # print(qry)
    all_users = db.query(models.User).all()
    return all_users

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UsersResponse)
def create_users(user : schemas.Users, db: Session = Depends(get_db)):
    # cur.execute("""INSERT INTO customers(name, sex, birth_date) VALUES( %s, %s , %s ) RETURNING *"""
    #             , (customer.name, customer.sex.value,str(customer.birthdate),))
    # new_customer = cur.fetchone()
    # conn.commit()
    # new_customer = models.Customer(name=customer.name, sex=customer.sex.value, birth_date=customer.birth_date)
    user_exist = db.query(models.User).filter(models.User.email == user.email).first()
    if user_exist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"Email already exits")
    hash_password = hash.hashed_value(user.password)
    user.password = hash_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", status_code=status.HTTP_200_OK,response_model=schemas.UsersResponse)
def get_users(id: int, db: Session = Depends(get_db)):
    # cur.execute("""SELECT * FROM customers WHERE id = %s""", (str(id),))
    # customer = cur.fetchone()
    # conn.commit()
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED,response_model=schemas.UsersResponse)
def update_users(id: int, user : schemas.Users, db: Session = Depends(get_db)):
    # cur.execute("""UPDATE customers SET updated_at = now() , name = %s, sex = %s , birth_date = %s WHERE id = %s RETURNING *"""
    #            , (customer.name, customer.sex,str(customer.birthdate),str(id),))
    # updated_customer = cur.fetchone()
    # conn.commit()
    hash_password = hash.hashed_value(user.password)
    user.password = hash_password
    update_qry = db.query(models.User).filter(models.User.id == id)
    updated_user = update_qry.first()
    if updated_user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    update_qry.update(user.model_dump(),synchronize_session=False)
    db.commit()
    updated_user = update_qry.first()
    return updated_user

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_users(id: int , db: Session = Depends(get_db)):
    # cur.execute("""DELETE FROM customers WHERE id = %s RETURNING *""", (str(id),))
    # deleted_customer = cur.fetchone()
    # conn.commit()
    del_qry = db.query(models.User).filter(models.User.id == id)
    deleted_user = del_qry.first()
    if deleted_user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    del_qry.delete(synchronize_session=False)
    db.commit()
    # db.refresh(deleted_customer)
    # return {"data": deleted_customer}
    return {"message" : f"customer with id : {id} deleted sucessfully"}

