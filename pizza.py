###Note about design patterns
###My code utilizes the abstract factory, builder, and facade pattern types.

from sqlalchemy import Column, Integer, Float, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import time
from abc import ABCMeta, abstractstaticmethod

from sqlalchemy.sql.expression import null
from sqlalchemy.sql.sqltypes import Boolean, PickleType

engine = create_engine('sqlite:///:memory:', echo=False)
Base = declarative_base()

activeEmployee = 2
activeCustomer = 1    
lastOrderNumber = 543210   
lastIDassign = 123456


class InventoryItem(Base):
    def __init__(self, name, qty, unitOfMeasure, unitPrice, type):
        self.name = name
        self.qty = qty
        self.unitOfMeasure = unitOfMeasure
        self.unitPrice = unitPrice
        self.type = type
        self.totalValue = (qty * unitPrice)

    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False, unique=True)
    qty = Column(Float)
    unitOfMeasure = Column(String)
    unitPrice = Column(Float)
    totalValue = Column(Float)
    type = Column(String)

    def __repr__(self):
        return "We have {1} {2} of {0} in stock. Costs ${3} per {2}.".format(self.name, self.qty, self.unitOfMeasure, self.unitPrice)

    def modifyQty(self, qtyAdjust):
        self.qty += qtyAdjust



class Person(Base):
    def __init__(self, firstName, lastName, phoneNumber, streetAddress, idNumber):
        self.firstName = firstName
        self.lastName = lastName
        self.phoneNumber = phoneNumber
        self.streetAddress = streetAddress
        self.idNumber = idNumber
        
    __tablename__ = 'people'

    id = Column(Integer, primary_key=True)
    firstName = Column(String)
    lastName = Column(String)
    phoneNumber = Column(String)
    streetAddress = Column(String)
    idNumber = Column(String)


    def __repr__(self):
        return "{} {}, {} {}".format(self.firstName, self.lastName, self.get_role(), self.idNumber)

    def get_role(self):
        if self.personType == "Employee":
            return "Employee"
        elif self.pastOrders:
            return "Existing Customer"
        else:
            return "New Customer"

    def get_orders(self):
        orders = session.query(Orders).filer_by()


    
    

class Customer(Person):
    def __init__(self,
                 firstName,
                 lastName,
                 phoneNumber,
                 address,
                 idNumber,
                 paymentMethod):
        self.paymentMethod = paymentMethod
        self.personType = "Customer"
        super().__init__(firstName, lastName, phoneNumber, address, idNumber)

    def createOrder(self):
        orderNumber = lastOrderNumber + 1
        self.assignOrder(self, orderNumber)
        session.add(Order(orderNumber, datetime.now(), self.idNumber, 0, []))



    # __tablename__ = 'customers'

    # id = Column(Integer, primary_key=True)
    # firstName = Column(String)
    # lastName = Column(String)
    # phoneNumber = Column(Integer)
    # address = Column(String)
    # idNumber = Column(Integer)
    # paymentMethod = Column(String)

class Employee(Person):
    def __init__(self,
                 firstName,
                 lastName,
                 phoneNumber,
                 address,
                 idNumber,
                 position,
                 payRate):
        self.position = position
        self.payRate = payRate
        self.personType = "Employee"
        super().__init__(firstName, lastName, phoneNumber, address, idNumber)

    
# Abstract factory for creating people (customers or employees)
class PeopleFactory(object):
    @classmethod
    def create(cls, name, *args):
        name = name.lower().strip()
        
        if name == 'customer':
            return Customer(*args)
        elif name == 'employee':
            return Employee(*args)

class Order():
    def __init__(self, orderNumber, orderTime, customer, employee, orderItems):
        self.orderNumber = orderNumber
        self.orderTime = orderTime
        self.customer = customer
        self.employee = employee
        self.orderItems = orderItems
        self.orderPaid = False
        self.cookingComplete = False
        self.orderComplete = False

    def __repr__(self):
        return """            Order Number: {}
            Name: {} {}
            Employee: {} {} 
            Order Delivered: {}
            Order Paid: {}
            Order Cooked: {}
            Order Items: {}""".format(self.orderNumber, 
            self.customer.firstName, 
            self.customer.lastName, 
            self.employee.firstName, 
            self.employee.lastName, 
            self.orderDelivered,
            self.orderPaid,
            self.cookingComplete,
            self.orderItems)

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    orderNumber = Column(Integer, nullable=False, unique=True)
    orderTime = Column(DateTime)
    customer = Column(Integer)
    employee = Column(Integer)
    orderItems = Column(PickleType)
    orderPaid = Column(Boolean)
    cookingComplete = Column(Boolean)
    orderComplete = Column(Boolean)


    def addOrderItem(self, orderItem):
        self.orderItems.append(orderItem)
        
    def removeOrderItem(self, orderItem):
        self.orderItem.pop(orderItem)
        
    def completeCooking(self):
        self.cookingComplete = True

    def deliverOrder(self):
        self.orderDelivered = True
        self.customer.pastOrders.append(self.customer.currentOrders.pop(self))

    def payOrder(self):
        self.orderPaid = True
        
# Facade for creating new orders     
class OrderBuilder(object):
    def __init__(self, employee, customer, orderNumber, orderTime, orderItems):
        self.customer = customer
        self.employee = employee
        self.orderNumber = orderNumber
        self.orderTime = orderTime
        self.orderItems = orderItems


    def create(self):
        
        __newOrder = Order(self.orderNumber, self.orderTime, self.customer, self.employee, self.orderItems)
        
        return __newOrder


class IFoodBuilder(metaclass=ABCMeta):
    #Builder Interface
    
    @abstractstaticmethod
    def setFoodType():
        #sets the food item type (e.g. pizza, sandwich, pasta)
        pass
    @abstractstaticmethod
    def setCarbBase():
        #sets type of carbohydrate base (e.g. 12" thin crust, penne pasta, baguette)
        pass
    @abstractstaticmethod 
    def setFoodToppings():
        #sets the types and amounts of toppings (e.g. pepperoni, double sausage, banana peppers)
        pass
    @abstractstaticmethod
    def setFoodQty():
        #sets the number of food items
        pass
    def setFoodPrice(self):
        #sets the price of the food item(s)
        pass
    def getFood(self):
        #return the food item
        pass
        
class FoodBuilder(IFoodBuilder):
    #The food item builder
    
    def __init__(self):
        self.food = Food()
    
    def setCarbBase(self, value):
        self.food.carbBase = value
        return self
    
    def setFoodType(self, value):
        self.food.foodType = value
        return self 

    def setFoodQty(self, value):
        self.food.foodQty = value
        return self

    def setFoodPrice(self, value):
        self.food.foodPrice = value
        return self
    
    def setFoodToppings(self, value):
        self.food.foodToppings = value
        return self

    def getResult(self):
        return self.food

class Food():
    def __init__(self, foodType="Pizza", carbBase="None", foodToppings=[], foodQty=0, foodPrice=0):
        self.foodType = foodType
        self.carbBase = carbBase
        self.foodToppings = foodToppings
        self.foodQty = foodQty
        self.foodPrice = foodPrice

    def __str__(self):
        return "{} {}(s) on {} with {} for {}".format(self.foodQty, 
                                                            self.foodType, 
                                                            self.carbBase, 
                                                            self.foodToppings, 
                                                            self.foodPrice)

class PizzaDirector():
    #Director builds instances of pizzas

    @staticmethod
    def construct(carbBase, foodToppings, foodQty, foodPrice):
        return FoodBuilder()\
            .setFoodType("Pizza")\
            .setCarbBase(carbBase)\
            .setFoodToppings(foodToppings)\
            .setFoodQty(foodQty)\
            .setFoodPrice(foodPrice)\
            .getResult()

class SandwichDirector():
    
    @staticmethod
    def construct(carbBase, foodToppings, foodQty, foodPrice):
        return FoodBuilder()\
                .setFoodType("Sandwich")\
                .setCarbBase(carbBase)\
                .setFoodToppings(foodToppings)\
                .setFoodQty(foodQty)\
                .setFoodPrice(foodPrice)\
                .getResult()

def createAccount():
    global lastIDassign
    print("\n\nNew User Registration\n~~~~~~~~~~~~~~~~~~~~~~~~~~~\nPlease enter the required information and press enter:\n\n")
    fname = input("First Name: ")
    lname = input("Last Name: ")
    pnumber = input("Phone Number: ")
    address1 = input("Address Line 1: ")
    address2 = input("Address Line 2: ")
    city = input("City: ")
    zipcode = input("ZIP Code: ")
    lastIDassign += 1
    idnumber = lastIDassign + 1
    session.add(PeopleFactory.create('customer', fname, lname, pnumber, str(address1 + address2 + city + zipcode), idnumber, 0))
    print("\n\nWelcome, {}!\n\nYour have successfully created a new account.\n\nYour new UserID is {}.".format(fname, idnumber))
    time.sleep(3)
    welcome()

def orderInput():
    print("\n\nPlace an Order\n~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")


def welcome():
    session.add(PeopleFactory.create('customer', 'fname', 'lname', 'pnumber', '1017 raymond ave', 1, [], [], 0))
    session.add(PeopleFactory.create('employee', 'efname', 'elname', 'pnumber', '1017 raymond ave', 2, [], [], 'Manager', 24.57))
    activeCustomer = session.query(Customer).filter_by(idNumber='1').first()
    activeEmployee = session.query(Person).filter_by(idNumber='2').first()
    global lastOrderNumber
    login = input('\n\nWelcome to The Pizza Palace!\n~~~~~~~~~~~~~~~~~~~~~~~~~~~\nPlease enter your user ID, or press enter to create a new account: ')
    if login == '':
        createAccount()
    user=session.query(Person).filter_by(idNumber=login).first()
    if user == None:
        print("\n\nError: No user found with ID {}.\n\nPlease try again.".format(login))
        time.sleep(2)
        welcome()

    placeOrTrack = input('\n\nWelcome back, {}!\n~~~~~~~~~~~~~~~~~~~~~~~~~~~\nWould you like to place a [N]ew order or [T]rack an existing order?\n\nPlease enter N or T: '.format(user.firstName))
    if placeOrTrack in ['n', 'N']:
        lastOrderNumber += 1
        session.add(OrderBuilder(activeCustomer, activeEmployee, lastOrderNumber, datetime.datetime.now(), []).create())


def main():
    global session
    global Session
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()


    welcome()


    # alex = PeopleFactory.create('customer', 'Alex', 'McKenzie', 9522613456, '1017 Raymond Ave, Apt 10, Saint Paul, MN 55114', 3942730, 1234567890)
    # print(alex)
    # ryan = PeopleFactory.create('employee', 'Xiaowei', 'Zhang', 6122065484, '2346 19th Ave NE, Minneapolis, MN 55386', 9123574, 'Shift Manager', 'Class 44')
    # print(ryan)
    # order = Facade(ryan, alex, 123456, datetime.datetime.now(), ['cheese pizza', 'sausage sandwich', 'coke']).createOrder()
    # print(order)

    # pizza = PizzaDirector.construct("12-inch Hand Tossed Crust", ["Mozerella Cheese", "Pepperoni", "Black Olives"], 1, 7.99)
    # print(pizza)
    # sandwich = SandwichDirector.construct("8-inch Baguette", ["Havarti Cheese", "Salami", "Banana Peppers"], 2, 6.99)
    # print(sandwich)
    

    # manually adding inventory items to the database here
    session.add_all([
            InventoryItem(name="Mozerella", qty=4.2, unitOfMeasure="kg", unitPrice=14.47, type="Cheese"),
            InventoryItem(name="Provolone", qty=2.8, unitOfMeasure="kg", unitPrice=16.14, type="Cheese"),
            InventoryItem(name="Pepperoni", qty=1.4, unitOfMeasure="kg", unitPrice=42.47, type="Meat"),
            InventoryItem(name="Sausage", qty=1.1, unitOfMeasure="kg", unitPrice=36.47, type="Meat"),
            InventoryItem(name="Jalapenos", qty=0.8, unitOfMeasure="kg", unitPrice=22.93, type="Veggie"),
            InventoryItem(name="Green Olives", qty=1.3, unitOfMeasure="kg", unitPrice=24.22, type="Veggie"),
            InventoryItem(name="Coke 2L", qty=17, unitOfMeasure="bottles", unitPrice=2.49, type="Drink")

        ])    
    # search InventoryItem table for Veggie toppings and print the result
    searchresult=session.query(InventoryItem).filter_by(type='Veggie').all()
    print(searchresult)

main()
