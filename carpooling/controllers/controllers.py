from odoo import http
from odoo.http import request


class CarPooling(http.Controller):
    @http.route('/car_pooling/car_pooling', auth='public')
    def index(self, **kw):
        return "Hello, world"

    @http.route('/car_pooling/car_pooling/objects', auth='public')
    def list(self, **kw):
        return http.request.render('car_pooling.listing', {
            'root': '/car_pooling/car_pooling',
            'objects': http.request.env['car_pooling.car_pooling'].search([]),
        })

    @http.route('/car_pooling/car_pooling/objects/<model("car_pooling.car_pooling"):obj>', auth='public')
    def object(self, obj, **kw):
        return http.request.render('car_pooling.object', {
            'object': obj
        })

    @http.route('/home/bookride', type='http', auth="public", website=True)
    def create_ticket_records(self):
        values = {}
        values.update({
        })
        return http.request.render('carpooling.website_helpdesk_form_ticket_submit_form_new', values)

    @http.route('/available-rides', type='http', auth="public", website=True)
    def get_available_rides(self):
        rides_obj = request.env['car.pooling'].sudo().search([('status', 'in', ('available', 'full'))])
        values = {}
        rides_list = []
        for rides in rides_obj:
            rides_list.append({
                'id': rides.id,
                'driver': rides.driver.name,
                'available_seat': rides.available_seat,
                'departure_date': rides.departure_date,
                'source_city': rides.source_city,
                'destination_city': rides.destination_city,
                # 'is_round_trip': 'Yes' if rides.is_round_trip else 'No',
                # 'return_date': rides.return_date,
                'ride_amount': rides.ride_amount,
                'car_name': rides.car_name,
                'car_plate_number': rides.car_plate_number,
            })

        values.update({
            'rides': rides_list
        })
        return http.request.render('carpooling.available_rides', values)

    @http.route('/my_controller/route', type='http', auth="public", website=True)
    def ride_booking(self, **post):
        user = request.env.user
        ride_details = []
        aaa = post.get('departure_date')
        datetime_string = aaa
        date, time = datetime_string.split('T')
        bbb = date + " " + time

        ride_details.append({
            'driver': user.id,
            'source_city': post.get('source_city'),
            'destination_city': post.get('destination_city'),
            'departure_date': bbb,
            'capacity': post.get('capacity'),
            'ride_amount': post.get('ride_amount'),
        })

        result = request.env['car.pooling'].sudo().create(ride_details)
        user.car_name = post.get('car_name')
        user.car_plate_number = post.get('car_plate_number')

        return request.render('carpooling.enquiry_thanks')

    @http.route('/book-ride', type='http', auth="public", website=True)
    def book_a_ride(self):
        rides_obj = request.env['car.pooling'].search([('status', 'in', ('available', 'full'))])
        for rides in rides_obj:
            result = request.env['car.pooling.passenger'].sudo().create({'trip_id': rides.id})
        return http.request.render('carpooling.payment_success')
