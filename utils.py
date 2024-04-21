import json
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_schema import Guests, Bookings, Payments, Feedback, Rooms, Services, RoomService, Base, PaymentMethods,RoomOffers,Offers
from datetime import datetime
from db_schema import Payments


def payments_to_dict(payments):
    payments_dict_list = []
    for payment in payments:
        payment_data = {
           'payment_id': payment.payment_id,
            'booking_id': payment.booking_id,
            'amount': payment.amount,
            'method_id':payment.method_id,
            'payment_date': payment.payment_date.strftime('%Y-%m-%d') if payment.payment_date else None
        }
        
        payments_dict_list.append(payment_data)
    return payments_dict_list

def feedbacks_to_dict(feedbacks):
    feedbacks_dict_list = []
    for feedback in feedbacks:
        feedback_data = {
            'feedback_id': feedback.feedback_id,
            'booking_id': feedback.booking_id,
            'rating': feedback.rating,
            'comments': feedback.comments
        }
        feedbacks_dict_list.append(feedback_data)
    return feedbacks_dict_list


def bookings_to_dict(bookings):
    bookings_dict_list = []
    for booking in bookings:
        booking_data = {
            'booking_id': booking.booking_id,
            'guest_id': booking.guest_id,
            'room_number': booking.room_number,
            'check_in_date': booking.check_in_date.strftime('%Y-%m-%d') if booking.check_in_date else None,
            'check_out_date': booking.check_out_date.strftime('%Y-%m-%d') if booking.check_out_date else None
        }
        bookings_dict_list.append(booking_data)
    return bookings_dict_list

def guests_to_dict(guests):
    guests_dict_list = []
    for guest in guests:
        guest_data = {
            'guest_id': guest.guest_id,
            'name': guest.name,
            'email': guest.email,
            'phone_number': guest.phone_number
        }
        guests_dict_list.append(guest_data)
    return guests_dict_list


def offers_to_dict(offers):
    offers_dict_list = []
    for offer in offers:
        offer_data = {
            'offer_id': offer.offer_id,
            'room_number': offer.room_number,
            'offer_name': offer.offer_name,
            # 'offer_description': offer.offer_description,
            # 'offer_discount': offer.offer_discount,
            'start_date': offer.start_date.strftime('%Y-%m-%d') if offer.start_date else None,
            'end_date': offer.end_date.strftime('%Y-%m-%d') if offer.end_date else None
        }
        offers_dict_list.append(offer_data)
    return offers_dict_list
 

def sort_payments_by_amount(lista):
    sorted_payments = sorted(lista, key=lambda x: x['amount'])
    added_payment_ids = []
    unique_sorted_payments = []

    for payment in sorted_payments:
        if payment['payment_id'] not in added_payment_ids:
            added_payment_ids.append(payment['payment_id'])
            unique_sorted_payments.append(payment)

    return unique_sorted_payments


def sort_guests_by_name(guests):
    return sorted(guests, key=lambda x: x['name'])


# def sort_offers_by_datestart(offers):
#     return sorted(offers, key=lambda x:datetime.strptime(x['start_date'], '%Y-%m-%d'))


def sort_feedbacks_by_rating(feedbacks):
    return sorted(feedbacks, key=lambda x: x['rating'] ,reverse=True)


def sort_bookings_by_latest_check_in_date(bookings):
    return sorted(bookings, key=lambda x: x['check_in_date'], reverse=True)
