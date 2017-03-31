#goal: map sentences to corresponding aspect.

#INPUT

#review, this algo needs all the review. Please process dataset.
d = """ Lovely location, however, for 820 euros this was really bad value.
The room was nice, but you could have been anywhere in the
world- it felt like a chain hotel in the worst sense. The room was
tiny!Normally Four Seasons have mind blowing service and
although they were nice it was not amazing. We had just been to
Claridge's in London which was fantasic and half the price. It
wasn't bad , but it wasn't great and not worth the money. A coke
was 10 euros! There was no free wireless- all in all very average. """

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
