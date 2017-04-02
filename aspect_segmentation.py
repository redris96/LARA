#goal: map sentences to corresponding aspect.

#INPUT

#review, this algo needs all the review. Please process dataset.

#Aspect Keywords

v = "value, price, quality, worth"
r = "room, suite, view, bed"
l = "location, traffic, minute, restaurant"
c = "clean, dirty, maintain, smell"
ci = "stuff, check, help, reservation"
s = "service, food, breakfast, buffet"
b = "business, center, computer, internet"

A = {"value":v.split(", "), "room":r.split(", "), "location":l.split(", "), "cleanliness":c.split(", "), "check in":ci.split(", "), "service":s.split(", "), "business service": b.split(", ")}

#selection threshold
p = 5
#Iterations 
I = 10

#Create Vocabulary
