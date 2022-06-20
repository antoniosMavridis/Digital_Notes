# YpoxreotikiErgasia22_E18102_MAVRIDIS_ANTONIOS
A Python application in Docker with Mongodb Database that simulates the GoogleKeep application.


# DIGITAL NOTES

## Περιγραφή της Εφαρμογής


### Entrypoint: /createSimpleUser
Με το συγκεκριμένο entrypoint γίνεται η εγγραφή ενός χρήστη στο σύστημα με το ονοματεπώνυμό του, το email του, το username του και ένα password. Γίνεται αναζήτηση του email που έδωσε ο χρήστης αν υπάρχει ήδη στη βάση, ως εγγρεγραμμένος και επίσης ελέγχεται και το username εάν κατέχεται από άλλον χρήστη, ώστε να ειδοποιηθεί με κατάλληλο μήνυμα. <p>
Η παραπάνω διαδιακασία πραγματοποιείται με την:
```
@app.route('/createSimpleUser', methods=['POST'])
```
Για την εισαγωγή δεδομένων στη βάση χρησιμοποιούμε την εξής εντολή:
```
curl -X POST localhost:5000/createSimpleUser -d 
'{"name":"antonis","username":"ant","password":"pass","e-mail":"emal@edu.gr"}' 
-H Content-Type:application/json
```
Έπειτα από την επιτυχής προσθήκη του νέου χρήστη, o χρήστης ενημερώνεται με το εξής επιτυχίας:
 ```
User antonis was added.
```
### Entrypoint: /login
Στην συνέχεια ο χρήστης θα χρειαστεί να κάνει login έτσι ώστε να έχει πρόσβαση στις υπόλοιπες λειτουργίες του συστήματος. <p>
Η παραπάνω διαδικασία πραγματοποιείται με την:
```
@app.route('/login', methods=['POST'])
``` 
Συγκεκριμένα, ο χρήστης δίνει το username του και το password που όρισε κατά την εγγραφή του. Πραγματοποιέιται αναζήτηση στη βάση ως εξής:
``` 
users.find_one({"username":data["username"], "password":data["password"]})
``` 
Aν α στοιχεία είναι έγκυρα και βρεθεί ο χρήστης , τότε καλείται η συνάρτηση create_session() με παράμετρο το username του χρήστη και θα γίνεται επιτυχής είσοδος στην υπηρεσία. Διαφορετικά, θα εμφανίζεται ανάλογο μήνυμα που θα προτρέπει το χρήστη να εισάγει τα στοιχεία του και πάλι. Μόνο στη περίπτωση που ένας χρήστης έχει κάνει
επιτυχημένα την είσοδό του στο σύστημα θα μπορεί να εκτελέσει τις υπόλοιπες λειτουργίες της εφαρμογής. <p>

Για την εισαγωγή δεδομένων στη βάση και την πραγματοποίηση του login χρησιμοποιούμε την εξής εντολή:
```
curl -X POST localhost:5000/login -d 
'{"username":"gian","password":"pass"}' 
-H Content-Type:application/json
```
Ως αποτέλεσμα έχουμε την δημιουργία του κατάλληλου AUTHORIZATION_ID το οποίο χρησιμοποιείται εκτενώς για τις υπόλοιπες διεργασίες. Αν πρόκειται για διαχειριστή του συστήματος δημιουργείται και ADMIN_AUTHORIZATION_ID.
 ```
Userid for user ant : f022c7a1-efac-11ec-bfc5-b42e99f51343
```
Για όλα τα παρακάτω endpoints απαιτείται η σύνδεση του χρήστη στο σύστημα. Για κάθε curl, εντολή εκτέλεσης, ο χρήστης δίνει τον κωδικό αυθεντικοποίησης του στο header. Ο κωδικός ελέγχεται με τη συνάρτηση is_session_valid() και αν δεν είναι έγκυρος επιστρέφεται κατάλληλο μήνυμα με status 401.

### Entrypoint: /createNote
Μέσω αυτού του enrtypoint ο χρήστης μπορεί να δημιουργήσει μια νέα σημείωση η οποία θα αποτελείται από έναν τίτλο, το κείμενο αναφοράς και λέξεις κλειδία. Η παραπάνω διαδιακασία πραγματοποιείται με την:
```
@app.route('/createNote', methods=['POST'])
``` 
 Οι παραπάνω πληροφορίες εισάγονται από το χρήστη, ενώ αποθηκεύεται αυτόματα και η ημερομηνία δημιουργίας για την εκάστοτε σημείωση ως εξής:
```
d1 = today.strftime("%d/%m/%Y")
data['date']=d1
 ```
Για την ειασωγή μιας σημειώσης στο σύστημα χρησιμοποιούμε την εξής εντολή:
 ```
curl -X POST localhost:5000/createNote -d 
'{"title":"A TITLE","text":"thi,"words":"test"}' 
-H Content-Type:application/json -H "Authorization: f022c7a1-efac-11ec-bfc5-b42e99f51343"
 ```
Έπειτα από την επιτυχή εισαγωγή της σημείωσης εμφανίζεται το εξής μήνυμα στον χρήστη:
 ```
NOTE A TITLE was added to database.
```
Αντίστοιχα για λόγου χάρη του παραδείγματος θα προσθέσουμε άλλες δύο σημειώσεις ως εξής:
```
curl -X POST localhost:5000/createNote -d 
'{"title":"A second TITLE","text":"this is another note","words":"test2"}' 
-H Content-Type:application/json -H "Authorization: f022c7a1-efac-11ec-bfc5-b42e99f51343"
```
```
NOTE A second TITLE was added to database.
```
```
curl -X POST localhost:5000/createNote -d 
'{"title":"A third TITLE","text":"this is a nother  one  note","words":"test3"}' 
-H Content-Type:application/json -H "Authorization: f022c7a1-efac-11ec-bfc5-b42e99f51343"
```
```
NOTE A third TITLE was added to database.
```
### Entrypoint: /searchNote
Μέσω αυτού του enrtypoint ο χρήστης μπορεί να αναζητά μια σημείωση με βάση τον τίτλο της. Η παραπάνω διαδιακασία πραγματοποιείται με την:
```
@app.route('/searchNote', methods=['POST'])
``` 
Η αναζήτηση της σημείωσης μπορεί να πραγματοποιηθεί ως εξής:
``` 
curl -X POST localhost:5000/searchNote -d '{"title":"A TITLE"}' 
-H Content-Type:application/json -H "Authorization: f022c7a1-efac-11ec-bfc5-b42e99f51343"
``` 
Στην περίπτωση που υπάρχει η σημειώση, επιστρέφονται τα δεδομένα της στον χρήστη. Στην συγκεκριμένη περίπτωση επιστρέφεται:
``` 
[
    {
        "title": "A TITLE",
        "text": "this is a note",
        "words": "test"
    }
]
``` 
 Τα αποτελέσματα που μπορούν να επιστραφούν στον χρήστη μπορεί να είναι από ένα ή και περισσότερα ή και κανένα. 

### Entrypoint: /searchWord
Μέσω αυτού του enrtypoint ο χρήστης μπορεί να αναζητά μια σημείωση με βάση λέξης κλειδίου. Η παραπάνω διαδιακασία πραγματοποιείται με την:
```
@app.route('/searchWord', methods=['POST'])
``` 
Η αναζήτηση της σημείωσης μπορεί να πραγματοποιηθεί ως εξής:
``` 
curl -X POST localhost:5000/searchNote -d '{"title":"A TITLE"}' 
-H Content-Type:application/json -H "Authorization: f022c7a1-efac-11ec-bfc5-b42e99f51343"
``` 
Στην περίπτωση που υπάρχει σε κάποια σημείωση η λέξη κλειδί επίστρεφεται στον χρήστη η αντίστοιχη σημείωση. Εάν υπάρχουν παραπάνω από μια σημειώσεις στην βάση τότε επιστρέφονται ανάλογα με την ημερομηνία της δημιουργίας τους. Στην συγκεκριμένη περίπτωση επιστρέφεται:
``` 
[
    {
        "title": "A TITLE",
        "text": "this is a note",
        "words": "test"
    },
    {
        "title": "A second TITLE",
        "text": "this is another note",
        "words": "test2"
    },
    {
        "title": "A third TITLE",
        "text": "this is another  one  note",
        "words": "test3"
    }
]

``` 
Τα αποτελέσματα που μπορούν να επιστραφούν στον χρήστη μπορεί να είναι από ένα ή και περισσότερα ή και κανένα. 
