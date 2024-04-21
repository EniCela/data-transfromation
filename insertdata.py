
import json
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_schema import Guests, Bookings, Payments, Feedback, Rooms, Services, RoomService, Base, PaymentMethods,RoomOffers,Offers
from datetime import datetime
from utils import*
from utils import payments_to_dict ,guests_to_dict ,offers_to_dict ,sort_feedbacks_by_rating ,sort_bookings_by_latest_check_in_date
from utils import sort_payments_by_amount ,sort_guests_by_name ,sort_offers_by_datestart ,feedbacks_to_dict ,bookings_to_dict

with open('object-client.json', 'r') as f:
    data = json.load(f)

engine = create_engine('sqlite:///hotelBooking.db')

Session = sessionmaker(bind=engine)
session = Session()
service_booking_id_counter = 0
payment_dicts = {}
room_services = []
lista=[]
lista2=[]
lista3=[]
lista4=[]
lista5=[]
payments_dict_list = []
added_payment_methods = []


for obj in data:
    guest = Guests(
        guest_id=obj['guest_id'],
        name=obj['name'],
        email=obj['email'],
        phone_number=obj['phone_number']
    )
    guests_dict=guests_to_dict([guest])
    lista2.append(guests_dict[0])
    

    for booking in obj['bookings']:
         for room in booking['room_number']:
            room_exist = session.query(Rooms).filter_by(room_number=room['room_number']).first()
            if not room_exist:
                room_data = Rooms(
                    room_number=room['room_number'],
                    type=room['type'],
                    rate_per_night=room['rate_per_night']
                )
                session.add(room_data)
                session.flush()


            booking_data = Bookings(
                booking_id=booking['booking_id'],
                guest_id=obj['guest_id'],
                room_number=room['room_number'],
                check_in_date=datetime.strptime(booking['check_in_date'], '%Y-%m-%d').date(),
                check_out_date=datetime.strptime(booking['check_out_date'], '%Y-%m-%d').date(),
            )
            booking_dict=bookings_to_dict([booking_data])
            lista5.append(booking_dict[0])
            
            # session.add(booking_data)
            # session.flush()



    for payment in booking['payments']:
        paymentmethod = payment['payment_method']
        payment_exist = session.query(Payments).filter_by(
        payment_id=payment['payment_id'],
        booking_id=booking['booking_id'],
        ).first()
    if not payment_exist:
        payment_obj = Payments(
            payment_id=payment['payment_id'],
            booking_id=booking['booking_id'],
            method_id=paymentmethod['method_id'],
            amount=payment['amount'],
            payment_date=datetime.strptime(payment['payment_date'], '%Y-%m-%d').date(),
        )
        payment_dict = payments_to_dict([payment_obj]) 
        lista.append(payment_dict[0])
    
        # session.add(payment_obj)
        # session.flush()


    paymentmethod = payment['payment_method']
    paymentmethod_exist = session.query(PaymentMethods).filter_by(
                method_id=paymentmethod['method_id'],
                ).first()
    if not paymentmethod_exist:
                payment_method = PaymentMethods(
                    method_id=paymentmethod['method_id'],
                    method_type=paymentmethod['method_type']
                )
                session.add(payment_method)
                session.flush()

  
    feedbacks_data = booking['feedback']
    feedback_exist = session.query(Feedback).filter_by(
            feedback_id=feedbacks_data['feedback_id']
            ).first()
    if not feedback_exist:
                feedback_obj= Feedback(
                feedback_id=feedbacks_data['feedback_id'],
                booking_id=booking['booking_id'],
                rating=feedbacks_data['rating'],
                comments=feedbacks_data['comments']
            )
                feedback_dict=feedbacks_to_dict([feedback_obj])
                lista4.append(feedback_dict[0])



    if "services" in booking:
                for services in booking['services']:
                    services_obj=Services(
                         service_id=services['service_id'],
                         name=services['name'],
                         description=services['description'],
                         cost=services['cost'],
                    )
                session.add(services_obj)
                session.flush()


    if 'offers' in room:
                for offers in room ['offers']:
                    offers_obj=RoomOffers(
                        offer_id=offers['offer_id'],
                        room_number=room['room_number'],
                        offer_name=offers['offer_name'],
                        start_date=datetime.strptime(offers['start_date'],'%Y-%m-%d').date(),
                        end_date=datetime.strptime(offers['end_date'],'%Y-%m-%d').date()
                    )
                    room_offers=offers_to_dict([offers_obj])
                    lista3.append(room_offers[0])    
                    # session.add(offers_obj)
                    # session.flush


    if 'offers' in room:
                for offers in room.get('offers', []):
                    offers_obj=Offers(
                        offer_id=offers['offer_id'],
                        offer_name=offers['offer_name'],
                        offer_description=offers['offer_description'],
                        offer_discount=offers['offer_discount'],
                    )
                    session.add(offers_obj)
                    session.flush()


# if "services" in booking and len(booking["services"]) > 0:
#     for service in booking["services"]:
#         service_booking_id_counter += 1 
#         room_service_dict = {
#             "service_booking_id": service_booking_id_counter,
#             "booking_id": booking['booking_id'],
#             "service_id": service['service_id'],
#             "quantity": service['quantity'],
#             "description": service['description']
#         }
#         room_services.append(room_service_dict)
# print(room_services)
        
    
    if "services" in booking and len(booking["services"]) > 0:
        service_booking_id_counter += 1 
        # for services in booking['services']:
        #service_booking_id_counter += 1 
        # print(service_booking_id_counter)
        for service in booking["services"]:
            roomservice_obj=RoomService(
                service_booking_id=service_booking_id_counter,
                booking_id=booking['booking_id'],                         
                service_id=service['service_id'],
                quantity=service['quantity'],
                description=service['description']
            )

    session.add(roomservice_obj)
    session.flush
  
session.commit()
session.close()







session = Session()

unique_sorted_payments = sort_payments_by_amount(lista)
for payment in unique_sorted_payments:
    payment_object = Payments(
        payment_id=payment['payment_id'],
        booking_id=payment['booking_id'],
        method_id=payment['method_id'],
        amount=payment['amount'],
        payment_date=datetime.strptime(payment['payment_date'], '%Y-%m-%d').date(),
    ) 
    session.add(payment_object)
    session.flush()

sorted_guests=sort_guests_by_name(lista2)
for guest_obj in sorted_guests:
        guest = Guests(
        guest_id=guest_obj['guest_id'],
        name=guest_obj['name'],
        email=guest_obj['email'],
        phone_number=guest_obj['phone_number']
    )
        session.add(guest)
        session.flush


sorted_offers = sort_offers_by_datestart(lista3)
for offer in sorted_offers:
    offersobj=RoomOffers(
        offer_id=offer['offer_id'],
        room_number=offer['room_number'],
        offer_name=offer['offer_name'],
        start_date=datetime.strptime(offer['start_date'],'%Y-%m-%d').date(),
        end_date=datetime.strptime(offer['end_date'],'%Y-%m-%d').date()
)
    session.add(offersobj)
    session.flush
  

Sorted_feedback=sort_feedbacks_by_rating(lista4)
for feed in Sorted_feedback:
        feedback= Feedback(
                feedback_id=feed['feedback_id'],
                booking_id=feed['booking_id'],
                rating=feed['rating'],
                comments=feed['comments']
            )
        session.add(feedback)
        session.flush

sorted_booking=sort_bookings_by_latest_check_in_date(lista5)
for booking in sorted_booking:
        booking_data = Bookings(
                booking_id=booking['booking_id'],
                guest_id=booking['guest_id'],
                room_number=booking['room_number'],
                check_in_date=datetime.strptime(booking['check_in_date'], '%Y-%m-%d').date(),
                check_out_date=datetime.strptime(booking['check_out_date'], '%Y-%m-%d').date(),
            )
        session.add(booking_data)
        session.flush

session.commit()
session.close()