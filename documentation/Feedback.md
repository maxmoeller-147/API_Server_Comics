Feedback gathered from: Charlisse, Inna (CoderAcademy's Students); Partner.
Reflexion done by Max Acosta on 26/08/2025.

Thanks to the feedback I could see a clearer path for improvement.

# “There is too many numbers (id's) on the screen.”    - Partner.

- Development Stage
- This feedback refers to the output of the data request in Insomnia when I was showing and testing how the CRUD operations worked, my partner seemed confused about what too see first as the output was showing all the id's of diferent orders, costumers and comics link to an Artist.
    
    * Thanks to this comment I implemented `id = auto_field(load_only=True` on every schema on schemas/schemas.py. This hides the id on the output but stills register it when input.


# “The Readme could have an improvement, The Routes Table looks all over the place in the preview“ - Charlisse (CoderAcademy Student) 
    
   - Final Stage of the project. Refinig and Making the code nicer.
   - I asked one of my cohort opinions on the project and she pointed my readme, specially the routes table, so I added lines and style to it making it more appealing to the user and easy to read.
   

# “You can add a description to the orders” - Partner.

- At plannig stage
- Thinking of ideas to make my ERD more complete and robust. My partner suggested that would be good to add a description when making and order.
    This was implemented straight away.


# “Price needs validations” - Inna (CoderAcademy Student) 

Development Stage
- Inna remind to add validation on the price on the Comic Operations.
 * I added:  
     # Validate Price    
        price_input = body_data.get("price")
        try:
            price_input = int(price_input)
        except (TypeError,ValueError):
            return {"message":"Price must be an integer."}, 400

To controllers/comic_controllers.py POST and PUT/PATCH operations.