SELECT Passenger_Name, Date_of_sale, Departure_airport, Arrival_airport, Departure_Time_And_Date, Cost
FROM ticket join departure on(idD = idDeparture) join flight on(idF = idFlight)
where 1
    and Date_of_sale="$date"