update ticket
set Passenger_Name = "$passenger", Date_of_sale = "$date", idC = "$cashier"
where 1
    and idTicket = "$idT"