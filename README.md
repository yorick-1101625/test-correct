# WP2 PULLED CHICKEN - 1C3  
Python versie: 3.12

Maak een virtual environment:\
    1) ```python -m venv venv```\
    2) ```.\venv\Scripts\activate```

Installeer packages:\
    ```pip install -r requirements.txt```

Start de app met:\
    ```python app.py```\
En ga naar http://127.0.0.1:5000

# Website
Log in met de email "kruwg@hr.nl" en wachtwoord "geheim" om in te loggen in een admin account.\
Om in te loggen in een normaal gebruiker account, log in met email "vried@hr.nl" en wachtwoord "geheimer".

## Vragen overview
Om vragen te importeren klik je op de knop "Upload Vragen" rechtsboven in het overzicht vak. 
Hierna klik je op "Bladeren" en kies je een .json bestand in het aangegeven formaat, zoals de bijgeleverde questions_extract.json.
Klik nu op uploaden, waarna je jouw vragen in het overzicht ziet staan.

Je kan hier met de zoekbalk zoeken op trefwoorden, vak en beoordeelstatus.
Met de pijltjes onderin kan je de volgende/vorige 10 vragen zien.

## Prompts
Bovenin zie je in de navigatiebalk het kopje prompts. Hier vind je het prompt overzicht.
Als je op de aanmaak knop drukt kan je een nieuw prompt met je gewenste naam, inhoud en categorie aanmaken.
Als je naast een bestaand op details klikt zie je de eigenschappen van een prompt.
Als je zelf de prompt hebt aangemaakt of je hebt admin rechten dan kan je een prompt verwijderen.
Je kan ook een prompt 'bewerken' waarmee je een kopie maakt van dat prompt die je vooraf kan bewerken.

## Gebruikers
Als je op het kopje Gebruikers klikt in de navigatiebalk kom je bij de gebruikers. Je kunt hier alleen komen met adminrechten.
Je kunt hier een nieuwe gebruiker aanmaken en, na op de wijzig knop te drukken, een gebruiker bewerken en verwijderen.
Wachtwoorden worden bij het aanmaken en bewerken gehasht voordat ze in de database komen.

## Indexeren
Terug in het kopje Vragen kan je naast een vraag op indexeren klikken voor de gewenste taxonomie categorie.
Hierna kan je een prompt kiezen van de bijbehorende categorie, minstens je 1 bestaand prompt hebt, anders kan je op 'nieuw prompt' klikken.
Je kan nu op genereer antwoord klikken.
Als de GPT een verkeerd antwoord geeft, krijg je dat hier te zien. Je kunt nu op 'opniew proberen' klikken om het nog eens te proberen. 
Anders krijg je de uitleg van de GPT te zien en het antwoord in de 'keuze taxonomie' dropdown. 
Het GPT antwoord staat aangegeven met 'GPT:'.
Je kunt de GPT nu naar wens corrigeren. Klik nu op Taxonomie opslaan.

Je wordt nu doorverwezen naar de eerstvolgende onbeoordeelde vraag.
Om terug te gaan naar het overzicht klik bovenin op Vragen.

Wanneer je een vraag op beide RTTI als Bloom hebt geïndexeert, kun je deze vinden wanneer je in het overzicht sorteert op beoordeelde vragen.
Als je nu op 'Exporteer beoordeelde vragen' klikt en vervolgens op download krijg je deze vragen in een nieuw json bestand.
Deze vraag kan je nu vinden door te sorteren op Geëxporteerd.


# Bronnen
How to iterate through database results, compare each value to that in an array and return the matching id? (n.d.). Stack Overflow. Retrieved November 13, 2024, from https://stackoverflow.com/questions/20527575/how-to-iterate-through-database-results-compare-each-value-to-that-in-an-array \
Creemers, L. (2023, December 31). Build a To-Do list app using Python Flask, Jinja2, and SQL. Lou’s Blog Exploring Tech. Retrieved November 13, 2024, from https://lovelacecoding.hashnode.dev/build-a-to-do-list-app-using-python-flask-jinja2-and-sql \
GeeksforGeeks. (2024, June 26). Flask message flashing. Retrieved December 13, 2024, from GeeksforGeeks. https://www.geeksforgeeks.org/flask-message-flashing/ \
GeeksforGeeks. (2022, June 16). How to use FlaskSession in Python Flask ? Retrieved December 10, 2024, from GeeksforGeeks. https://www.geeksforgeeks.org/how-to-use-flask-session-in-python-flask/ \
GeeksforGeeks. (2022b, July 19). Reading and writing JSON to a file in Python. Retrieved December 8, 2024, from GeeksforGeeks. https://www.geeksforgeeks.org/reading-and-writing-json-to-a-file-in-python/ \
W3Schools. (n.d.). HTML Tables. Retrieved December 10, 2024, from W3Schools.com. (n.d.).  https://www.w3schools.com/html/html_tables.asp 
