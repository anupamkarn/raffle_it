**Raffle_it**
----
  Raffle_it contains backend servises for Lucky draw ticketing system.The implementation is
  completely modular and documented. Its been implemented by creating blueprints and application
  factories concepts. Curretly it only contains tickets blueprints.
  Below mentioned points where the top level functional requirements
  - Design an API which allows users to get the raffle tickets. This API can be
    consumed in a lot of ways like We can call this API after the user has placed
    an Order.
  - Design an API which shows the next Lucky Draw Event timing & the
    corresponding reward. For example - Lucky Draw can run everyday at 8AM.
    Reward on say 10th Feb is Phone, 11th Feb is Washing Machine etc
  - Design an API which allows users to participate in the game. Once a user
    has participated with a raffle ticket, she shouldn’t be able to participate
    again in the same event.
  - Design an API which lists all the winners of all the events in the last one
    week.
  - Compute the winner for the event and announce the winner.

  Some of the Assumptions where made before implementing the above requirements
  - Tickets will always belong to a event. Distributing a ticket will mean participating for that event
  - We are assuming that user authentication is well versed taken care off hence to authentication steps 
    are taken into consideration
  - Winner selection is currently implementated base on a api call but ideally it should be completely 
    event driven (sse) with the help of redis message broker.
  - Database is selected as mongoDB, and which is consumed through cloud servises (atlas)
  - Appologies for insuffient testing data

For setting up backend code.
clone the repo.
install flask.
```
export FLASK_APP=raffle
export FLASK_ENV=development
flask run
```

Below are the list of APIS

* **URL**

  get_ticket(username)
  ticket/<username>?eventID=1

* **Method:**

  `GET`
  

* **Data Params**

  eventID

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** 
```json
{
   "_id":{
      "$oid":"608ecf69460476225dc97911"
   },
   "name":"Daily Lucky draw event",
   "event_id":"1",
   "time":"120000",
   "start_date":{
      "$date":1489732140000
   },
   "frequency":"D",
   "ticket_list":[
      "1",
      "5",
      "9",
      "3",
      "7",
      "8"
   ],
   "max_participants":"10",
   "participants":[
      {
         "name":"alice",
         "ticket_no":"2"
      },
      {
         "name":"bob",
         "ticket_no":"4"
      },
      {
         "name":"Alex",
         "ticket_no":"6"
      },
      {
         "name":"Anupam",
         "ticket_no":"10"
      }
   ]
}
```
 
* **Error Response:**
  Multiple error responses please check a API code.
  

* **URL**

  get_upcoming_draws()
  ticket/upcoming

* **Method:**

  `GET`
  

* **Data Params**

  None

 * **URL**

  get_winners()
  ticket/winners

* **Method:**

  `GET`
  

* **Data Params**

  None


* **URL**

  check_draw()
  ticket/update_events

* **Method:**

  `GET`
  

* **Data Params**

  None

