from django.core.exceptions import ValidationError


def validate_seat_in_row(row, seat, planetarium_dome):
    rows_in_dome = planetarium_dome.rows
    seats_in_row = planetarium_dome.seats_in_row

    if row > rows_in_dome:
        raise ValidationError(f"Only {rows_in_dome} rows. No row № {row}")

    if seat > seats_in_row:
        raise ValidationError(f"No seat № {seat}. The maximum is {seats_in_row} seats.")
