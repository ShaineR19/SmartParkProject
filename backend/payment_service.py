class PaymentService:
    @staticmethod
    def calculate_duration(entry_time, exit_time):
        difference = exit_time - entry_time
        seconds = difference.total_seconds()
        hours = seconds / 3600

        return hours

    @staticmethod
    def calculate_fee(
        duration_hours, 
        hourly_rate
    ):
        if duration_hours < 0:
            raise ValueError(
                "Parking duration cannot be negative."
            )
        if hourly_rate < 0:
            raise ValueError(
                "Hourly rate cannot be negative."
            )
        fee = duration_hours * hourly_rate

        return round(fee, 2)