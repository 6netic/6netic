from datetime import date


class Compute:
    """ Class to compute days """

    def __init__(self, departureDate, hour, sharing, distance):
        self.bank_holidays = [
            date(2022, 1, 1), date(2022, 4, 18), date(2022, 5, 1), date(2022, 5, 8),
            date(2022, 5, 26), date(2022, 6, 6), date(2022, 7, 14), date(2022, 8, 15),
            date(2022, 11, 1), date(2022, 11, 11), date(2022, 12, 25),
            date(2023, 1, 1), date(2023, 4, 10), date(2023, 5, 1), date(2023, 5, 8),
            date(2023, 5, 29), date(2023, 7, 14), date(2023, 8, 15), date(2023, 11, 1),
            date(2023, 11, 11), date(2023, 12, 25),
            date(2024, 1, 1), date(2024, 4, 1), date(2024, 5, 1), date(2024, 5, 8),
            date(2024, 5, 9), date(2024, 5, 20), date(2024, 7, 14), date(2024, 8, 15),
            date(2024, 11, 1), date(2024, 11, 11), date(2024, 12, 25),
            date(2025, 1, 1), date(2025, 4, 21), date(2025, 5, 1), date(2025, 5, 8),
            date(2025, 5, 29), date(2025, 6, 9), date(2025, 7, 14), date(2025, 8, 15),
            date(2025, 11, 1), date(2025, 11, 11), date(2025, 12, 25),
            date(2026, 1, 1), date(2026, 4, 6), date(2026, 5, 1), date(2026, 5, 8),
            date(2026, 5, 14), date(2026, 5, 25), date(2026, 7, 14), date(2026, 8, 15),
            date(2026, 11, 1), date(2026, 11, 11), date(2026, 12, 25)
        ]
        self.departure_date = departureDate
        self.hour = hour
        self.sharing = sharing
        self.distance = distance / 1000
        self.price_per_kilometre_day = 1.01
        self.price_per_kilometre_night = 1.56
        self.price_per_kilometre_we = 1.61
        self.reduction_rate_1 = 0.95
        self.reduction_rate_2 = 0.92
        self.reduction_rate_3 = 0.84
        self.reduction_rate_4 = 0.76


    def calculate_individual_price(self):
        """ Calculates the price """

        price_per_kilometre = float
        booking_day = self.departure_date.strftime("%a")
        if (booking_day == "Mon" or booking_day == "Tue" or
            booking_day == "Wed" or booking_day == "Thu" or booking_day == "Fri"):
            if (int(self.hour) >= 8 and int(self.hour) < 20):
                price_per_kilometre = self.price_per_kilometre_day
            else:
                price_per_kilometre = self.price_per_kilometre_night
        if (booking_day == "Sat" or booking_day == "Sun" or self.departure_date in self.bank_holidays):
            price_per_kilometre = self.price_per_kilometre_we
        price = round(price_per_kilometre * self.distance, 2)
        return price, self.departure_date, self.sharing


    def compute_grouped_price(self, bookings_in_base):
        """ Calculates final price considerating reductions"""

        booking_list, unique_booking_list, prices_dict = [], [], {}
        for booking in bookings_in_base:
            booking_item = [booking.departureTime, float(booking.price)]
            booking_list.append(booking_item)
            if booking_item not in unique_booking_list:
                unique_booking_list.append(booking_item)
        reduction_rate = float()
        for hour in unique_booking_list:
            if (booking_list.count([hour][0][0]) + 1) <= 3:
                reduction_rate = self.reduction_rate_1
            elif (booking_list.count([hour][0][0]) + 1) <= 4 and (booking_list.count([hour][0][0]) + 1) <= 7:
                reduction_rate = self.reduction_rate_2
            elif (booking_list.count([hour][0][0]) + 1) <= 8 and (booking_list.count([hour][0][0]) + 1) <= 22:
                reduction_rate = self.reduction_rate_2
            elif (booking_list.count([hour][0][0]) + 1) <= 23 and (booking_list.count([hour][0][0]) + 1) <= 54:
                reduction_rate = self.reduction_rate_2
            prices_dict[[hour][0][0]] = round([hour][0][1] * reduction_rate, 2)
        return prices_dict