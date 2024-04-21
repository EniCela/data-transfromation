import enum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Enum, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

engine = create_engine('sqlite:///hotelBooking.db', echo=True)

Base = declarative_base()


class Guests(Base):
    __tablename__ = 'guests'

    guest_id = Column(String, primary_key=True)
    name = Column(String)
    email = Column(String)
    phone_number = Column(String)

class Rooms(Base):
    __tablename__ = 'rooms'

    room_number = Column(Integer, primary_key=True)
    type = Column(String)
    rate_per_night = Column(Float)

class Bookings(Base):
    __tablename__ = 'bookings'

    booking_id = Column(String, primary_key=True)
    guest_id = Column(String, ForeignKey('guests.guest_id'))
    room_number = Column(String, ForeignKey('rooms.room_number'))
    check_in_date = Column(Date)
    check_out_date = Column(Date)
    guest = relationship("Guests", backref="bookings")
    room = relationship("Rooms", backref="bookings")

class Services(Base):
    __tablename__ = 'services'

    service_id = Column(String, primary_key=True)
    name = Column(String)
    description = Column(String)
    cost = Column(String)

class RoomService(Base):
    __tablename__ = 'room_service'

    service_booking_id = Column(String, primary_key=True)
    booking_id = Column(String, ForeignKey('bookings.booking_id'))
    service_id = Column(String, ForeignKey('services.service_id'))
    quantity = Column(String)
    description = Column(String)

    booking = relationship("Bookings", backref="room_service")
    service = relationship("Services", backref="room_service")

class Payments(Base):
    __tablename__ = 'payments'

    payment_id = Column(String, primary_key=True)
    booking_id = Column(String, ForeignKey('bookings.booking_id'))
    method_id = Column(Integer, primary_key=True)
    amount = Column(String)
    payment_date = Column(Date)

class Feedback(Base):
    __tablename__ = 'feedback'

    feedback_id = Column(Integer, primary_key=True)
    booking_id = Column(Integer, ForeignKey('bookings.booking_id'))
    rating = Column(Integer, nullable=False)
    comments = Column(String)

class RoomOffers(Base):
    __tablename__ = 'room_offers'

    offer_id = Column(Integer, primary_key=True)
    room_number = Column(Integer, ForeignKey('rooms.room_number'))
    offer_name = Column(String(100))
    # offer_description = Column(String)
    # offer_discount = Column(Float(precision=2))
    start_date = Column(Date)
    end_date = Column(Date)

class Offers(Base):
    __tablename__ = 'offers'

    offer_id = Column(Integer, primary_key=True)
    offer_name = Column(String(100))
    offer_description = Column(String)
    offer_discount = Column(Float(precision=2))

class PaymentMethods(Base):
    __tablename__ = 'payment_methods'

    method_id = Column(Integer, primary_key=True)
    method_type = Column(String(50), nullable=False)


# class BookingServices(Base):
#     __tablename__ = 'booking_services'

#     #booking_service_id = Column(Integer, primary_key=True)
#     booking_id = Column(Integer,  ForeignKey('bookings.booking_id'), primary_key=True)
#     service_id = Column(Integer, ForeignKey('services.service_id'))
#     quantity = Column(Integer, nullable=False)

    # booking = relationship("Bookings", backref="booking_services")
    # service = relationship("Services", backref="booking_services")


Base.metadata.create_all(engine)