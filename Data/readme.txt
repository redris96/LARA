1. Text Directory:
Parsed reviews crawled from TripAdvisor (http://www.tripadvisor.com). 
Meta data includes: Author, Content, Date, Number of Reader, Number of Helpful Judgment, Overall rating, Value aspect rating, Rooms aspect rating, Location aspect rating, Cleanliness aspect rating, Check in/front desk aspect rating, Service aspect rating and Business Service aspect rating. Ratings ranges from 0 to 5 stars, and -1 indicates this aspect rating is missing in the orginal html file.

2. Aspect Directory:
Segmented reviews by boot-stripping methods. 
Meta data includes: Author, Content, Date, Ratings (Overall, Value, Rooms, Location, Cleanliness, Check in/front desk, Service and Business Service) and Aspect Segments (Overall, Value, Rooms, Location, Cleanliness, Check in/front desk, Service and Business Service).

3. Vector Directory:
Vector representation of the segmented reviews. We aggregate the reviews associating with the same hotel and discard the hotels with missing aspect segments ('h-review'). The format of this file is as follows:
Hotel_ID	Overall_Rating	Value_Rating	Room_Rating	Location_Rating	Cleanliness_Rating	Check_in/front_desk_Rating	Service_Rating	Business_Service_Rating
Aspect segments (corresponding to the order of aspect ratings): [term_index:term_count ]+

4. Note:
All the text reviews, aspect segmented reviews and vectors are organized by their Hotel ID.

5. JSON Directory (new):
JSON format of all the hotel reviews we have collected from TripAdvisor for the research of LARA. 
IMPORTANT: because the data was crawled in different time period, the format is slightly different across different hotel files, e.g., some hotels do not have location, price info, and some reviews do not have reviewer location etc. This is our most comprehensive collection of hotel reviews.