SELECT idTicket, Departure_airport, Arrival_airport, Departure_Time_And_Date, cost
FROM ticket join departure on(idD = idDeparture) join flight on(idF = idFlight)
Where 1
    and idC is null
    and Departure_airport = "$departure"
    and Arrival_airport = "$destiny"
    and Departure_Time_And_Date = "$date"