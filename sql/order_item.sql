SELECT idTicket, Departure_airport, Arrival_airport, Departure_Time_And_Date, cost
FROM ticket join departure on(idD = idDeparture) join flight on(idF = idFlight)
where 1
    and idTicket = '$item_id'