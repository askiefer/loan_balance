### Balance Bank Loans Answers

1. How long did you spend working on the problem? What did you find to be the most difficult part?

I spent about 3.5 hours on this assignment. I found the most difficult part to be minimizing the loops needed to assign a loan to a facility. 

Given more time, I would have written tests and refactored the code for additional clarity. I might have also added utility functions. One such function might be a check_csv_headers() function to check each csv for the appropriate headers, to avoid potential KeyErrors when instantiating my Loan, Facility, and Covenant classes and write_to_csv() and read_in_csv() functions.

2. How would you modify your data model or code to account for an eventual introduction of new, as-of-yet unknown types of covenants, beyond just maximum default likelihood and state restrictions?

I would have added additional attributes for the new covenant restrictions in my Covenant class and added additional methods for determining whether the loan or facility violates these restrictions (similar to the banned_facility_id(), above_default(), and banned_state() moethds).

3. How would you architect your solution as a production service wherein new facilities can be introduced at arbitrary points in time. Assume these facilities become available by the finance team emailing your team and describing the addition with a new set of CSVs.

I would create a data pipeline for the facilities received from the finance team. The pipeline could consist of a preprocess check of the csvs and storing it, say on a cloud storage service. A watcher process could take the csv, perform additional data pre-processing if needed, and import the data into a Facilities data table within a relational database. This database could then be accessed by the balance_loans code to check and assign a loan to a facility.  

4. Your solution most likely simulates the streaming process by directly calling a method in your code to process the loans inside of a for loop. What would a REST API look like for this same service? Stakeholders using the API will need, at a minimum, to be able to request a loan be assigned to a facility, and read the funding status of a loan, as well as query the capacities remaining in facilities.

If I were creating a REST API for loan balancing, I would create a service that allows a stakeholder to pass a loan_id to an endpoint  (something like ‘assign_loan/loan_id=<loan_id>’), which processes and assigns the loan to an appropriate facility, returns a success (or failure) response with the facility id. To query a facility’s capacity remaining, I might create a set of facility endpoints that provide information about the facility, e.g. ‘facility/facility_id=<facility_id>/capacity’

5. How might you improve your assignment algorithm if you were permitted to assign loans in batch rather than streaming? We are not looking for code here, but pseudo code or description of a revised algorithm appreciated.

A batch processing system might better balance resources by processing the loan assignments at night when additional computing resources are unused. A revised algorithm might create multiple jobs that process a fixed quantity of loans in parallel, perhaps using multiple threads. If this data was housed in a database, I would assign a facility_id to a loan once a loan has been processed. The batch job could then skip loans that already have an assigned facility_id. This would avoid re-processing already processed loans and reduce the resources needed.

6. Discuss your solution’s runtime complexity.

My solution has a best case runtime of O(n) and a worst case runtime of O(n^2). The outer for loop iterates through each loan, while the inner while loop iterates through the facility objects and checks each loan against its amount remaining and covenants.  
