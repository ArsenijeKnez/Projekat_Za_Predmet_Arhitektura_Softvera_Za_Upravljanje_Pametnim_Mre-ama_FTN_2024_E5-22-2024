#Purchase Ontology

**Purchase Ontology** predstavlja semantički model za opisivanje procesa kupovine u e-trgovini.
Zasniva se na RDF (Resource Description Framework) standardu i omogućava strukturisano, interoperabilno i semantički bogato predstavljanje informacija o korisnicima, proizvodima, porudžbinama, plaćanjima i isporukama.


##Opis projekta

Ova ontologija modeluje osnovne entitete e-trgovine i njihove odnose:

* **Korisnici (User)** – predstavljaju kupce ili administratore sistema.
* **Proizvodi (Product)** – objekti prodaje, sa atributima kao što su naziv, cena i identifikator.
* **Porudžbine (Order)** – povezuju korisnike sa proizvodima, popustima, plaćanjima i isporukama.
* **Plaćanje (Payment)** – sadrži informacije o iznosu i metodu plaćanja.
* **Isporuka (Shipping)** – opisuje adresu i status isporuke.
* **Recenzije (Review)** – omogućavaju korisnicima da ocenjuju proizvode.
* **Obaveštenja (Notification)** – prikazuju poruke koje korisnici primaju.
* **Popusti (Discount)** – definišu procente umanjenja cene tokom kupovine.

Ontologija koristi prefikse poput `tto:` (taxonomy/ontology) i `ttr:` (taxonomy/resource) radi lakšeg organizovanja podataka.

##Tehnologije

* **RDF / Turtle (TTL)** — standardni format za opis semantičkih podataka
* **RDFS** — definisanje tipova, domena i odnosa između klasa
* **SPARQL** — jezik za pretraživanje RDF grafova
* **SPARQL-Playground** [Za testiranje](https://github.com/calipho-sib/sparql-playground)
